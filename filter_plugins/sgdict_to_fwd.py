from ansible import errors
from ansible.utils.display import Display
import jinja2

class FilterModule(object):
    def filters(self):
        return {
            'items_to_sgdict': self.items_to_sgdict,
            'sgdict_to_fwd': self.sgdict_to_fwd,
            'sgdicts_to_fwd': self.sgdict_list_to_fwd,
        }

    def items_to_sgdict(self, src):
        sg_return={}
        for item in src:
            if 'security_groups' in item.keys():
                for sg_item in item['security_groups']:
                    if 'security_group_rules' in sg_item.keys():
                        sg_return[sg_item['id']]=sg_item
                        sg_return[sg_item['name']]=sg_item
        return sg_return

    def sgdict_to_fwd(self, src, sg_name_or_id):
        return _sgdict_to_fwd(src, sg_name_or_id)
    def sgdict_list_to_fwd(self, src, sg_name_or_id_list):
        fwd_rule_list=[]
        for sg_item in sg_name_or_id_list:
            fwd_rule_list=fwd_rule_list+(_sgdict_to_fwd(src, sg_item))
        return fwd_rule_list

def _sgdict_to_fwd(src, sg_name_or_id):
    """ _sgdict_to_fwd converts an Openstack security group dictionary into a Firewalld list of rules """
    rule_list=[]
    fwd_defaults={'zone': 'public','permanent': True, 'immediate': False, 'state': 'enabled' }

    for sg_rule in src[sg_name_or_id]['security_group_rules']:
        #print(sg_rule)
        fwd_rule={}
        if sg_rule['direction']=='ingress' and sg_rule['ethertype'] =='IPv4' and not sg_rule['remote_address_group_id']:
            #print(json.dumps(sg_rule, indent=2))
            #if not sg_rule['remote_ip_prefix']:
            #    print('No remote CIDR in this ingress rule not yet supported skipping rule ' + sg_rule['id'])
            #if sg_rule['protocol']=='icmp':
            #    print('I do not understand how to handle this type of icmp in firewalld, since you understand icmp better than I please help implenent this feature or just allow or reject all. leaving ICMP in default state(allow) from rule ' + sg_rule['id'])

            if sg_rule['protocol'] and sg_rule['protocol'] in ['tcp', 'udp', 'sctp', 'dccp']:
                if sg_rule['port_range_min'] and sg_rule['port_range_max']:
                    if sg_rule['remote_ip_prefix']:
                        fwd_rule=fwd_defaults.copy()
                        fwd_rule['rich_rule']='rule family="ipv4" source address="%s" port="%d-%d/%s" accept' %(sg_rule['remote_ip_prefix'],sg_rule['port_range_min'],sg_rule['port_range_max'],sg_rule['protocol'])
                    else:
                        fwd_rule=fwd_defaults.copy()
                        fwd_rule['port']='%d-%d/%s'%(sg_rule['port_range_min'],sg_rule['port_range_max'],sg_rule['protocol'])
                else:
                    fwd_rule=fwd_defaults.copy()
                    fwd_rule['protocol']=sg_rule['protocol']
            if not sg_rule['protocol']:
                fwd_rule=fwd_defaults.copy()
                fwd_rule['rich_rule']='rule family="ipv4" source address="%s" accept' %(sg_rule['remote_ip_prefix'])
            if fwd_rule:
                rule_list.append(fwd_rule)
    # if our list of firewalld rules is not empty prepend the drop all traffic rule to make it as similar as possible to a real securrity group
    # this is the default for the public zone in firewalld so use that and most cases this will be a null operation
    if rule_list:
        rule_list.insert(0,{'zone': 'public','permanent': True, 'immediate': False, 'state': 'enabled', 'target': 'default' })

    return rule_list