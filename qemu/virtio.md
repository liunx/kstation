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

### register virtio_queue_guest_notifier_read

```c
Thread 3 "qemu-system-aar" hit Breakpoint 3, virtio_queue_set_guest_notifier_fd_handler (vq=vq@entry=0x5555578f1ea0, assign=assign@entry=true, with_irqfd=with_irqfd@entry=false) at ../hw/virtio/virtio.c:3428
3428            event_notifier_set_handler(&vq->guest_notifier,
(gdb) bt
#0  virtio_queue_set_guest_notifier_fd_handler (vq=vq@entry=0x5555578f1ea0, assign=assign@entry=true,
    with_irqfd=with_irqfd@entry=false) at ../hw/virtio/virtio.c:3428
#1  0x0000555555b299a6 in virtio_pci_set_guest_notifier_fd_handler (with_irqfd=false, assign=true, n=0,
    vq=0x5555578f1ea0, vdev=0x5555578e9340) at ../hw/virtio/virtio-pci.c:1150
#2  virtio_pci_set_guest_notifier (d=d@entry=0x5555578e0f80, n=n@entry=0, assign=assign@entry=true,
    with_irqfd=with_irqfd@entry=false) at ../hw/virtio/virtio-pci.c:1175
#3  0x0000555555b2b720 in virtio_pci_set_guest_notifiers (d=0x5555578e0f80, nvqs=1, assign=true)
    at ../hw/virtio/virtio-pci.c:1238
#4  0x0000555555e902f8 in vu_rng_start (vdev=0x5555578e9340) at ../hw/virtio/vhost-user-rng.c:43
#5  0x0000555555e6aeb3 in virtio_set_status (vdev=vdev@entry=0x5555578e9340, val=val@entry=15 '\017')
    at ../hw/virtio/virtio.c:2032
#6  0x0000555555b2905f in virtio_pci_common_write (opaque=0x5555578e0f80, addr=<optimized out>, val=<optimized out>,
    size=<optimized out>) at ../hw/virtio/virtio-pci.c:1539
#7  0x0000555555e9ac34 in memory_region_write_accessor (mr=mr@entry=0x5555578e1ab0, addr=20,
    value=value@entry=0x7ffff67b4148, size=size@entry=1, shift=<optimized out>, mask=mask@entry=255, attrs=...)
    at ../softmmu/memory.c:493
#8  0x0000555555e96c76 in access_with_adjusted_size (addr=addr@entry=20, value=value@entry=0x7ffff67b4148,
    size=size@entry=1, access_size_min=<optimized out>, access_size_max=<optimized out>,
    access_fn=0x555555e9abb0 <memory_region_write_accessor>, mr=0x5555578e1ab0, attrs=...) at ../softmmu/memory.c:555
#9  0x0000555555e9a2c8 in memory_region_dispatch_write (mr=mr@entry=0x5555578e1ab0, addr=addr@entry=20,
    data=<optimized out>, data@entry=15, op=op@entry=MO_8, attrs=...) at ../softmmu/memory.c:1522
#10 0x0000555555f17792 in io_writex (env=env@entry=0x555556efa1d0, full=full@entry=0x7fff2105e070,
    mmu_idx=mmu_idx@entry=4, val=val@entry=15, addr=addr@entry=18446743798984396820,
    retaddr=retaddr@entry=140736272268301, op=MO_8) at ../accel/tcg/cputlb.c:1430
#11 0x0000555555f1b777 in store_helper (op=MO_8, retaddr=140736272268301, oi=<optimized out>, val=15,
    addr=18446743798984396820, env=0x555556efa1d0) at ../accel/tcg/cputlb.c:2454
#12 full_stb_mmu (env=0x555556efa1d0, addr=18446743798984396820, val=15, oi=<optimized out>, retaddr=140736272268301)
    at ../accel/tcg/cputlb.c:2503
#13 0x00007fffb783fc0d in code_gen_buffer ()
#14 0x0000555555f0cacb in cpu_tb_exec (cpu=cpu@entry=0x555556ef79e0,
    itb=itb@entry=0x7fffb7983ac0 <code_gen_buffer+127416979>, tb_exit=tb_exit@entry=0x7ffff67b4804)
    at ../accel/tcg/cpu-exec.c:460
#15 0x0000555555f0ceba in cpu_loop_exec_tb (tb_exit=0x7ffff67b4804, last_tb=<synthetic pointer>, pc=<optimized out>,
    tb=0x7fffb7983ac0 <code_gen_buffer+127416979>, cpu=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:893
#16 cpu_exec_loop (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0) at ../accel/tcg/cpu-exec.c:1013
#17 0x0000555555f0d7a1 in cpu_exec_setjmp (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0)
    at ../accel/tcg/cpu-exec.c:1043
#18 0x0000555555f0de00 in cpu_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:1069
#19 0x0000555555f280e4 in tcg_cpus_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops.c:81
#20 0x0000555555f28237 in mttcg_cpu_thread_fn (arg=arg@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops-mttcg.c:95
#21 0x000055555609e711 in qemu_thread_start (args=<optimized out>) at ../util/qemu-thread-posix.c:541
#22 0x00007ffff7694ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#23 0x00007ffff7726a40 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```

### virtio_queue_guest_notifier_read --> virtio_pci_notify

```c
Thread 1 "qemu-system-aar" hit Breakpoint 7, virtio_notify_vector (vdev=0x5555578e9340, vector=65535) at ../hw/virtio/virtio.c:1977
1977        BusState *qbus = qdev_get_parent_bus(DEVICE(vdev));
(gdb) n
1978        VirtioBusClass *k = VIRTIO_BUS_GET_CLASS(qbus);
(gdb)
1980        if (virtio_device_disabled(vdev)) {
(gdb)
1984        if (k->notify) {
(gdb)
1985            k->notify(qbus->parent, vector);
(gdb) s
virtio_pci_notify (d=0x5555578e0f80, vector=65535) at ../hw/virtio/virtio-pci.c:72
72      {
```

### virtio_pci_vector_poll

```c
Thread 3 "qemu-system-aar" hit Breakpoint 1, virtio_pci_vector_poll (dev=0x5555578e0f80, vector_start=0, vector_end=1) at ../hw/virtio/virtio-pci.c:1107
1107        for (queue_no = 0; queue_no < proxy->nvqs_with_notifiers; queue_no++) {
(gdb) bt
#0  virtio_pci_vector_poll (dev=0x5555578e0f80, vector_start=0, vector_end=1) at ../hw/virtio/virtio-pci.c:1107
#1  0x0000555555a6a361 in msix_set_vector_notifiers (dev=dev@entry=0x5555578e0f80,
    use_notifier=use_notifier@entry=0x555555b29b70 <virtio_pci_vector_unmask>,
    release_notifier=release_notifier@entry=0x555555b297a0 <virtio_pci_vector_mask>,
    poll_notifier=poll_notifier@entry=0x555555b2b2d0 <virtio_pci_vector_poll>) at ../hw/pci/msix.c:641
#2  0x0000555555b2b869 in virtio_pci_set_guest_notifiers (d=0x5555578e0f80, nvqs=1, assign=<optimized out>)
    at ../hw/virtio/virtio-pci.c:1268
#3  0x0000555555e902f8 in vu_rng_start (vdev=0x5555578e9340) at ../hw/virtio/vhost-user-rng.c:43
#4  0x0000555555e6aeb3 in virtio_set_status (vdev=vdev@entry=0x5555578e9340, val=val@entry=15 '\017')
    at ../hw/virtio/virtio.c:2032
#5  0x0000555555b2905f in virtio_pci_common_write (opaque=0x5555578e0f80, addr=<optimized out>, val=<optimized out>,
    size=<optimized out>) at ../hw/virtio/virtio-pci.c:1539
#6  0x0000555555e9ac34 in memory_region_write_accessor (mr=mr@entry=0x5555578e1ab0, addr=20,
    value=value@entry=0x7ffff67b4148, size=size@entry=1, shift=<optimized out>, mask=mask@entry=255, attrs=...)
    at ../softmmu/memory.c:493
#7  0x0000555555e96c76 in access_with_adjusted_size (addr=addr@entry=20, value=value@entry=0x7ffff67b4148,
    size=size@entry=1, access_size_min=<optimized out>, access_size_max=<optimized out>,
    access_fn=0x555555e9abb0 <memory_region_write_accessor>, mr=0x5555578e1ab0, attrs=...) at ../softmmu/memory.c:555
#8  0x0000555555e9a2c8 in memory_region_dispatch_write (mr=mr@entry=0x5555578e1ab0, addr=addr@entry=20,
    data=<optimized out>, data@entry=15, op=op@entry=MO_8, attrs=...) at ../softmmu/memory.c:1522
#9  0x0000555555f17792 in io_writex (env=env@entry=0x555556efa1d0, full=full@entry=0x7fff2036eed0,
    mmu_idx=mmu_idx@entry=4, val=val@entry=15, addr=addr@entry=18446743798984396820,
    retaddr=retaddr@entry=140736167358605, op=MO_8) at ../accel/tcg/cputlb.c:1430
#10 0x0000555555f1b777 in store_helper (op=MO_8, retaddr=140736167358605, oi=<optimized out>, val=15,
    addr=18446743798984396820, env=0x555556efa1d0) at ../accel/tcg/cputlb.c:2454
#11 full_stb_mmu (env=0x555556efa1d0, addr=18446743798984396820, val=15, oi=<optimized out>, retaddr=140736167358605)
    at ../accel/tcg/cputlb.c:2503
#12 0x00007fffb143308d in code_gen_buffer ()
#13 0x0000555555f0cacb in cpu_tb_exec (cpu=cpu@entry=0x555556ef79e0,
    itb=itb@entry=0x7fffb1574340 <code_gen_buffer+22496019>, tb_exit=tb_exit@entry=0x7ffff67b4804)
    at ../accel/tcg/cpu-exec.c:460
#14 0x0000555555f0ceba in cpu_loop_exec_tb (tb_exit=0x7ffff67b4804, last_tb=<synthetic pointer>, pc=<optimized out>,
    tb=0x7fffb1574340 <code_gen_buffer+22496019>, cpu=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:893
#15 cpu_exec_loop (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0) at ../accel/tcg/cpu-exec.c:1013
#16 0x0000555555f0d7a1 in cpu_exec_setjmp (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0)
    at ../accel/tcg/cpu-exec.c:1043
#17 0x0000555555f0de00 in cpu_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:1069
#18 0x0000555555f280e4 in tcg_cpus_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops.c:81
#19 0x0000555555f28237 in mttcg_cpu_thread_fn (arg=arg@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops-mttcg.c:95
#20 0x000055555609e711 in qemu_thread_start (args=<optimized out>) at ../util/qemu-thread-posix.c:541
#21 0x00007ffff7694ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#22 0x00007ffff7726a40 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```

### virtio_pci_set_guest_notifiers

```c
Thread 3 "qemu-system-aar" hit Breakpoint 3, virtio_pci_set_guest_notifiers (d=0x5555578e0f80, nvqs=1, assign=true) at ../hw/virtio/virtio-pci.c:1198
1198    {
(gdb) bt
#0  virtio_pci_set_guest_notifiers (d=0x5555578e0f80, nvqs=1, assign=true) at ../hw/virtio/virtio-pci.c:1198
#1  0x0000555555e902f8 in vu_rng_start (vdev=0x5555578e9340) at ../hw/virtio/vhost-user-rng.c:43
#2  0x0000555555e6aeb3 in virtio_set_status (vdev=vdev@entry=0x5555578e9340, val=val@entry=15 '\017')
    at ../hw/virtio/virtio.c:2032
#3  0x0000555555b2905f in virtio_pci_common_write (opaque=0x5555578e0f80, addr=<optimized out>, val=<optimized out>,
    size=<optimized out>) at ../hw/virtio/virtio-pci.c:1539
#4  0x0000555555e9ac34 in memory_region_write_accessor (mr=mr@entry=0x5555578e1ab0, addr=20,
    value=value@entry=0x7ffff67b4148, size=size@entry=1, shift=<optimized out>, mask=mask@entry=255, attrs=...)
    at ../softmmu/memory.c:493
#5  0x0000555555e96c76 in access_with_adjusted_size (addr=addr@entry=20, value=value@entry=0x7ffff67b4148,
    size=size@entry=1, access_size_min=<optimized out>, access_size_max=<optimized out>,
    access_fn=0x555555e9abb0 <memory_region_write_accessor>, mr=0x5555578e1ab0, attrs=...) at ../softmmu/memory.c:555
#6  0x0000555555e9a2c8 in memory_region_dispatch_write (mr=mr@entry=0x5555578e1ab0, addr=addr@entry=20,
    data=<optimized out>, data@entry=15, op=op@entry=MO_8, attrs=...) at ../softmmu/memory.c:1522
#7  0x0000555555f17792 in io_writex (env=env@entry=0x555556efa1d0, full=full@entry=0x7fff217ce320,
    mmu_idx=mmu_idx@entry=4, val=val@entry=15, addr=addr@entry=18446743798984396820,
    retaddr=retaddr@entry=140736376319309, op=MO_8) at ../accel/tcg/cputlb.c:1430
#8  0x0000555555f1b777 in store_helper (op=MO_8, retaddr=140736376319309, oi=<optimized out>, val=15,
    addr=18446743798984396820, env=0x555556efa1d0) at ../accel/tcg/cputlb.c:2454
#9  full_stb_mmu (env=0x555556efa1d0, addr=18446743798984396820, val=15, oi=<optimized out>, retaddr=140736376319309)
    at ../accel/tcg/cputlb.c:2503
#10 0x00007fffbdb7ad4d in code_gen_buffer ()
#11 0x0000555555f0cacb in cpu_tb_exec (cpu=cpu@entry=0x555556ef79e0,
    itb=itb@entry=0x7fffbdcb9dc0 <code_gen_buffer+231447955>, tb_exit=tb_exit@entry=0x7ffff67b4804)
    at ../accel/tcg/cpu-exec.c:460
#12 0x0000555555f0ceba in cpu_loop_exec_tb (tb_exit=0x7ffff67b4804, last_tb=<synthetic pointer>, pc=<optimized out>,
    tb=0x7fffbdcb9dc0 <code_gen_buffer+231447955>, cpu=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:893
#13 cpu_exec_loop (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0) at ../accel/tcg/cpu-exec.c:1013
#14 0x0000555555f0d7a1 in cpu_exec_setjmp (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0)
    at ../accel/tcg/cpu-exec.c:1043
#15 0x0000555555f0de00 in cpu_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:1069
#16 0x0000555555f280e4 in tcg_cpus_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops.c:81
#17 0x0000555555f28237 in mttcg_cpu_thread_fn (arg=arg@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops-mttcg.c:95
#18 0x000055555609e711 in qemu_thread_start (args=<optimized out>) at ../util/qemu-thread-posix.c:541
#19 0x00007ffff7694ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#20 0x00007ffff7726a40 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```

### virtio_pci_ioeventfd_assign (vhost_dev_enable_notifiers)

```c
Thread 3 "qemu-system-aar" hit Breakpoint 5, virtio_pci_ioeventfd_assign (d=0x5555578e0f80, notifier=0x5555578f1f14, n=0, assign=true) at ../hw/virtio/virtio-pci.c:329
329     {
(gdb) bt
#0  virtio_pci_ioeventfd_assign (d=0x5555578e0f80, notifier=0x5555578f1f14, n=0, assign=true)
    at ../hw/virtio/virtio-pci.c:329
#1  0x0000555555b274cc in virtio_bus_set_host_notifier (bus=0x5555578e92c0, n=n@entry=0, assign=assign@entry=true)
    at ../hw/virtio/virtio-bus.c:296
#2  0x0000555555e7556a in vhost_dev_enable_notifiers (hdev=hdev@entry=0x5555578e9580, vdev=vdev@entry=0x5555578e9340)
    at ../hw/virtio/vhost.c:1572
#3  0x0000555555e902d9 in vu_rng_start (vdev=0x5555578e9340) at ../hw/virtio/vhost-user-rng.c:37
#4  0x0000555555e6aeb3 in virtio_set_status (vdev=vdev@entry=0x5555578e9340, val=val@entry=15 '\017')
    at ../hw/virtio/virtio.c:2032
#5  0x0000555555b2905f in virtio_pci_common_write (opaque=0x5555578e0f80, addr=<optimized out>, val=<optimized out>,
    size=<optimized out>) at ../hw/virtio/virtio-pci.c:1539
#6  0x0000555555e9ac34 in memory_region_write_accessor (mr=mr@entry=0x5555578e1ab0, addr=20,
    value=value@entry=0x7ffff67b4148, size=size@entry=1, shift=<optimized out>, mask=mask@entry=255, attrs=...)
    at ../softmmu/memory.c:493
#7  0x0000555555e96c76 in access_with_adjusted_size (addr=addr@entry=20, value=value@entry=0x7ffff67b4148,
    size=size@entry=1, access_size_min=<optimized out>, access_size_max=<optimized out>,
    access_fn=0x555555e9abb0 <memory_region_write_accessor>, mr=0x5555578e1ab0, attrs=...) at ../softmmu/memory.c:555
#8  0x0000555555e9a2c8 in memory_region_dispatch_write (mr=mr@entry=0x5555578e1ab0, addr=addr@entry=20,
    data=<optimized out>, data@entry=15, op=op@entry=MO_8, attrs=...) at ../softmmu/memory.c:1522
#9  0x0000555555f17792 in io_writex (env=env@entry=0x555556efa1d0, full=full@entry=0x7fff220f3580,
    mmu_idx=mmu_idx@entry=4, val=val@entry=15, addr=addr@entry=18446743798984396820,
    retaddr=retaddr@entry=140736480591117, op=MO_8) at ../accel/tcg/cputlb.c:1430
#10 0x0000555555f1b777 in store_helper (op=MO_8, retaddr=140736480591117, oi=<optimized out>, val=15,
    addr=18446743798984396820, env=0x555556efa1d0) at ../accel/tcg/cputlb.c:2454
#11 full_stb_mmu (env=0x555556efa1d0, addr=18446743798984396820, val=15, oi=<optimized out>, retaddr=140736480591117)
    at ../accel/tcg/cputlb.c:2503
#12 0x00007fffc3eebd0d in code_gen_buffer ()
#13 0x0000555555f0cacb in cpu_tb_exec (cpu=cpu@entry=0x555556ef79e0,
    itb=itb@entry=0x7fffc402ea80 <code_gen_buffer+335735379>, tb_exit=tb_exit@entry=0x7ffff67b4804)
    at ../accel/tcg/cpu-exec.c:460
#14 0x0000555555f0ceba in cpu_loop_exec_tb (tb_exit=0x7ffff67b4804, last_tb=<synthetic pointer>, pc=<optimized out>,
    tb=0x7fffc402ea80 <code_gen_buffer+335735379>, cpu=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:893
#15 cpu_exec_loop (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0) at ../accel/tcg/cpu-exec.c:1013
#16 0x0000555555f0d7a1 in cpu_exec_setjmp (cpu=cpu@entry=0x555556ef79e0, sc=sc@entry=0x7ffff67b48b0)
    at ../accel/tcg/cpu-exec.c:1043
#17 0x0000555555f0de00 in cpu_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/cpu-exec.c:1069
#18 0x0000555555f280e4 in tcg_cpus_exec (cpu=cpu@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops.c:81
#19 0x0000555555f28237 in mttcg_cpu_thread_fn (arg=arg@entry=0x555556ef79e0) at ../accel/tcg/tcg-accel-ops-mttcg.c:95
#20 0x000055555609e711 in qemu_thread_start (args=<optimized out>) at ../util/qemu-thread-posix.c:541
#21 0x00007ffff7694ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#22 0x00007ffff7726a40 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
```

### vhost-user-rng-pci.c

```c
static void vhost_user_rng_pci_instance_init(Object *obj)
{
    VHostUserRNGPCI *dev = VHOST_USER_RNG_PCI(obj);

    // connect to "vhost-user-rng"
    virtio_instance_init_common(obj, &dev->vdev, sizeof(dev->vdev),
                                TYPE_VHOST_USER_RNG);
}

static const VirtioPCIDeviceTypeInfo vhost_user_rng_pci_info = {
    .base_name = TYPE_VHOST_USER_RNG_PCI,
    .non_transitional_name = "vhost-user-rng-pci",
    .instance_size = sizeof(VHostUserRNGPCI),
    .instance_init = vhost_user_rng_pci_instance_init,
    .class_init = vhost_user_rng_pci_class_init,
};

static void vhost_user_rng_pci_register(void)
{
    // register to "virtio-device"
    virtio_pci_types_register(&vhost_user_rng_pci_info);
}

```

### virtio_device_class_init --> virtio_device_realize --> virtio_bus_device_plugged --> virtio_pci_device_plugged

```c
Thread 1 "qemu-system-aar" hit Breakpoint 1, virtio_pci_device_plugged (d=0x5555578e0f80, errp=0x7fffffffd220) at ../hw/virtio/virtio-pci.c:1882
1882    {
(gdb) bt
#0  virtio_pci_device_plugged (d=0x5555578e0f80, errp=0x7fffffffd220) at ../hw/virtio/virtio-pci.c:1882
#1  0x0000555555b26cc3 in virtio_bus_device_plugged (vdev=vdev@entry=0x5555578e9340, errp=errp@entry=0x7fffffffd270)
    at ../hw/virtio/virtio-bus.c:74
#2  0x0000555555e686a2 in virtio_device_realize (dev=0x5555578e9340, errp=0x7fffffffd2d0)
    at ../hw/virtio/virtio.c:3612
#3  0x0000555555f2eb7b in device_set_realized (obj=<optimized out>, value=<optimized out>, errp=0x7fffffffd470)
    at ../hw/core/qdev.c:510
#4  0x0000555555f32a6a in property_set_bool (obj=0x5555578e9340, v=<optimized out>, name=<optimized out>,
    opaque=0x555556b83390, errp=0x7fffffffd470) at ../qom/object.c:2285
#5  0x0000555555f35b28 in object_property_set (obj=obj@entry=0x5555578e9340,
    name=name@entry=0x555556205fb3 "realized", v=v@entry=0x5555578f1570, errp=errp@entry=0x7fffffffd470)
    at ../qom/object.c:1420
#6  0x0000555555f39024 in object_property_set_qobject (obj=obj@entry=0x5555578e9340,
    name=name@entry=0x555556205fb3 "realized", value=value@entry=0x5555578f14b0, errp=errp@entry=0x7fffffffd470)
    at ../qom/qom-qobject.c:28
#7  0x0000555555f36179 in object_property_set_bool (obj=0x5555578e9340, name=0x555556205fb3 "realized",
    value=<optimized out>, errp=0x7fffffffd470) at ../qom/object.c:1489
#8  0x0000555555a6f989 in pci_qdev_realize (qdev=<optimized out>, errp=<optimized out>) at ../hw/pci/pci.c:2098
#9  0x0000555555f2eb7b in device_set_realized (obj=<optimized out>, value=<optimized out>, errp=0x7fffffffd6b0)
    at ../hw/core/qdev.c:510
#10 0x0000555555f32a6a in property_set_bool (obj=0x5555578e0f80, v=<optimized out>, name=<optimized out>,
    opaque=0x555556b83390, errp=0x7fffffffd6b0) at ../qom/object.c:2285
#11 0x0000555555f35b28 in object_property_set (obj=obj@entry=0x5555578e0f80,
    name=name@entry=0x555556205fb3 "realized", v=v@entry=0x5555578eb5b0, errp=errp@entry=0x7fffffffd6b0)
    at ../qom/object.c:1420
#12 0x0000555555f39024 in object_property_set_qobject (obj=obj@entry=0x5555578e0f80,
    name=name@entry=0x555556205fb3 "realized", value=value@entry=0x5555578eb840, errp=errp@entry=0x7fffffffd6b0)
    at ../qom/qom-qobject.c:28
#13 0x0000555555f36179 in object_property_set_bool (obj=0x5555578e0f80, name=name@entry=0x555556205fb3 "realized",
    value=value@entry=true, errp=errp@entry=0x7fffffffd6b0) at ../qom/object.c:1489
#14 0x0000555555f2f532 in qdev_realize (dev=<optimized out>, bus=bus@entry=0x55555708b140,
    errp=errp@entry=0x7fffffffd6b0) at ../hw/core/qdev.c:292
#15 0x0000555555b4e8f7 in qdev_device_add_from_qdict (opts=opts@entry=0x555557743f60,
    from_json=from_json@entry=false, errp=0x7fffffffd6b0, errp@entry=0x555556acbfd8 <error_fatal>)
    at ../softmmu/qdev-monitor.c:714
#16 0x0000555555b4ea26 in qdev_device_add (opts=0x555556b80300, errp=errp@entry=0x555556acbfd8 <error_fatal>)
    at ../softmmu/qdev-monitor.c:733
#17 0x0000555555b50ff3 in device_init_func (opaque=<optimized out>, opts=<optimized out>,
    errp=0x555556acbfd8 <error_fatal>) at ../softmmu/vl.c:1140
#18 0x00005555560a6a32 in qemu_opts_foreach (list=<optimized out>, func=func@entry=0x555555b50fe0 <device_init_func>,
    opaque=opaque@entry=0x0, errp=errp@entry=0x555556acbfd8 <error_fatal>) at ../util/qemu-option.c:1135
#19 0x0000555555b5380a in qemu_create_cli_devices () at ../softmmu/vl.c:2542
#20 qmp_x_exit_preconfig (errp=<optimized out>) at ../softmmu/vl.c:2610
#21 0x0000555555b57233 in qmp_x_exit_preconfig (errp=<optimized out>) at ../softmmu/vl.c:2604
--Type <RET> for more, q to quit, c to continue without paging--
#22 qemu_init (argc=<optimized out>, argv=<optimized out>) at ../softmmu/vl.c:3612
#23 0x00005555558b681d in main (argc=<optimized out>, argv=<optimized out>) at ../softmmu/main.c:47
```
