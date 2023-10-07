### qemu virtio-rng

* hw/virtio/virtio-rng-pci.c

* hw/virtio/virtio-rng.c

* hw/virtio/vhost-user-rng-pci.c

* hw/virtio/vhost-user-rng.c

### virtio-rng from kernel to qemu

1. virtio_pci_common_write

2. virtio_set_status

3. vu_rng_set_status

4. vu_rng_start

   * k->set_guest_notifiers -> virtio_pci_set_guest_notifiers

### qemu to vhost-device-rng

1. vhost_dev_start

2. vhost_virtqueue_start

3. dev->vhost_ops->vhost_set_vring_base

4. vhost_user_set_vring_base

5. vhost_user_write

6. cc->chr_write = fd_chr_write

### qemu debug linux kernel

1. virtio_device_ready

2. dev->config->set_status(dev, status | VIRTIO_CONFIG_S_DRIVER_OK);

3. virtio-pci_modern.c:vp_set_status-->vp_modern_set_status

4. vp_iowrite8 --> iowrite8