### virtio-rng

```console
    Breakpoint 1, probe_common (vdev=vdev@entry=0xffffff800134d400) at drivers/char/hw_random/virtio-rng.c:95
    95              vi->index = index = ida_simple_get(&rng_index_ida, 0, 0, GFP_KERNEL);
    (gdb) bt
    #0  probe_common (vdev=vdev@entry=0xffffff800134d400) at drivers/char/hw_random/virtio-rng.c:95
    #1  0xffffffc0086e574c in virtrng_probe (vdev=0xffffff800134d400) at drivers/char/hw_random/virtio-rng.c:147
    #2  0xffffffc0083c152c in virtio_dev_probe (_d=0xffffff800134d410) at drivers/virtio/virtio.c:273
    #3  0xffffffc00848a38c in call_driver_probe (drv=0xffffffc008a47f00 <virtio_rng_driver>, dev=0xffffff800134d410)
        at drivers/base/dd.c:517
    #4  really_probe (dev=dev@entry=0xffffff800134d410, drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>)
        at drivers/base/dd.c:596
    #5  0xffffffc00848a6a8 in really_probe (drv=0xffffffc008a47f00 <virtio_rng_driver>, dev=0xffffff800134d410)
        at drivers/base/dd.c:558
    #6  __driver_probe_device (drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>, dev=dev@entry=0xffffff800134d410)
        at drivers/base/dd.c:751
    #7  0xffffffc00848a7a4 in driver_probe_device (drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>,
        dev=dev@entry=0xffffff800134d410) at drivers/base/dd.c:781
    #8  0xffffffc00848afd8 in __driver_attach (data=0xffffffc008a47f00 <virtio_rng_driver>, dev=0xffffff800134d410)
        at drivers/base/dd.c:1140
    #9  __driver_attach (dev=0xffffff800134d410, data=0xffffffc008a47f00 <virtio_rng_driver>) at drivers/base/dd.c:1092
    #10 0xffffffc008487df0 in bus_for_each_dev (bus=<optimized out>, start=start@entry=0x0,
        data=data@entry=0xffffffc008a47f00 <virtio_rng_driver>, fn=fn@entry=0xffffffc00848aee0 <__driver_attach>)
        at drivers/base/bus.c:301
    #11 0xffffffc008489c24 in driver_attach (drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>) at drivers/base/dd.c:1157
    #12 0xffffffc008489624 in bus_add_driver (drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>) at drivers/base/bus.c:618
    #13 0xffffffc00848ba38 in driver_register (drv=drv@entry=0xffffffc008a47f00 <virtio_rng_driver>)
        at drivers/base/driver.c:171
    #14 0xffffffc0083c0cd8 in register_virtio_driver (driver=driver@entry=0xffffffc008a47f00 <virtio_rng_driver>)
        at drivers/virtio/virtio.c:325
    #15 0xffffffc0088acbe8 in virtio_rng_driver_init () at drivers/char/hw_random/virtio-rng.c:216
    #16 0xffffffc0080128d0 in do_one_initcall (fn=0xffffffc0088acbd0 <virtio_rng_driver_init>) at init/main.c:1306
    #17 0xffffffc008891438 in do_initcall_level (command_line=0xffffff8001137280 "rootwait", level=6) at init/main.c:1379
    #18 do_initcalls () at init/main.c:1395
    #19 do_basic_setup () at init/main.c:1414
    #20 kernel_init_freeable () at init/main.c:1617
    #21 0xffffffc0086e9878 in kernel_init (unused=<optimized out>) at init/main.c:1508
    #22 0xffffffc008013de0 in ret_from_fork () at arch/arm64/kernel/entry.S:756
    Backtrace stopped: previous frame identical to this frame (corrupt stack?)
    (gdb)

```

### vq->notify --> virtio_pci_common.c:vp_notify



