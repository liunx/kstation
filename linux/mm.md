## Memory Management

### Detect Physical Memory Layout

* Get memory map from BIOS E820 interrrupt

    ```c
    Breakpoint 2, e820__memory_setup () at arch/x86/kernel/e820.c:1310
    1310            pr_info("BIOS-provided physical RAM map:\n");
    (gdb) bt
    #0  e820__memory_setup () at arch/x86/kernel/e820.c:1310
    #1  0xffffffff82e240d7 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:954
    #2  0xffffffff82e1a1b7 in start_kernel () at init/main.c:959
    #3  0xffffffff82e194a1 in x86_64_start_reservations (
        real_mode_data=real_mode_data@entry=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>) at arch/x86/kernel/head64.c:556
    #4  0xffffffff82e1956c in x86_64_start_kernel (
        real_mode_data=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>)
        at arch/x86/kernel/head64.c:537
    #5  0xffffffff81000145 in secondary_startup_64 () at arch/x86/kernel/head_64.S:358
    #6  0x0000000000000000 in ?? ()
    ```

### MemBlock Memory Management

* memblock_add_range

    ```c
    Breakpoint 2, memblock_add_range (type=type@entry=0xffffffff82ed2c18 <memblock+56>, base=16777216,
        size=size@entry=35651584, flags=flags@entry=MEMBLOCK_NONE, nid=1) at mm/memblock.c:591
    591             if (type->regions[0].size == 0) {
    (gdb) bt
    #0  memblock_add_range (type=type@entry=0xffffffff82ed2c18 <memblock+56>, base=16777216, size=size@entry=35651584,
        flags=flags@entry=MEMBLOCK_NONE, nid=1) at mm/memblock.c:591
    #1  0xffffffff82e6f481 in memblock_reserve (base=<optimized out>, size=35651584) at mm/memblock.c:860
    #2  0xffffffff82e23eb7 in early_reserve_memory () at arch/x86/kernel/setup.c:783
    #3  setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:951
    #4  0xffffffff82e1a1b7 in start_kernel () at init/main.c:959
    #5  0xffffffff82e194a1 in x86_64_start_reservations (
        real_mode_data=real_mode_data@entry=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>) at arch/x86/kernel/head64.c:556
    #6  0xffffffff82e1956c in x86_64_start_kernel (
        real_mode_data=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>)
        at arch/x86/kernel/head64.c:537
    #7  0xffffffff81000145 in secondary_startup_64 () at arch/x86/kernel/head_64.S:358
    ```

* memblock debug

    boot with command with "memblock=debug"

### Memory Model

### Buddy System

* __alloc_pages

    ```c
    Breakpoint 3, __alloc_pages (gfp=gfp@entry=4197824, order=1, preferred_nid=preferred_nid@entry=0,
        nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5529
    5529            struct alloc_context ac = { };
    (gdb) bt
    #0  __alloc_pages (gfp=gfp@entry=4197824, order=1, preferred_nid=preferred_nid@entry=0,
        nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5529
    #1  0xffffffff813b283b in __alloc_pages_node (order=order@entry=1, gfp_mask=4197824, nid=0)
        at ./include/linux/gfp.h:237
    #2  alloc_pages_node (order=order@entry=1, gfp_mask=4197824, nid=0) at ./include/linux/gfp.h:260
    #3  alloc_pages (order=order@entry=1, gfp_mask=4197824) at ./include/linux/gfp.h:271
    #4  __get_free_pages (gfp_mask=gfp_mask@entry=4197824, order=order@entry=1) at mm/page_alloc.c:5609
    #5  0xffffffff81168243 in _pgd_alloc () at arch/x86/mm/pgtable.c:414
    #6  pgd_alloc (mm=mm@entry=0xffff8881015a3680) at arch/x86/mm/pgtable.c:430
    #7  0xffffffff81177884 in mm_alloc_pgd (mm=0xffff8881015a3680) at kernel/fork.c:732
    #8  mm_init (mm=mm@entry=0xffff8881015a3680, user_ns=<optimized out>, p=<optimized out>) at kernel/fork.c:1151
    #9  0xffffffff8117964b in dup_mm (oldmm=0xffff8881015a2b40, tsk=<optimized out>) at kernel/fork.c:1529
    #10 0xffffffff8117aa4b in copy_mm (tsk=0xffff888101679980, clone_flags=18874368) at kernel/fork.c:1581
    #11 copy_process (pid=pid@entry=0x0 <fixed_percpu_data>, trace=trace@entry=0, node=node@entry=-1,
        args=args@entry=0xffffc900001a7e90) at kernel/fork.c:2259
    #12 0xffffffff8117c4d1 in kernel_clone (args=args@entry=0xffffc900001a7e90) at kernel/fork.c:2679
    #13 0xffffffff8117cbe6 in __do_sys_clone (clone_flags=<optimized out>, newsp=<optimized out>,
        parent_tidptr=<optimized out>, child_tidptr=<optimized out>, tls=<optimized out>) at kernel/fork.c:2820
    #14 0xffffffff8117d005 in __se_sys_clone (tls=<optimized out>, child_tidptr=<optimized out>,
        parent_tidptr=<optimized out>, newsp=<optimized out>, clone_flags=<optimized out>) at kernel/fork.c:2804
    #15 __x64_sys_clone (regs=<optimized out>) at kernel/fork.c:2804
    #16 0xffffffff81c69c89 in do_syscall_x64 (nr=<optimized out>, regs=0xffffc900001a7f58) at arch/x86/entry/common.c:50
    #17 do_syscall_64 (regs=0xffffc900001a7f58, nr=<optimized out>) at arch/x86/entry/common.c:80
    #18 0xffffffff81e0009b in entry_SYSCALL_64 () at arch/x86/entry/entry_64.S:120

    ```
    This is the 'heart' of the zoned buddy allocator.

### Page Frame Reclaiming

    ```c
    Breakpoint 1, __alloc_pages_direct_compact (gfp_mask=gfp_mask@entry=1387594, order=order@entry=0,
        alloc_flags=alloc_flags@entry=2112, ac=ac@entry=0xffffc90000157bc8, prio=prio@entry=COMPACT_PRIO_SYNC_LIGHT,
        compact_result=compact_result@entry=0xffffc90000157bc4) at mm/page_alloc.c:4488
    4488    {
    (gdb) bt
    #0  __alloc_pages_direct_compact (gfp_mask=gfp_mask@entry=1387594, order=order@entry=0,
        alloc_flags=alloc_flags@entry=2112, ac=ac@entry=0xffffc90000157bc8, prio=prio@entry=COMPACT_PRIO_SYNC_LIGHT,
        compact_result=compact_result@entry=0xffffc90000157bc4) at mm/page_alloc.c:4488
    #1  0xffffffff813b064d in __alloc_pages_slowpath (ac=0xffffc90000157bc8, order=0, gfp_mask=<optimized out>)
        at mm/page_alloc.c:5193
    #2  __alloc_pages (gfp=<optimized out>, gfp@entry=1387722, order=order@entry=0, preferred_nid=preferred_nid@entry=0,
        nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5572
    #3  0xffffffff813b2497 in __folio_alloc (gfp=gfp@entry=1125578, order=order@entry=0,
        preferred_nid=preferred_nid@entry=0, nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5591
    #4  0xffffffff81333a86 in __folio_alloc_node (order=0, nid=0, gfp=1125578) at ./include/linux/gfp.h:246
    #5  folio_alloc (order=0, gfp=1125578) at ./include/linux/gfp.h:275
    #6  filemap_alloc_folio (order=0, gfp=1125578) at ./include/linux/pagemap.h:474
    #7  page_cache_ra_unbounded (ractl=0xffffc90000157d48, nr_to_read=32, lookahead_size=8) at mm/readahead.c:248
    #8  0xffffffff81333c30 in do_page_cache_ra (ractl=ractl@entry=0xffffc90000157d48, nr_to_read=<optimized out>,
        lookahead_size=<optimized out>) at mm/readahead.c:300
    #9  0xffffffff81334660 in page_cache_ra_order (ractl=ractl@entry=0xffffc90000157d48, ra=<optimized out>,
        new_order=new_order@entry=0) at mm/readahead.c:560
    #10 0xffffffff813250fb in do_sync_mmap_readahead (vmf=0xffffc90000157df0) at mm/filemap.c:3044
    #11 filemap_fault (vmf=0xffffc90000157df0) at mm/filemap.c:3136
    #12 0xffffffff81374627 in __do_fault (vmf=vmf@entry=0xffffc90000157df0) at mm/memory.c:4212
    #13 0xffffffff8137afc5 in do_read_fault (vmf=0xffffc90000157df0) at mm/memory.c:4563
    #14 do_fault (vmf=0xffffc90000157df0) at mm/memory.c:4692
    #15 handle_pte_fault (vmf=0xffffc90000157df0) at mm/memory.c:4964
    #16 __handle_mm_fault (vma=vma@entry=0xffff888000a58220, address=address@entry=94460052262960, flags=flags@entry=852)
        at mm/memory.c:5106
    #17 0xffffffff8137c11a in handle_mm_fault (vma=vma@entry=0xffff888000a58220, address=address@entry=94460052262960,
        flags=flags@entry=852, regs=regs@entry=0xffffc90000157f58) at mm/memory.c:5227
    #18 0xffffffff81c707ff in do_user_addr_fault (address=94460052262960, error_code=20, regs=0xffffc90000157f58)
        at arch/x86/mm/fault.c:1428
    #19 handle_page_fault (address=94460052262960, error_code=20, regs=0xffffc90000157f58) at arch/x86/mm/fault.c:1519
    #20 exc_page_fault (regs=0xffffc90000157f58, error_code=20) at arch/x86/mm/fault.c:1575
    #21 0xffffffff81e00b77 in asm_exc_page_fault () at ./arch/x86/include/asm/idtentry.h:570
    ```

* balance_pgdat

    ```c
    Breakpoint 1, balance_pgdat (pgdat=pgdat@entry=0xffffffff8278c380 <contig_page_data>, order=order@entry=0,
        highest_zoneidx=highest_zoneidx@entry=3) at mm/vmscan.c:7025
    7025            for (i = 0; i <= highest_zoneidx; i++) {
    (gdb) bt
    #0  balance_pgdat (pgdat=pgdat@entry=0xffffffff8278c380 <contig_page_data>, order=order@entry=0,
        highest_zoneidx=highest_zoneidx@entry=3) at mm/vmscan.c:7025
    #1  0xffffffff813441d9 in kswapd (p=p@entry=0xffffffff8278c380 <contig_page_data>) at mm/vmscan.c:7387
    #2  0xffffffff811b3857 in kthread (_create=<optimized out>) at kernel/kthread.c:376
    #3  0xffffffff81002292 in ret_from_fork () at arch/x86/entry/entry_64.S:306
    ```

### Memory Allocator

#### Slab

* ____cache_alloc

    ```c
    Breakpoint 1, cpu_cache_get (cachep=0xffff888003443400, cachep=0xffff888003443400) at mm/slab.c:395
    395             return this_cpu_ptr(cachep->cpu_cache);
    (gdb) bt
    #0  cpu_cache_get (cachep=0xffff888003443400, cachep=0xffff888003443400) at mm/slab.c:395
    #1  ____cache_alloc (flags=<optimized out>, cachep=0xffff888003443400) at mm/slab.c:3009
    #2  __do_cache_alloc (nodeid=-1, flags=<optimized out>, cachep=0xffff888003443400) at mm/slab.c:3226
    #3  slab_alloc_node (caller=<optimized out>, orig_size=<optimized out>, nodeid=-1, flags=<optimized out>,
        lru=0x0 <fixed_percpu_data>, cachep=0xffff888003443400) at mm/slab.c:3250
    #4  slab_alloc (caller=<optimized out>, orig_size=<optimized out>, flags=3264, lru=0x0 <fixed_percpu_data>,
        cachep=0xffff888003443400) at mm/slab.c:3265
    #5  __kmem_cache_alloc_lru (flags=3264, lru=0x0 <fixed_percpu_data>, cachep=0xffff888003443400) at mm/slab.c:3442
    #6  kmem_cache_alloc (cachep=0xffff888003443400, flags=flags@entry=3264) at mm/slab.c:3461
    ```

#### Slub

* ____slab_alloc

    ```c
    Breakpoint 2, ___slab_alloc (s=s@entry=0xffff888003443900, gfpflags=gfpflags@entry=3264, node=node@entry=-1,
        addr=addr@entry=18446744071582628515, c=c@entry=0xffff888003a2d9c0, orig_size=orig_size@entry=64) at mm/slub.c:323
    323             raw_cpu_inc(s->cpu_slab->stat[si]);
    (gdb) bt
    #0  ___slab_alloc (s=s@entry=0xffff888003443900, gfpflags=gfpflags@entry=3264, node=node@entry=-1,
        addr=addr@entry=18446744071582628515, c=c@entry=0xffff888003a2d9c0, orig_size=orig_size@entry=64) at mm/slub.c:323
    #1  0xffffffff813cd78b in __slab_alloc (s=s@entry=0xffff888003443900, gfpflags=gfpflags@entry=3264,
        node=node@entry=-1, addr=addr@entry=18446744071582628515, orig_size=orig_size@entry=64, c=<optimized out>)
        at mm/slub.c:3279
    #2  0xffffffff813ce2f3 in slab_alloc_node (orig_size=64, addr=18446744071582628515, node=-1, gfpflags=3264,
        lru=0x0 <fixed_percpu_data>, s=0xffff888003443900) at mm/slub.c:3364
    #3  slab_alloc (orig_size=64, addr=18446744071582628515, gfpflags=3264, lru=0x0 <fixed_percpu_data>,
        s=0xffff888003443900) at mm/slub.c:3406
    #4  __kmem_cache_alloc_lru (gfpflags=gfpflags@entry=3264, lru=0x0 <fixed_percpu_data>, s=0xffff888003443900)
        at mm/slub.c:3413
    #5  kmem_cache_alloc (s=0xffff888003443900, gfpflags=gfpflags@entry=3264) at mm/slub.c:3422
    #6  0xffffffff8139baa3 in anon_vma_chain_alloc (gfp=3264) at mm/rmap.c:141
    #7  __anon_vma_prepare (vma=vma@entry=0xffff888000a1cb28) at mm/rmap.c:195
    #8  0xffffffff8137bf76 in anon_vma_prepare (vma=0xffff888000a1cb28) at ./include/linux/rmap.h:159
    #9  anon_vma_prepare (vma=0xffff888000a1cb28) at ./include/linux/rmap.h:154
    #10 do_anonymous_page (vmf=0xffffc900001cfbd0) at mm/memory.c:4121
    #11 handle_pte_fault (vmf=0xffffc900001cfbd0) at mm/memory.c:4962
    #12 __handle_mm_fault (vma=vma@entry=0xffff888000a1cb28, address=address@entry=140737488351216, flags=flags@entry=129)
        at mm/memory.c:5106
    #13 0xffffffff8137c1a8 in handle_mm_fault (vma=vma@entry=0xffff888000a1cb28, address=address@entry=140737488351216,
    ```