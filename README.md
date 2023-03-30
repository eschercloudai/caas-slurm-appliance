# caas-slurm-appliance

This repository adapts the [StackHPC Slurm Appliance](https://github.com/stackhpc/ansible-slurm-appliance)
for use within the Cluster-as-a-Service system of the [Azimuth Cloud Portal](https://github.com/stackhpc/azimuth).


git clone  --recurse-submodules --remote-submodules --branch <thisbranch> git@github.com:eschercloudai/caas-slurm-appliance.git
cd caas-slurm-appliance/

add your public keys to the list in cluster_extra_vars.yml
cluster_user_ssh_public_keys:
  - ssh_ed25519 ....

source your openstack openrc file 

source ~/venv/bin/activate

ansible-playbook -i inventory -e @cluster_extra_vars.yml slurm-infra.yml