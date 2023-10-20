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

### Init VIRTIO PCI Bars

* hw/virtio/virtio-pci.c:virtio_pci_realize

### init pci operations

```c
memory_region_init_io(&s->io, OBJECT(pci), &serial_io_ops, s, "serial", 8);
pci_register_bar(&pci->dev, 0, PCI_BASE_ADDRESS_SPACE_IO, &s->io);
```

### static void virtio_queue_guest_notifier_read(EventNotifier *n)

```c
(gdb) bt
#0  virtio_queue_guest_notifier_read (n=0x5555577edc98) at ../hw/virtio/virtio.c:4011
#1  0x000055555603ffe8 in aio_dispatch_handler (ctx=ctx@entry=0x555556a7a350, node=0x7fff2001ff10)
    at ../util/aio-posix.c:369
#2  0x00005555560408d2 in aio_dispatch_handlers (ctx=0x555556a7a350) at ../util/aio-posix.c:412
#3  aio_dispatch (ctx=0x555556a7a350) at ../util/aio-posix.c:422
#4  0x0000555556053d12 in aio_ctx_dispatch (source=<optimized out>, callback=<optimized out>,
    user_data=<optimized out>) at ../util/async.c:320
#5  0x00007ffff7b9562b in g_main_context_dispatch ()
   from /home/liunx/Work/CloudEdge/Work/build/buildroot/aarch64/host/lib/libglib-2.0.so.0
#6  0x0000555556056280 in glib_pollfds_poll () at ../util/main-loop.c:297
#7  os_host_main_loop_wait (timeout=3890441) at ../util/main-loop.c:320
#8  main_loop_wait (nonblocking=nonblocking@entry=0) at ../util/main-loop.c:606
#9  0x0000555555af6ed3 in qemu_main_loop () at ../softmmu/runstate.c:739
#10 0x0000555555edebbb in qemu_default_main () at ../softmmu/main.c:37
#11 0x00007ffff7629d90 in __libc_start_call_main (main=main@entry=0x555555893e50 <main>, argc=argc@entry=42,
    argv=argv@entry=0x7fffffffd868) at ../sysdeps/nptl/libc_start_call_main.h:58
#12 0x00007ffff7629e40 in __libc_start_main_impl (main=0x555555893e50 <main>, argc=42, argv=0x7fffffffd868,
    init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffd858)
    at ../csu/libc-start.c:392
#13 0x00005555558956e5 in _start ()
```