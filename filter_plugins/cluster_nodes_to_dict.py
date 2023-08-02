
class FilterModule(object):
    def filters(self):
        return {
            'key_generic_list_of_dicts': self.key_generic_list_of_dicts,
        }

    def key_generic_list_of_dicts(self, src, key):
        return_dict={}
        for item in src:
            return_dict[item[key]]=item
        return return_dict