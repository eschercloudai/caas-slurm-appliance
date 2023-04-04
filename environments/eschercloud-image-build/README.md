# Eschercloud image-build

Use this environment to build OpenHPC Slurm images using packer:

```
source eschercloud-image-build/activate
cd eschercloud-image-build/packer
PACKER_LOG=1 packer build -only openstack.openhpc -on-error=ask -var-file=$PKR_VAR_environment_root/builder.pkrvars.hcl openstack.pkr.hcl
```

Creates `eschercloud-image-build/packer/packer-manifest.json`, containing latest image UUID.