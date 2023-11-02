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

## Process Management

### kernel_clone (do_fork)

```c
Breakpoint 1, copy_process (pid=pid@entry=0x0, trace=trace@entry=0, node=node@entry=-1,
    args=args@entry=0xffffffc00928bd78) at kernel/fork.c:2011
warning: Source file is more recent than executable.
2011            if ((clone_flags & (CLONE_NEWNS|CLONE_FS)) == (CLONE_NEWNS|CLONE_FS))
(gdb) bt
#0  copy_process (pid=pid@entry=0x0, trace=trace@entry=0, node=node@entry=-1, args=args@entry=0xffffffc00928bd78)
    at kernel/fork.c:2011
#1  0xffffffc00803b96c in kernel_clone (args=args@entry=0xffffffc00928bd78) at kernel/fork.c:2679
#2  0xffffffc00803bd38 in __do_sys_clone (clone_flags=<optimized out>, newsp=<optimized out>,
    parent_tidptr=<optimized out>, tls=<optimized out>, child_tidptr=<optimized out>) at kernel/fork.c:2820
#3  0xffffffc00803c0f0 in __se_sys_clone (child_tidptr=<optimized out>, tls=<optimized out>,
    parent_tidptr=<optimized out>, newsp=<optimized out>, clone_flags=<optimized out>) at kernel/fork.c:2788
#4  __arm64_sys_clone (regs=<optimized out>) at kernel/fork.c:2788
#5  0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc00928beb0)
    at arch/arm64/kernel/syscall.c:38
#6  invoke_syscall (regs=regs@entry=0xffffffc00928beb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#7  0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc00928beb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#8  0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc00928beb0) at arch/arm64/kernel/syscall.c:206
#9  0xffffffc00874de6c in el0_svc (regs=0xffffffc00928beb0) at arch/arm64/kernel/entry-common.c:637
#10 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#11 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```

### release_task

```c
Breakpoint 2, release_task (p=p@entry=0xffffff80025dc380) at kernel/exit.c:247
247             dec_rlimit_ucounts(task_ucounts(p), UCOUNT_RLIMIT_NPROC, 1);
(gdb) bt
#0  release_task (p=p@entry=0xffffff80025dc380) at kernel/exit.c:247
#1  0xffffffc008041af8 in wait_task_zombie (p=0xffffff80025dc380, wo=0xffffffc009283ce0) at kernel/exit.c:1205
#2  wait_consider_task (wo=wo@entry=0xffffffc009283ce0, ptrace=<optimized out>, ptrace@entry=0,
    p=p@entry=0xffffff80025dc380) at kernel/exit.c:1432
#3  0xffffffc008041dd0 in do_wait_thread (tsk=0xffffff80025d8000, wo=0xffffffc009283ce0) at kernel/exit.c:1495
#4  do_wait (wo=wo@entry=0xffffffc009283ce0) at kernel/exit.c:1612
#5  0xffffffc0080434a0 in kernel_wait4 (upid=<optimized out>, stat_addr=0x7fca3cc00c, options=<optimized out>, ru=0x0)
    at kernel/exit.c:1775
#6  0xffffffc008043654 in __do_sys_wait4 (upid=<optimized out>, stat_addr=<optimized out>, options=<optimized out>,
    ru=<optimized out>) at kernel/exit.c:1803
#7  0xffffffc0080437e4 in __se_sys_wait4 (ru=<optimized out>, options=<optimized out>, stat_addr=<optimized out>,
    upid=<optimized out>) at kernel/exit.c:1799
#8  __arm64_sys_wait4 (regs=<optimized out>) at kernel/exit.c:1799
#9  0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc009283eb0)
    at arch/arm64/kernel/syscall.c:38
#10 invoke_syscall (regs=regs@entry=0xffffffc009283eb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#11 0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc009283eb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#12 0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc009283eb0) at arch/arm64/kernel/syscall.c:206
#13 0xffffffc00874de6c in el0_svc (regs=0xffffffc009283eb0) at arch/arm64/kernel/entry-common.c:637
#14 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#15 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```

### find_new_reaper

```c
Breakpoint 3, find_new_reaper (child_reaper=0xffffff80014b8000, father=0xffffff80025d8000) at kernel/exit.c:622
622             thread = find_alive_thread(father);
(gdb) bt
#0  find_new_reaper (child_reaper=0xffffff80014b8000, father=0xffffff80025d8000) at kernel/exit.c:622
#1  forget_original_parent (dead=0xffffffc009233db8, father=0xffffff80025d8000) at kernel/exit.c:697
#2  exit_notify (group_dead=1, tsk=0xffffff80025d8000) at kernel/exit.c:730
#3  do_exit (code=code@entry=0) at kernel/exit.c:889
#4  0xffffffc008043324 in do_group_exit (exit_code=0) at kernel/exit.c:1019
#5  0xffffffc008043398 in __do_sys_exit_group (error_code=<optimized out>) at kernel/exit.c:1030
#6  __se_sys_exit_group (error_code=<optimized out>) at kernel/exit.c:1028
#7  __arm64_sys_exit_group (regs=<optimized out>) at kernel/exit.c:1028
#8  0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc009233eb0)
    at arch/arm64/kernel/syscall.c:38
#9  invoke_syscall (regs=regs@entry=0xffffffc009233eb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#10 0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc009233eb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#11 0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc009233eb0) at arch/arm64/kernel/syscall.c:206
#12 0xffffffc00874de6c in el0_svc (regs=0xffffffc009233eb0) at arch/arm64/kernel/entry-common.c:637
#13 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#14 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```

## Process Scheduling

### pick_next_entity

```c
Breakpoint 1, pick_next_entity (cfs_rq=cfs_rq@entry=0xffffff807fbcd0c0, curr=0xffffff800157da80)
    at kernel/sched/fair.c:5014
5014    {
(gdb) bt
#0  pick_next_entity (cfs_rq=cfs_rq@entry=0xffffff807fbcd0c0, curr=0xffffff800157da80) at kernel/sched/fair.c:5014
#1  0xffffffc00807f468 in pick_next_task_fair (rq=rq@entry=0xffffff807fbcd000, prev=prev@entry=0xffffff800157da00,
    rf=rf@entry=0xffffffc00915bd68) at kernel/sched/fair.c:7786
#2  0xffffffc008750e08 in __pick_next_task (rf=0xffffffc00915bd68, prev=0xffffff800157da00, rq=0xffffff807fbcd000)
    at kernel/sched/core.c:5864
#3  pick_next_task (rf=0xffffffc00915bd68, prev=0xffffff800157da00, rq=0xffffff807fbcd000) at kernel/sched/core.c:6373
#4  __schedule (sched_mode=sched_mode@entry=0) at kernel/sched/core.c:6518
#5  0xffffffc0087513c0 in schedule () at kernel/sched/core.c:6630
#6  0xffffffc00875872c in schedule_timeout (timeout=timeout@entry=125) at kernel/time/timer.c:1935
#7  0xffffffc008165a9c in kcompactd (p=0xffffffc008b97a80 <contig_page_data>) at mm/compaction.c:2949
#8  0xffffffc008065958 in kthread (_create=0xffffff800162a900) at kernel/kthread.c:376
#9  0xffffffc008015984 in ret_from_fork () at arch/arm64/kernel/entry.S:860
```

### enqueue_entity

```c
Breakpoint 3, enqueue_entity (flags=<optimized out>, se=0xffffff800157da80, cfs_rq=0xffffff807fbcd0c0)
    at kernel/sched/fair.c:4761
4761            bool renorm = !(flags & ENQUEUE_WAKEUP) || (flags & ENQUEUE_MIGRATED);
(gdb) bt
#0  enqueue_entity (flags=<optimized out>, se=0xffffff800157da80, cfs_rq=0xffffff807fbcd0c0)
    at kernel/sched/fair.c:4761
#1  enqueue_task_fair (rq=0xffffff807fbcd000, p=<optimized out>, flags=<optimized out>) at kernel/sched/fair.c:6118
#2  0xffffffc0080713d4 in enqueue_task (flags=<optimized out>, p=0xffffff800157da00, rq=0xffffff807fbcd000)
    at kernel/sched/core.c:2060
#3  activate_task (flags=<optimized out>, p=0xffffff800157da00, rq=0xffffff807fbcd000) at kernel/sched/core.c:2088
#4  ttwu_do_activate (rq=rq@entry=0xffffff807fbcd000, p=p@entry=0xffffff800157da00, wake_flags=wake_flags@entry=0,
    rf=rf@entry=0xffffffc008003df8 <_text+15864>) at kernel/sched/core.c:3696
#5  0xffffffc008072e7c in ttwu_queue (wake_flags=0, cpu=<optimized out>, p=0xffffff800157da00)
    at kernel/sched/core.c:3901
#6  try_to_wake_up (p=0xffffff800157da00, state=state@entry=3, wake_flags=wake_flags@entry=0)
    at kernel/sched/core.c:4224
#7  0xffffffc008073118 in wake_up_process (p=<optimized out>) at kernel/sched/core.c:4358
#8  0xffffffc0080cea64 in process_timeout (t=t@entry=0xffffffc00915bd80) at kernel/time/timer.c:1862
#9  0xffffffc0080ceb7c in call_timer_fn (timer=timer@entry=0xffffffc00915bd80,
    fn=fn@entry=0xffffffc0080cea50 <process_timeout>, baseclk=<optimized out>) at kernel/time/timer.c:1474
#10 0xffffffc0080ceca8 in expire_timers (base=base@entry=0xffffff807fbc7000,
    head=head@entry=0xffffffc008003f00 <_text+16128>) at kernel/time/timer.c:1519
#11 0xffffffc0080cf7f4 in __run_timers (base=0xffffff807fbc7000) at kernel/time/timer.c:1790
#12 __run_timers (base=0xffffff807fbc7000) at kernel/time/timer.c:1763
#13 run_timer_softirq (h=<optimized out>) at kernel/time/timer.c:1803
#14 0xffffffc00801012c in __do_softirq () at kernel/softirq.c:571
#15 0xffffffc008015a00 in ____do_softirq (regs=<optimized out>) at arch/arm64/kernel/irq.c:79
#16 0xffffffc0080159c0 in call_on_irq_stack () at arch/arm64/kernel/entry.S:889
```

### dequeue_entity

```c
Breakpoint 2, dequeue_entity (flags=<optimized out>, se=<optimized out>, cfs_rq=<optimized out>)
    at kernel/sched/fair.c:4874
4874            update_curr(cfs_rq);
(gdb) bt
#0  dequeue_entity (flags=<optimized out>, se=<optimized out>, cfs_rq=<optimized out>) at kernel/sched/fair.c:4874
#1  dequeue_task_fair (rq=0xffffff807fbcd000, p=0xffffff800157da00, flags=9) at kernel/sched/fair.c:6196
#2  0xffffffc008751020 in dequeue_task (flags=9, p=0xffffff800157da00, rq=0xffffff807fbcd000)
    at kernel/sched/core.c:2080
#3  deactivate_task (flags=9, p=0xffffff800157da00, rq=0xffffff807fbcd000) at kernel/sched/core.c:2097
#4  __schedule (sched_mode=sched_mode@entry=0) at kernel/sched/core.c:6508
#5  0xffffffc0087513c0 in schedule () at kernel/sched/core.c:6630
#6  0xffffffc00875872c in schedule_timeout (timeout=timeout@entry=125) at kernel/time/timer.c:1935
#7  0xffffffc008165a9c in kcompactd (p=0xffffffc008b97a80 <contig_page_data>) at mm/compaction.c:2949
#8  0xffffffc008065958 in kthread (_create=0xffffff800162a900) at kernel/kthread.c:376
#9  0xffffffc008015984 in ret_from_fork () at arch/arm64/kernel/entry.S:860
```

### pick_next_task_fair

```c
Breakpoint 4, pick_next_task_fair (rq=rq@entry=0xffffff807fbcd000, prev=prev@entry=0xffffff800157da00,
    rf=0xffffffc00915bd28, rf@entry=0xffffffc00915bd68) at kernel/sched/fair.c:7733
7733    {
(gdb) bt
#0  pick_next_task_fair (rq=rq@entry=0xffffff807fbcd000, prev=prev@entry=0xffffff800157da00, rf=0xffffffc00915bd28,
    rf@entry=0xffffffc00915bd68) at kernel/sched/fair.c:7733
#1  0xffffffc008750e08 in __pick_next_task (rf=0xffffffc00915bd68, prev=0xffffff800157da00, rq=0xffffff807fbcd000)
    at kernel/sched/core.c:5864
#2  pick_next_task (rf=0xffffffc00915bd68, prev=0xffffff800157da00, rq=0xffffff807fbcd000) at kernel/sched/core.c:6373
#3  __schedule (sched_mode=sched_mode@entry=0) at kernel/sched/core.c:6518
#4  0xffffffc0087513c0 in schedule () at kernel/sched/core.c:6630
#5  0xffffffc00875872c in schedule_timeout (timeout=timeout@entry=125) at kernel/time/timer.c:1935
#6  0xffffffc008165a9c in kcompactd (p=0xffffffc008b97a80 <contig_page_data>) at mm/compaction.c:2949
#7  0xffffffc008065958 in kthread (_create=0xffffff800162a900) at kernel/kthread.c:376
#8  0xffffffc008015984 in ret_from_fork () at arch/arm64/kernel/entry.S:860
```

### context_switch

```c
Breakpoint 5, context_switch (rf=0xffffffc008ab3d88, next=0xffffff80025d9680, prev=0xffffffc008ac8a00 <init_task>,
    rq=0xffffff807fbcd000) at kernel/sched/core.c:5208
5208            if (!next->mm) {                                // to kernel
(gdb) bt
#0  context_switch (rf=0xffffffc008ab3d88, next=0xffffff80025d9680, prev=0xffffffc008ac8a00 <init_task>,
    rq=0xffffff807fbcd000) at kernel/sched/core.c:5208
#1  __schedule (sched_mode=sched_mode@entry=0) at kernel/sched/core.c:6554
#2  0xffffffc008751718 in schedule_idle () at kernel/sched/core.c:6658
#3  0xffffffc008086384 in do_idle () at kernel/sched/idle.c:331
#4  0xffffffc008086588 in cpu_startup_entry (state=state@entry=CPUHP_ONLINE) at kernel/sched/idle.c:400
#5  0xffffffc00874f434 in rest_init () at init/main.c:729
#6  0xffffffc00898086c in arch_call_rest_init () at init/main.c:890
```

## Process Communication

### pipe_read

```c
Breakpoint 1, pipe_read (iocb=<optimized out>, to=0xffffffc0092abd60) at fs/pipe.c:235
235             struct pipe_inode_info *pipe = filp->private_data;
(gdb) bt
#0  pipe_read (iocb=<optimized out>, to=0xffffffc0092abd60) at fs/pipe.c:235
#1  0xffffffc0081d663c in call_read_iter (iter=0xffffffc0092abd60, kio=0xffffffc0092abd88, file=0xffffff800261f000)
    at ./include/linux/fs.h:2199
#2  new_sync_read (ppos=0x0, len=4096, buf=0x555887d320 <error: Cannot access memory at address 0x555887d320>,
    filp=0xffffff800261f000) at fs/read_write.c:389
#3  vfs_read (file=file@entry=0xffffff800261f000,
    buf=buf@entry=0x555887d320 <error: Cannot access memory at address 0x555887d320>, count=count@entry=4096,
    pos=pos@entry=0x0) at fs/read_write.c:470
#4  0xffffffc0081d6f8c in ksys_read (fd=<optimized out>,
    buf=0x555887d320 <error: Cannot access memory at address 0x555887d320>, count=4096) at fs/read_write.c:613
#5  0xffffffc0081d6fcc in __do_sys_read (count=<optimized out>, buf=<optimized out>, fd=<optimized out>)
    at fs/read_write.c:623
#6  __se_sys_read (count=<optimized out>, buf=<optimized out>, fd=<optimized out>) at fs/read_write.c:621
#7  __arm64_sys_read (regs=<optimized out>) at fs/read_write.c:621
#8  0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc0092abeb0)
    at arch/arm64/kernel/syscall.c:38
#9  invoke_syscall (regs=regs@entry=0xffffffc0092abeb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#10 0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc0092abeb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#11 0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc0092abeb0) at arch/arm64/kernel/syscall.c:206
#12 0xffffffc00874de6c in el0_svc (regs=0xffffffc0092abeb0) at arch/arm64/kernel/entry-common.c:637
#13 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#14 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```

## Program Execution

### Execution Tracing

```c
Breakpoint 1, ptrace_request (child=child@entry=0xffffff80025d8000, request=request@entry=16900,
    addr=addr@entry=1029, data=data@entry=549433396296) at kernel/ptrace.c:1033
1033            bool seized = child->ptrace & PT_SEIZED;
(gdb) bt
#0  ptrace_request (child=child@entry=0xffffff80025d8000, request=request@entry=16900, addr=addr@entry=1029,
    data=data@entry=549433396296) at kernel/ptrace.c:1033
#1  0xffffffc00801b8cc in arch_ptrace (child=child@entry=0xffffff80025d8000, request=request@entry=16900,
    addr=addr@entry=1029, data=data@entry=549433396296) at arch/arm64/kernel/ptrace.c:2073
#2  0xffffffc00804ae08 in __do_sys_ptrace (data=<optimized out>, addr=<optimized out>, pid=<optimized out>,
    request=16900) at kernel/ptrace.c:1296
#3  __se_sys_ptrace (data=<optimized out>, addr=<optimized out>, pid=<optimized out>, request=16900)
    at kernel/ptrace.c:1269
#4  __arm64_sys_ptrace (regs=<optimized out>) at kernel/ptrace.c:1269
#5  0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc0092abeb0)
    at arch/arm64/kernel/syscall.c:38
#6  invoke_syscall (regs=regs@entry=0xffffffc0092abeb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#7  0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc0092abeb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#8  0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc0092abeb0) at arch/arm64/kernel/syscall.c:206
#9  0xffffffc00874de6c in el0_svc (regs=0xffffffc0092abeb0) at arch/arm64/kernel/entry-common.c:637
#10 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#11 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```

### Executable Formats

```c
Breakpoint 2, load_elf_binary (bprm=0xffffff8002586c00) at fs/binfmt_elf.c:841
841             struct elfhdr *elf_ex = (struct elfhdr *)bprm->buf;
(gdb) bt
#0  load_elf_binary (bprm=0xffffff8002586c00) at fs/binfmt_elf.c:841
#1  0xffffffc0081e010c in search_binary_handler (bprm=0xffffff8002586c00) at fs/exec.c:1727
#2  exec_binprm (bprm=0xffffff8002586c00) at fs/exec.c:1768
#3  bprm_execve (flags=<optimized out>, filename=<optimized out>, fd=<optimized out>, bprm=0xffffff8002586c00)
    at fs/exec.c:1837
#4  bprm_execve (bprm=0xffffff8002586c00, fd=<optimized out>, filename=<optimized out>, flags=<optimized out>)
    at fs/exec.c:1799
#5  0xffffffc0081e05ac in do_execveat_common (fd=fd@entry=-100, filename=0xffffff8001568000, argv=..., envp=...,
    flags=flags@entry=0) at fs/exec.c:1942
#6  0xffffffc0081e12f0 in do_execve (__envp=0x5566ce5670, __argv=0x5566ce5660, filename=<optimized out>)
    at fs/exec.c:2016
#7  __do_sys_execve (envp=0x5566ce5670, argv=0x5566ce5660, filename=<optimized out>) at fs/exec.c:2092
#8  __se_sys_execve (envp=<optimized out>, argv=<optimized out>, filename=<optimized out>) at fs/exec.c:2087
#9  __arm64_sys_execve (regs=<optimized out>) at fs/exec.c:2087
#10 0xffffffc008026c74 in __invoke_syscall (syscall_fn=<optimized out>, regs=0xffffffc00927beb0)
    at arch/arm64/kernel/syscall.c:38
#11 invoke_syscall (regs=regs@entry=0xffffffc00927beb0, scno=<optimized out>, sc_nr=sc_nr@entry=451,
    syscall_table=<optimized out>) at arch/arm64/kernel/syscall.c:52
#12 0xffffffc008026d94 in el0_svc_common (regs=regs@entry=0xffffffc00927beb0, scno=<optimized out>,
    syscall_table=<optimized out>, sc_nr=451) at arch/arm64/kernel/syscall.c:142
#13 0xffffffc008026e6c in do_el0_svc (regs=regs@entry=0xffffffc00927beb0) at arch/arm64/kernel/syscall.c:206
#14 0xffffffc00874de6c in el0_svc (regs=0xffffffc00927beb0) at arch/arm64/kernel/entry-common.c:637
#15 0xffffffc00874e278 in el0t_64_sync_handler (regs=<optimized out>) at arch/arm64/kernel/entry-common.c:655
#16 0xffffffc008011548 in el0t_64_sync () at arch/arm64/kernel/entry.S:581
```