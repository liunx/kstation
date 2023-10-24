### virtio-rng

```c
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

### setup_vq

```c
#0  setup_vq (vp_dev=0xffffff800134ec00, info=<optimized out>, index=<optimized out>,
    callback=0xffffffc0082d3550 <virtio_fs_vq_done>, name=<optimized out>, ctx=<optimized out>, msix_vec=1)
    at drivers/virtio/virtio_pci_modern.c:227
#1  0xffffffc0083d46b0 in vp_setup_vq (vdev=vdev@entry=0xffffff800134ec00, index=0,
    callback=0xffffffc0082d3550 <virtio_fs_vq_done>, name=0xffffff800138ece0 "hiprio", ctx=false,
    msix_vec=msix_vec@entry=1) at drivers/virtio/virtio_pci_common.c:189
#2  0xffffffc0083d4c98 in vp_find_vqs_msix (vdev=vdev@entry=0xffffff800134ec00, nvqs=nvqs@entry=2,
    vqs=vqs@entry=0xffffff80018d3900, callbacks=callbacks@entry=0xffffff80018d3980,
    names=names@entry=0xffffff80018d3a00, per_vq_vectors=per_vq_vectors@entry=true, ctx=ctx@entry=0x0,
    desc=desc@entry=0x0) at drivers/virtio/virtio_pci_common.c:323
#3  0xffffffc0083d4f08 in vp_find_vqs (vdev=vdev@entry=0xffffff800134ec00, nvqs=2, vqs=0xffffff80018d3900,
    callbacks=0xffffff80018d3980, names=0xffffff80018d3a00, ctx=0x0, desc=0x0)
    at drivers/virtio/virtio_pci_common.c:400
#4  0xffffffc0083d3ffc in vp_modern_find_vqs (vdev=0xffffff800134ec00, nvqs=<optimized out>, vqs=<optimized out>,
    callbacks=<optimized out>, names=<optimized out>, ctx=<optimized out>, desc=<optimized out>)
    at drivers/virtio/virtio_pci_modern.c:259
#5  0xffffffc0082d4d80 in virtio_find_vqs (desc=0x0, names=0xffffff80018d3a00, callbacks=0xffffff80018d3980,
    vqs=0xffffff80018d3900, nvqs=<optimized out>, vdev=0xffffff800134ec00) at ./include/linux/virtio_config.h:206
#6  virtio_fs_setup_vqs (fs=0xffffff80018d3880, vdev=0xffffff800134ec00) at fs/fuse/virtio_fs.c:713
#7  virtio_fs_probe (vdev=0xffffff800134ec00) at fs/fuse/virtio_fs.c:876
#8  0xffffffc0083cedcc in virtio_dev_probe (_d=0xffffff800134ec10) at drivers/virtio/virtio.c:273
#9  0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b0a020 <virtio_fs_driver>, dev=0xffffff800134ec10)
    at drivers/base/dd.c:517
```

### random_recv_done

```c
#0  random_recv_done (vq=<optimized out>) at drivers/char/hw_random/virtio-rng.c:37
#1  0xffffffc0083d004c in vring_interrupt (irq=53, _vq=<optimized out>) at drivers/virtio/virtio_ring.c:2165
#2  vring_interrupt (irq=irq@entry=53, _vq=<optimized out>) at drivers/virtio/virtio_ring.c:2147
#3  0xffffffc0083d479c in vp_vring_interrupt (irq=irq@entry=53, opaque=0xffffff800134f400)
    at drivers/virtio/virtio_pci_common.c:68
#4  0xffffffc0083d4830 in vp_interrupt (irq=53, opaque=<optimized out>) at drivers/virtio/virtio_pci_common.c:99
#5  0xffffffc00809c3fc in __handle_irq_event_percpu (desc=desc@entry=0xffffff80018d7400,
    flags=flags@entry=0xffffffc008003f54 <_text+16212>) at kernel/irq/handle.c:156
#6  0xffffffc00809c610 in handle_irq_event_percpu (desc=0xffffff80018d7400) at kernel/irq/handle.c:196
#7  handle_irq_event (desc=desc@entry=0xffffff80018d7400) at kernel/irq/handle.c:213
#8  0xffffffc0080a2170 in handle_fasteoi_irq (desc=0xffffff80018d7400) at kernel/irq/chip.c:717
#9  0xffffffc00809bbb0 in generic_handle_irq_desc (desc=<optimized out>) at ./include/linux/irqdesc.h:158
#10 handle_irq_desc (desc=<optimized out>) at kernel/irq/irqdesc.c:646
#11 handle_domain_irq (domain=<optimized out>, hwirq=37, regs=regs@entry=0xffffffc008e3bb70)
    at kernel/irq/irqdesc.c:701
#12 0xffffffc00836c974 in gic_handle_irq (regs=0xffffffc008e3bb70) at drivers/irqchip/irq-gic.c:372
#13 0xffffffc008013e3c in call_on_irq_stack () at arch/arm64/kernel/entry.S:785
```

### request virtio irq

```c
Breakpoint 4, dev_name (dev=<optimized out>) at drivers/virtio/virtio_pci_common.c:364
364             err = request_irq(vp_dev->pci_dev->irq, vp_interrupt, IRQF_SHARED,
(gdb) bt
#0  dev_name (dev=<optimized out>) at drivers/virtio/virtio_pci_common.c:364
#1  vp_find_vqs_intx (ctx=0x0, names=0xffffffc00800bbb0 <_text+48048>, callbacks=0xffffffc00800bba8 <_text+48040>,
    vqs=0xffffffc00800bba0 <_text+48032>, nvqs=1, vdev=0xffffff800134f400) at drivers/virtio/virtio_pci_common.c:364
#2  vp_find_vqs (vdev=vdev@entry=0xffffff800134f400, nvqs=1, vqs=0xffffffc00800bba0 <_text+48032>,
    callbacks=0xffffffc00800bba8 <_text+48040>, names=0xffffffc00800bbb0 <_text+48048>, ctx=0x0, desc=0x0)
    at drivers/virtio/virtio_pci_common.c:408
#3  0xffffffc0083d3ffc in vp_modern_find_vqs (vdev=0xffffff800134f400, nvqs=<optimized out>, vqs=<optimized out>,
    callbacks=<optimized out>, names=<optimized out>, ctx=<optimized out>, desc=<optimized out>)
    at drivers/virtio/virtio_pci_modern.c:259
#4  0xffffffc008419508 in virtio_find_single_vq (c=<optimized out>, n=0xffffffc0088ec470 "input",
    vdev=0xffffff800134f400) at ./include/linux/virtio_config.h:193
#5  probe_common (vdev=0xffffff800134f400) at drivers/char/hw_random/virtio-rng.c:113
#6  0xffffffc0084195a0 in virtrng_probe (vdev=<optimized out>) at drivers/char/hw_random/virtio-rng.c:146
#7  0xffffffc0083cedcc in virtio_dev_probe (_d=0xffffff800134f410) at drivers/virtio/virtio.c:273
#8  0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b18260 <virtio_rng_driver>, dev=0xffffff800134f410)
    at drivers/base/dd.c:517
```

### mdev->notify_base initialize

```c
Breakpoint 2, vp_modern_probe (mdev=mdev@entry=0xffffff800134ef30) at drivers/virtio/virtio_pci_modern_dev.c:310
310                     mdev->notify_base = vp_modern_map_capability(mdev, notify,
(gdb) bt
#0  vp_modern_probe (mdev=mdev@entry=0xffffff800134ef30) at drivers/virtio/virtio_pci_modern_dev.c:310
#1  0xffffffc0083d41a8 in virtio_pci_modern_probe (vp_dev=vp_dev@entry=0xffffff800134ec00)
    at drivers/virtio/virtio_pci_modern.c:425
#2  0xffffffc0083d44e0 in virtio_pci_probe (pci_dev=0xffffff80010b5000, id=<optimized out>)
    at drivers/virtio/virtio_pci_common.c:543
#3  0xffffffc008397df8 in local_pci_probe (_ddi=<synthetic pointer>) at drivers/pci/pci-driver.c:323
#4  pci_call_probe (id=0xffffffc008755208 <virtio_pci_id_table>, dev=0xffffff80010b5000,
    drv=0xffffffc008b10fe0 <virtio_pci_driver>) at drivers/pci/pci-driver.c:380
#5  __pci_device_probe (pci_dev=0xffffff80010b5000, drv=0xffffffc008b10fe0 <virtio_pci_driver>)
    at drivers/pci/pci-driver.c:405
#6  pci_device_probe (dev=0xffffff80010b50b0) at drivers/pci/pci-driver.c:448
#7  0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b11058 <virtio_pci_driver+120>, dev=0xffffff80010b50b0)
    at drivers/base/dd.c:517
```

### vq->priv (notify address)

* vq->priv initialize

    ```c
    Breakpoint 3, setup_vq (vp_dev=0xffffff800134f400, info=<optimized out>, index=<optimized out>, callback=0xffffffc0084191b0 <random_recv_done>, name=<optimized out>, ctx=<optimized out>, msix_vec=65535) at drivers/virtio/virtio_pci_modern.c:227
    227             vq->priv = (void __force *)vp_modern_map_vq_notify(mdev, index, NULL);
    (gdb) bt
    #0  setup_vq (vp_dev=0xffffff800134f400, info=<optimized out>, index=<optimized out>,
        callback=0xffffffc0084191b0 <random_recv_done>, name=<optimized out>, ctx=<optimized out>, msix_vec=65535)
        at drivers/virtio/virtio_pci_modern.c:227
    #1  0xffffffc0083d46b0 in vp_setup_vq (vdev=0xffffff800134f400, index=0,
        callback=0xffffffc0084191b0 <random_recv_done>, name=0xffffffc0088ec470 "input", ctx=false, msix_vec=65535)
        at drivers/virtio/virtio_pci_common.c:189
    #2  0xffffffc0083d4fcc in vp_find_vqs_intx (ctx=0x0, names=0xffffffc00800bbb0 <_text+48048>,
        callbacks=0xffffffc00800bba8 <_text+48040>, vqs=0xffffffc00800bba0 <_text+48032>, nvqs=1, vdev=0xffffff800134f400)
        at drivers/virtio/virtio_pci_common.c:376
    #3  vp_find_vqs (vdev=vdev@entry=0xffffff800134f400, nvqs=1, vqs=0xffffffc00800bba0 <_text+48032>,
        callbacks=0xffffffc00800bba8 <_text+48040>, names=0xffffffc00800bbb0 <_text+48048>, ctx=0x0, desc=<optimized out>)
        at drivers/virtio/virtio_pci_common.c:408
    #4  0xffffffc0083d3ffc in vp_modern_find_vqs (vdev=0xffffff800134f400, nvqs=<optimized out>, vqs=<optimized out>,
        callbacks=<optimized out>, names=<optimized out>, ctx=<optimized out>, desc=<optimized out>)
        at drivers/virtio/virtio_pci_modern.c:259
    #5  0xffffffc008419508 in virtio_find_single_vq (c=<optimized out>, n=0xffffffc0088ec470 "input",
        vdev=0xffffff800134f400) at ./include/linux/virtio_config.h:193
    #6  probe_common (vdev=0xffffff800134f400) at drivers/char/hw_random/virtio-rng.c:113
    #7  0xffffffc0084195a0 in virtrng_probe (vdev=<optimized out>) at drivers/char/hw_random/virtio-rng.c:146
    #8  0xffffffc0083cedcc in virtio_dev_probe (_d=0xffffff800134f410) at drivers/virtio/virtio.c:273
    #9  0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b18260 <virtio_rng_driver>, dev=0xffffff800134f410)
        at drivers/base/dd.c:517
    ```

* vq->priv post usage

    ```c
    Breakpoint 4, vp_notify (vq=0xffffff8001abbf00) at drivers/virtio/virtio_pci_common.c:45
    warning: Source file is more recent than executable.
    45              iowrite16(vq->index, (void __iomem *)vq->priv);
    (gdb) bt
    #0  vp_notify (vq=0xffffff8001abbf00) at drivers/virtio/virtio_pci_common.c:45
    #1  0xffffffc0083d0118 in virtqueue_notify (_vq=0xffffff8001abbf00) at drivers/virtio/virtio_ring.c:1949
    #2  virtqueue_kick (vq=0xffffff8001abbf00) at drivers/virtio/virtio_ring.c:1972
    #3  0xffffffc0084192b4 in register_buffer (size=<optimized out>,
        buf=0xffffff8001ac0c80 "/bus/virtio/drivers/virtio_rproc_serial", vi=0xffffff8001abbe00)
        at drivers/char/hw_random/virtio-rng.c:50
    #4  virtio_read (rng=<optimized out>, buf=0xffffff8001ac0c80, size=<optimized out>, wait=false)
        at drivers/char/hw_random/virtio-rng.c:63
    #5  0xffffffc008418bc8 in rng_get_data (wait=0, size=16,
        buffer=0xffffff8001ac0c80 "/bus/virtio/drivers/virtio_rproc_serial", rng=0xffffff8001abbe00)
        at drivers/char/hw_random/core.c:192
    #6  add_early_randomness (rng=rng@entry=0xffffff8001abbe00) at drivers/char/hw_random/core.c:70
    #7  0xffffffc008418f2c in hwrng_register (rng=rng@entry=0xffffff8001abbe00) at drivers/char/hw_random/core.c:517
    #8  0xffffffc00841918c in virtrng_scan (vdev=<optimized out>) at drivers/char/hw_random/virtio-rng.c:159
    #9  0xffffffc0083cedf8 in virtio_dev_probe (_d=0xffffff800134f410) at drivers/virtio/virtio.c:282
    #10 0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b18260 <virtio_rng_driver>, dev=0xffffff800134f410)
        at drivers/base/dd.c:517
    ```

### virtio-rng register_buffer(...)

* register buffer

    ```c
    Breakpoint 2, virtqueue_add_split (_vq=_vq@entry=0xffffff8001aca400, sgs=0xffffffc008dabb80, total_sg=<optimized out>, out_sgs=<optimized out>, in_sgs=2, data=0xffffff8002574390, ctx=ctx@entry=0x0, gfp=<optimized out>) at drivers/virtio/virtio_ring.c:607
    607             vq->split.desc_state[head].data = data;
    (gdb) bt
    #0  virtqueue_add_split (_vq=0xffffff8001abbf00, sgs=sgs@entry=0xffffffc008eabcc8, total_sg=1,
        out_sgs=<optimized out>, in_sgs=1, data=0xffffff8001ac0c80, ctx=0x0, gfp=<optimized out>)
        at drivers/virtio/virtio_ring.c:611
    #1  0xffffffc0083d1508 in virtqueue_add (gfp=3264, ctx=0x0, data=0xffffff8001ac0c80, in_sgs=1, out_sgs=0, total_sg=1,
        sgs=0xffffffc008eabcc8, _vq=<optimized out>) at drivers/virtio/virtio_ring.c:1806
    #2  virtqueue_add_inbuf (vq=<optimized out>, sg=<optimized out>, sg@entry=0xffffffc008eabd08, num=num@entry=1,
        data=data@entry=0xffffff8001ac0c80, gfp=gfp@entry=3264) at drivers/virtio/virtio_ring.c:1885
    #3  0xffffffc0084192ac in register_buffer (size=<optimized out>,
        buf=0xffffff8001ac0c80 "\036&ݧU\207E\346~\222x\003,\026\237\342\067\316q\221\354\024\031\237+Brg\rTA\\@_\342\267\363\264\232J\030)jz!\a\255\031\272\064\371\352\217J\217\246\001\210RaS\342E]", vi=0xffffff8001abbe00)
        at drivers/char/hw_random/virtio-rng.c:48
    #4  virtio_read (rng=<optimized out>, buf=0xffffff8001ac0c80, size=<optimized out>, wait=true)
        at drivers/char/hw_random/virtio-rng.c:63
    #5  0xffffffc0084185c4 in rng_get_data (wait=1, size=64,
        buffer=0xffffff8001ac0c80 "\036&ݧU\207E\346~\222x\003,\026\237\342\067\316q\221\354\024\031\237+Brg\rTA\\@_\342\267\363\264\232J\030)jz!\a\255\031\272\064\371\352\217J\217\246\001\210RaS\342E]", rng=0xffffff8001abbe00)
        at drivers/char/hw_random/core.c:192
    #6  rng_dev_read (filp=0xffffff8002872000, buf=0x7ff8ca3450 <error: Cannot access memory at address 0x7ff8ca3450>,
        size=2460, offp=<optimized out>) at drivers/char/hw_random/core.c:229
    #7  0xffffffc0081acb00 in vfs_read (file=file@entry=0xffffff8002872000,
        buf=buf@entry=0x7ff8ca3450 <error: Cannot access memory at address 0x7ff8ca3450>, count=count@entry=2500,
        pos=pos@entry=0xffffffc008eabdf0) at fs/read_write.c:483
    #8  0xffffffc0081acf38 in ksys_read (fd=<optimized out>,
        buf=0x7ff8ca3450 <error: Cannot access memory at address 0x7ff8ca3450>, count=2500) at fs/read_write.c:623
    #9  0xffffffc0081acff0 in __do_sys_read (count=<optimized out>, buf=<optimized out>, fd=<optimized out>)
        at fs/read_write.c:633
    #10 __se_sys_read (count=<optimized out>, buf=<optimized out>, fd=<optimized out>) at fs/read_write.c:631
    #11 __arm64_sys_read (regs=<optimized out>) at fs/read_write.c:631
    #12 0xffffffc008023754 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc008eabeb0)
        at arch/arm64/kernel/syscall.c:38
    ```

* fetch data from buffer

    ```c
    Breakpoint 4, virtqueue_get_buf_ctx_split (_vq=0xffffff8001abbf00, len=0xffffff8001abbebc, ctx=ctx@entry=0x0) at drivers/virtio/virtio_ring.c:790
    790             detach_buf_split(vq, i, ctx);
    (gdb) bt
    #0  virtqueue_get_buf_ctx_split (_vq=0xffffff8001abbf00, len=0xffffff8001abbebc, ctx=ctx@entry=0x0)
        at drivers/virtio/virtio_ring.c:790
    #1  0xffffffc0083d00c0 in virtqueue_get_buf_ctx (ctx=0x0, len=len@entry=0xffffff8001abbebc, _vq=<optimized out>)
        at drivers/virtio/virtio_ring.c:2000
    #2  virtqueue_get_buf (_vq=<optimized out>, len=len@entry=0xffffff8001abbebc) at drivers/virtio/virtio_ring.c:2006
    #3  0xffffffc0084191d4 in random_recv_done (vq=<optimized out>) at drivers/char/hw_random/virtio-rng.c:34
    #4  0xffffffc0083d004c in vring_interrupt (irq=53, _vq=<optimized out>) at drivers/virtio/virtio_ring.c:2165
    #5  vring_interrupt (irq=irq@entry=53, _vq=<optimized out>) at drivers/virtio/virtio_ring.c:2147
    #6  0xffffffc0083d479c in vp_vring_interrupt (irq=irq@entry=53, opaque=0xffffff800134f400)
        at drivers/virtio/virtio_pci_common.c:68
    #7  0xffffffc0083d4830 in vp_interrupt (irq=53, opaque=<optimized out>) at drivers/virtio/virtio_pci_common.c:99
    #8  0xffffffc00809c3fc in __handle_irq_event_percpu (desc=desc@entry=0xffffff80018d7400,
        flags=flags@entry=0xffffffc008003f54 <_text+16212>) at kernel/irq/handle.c:156
    #9  0xffffffc00809c610 in handle_irq_event_percpu (desc=0xffffff80018d7400) at kernel/irq/handle.c:196
    #10 handle_irq_event (desc=desc@entry=0xffffff80018d7400) at kernel/irq/handle.c:213
    #11 0xffffffc0080a2170 in handle_fasteoi_irq (desc=0xffffff80018d7400) at kernel/irq/chip.c:717
    #12 0xffffffc00809bbb0 in generic_handle_irq_desc (desc=<optimized out>) at ./include/linux/irqdesc.h:158
    #13 handle_irq_desc (desc=<optimized out>) at kernel/irq/irqdesc.c:646
    #14 handle_domain_irq (domain=<optimized out>, hwirq=37, regs=regs@entry=0xffffffc008eabae0)
        at kernel/irq/irqdesc.c:701
    #15 0xffffffc00836c974 in gic_handle_irq (regs=0xffffffc008eabae0) at drivers/irqchip/irq-gic.c:372
    #16 0xffffffc008013e3c in call_on_irq_stack () at arch/arm64/kernel/entry.S:785
    ```

### create virtqueue for virtio-rng

```c
Breakpoint 5, vring_create_virtqueue_split (name=0xffffffc0088ec470 "input", callback=0xffffffc0084191b0 <random_recv_done>, notify=0xffffffc0083d48e0 <vp_notify>, context=false, may_reduce_num=true, weak_barriers=true, vdev=0xffffff800134f400, vring_align=64, num=4, index=0) at drivers/virtio/virtio_ring.c:967
967             vq = __vring_new_virtqueue(index, vring, vdev, weak_barriers, context,
(gdb) bt
#0  vring_create_virtqueue_split (name=0xffffffc0088ec470 "input", callback=0xffffffc0084191b0 <random_recv_done>,
    notify=0xffffffc0083d48e0 <vp_notify>, context=false, may_reduce_num=true, weak_barriers=true,
    vdev=0xffffff800134f400, vring_align=64, num=4, index=0) at drivers/virtio/virtio_ring.c:967
#1  vring_create_virtqueue (index=index@entry=0, num=num@entry=4, vring_align=vring_align@entry=64,
    vdev=vdev@entry=0xffffff800134f400, weak_barriers=weak_barriers@entry=true,
    may_reduce_num=may_reduce_num@entry=true, context=context@entry=false, notify=0xffffffc0083d48e0 <vp_notify>,
    callback=0xffffffc0084191b0 <random_recv_done>, name=0xffffffc0088ec470 "input")
    at drivers/virtio/virtio_ring.c:2276
#2  0xffffffc0083d3a98 in setup_vq (vp_dev=0xffffff800134f400, info=0xffffff8001ab9780, index=0,
    callback=0xffffffc0084191b0 <random_recv_done>, name=0xffffffc0088ec470 "input", ctx=<optimized out>,
    msix_vec=65535) at drivers/virtio/virtio_pci_modern.c:214
#3  0xffffffc0083d46b0 in vp_setup_vq (vdev=0xffffff800134f400, index=0,
    callback=0xffffffc0084191b0 <random_recv_done>, name=0xffffffc0088ec470 "input", ctx=false, msix_vec=65535)
    at drivers/virtio/virtio_pci_common.c:189
#4  0xffffffc0083d4fcc in vp_find_vqs_intx (ctx=0x0, names=0xffffffc00800bbb0 <_text+48048>,
    callbacks=0xffffffc00800bba8 <_text+48040>, vqs=0xffffffc00800bba0 <_text+48032>, nvqs=1, vdev=0xffffff800134f400)
    at drivers/virtio/virtio_pci_common.c:376
#5  vp_find_vqs (vdev=vdev@entry=0xffffff800134f400, nvqs=1, vqs=0xffffffc00800bba0 <_text+48032>,
    callbacks=0xffffffc00800bba8 <_text+48040>, names=0xffffffc00800bbb0 <_text+48048>, ctx=0x0, desc=<optimized out>)
    at drivers/virtio/virtio_pci_common.c:408
#6  0xffffffc0083d3ffc in vp_modern_find_vqs (vdev=0xffffff800134f400, nvqs=<optimized out>, vqs=<optimized out>,
    callbacks=<optimized out>, names=<optimized out>, ctx=<optimized out>, desc=<optimized out>)
    at drivers/virtio/virtio_pci_modern.c:259
#7  0xffffffc008419508 in virtio_find_single_vq (c=<optimized out>, n=0xffffffc0088ec470 "input",
    vdev=0xffffff800134f400) at ./include/linux/virtio_config.h:193
#8  probe_common (vdev=0xffffff800134f400) at drivers/char/hw_random/virtio-rng.c:114
#9  0xffffffc0084195a0 in virtrng_probe (vdev=<optimized out>) at drivers/char/hw_random/virtio-rng.c:147
#10 0xffffffc0083cedcc in virtio_dev_probe (_d=0xffffff800134f410) at drivers/virtio/virtio.c:273
#11 0xffffffc00849c1ec in call_driver_probe (drv=0xffffffc008b18260 <virtio_rng_driver>, dev=0xffffff800134f410)
    at drivers/base/dd.c:517
```