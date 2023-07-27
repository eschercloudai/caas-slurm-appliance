# NL1-CI cluster

Intended to be driven with CI tooling test images created using the eschercloud-image-build environment.

Update the `cluster_image` variable in `cluster_extra_vars.yml` with an updated image UUID from
eschercloud-image-build/packer/packer-manifest.json, then deploy a cluster like this:

```
source NL1-CI/activate
export OS_CLOUD=openstack

# Configure
ansible-playbook -e ${APPLIANCES_ENVIRONMENT_ROOT}/cluster_extra_vars.yml ${APPLIANCES_ENVIRONMENT_ROOT}/../../slurm-infra.yml

# Tear down
ansible-playbook -e ${APPLIANCES_ENVIRONMENT_ROOT}/cluster_extra_vars.yml -e cluster_state=absent ${APPLIANCES_ENVIRONMENT_ROOT}/../../slurm-infra.yml
```