# Generic Installers

This role does 4 or optionally 5 things

1. Optionally download installers from a remote source using a list of urls
2. copy these installers into the shared cluster filesystem (default /home/installers but relocatable)
3. run  executable installers with the arguments specified on all the cluster nodes
4. extract tar files to a specific loacation on the nodes
   1. use extra_opts to transform paths if needed
5. copy (not template) module files to a specific location

## top level variables explained 

- `generic_installers_remote_urls`

  This is just a list of urls to doenload onto the deploy node. This is default to an empty list and assumes that you will manually populate this before you run the playbook.

- `generic_installers_local_dir`

  This is the path on the deploy node where the installers can be foud or where they are downloaded too. The default is `$HOME/installers/`.

- `generic_installers_cluster_staging_dir`

  This is the path on the staging node where the installers will be copied to. the default is again `$HOME/installers/`. This  home dir should be on the cluster shared files system and ideally be high performance as all nodes will be reading from this at once, a beegfs filsystem is ideal.

- `generic_installers_staging_node`

  this is the hostname of the staging node.

  This needs to have access to the shared cluster filesystem

  This will need overriding in ALL terraform based clusters as it defaults to the first entry in the ALL group which will be localhost. Try "{{ groups['cluster'] | first }}" instead

- `generic_installers_force_stage: false`

  this is used to force the role calculate checksums on the installer files to makes sure that the contents and the filenames match on the deploy and cluster side. We disable this by default as this is used to install cuda runtimes which are huge files and generally if the file exists in the path we have specified it is more than likely to actually be the same this speeds things up by almost a minute on a typical run.

- `generic_installers_default` - This contains default values which are used for almost all clusters see generic_installers_dict. This should normally not be changed unless we are installing software. that conflicts with the defaults. In this case we should override the defaults and leave generic_installers_extra as an empty dict.

- `generic_installers_extra`- This is merged on top of generic_installers_default and can be used to override or simply extend the defaults without having to redefine the existing defaults.

- `generic_installers_dict`

  This is a complex dict made by merging `generic_installers_default` + `generic_installers_extra` the structure of all three variables is the same and we will now cover the options.

## generic_installers_dict structure

this is a nested dict the first level is the filename of the installer file as it is in the `generic_installers_local_dir` (/home/installers) on the deploy node. this is the default settings as in the first ever version

```yaml
generic_installers_default:
  nccl_2.18.3-1+cuda11.0_x86_64.txz:
    type: "extract"
    dest: "/usr/local"
    creates: "/usr/local/nccl_2.18.3-cuda11.0"
    extra_opts: 
      - '--transform'
      - 's/(.+)-1\+(.+)(_x86_64)/\1-\2/xg'
  nccl_2.18.3-1+cuda12.2_x86_64.txz:
    type: "extract"
    dest: "/usr/local"
    creates: "/usr/local/nccl_2.18.3-cuda12.2"
    extra_opts: 
      - '--transform'
      - 's/(.+)-1\+(.+)(_x86_64)/\1-\2/xg'
  cuda_11.8.0_520.61.05_linux.run:
    type: "exec"
    args: "--toolkit --silent"
    module_source: "{{ generic_installers_local_dir }}/modulefiles/cuda11/11.8.lua"
    mode: "0755"
    module_dir: "/opt/ohpc/pub/modulefiles/cuda11/"
    creates: "/usr/local/cuda-11.8/bin"
  cuda_12.2.0_535.54.03_linux.run:
    type: "exec"
    mode: "0755"
    args: "--toolkit --silent"
    module_source: "{{ generic_installers_local_dir }}/modulefiles/cuda12/12.2.lua"
    module_dir: "/opt/ohpc/pub/modulefiles/cuda12/"
    creates: "/usr/local/cuda-12.2/bin"
```

this example includes ALL possible functions of the role. As you can see there are 4 installer files required and they are:

1. nccl_2.18.3-1+cuda11.0_x86_64.txz
2. nccl_2.18.3-1+cuda12.2_x86_64.txz
3. cuda_11.8.0_520.61.05_linux.run
4. cuda_12.2.0_535.54.03_linux.run

Files 1 and 2 are tgz files that we extract to a specific location and then are done (here we use the transform option but we will cover that in a moment). You can tell that they are this because type is set to "extract"  and that are compressed tar files.  Files 3 and 4 are .run files that need to be executed so we specify the "exec" type option. If you make a typo in the type option it will be skipped.

### options for extract type installers

- `dest` - This is the path on the compute nodes where we extract the tar file. if it doesn't exist it (and any required parent dirs) will be created with default owner and permissions
- `extra_opts` - this is included for all the examples cases but it is not required. This allows you to specify any of the advanced options supported by gnu tar. Here we demonstrate the use of the transform to reformat the extracted directory to remove the superflous `_x86_64`  and replace `-1+` with just `-`.

### options for exec type installers

- `mode` - This is optional but recommend. This sets the permissions of the target node. This is almost certainly required when downloading a file from the internet to make sure it is created with executable file permissions on the target node.
- `args`- This is optional. Most installers will require arguments to be set the install path and ensure it does not prompt.

### options for BOTH installers

- `creates` - This should be considered mandatory. Make sure that this points to a path that will only exist once the install has completed. This will dramatically speed up subsequent runs. This is included for all example defaults

Both the following are optional and both need to be set or the module related tasks will be skipped

- `module_source` - This is the path to the module file you want to copy to the `module_dir`. This module file MUST be on the deploy node and the example above sets it to a subdir of the `{{ generic_installers_local_dir }}`. This is used in combination with `module_dir`. 
- `module_dir` - This is where the module file will be copied to. if it does not exist the role will try to created it recursively using the default root owner and directory permissions (0755) for all created dirs.



