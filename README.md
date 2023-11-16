# caas-slurm-appliance

This repository adapts the [StackHPC Slurm Appliance](https://github.com/stackhpc/ansible-slurm-appliance)
for use within the Cluster-as-a-Service system of the [Azimuth Cloud Portal](https://github.com/stackhpc/azimuth).

## changes introduces in the freeipa_external branch
This change allows you to link the cluster to an external but routable freeipa cluster e.g. one produced by caas-ipa-appliance. In my test cluster I am using a private ipa server and I am putting the nodes into the root domain. 

this is in a very early state and needs securing asap, I'm passing an IPA admin password in a group var in the test cluster for now. This will be routed via a secured api soon.

for this to work  we need to use the ipa cluster as the dns resolver for all clients so we mak all nodes freeipa clients by default. I do this in the nested inventory now so that basic clusters can still be created without freeipa. The example test cluster does this using the `caas-slurm-appliance/environments/test/inventory/groups` ini file reproduced here. 
```
[freeipa_client:children]
cluster
```
To make this work, I have updated the inventory parsing to check this inventory path *after* the common inventory. If you see errors about non-existent grous, make sure it's parsing the inventory dirs in the right order so that the freeipa_client group exists before it is used. mor elaborate inheritence can be added if needed with more group layers or using finer grained groups.

the default vars used to configure the nodes are set in `caas-slurm-appliance/environments/test/inventory/group_vars/freeipa/defaylts.yml` and are repeated here:
```
resolv_conf_nameservers: "{{ external_freeipa_servers.server_ip_list }}"
# all freeipa nodes need to have a fqdn set for the host to be properly added to the correct ipa domain
node_fqdn: "{{ inventory_hostname }}.{{external_freeipa_servers.freeipa_domain }}"
```
You will note that we are referring to a  external_freeipa_servers.server_ip_list variable and might be wondering what is this. We'll you need to set it and I assume that it is defined in the `caas-slurm-appliance/environments/test/cluster_extra_vars.yml` include file like this:
```
external_freeipa_servers:
  freeipa_domain: dskjbfsdk.internal
  freeipa_realm: DSKJBFSDK.INTERNAL
  server_hostname_list:
    - test-ipa-1.dskjbfsdk.internal
    - test-ipa-2.dskjbfsdk.internal
    - test-ipa-3.dskjbfsdk.internal
  server_ip_list:
    - 192.168.13.114
    - 192.168.13.150
    - 192.168.13.111
```
right now you construct this manually but this will be an output of the caas-ipa-appliance stored in a secured api
