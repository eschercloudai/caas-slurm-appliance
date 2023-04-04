flavor = "g.2.standard"
networks = ["53b5d32d-7c32-490c-85c3-7feab2378c07"]
source_image_name = "Rocky-8-GenericCloud-Base-8.7-20230215.0"
fatimage_source_image_name = "Rocky-8-GenericCloud-Base-8.7-20230215.0"
floating_ip_network = "Internet"
security_groups = ["SSH"]
ssh_keypair_name = ""
ssh_private_key_file = ""
use_blockstorage_volume = true
volume_size = 15
reuse_ips = true
metadata = {
    hw_scsi_model = "virtio-scsi",
    hw_disk_bus = "scsi",
    hw_vif_multiqueue_enabled = true
}