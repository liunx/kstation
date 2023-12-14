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

### MemBlock

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

* memblock_dump_all

    ```c
    Breakpoint 1, memblock_dump_all () at mm/memblock.c:1917
    1917            pr_info("MEMBLOCK configuration:\n");
    (gdb) bt
    #0  memblock_dump_all () at mm/memblock.c:1917
    #1  0xffffffff82e39639 in e820__memblock_setup () at arch/x86/kernel/e820.c:1349
    #2  0xffffffff82e364f8 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:1133
    #3  0xffffffff82e2c1b7 in start_kernel () at init/main.c:959
    #4  0xffffffff82e2b4a1 in x86_64_start_reservations (
        real_mode_data=real_mode_data@entry=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>) at arch/x86/kernel/head64.c:556
    #5  0xffffffff82e2b56c in x86_64_start_kernel (
        real_mode_data=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>)
        at arch/x86/kernel/head64.c:537
    #6  0xffffffff81000145 in secondary_startup_64 () at arch/x86/kernel/head_64.S:358
    ```

* memblock debug

    boot with command with "memblock=debug"

* BIOS and memblock output

```c
...
BIOS-provided physical RAM map:
BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
BIOS-e820: [mem 0x0000000000100000-0x0000000003fdcfff] usable
BIOS-e820: [mem 0x0000000003fdd000-0x0000000003ffffff] reserved
BIOS-e820: [mem 0x00000000feffc000-0x00000000feffffff] reserved
BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
...
MEMBLOCK configuration:
 memory size = 0x0000000003f7bc00 reserved size = 0x000000000227a000
 memory.cnt  = 0x2
 memory[0x0]    [0x0000000000001000-0x000000000009efff], 0x000000000009e000 bytes flags: 0x0
 memory[0x1]    [0x0000000000100000-0x0000000003fdcfff], 0x0000000003edd000 bytes flags: 0x0
 reserved.cnt  = 0x3
 reserved[0x0]  [0x0000000000000000-0x000000000000ffff], 0x0000000000010000 bytes flags: 0x0
 reserved[0x1]  [0x000000000009f000-0x00000000000fffff], 0x0000000000061000 bytes flags: 0x0
 reserved[0x2]  [0x0000000001000000-0x0000000003208fff], 0x0000000002209000 bytes flags: 0x0
...
```

### Memory Model

* sparse_init

    ```c
    Breakpoint 1, memblocks_present () at mm/sparse.c:271
    271             for_each_mem_pfn_range(i, MAX_NUMNODES, &start, &end, &nid)
    (gdb) bt
    #0  memblocks_present () at mm/sparse.c:271
    #1  sparse_init () at mm/sparse.c:564
    #2  0xffffffff82e4e836 in paging_init () at arch/x86/mm/init_64.c:816
    #3  0xffffffff82e36592 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:1253
    #4  0xffffffff82e2c1b7 in start_kernel () at init/main.c:959
    #5  0xffffffff82e2b4a1 in x86_64_start_reservations (
        real_mode_data=real_mode_data@entry=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>) at arch/x86/kernel/head64.c:556
    #6  0xffffffff82e2b56c in x86_64_start_kernel (
        real_mode_data=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>)
        at arch/x86/kernel/head64.c:537
    #7  0xffffffff81000145 in secondary_startup_64 () at arch/x86/kernel/head_64.S:358
    ```

### NUMA Node

* numa_register_memblks

    ```c
    Breakpoint 1, numa_register_memblks (mi=0xffffffff82f020c0 <numa_meminfo>) at arch/x86/mm/numa.c:552
    552             node_possible_map = numa_nodes_parsed;
    (gdb) bt
    #0  numa_register_memblks (mi=0xffffffff82f020c0 <numa_meminfo>) at arch/x86/mm/numa.c:552
    #1  numa_init (init_func=<optimized out>) at arch/x86/mm/numa.c:679
    #2  0xffffffff82e6b887 in x86_numa_init () at arch/x86/mm/numa.c:729
    #3  0xffffffff82e6b98e in initmem_init () at arch/x86/mm/numa_64.c:12
    #4  0xffffffff82e51572 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:1236
    #5  0xffffffff82e471b7 in start_kernel () at init/main.c:959
    #6  0xffffffff82e464a1 in x86_64_start_reservations (
        real_mode_data=real_mode_data@entry=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>) at arch/x86/kernel/head64.c:556
    #7  0xffffffff82e4656c in x86_64_start_kernel (
        real_mode_data=0x13b00 <exception_stacks+31488> <error: Cannot access memory at address 0x13b00>)
        at arch/x86/kernel/head64.c:537
    #8  0xffffffff81000145 in secondary_startup_64 () at arch/x86/kernel/head_64.S:358
    ```

* alloc_node_data

    ```c
    Breakpoint 1, alloc_node_data (nid=0) at arch/x86/mm/numa.c:216
    216             printk(KERN_INFO "NODE_DATA(%d) allocated [mem %#010Lx-%#010Lx]\n", nid,
    (gdb) bt
    #0  alloc_node_data (nid=0) at arch/x86/mm/numa.c:216
    #1  numa_register_memblks (mi=0xffffffff82f020c0 <numa_meminfo>) at arch/x86/mm/numa.c:611
    #2  numa_init (init_func=<optimized out>) at arch/x86/mm/numa.c:679
    #3  0xffffffff82e6b887 in x86_numa_init () at arch/x86/mm/numa.c:729
    #4  0xffffffff82e6b98e in initmem_init () at arch/x86/mm/numa_64.c:12
    #5  0xffffffff82e51572 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:1236
    #6  0xffffffff82e471b7 in start_kernel () at init/main.c:959
    ```

* numa_cleanup_meminfo

    ```c
    Breakpoint 1, numa_cleanup_meminfo (mi=mi@entry=0xffffffff82f020c0 <numa_meminfo>) at arch/x86/mm/numa.c:314
    314                             printk(KERN_INFO "NUMA: Node %d [mem %#010Lx-%#010Lx] + [mem %#010Lx-%#010Lx] -> [mem %#010Lx-%#010Lx]\n",
    (gdb) bt
    #0  numa_cleanup_meminfo (mi=mi@entry=0xffffffff82f020c0 <numa_meminfo>) at arch/x86/mm/numa.c:314
    #1  0xffffffff82e6b2ad in numa_init (init_func=0xffffffff82e6c0b4 <x86_acpi_numa_init>) at arch/x86/mm/numa.c:673
    #2  0xffffffff82e6b887 in x86_numa_init () at arch/x86/mm/numa.c:729
    #3  0xffffffff82e6b98e in initmem_init () at arch/x86/mm/numa_64.c:12
    #4  0xffffffff82e51572 in setup_arch (cmdline_p=cmdline_p@entry=0xffffffff82603ed8) at arch/x86/kernel/setup.c:1236
    #5  0xffffffff82e471b7 in start_kernel () at init/main.c:959
    ```

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

* compaction_suitable (called from kcompactd)

    ```c
    Breakpoint 1, compaction_suitable (zone=0xffff888003fd9000, order=-1, alloc_flags=<optimized out>,
        highest_zoneidx=<optimized out>) at mm/compaction.c:2244
    2244            if (ret == COMPACT_CONTINUE && (order > PAGE_ALLOC_COSTLY_ORDER)) {
    (gdb) bt
    #0  compaction_suitable (zone=0xffff888003fd9000, order=-1, alloc_flags=<optimized out>,
        highest_zoneidx=<optimized out>) at mm/compaction.c:2244
    #1  0xffffffff813734ac in compact_zone (cc=cc@entry=0xffffc900000cbdd0, capc=capc@entry=0x0 <fixed_percpu_data>)
        at mm/compaction.c:2312
    #2  0xffffffff81374de7 in proactive_compact_node (pgdat=pgdat@entry=0xffff888003fd9000) at mm/compaction.c:2666
    #3  0xffffffff81375477 in kcompactd (p=p@entry=0xffff888003fd9000) at mm/compaction.c:2976
    #4  0xffffffff811b7a37 in kthread (_create=<optimized out>) at kernel/kthread.c:376
    ```

* compaction_suitable (called from kswapd)

    ```c
    Breakpoint 1, compaction_suitable (zone=zone@entry=0xffff888003fd9000, order=1, alloc_flags=alloc_flags@entry=0,
        highest_zoneidx=<optimized out>) at mm/compaction.c:2244
    2244            if (ret == COMPACT_CONTINUE && (order > PAGE_ALLOC_COSTLY_ORDER)) {
    (gdb) bt
    #0  compaction_suitable (zone=zone@entry=0xffff888003fd9000, order=1, alloc_flags=alloc_flags@entry=0,
        highest_zoneidx=<optimized out>) at mm/compaction.c:2244
    #1  0xffffffff8134d79e in should_continue_reclaim (sc=0xffffc900000e3dc8, nr_reclaimed=<optimized out>,
        pgdat=0xffff888003fd9000) at mm/vmscan.c:6051
    #2  shrink_node (pgdat=pgdat@entry=0xffff888003fd9000, sc=sc@entry=0xffffc900000e3dc8) at mm/vmscan.c:6223
    #3  0xffffffff8134e2c6 in kswapd_shrink_node (sc=0xffffc900000e3dc8, pgdat=0xffff888003fd9000) at mm/vmscan.c:6937
    #4  balance_pgdat (pgdat=pgdat@entry=0xffff888003fd9000, order=order@entry=1, highest_zoneidx=highest_zoneidx@entry=3)
        at mm/vmscan.c:7127
    #5  0xffffffff8134e944 in kswapd (p=p@entry=0xffff888003fd9000) at mm/vmscan.c:7387
    #6  0xffffffff811b7a37 in kthread (_create=<optimized out>) at kernel/kthread.c:376
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

#### shrink_node

* kswapd (slow path)

    ```c
    Breakpoint 1, shrink_node (pgdat=pgdat@entry=0xffff888003fd9000, sc=sc@entry=0xffffc900000e3dc8) at mm/vmscan.c:6132
    6132    {
    (gdb) bt
    #0  shrink_node (pgdat=pgdat@entry=0xffff888003fd9000, sc=sc@entry=0xffffc900000e3dc8) at mm/vmscan.c:6132
    #1  0xffffffff8134e2c6 in kswapd_shrink_node (sc=0xffffc900000e3dc8, pgdat=0xffff888003fd9000) at mm/vmscan.c:6937
    #2  balance_pgdat (pgdat=pgdat@entry=0xffff888003fd9000, order=order@entry=3, highest_zoneidx=highest_zoneidx@entry=2)
        at mm/vmscan.c:7127
    #3  0xffffffff8134e944 in kswapd (p=p@entry=0xffff888003fd9000) at mm/vmscan.c:7387
    #4  0xffffffff811b7a37 in kthread (_create=<optimized out>) at kernel/kthread.c:376
    #5  0xffffffff81002292 in ret_from_fork () at arch/x86/entry/entry_64.S:306
    ```

* alloc_pages (__alloc_pages_slowpath branch)

    ```c
    Breakpoint 1, shrink_node (pgdat=pgdat@entry=0xffff888003fd9000, sc=sc@entry=0xffffc900001bfc28) at mm/vmscan.c:6132
    6132    {
    (gdb) bt
    #0  shrink_node (pgdat=pgdat@entry=0xffff888003fd9000, sc=sc@entry=0xffffc900001bfc28) at mm/vmscan.c:6132
    #1  0xffffffff8134f929 in shrink_zones (sc=0xffffc900001bfc28, zonelist=0xffff888003fda900) at mm/vmscan.c:6386
    #2  do_try_to_free_pages (sc=0xffffc900001bfc28, zonelist=0xffff888003fda900) at mm/vmscan.c:6448
    #3  try_to_free_pages (zonelist=0xffff888003fda900, order=order@entry=1, gfp_mask=gfp_mask@entry=4197824,
        nodemask=<optimized out>) at mm/vmscan.c:6683
    #4  0xffffffff813cc433 in __perform_reclaim (ac=0xffffc900001bfd30, order=1, gfp_mask=4197824) at mm/page_alloc.c:4759
    #5  __alloc_pages_direct_reclaim (did_some_progress=<synthetic pointer>, ac=0xffffc900001bfd30, alloc_flags=2112,
        order=1, gfp_mask=4197824) at mm/page_alloc.c:4781
    #6  __alloc_pages_slowpath (ac=0xffffc900001bfd30, order=1, gfp_mask=<optimized out>) at mm/page_alloc.c:5187
    #7  __alloc_pages (gfp=<optimized out>, gfp@entry=4197824, order=order@entry=1, preferred_nid=<optimized out>,
        nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5572
    #8  0xffffffff813e8243 in alloc_pages (gfp=gfp@entry=4197824, order=order@entry=1) at mm/mempolicy.c:2287
    #9  0xffffffff813c1261 in __get_free_pages (gfp_mask=gfp_mask@entry=4197824, order=order@entry=1)
        at mm/page_alloc.c:5609
    #10 0xffffffff81169993 in _pgd_alloc () at arch/x86/mm/pgtable.c:414
    ```

* get_page_from_freelist (fast path)


### Memory Allocator

* start_kernel
  * mm_init
    * kmem_cache_init

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

* ____slab_alloc (init kmem_cache_cpu.slab when required)

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

* init_kmem_cache_cpus (init kmem_cache_cpu.tid)

    ```c
    Breakpoint 2, init_kmem_cache_cpus (s=<optimized out>) at mm/slub.c:2401
    2401                    c->tid = init_tid(cpu);
    (gdb) bt
    #0  init_kmem_cache_cpus (s=<optimized out>) at mm/slub.c:2401
    #1  alloc_kmem_cache_cpus (s=0xffffffff82ee1c40 <boot_kmem_cache_node>) at mm/slub.c:4032
    #2  kmem_cache_open (flags=flags@entry=54788096, s=0xffffffff82ee1c40 <boot_kmem_cache_node>,
        s@entry=0xffff888003440000) at mm/slub.c:4351
    #3  __kmem_cache_create (s=s@entry=0xffffffff82ee1c40 <boot_kmem_cache_node>, flags=flags@entry=8192)
        at mm/slub.c:4907
    #4  0xffffffff82e5e43a in create_boot_cache (s=0xffffffff82ee1c40 <boot_kmem_cache_node>,
        name=name@entry=0xffffffff824ce259 "kmem_cache_node", size=size@entry=64, flags=flags@entry=8192,
        useroffset=useroffset@entry=0, usersize=usersize@entry=0) at mm/slab_common.c:646
    #5  0xffffffff82e62cd3 in kmem_cache_init () at mm/slub.c:4841
    #6  0xffffffff82e2d554 in mm_init () at init/main.c:845
    #7  start_kernel () at init/main.c:997
    ```

* __alloc_percpu (init kmem_cache.cpu_slab)

    ```c
    Breakpoint 4, alloc_kmem_cache_cpus (s=0xffffffff82ee1c40 <boot_kmem_cache_node>) at mm/slub.c:4026
    4026            s->cpu_slab = __alloc_percpu(sizeof(struct kmem_cache_cpu),
    (gdb) bt
    #0  alloc_kmem_cache_cpus (s=0xffffffff82ee1c40 <boot_kmem_cache_node>) at mm/slub.c:4026
    #1  kmem_cache_open (flags=flags@entry=54788096, s=0xffffffff82ee1c40 <boot_kmem_cache_node>,
        s@entry=0xffff888003440000) at mm/slub.c:4351
    #2  __kmem_cache_create (s=s@entry=0xffffffff82ee1c40 <boot_kmem_cache_node>, flags=flags@entry=8192)
        at mm/slub.c:4907
    #3  0xffffffff82e5e43a in create_boot_cache (s=0xffffffff82ee1c40 <boot_kmem_cache_node>,
        name=name@entry=0xffffffff824ce259 "kmem_cache_node", size=size@entry=64, flags=flags@entry=8192,
        useroffset=useroffset@entry=0, usersize=usersize@entry=0) at mm/slab_common.c:646
    #4  0xffffffff82e62cd3 in kmem_cache_init () at mm/slub.c:4841
    #5  0xffffffff82e2d554 in mm_init () at init/main.c:845
    #6  start_kernel () at init/main.c:997
    ```

* kmem_cache_open --> init_kmem_cache_nodes (init kmem_cache.node)

* slab_state = FULL

    ```c
    Breakpoint 1, slab_sysfs_init () at mm/slub.c:6034
    6034            slab_state = FULL;
    (gdb) bt
    #0  slab_sysfs_init () at mm/slub.c:6034
    #1  0xffffffff810011fc in do_one_initcall (fn=0xffffffff82e62614 <slab_sysfs_init>) at init/main.c:1303
    #2  0xffffffff82e2db49 in do_initcall_level (command_line=0xffff888003474780 "rootwait", level=6) at init/main.c:1376
    #3  do_initcalls () at init/main.c:1392
    #4  do_basic_setup () at init/main.c:1411
    #5  kernel_init_freeable () at init/main.c:1631
    #6  0xffffffff81c9495a in kernel_init (unused=<optimized out>) at init/main.c:1519
    #7  0xffffffff81002292 in ret_from_fork () at arch/x86/entry/entry_64.S:306
    ```

* do_slab_free

    ```c
    Breakpoint 1, do_slab_free (addr=18446744071580593291, cnt=1, tail=0x0 <fixed_percpu_data>, head=0xffff888003448160,
        slab=0xffffea00000d1200, s=0xffff888003441400) at mm/slub.c:3596
    3596            void *tail_obj = tail ? : head;
    (gdb) bt
    #0  do_slab_free (addr=18446744071580593291, cnt=1, tail=0x0 <fixed_percpu_data>, head=0xffff888003448160,
        slab=0xffffea00000d1200, s=0xffff888003441400) at mm/slub.c:3596
    #1  slab_free (addr=18446744071580593291, cnt=1, p=<synthetic pointer>, tail=<optimized out>, head=<optimized out>,
        slab=0xffffea00000d1200, s=0xffff888003441400) at mm/slub.c:3662
    #2  __kmem_cache_free (s=0xffff888003441400, x=x@entry=0xffff888003448160, caller=18446744071580593291)
        at mm/slub.c:3674
    #3  0xffffffff8135f9ac in kfree (object=object@entry=0xffff888003448160) at mm/slab_common.c:1007
    ```


### Initialization of Memory Management

    * build_zonelists

    ```c
    Breakpoint 1, build_zonelists (pgdat=0xffff8881bfff9000) at mm/page_alloc.c:6480
    6480    {
    (gdb) bt
    #0  build_zonelists (pgdat=0xffff8881bfff9000) at mm/page_alloc.c:6480
    #1  0xffffffff813c0a7b in __build_all_zonelists (data=data@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:6637
    #2  0xffffffff82e7c3dc in build_all_zonelists_init () at mm/page_alloc.c:6664
    #3  0xffffffff81ca8840 in build_all_zonelists (pgdat=pgdat@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:6697
    #4  0xffffffff82e47295 in start_kernel () at init/main.c:967
    ```

    ```c
    Breakpoint 1, build_all_zonelists (pgdat=pgdat@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:6721
    6721            pr_info("Policy zone: %s\n", zone_names[policy_zone]);
    (gdb) bt
    #0  build_all_zonelists (pgdat=pgdat@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:6721
    #1  0xffffffff82e49295 in start_kernel () at init/main.c:967
    ```

### Page Reclaim

* try_to_free_pages

```c
Breakpoint 1, try_to_free_pages (zonelist=0xffff888003fda900, order=order@entry=0, gfp_mask=gfp_mask@entry=1387594,
    nodemask=0x0 <fixed_percpu_data>) at mm/vmscan.c:6650
6650    {
(gdb) bt
#0  try_to_free_pages (zonelist=0xffff888003fda900, order=order@entry=0, gfp_mask=gfp_mask@entry=1387594,
    nodemask=0x0 <fixed_percpu_data>) at mm/vmscan.c:6650
#1  0xffffffff813cc433 in __perform_reclaim (ac=0xffffc90000123af0, order=0, gfp_mask=1387594) at mm/page_alloc.c:4759
#2  __alloc_pages_direct_reclaim (did_some_progress=<synthetic pointer>, ac=0xffffc90000123af0, alloc_flags=2240,
    order=0, gfp_mask=1387594) at mm/page_alloc.c:4781
#3  __alloc_pages_slowpath (ac=0xffffc90000123af0, order=0, gfp_mask=<optimized out>) at mm/page_alloc.c:5187
#4  __alloc_pages (gfp=<optimized out>, gfp@entry=1387722, order=order@entry=0, preferred_nid=<optimized out>,
    nodemask=nodemask@entry=0x0 <fixed_percpu_data>) at mm/page_alloc.c:5572
#5  0xffffffff813e8243 in alloc_pages (gfp=gfp@entry=1387722, order=order@entry=0) at mm/mempolicy.c:2287
#6  0xffffffff813e82fb in folio_alloc (gfp=gfp@entry=1125578, order=order@entry=0) at mm/mempolicy.c:2297
#7  0xffffffff81324866 in filemap_alloc_folio (gfp=gfp@entry=1125578, order=order@entry=0) at mm/filemap.c:971
#8  0xffffffff8133c05b in page_cache_ra_unbounded (ractl=0xffffc90000123d20, nr_to_read=32,
    lookahead_size=<optimized out>) at mm/readahead.c:248
#9  0xffffffff8133c210 in do_page_cache_ra (ractl=ractl@entry=0xffffc90000123d20, nr_to_read=<optimized out>,
    lookahead_size=<optimized out>) at mm/readahead.c:300
#10 0xffffffff8133c7c2 in page_cache_ra_order (ractl=ractl@entry=0xffffc90000123d20, ra=0xffff888000a0dc98,
    new_order=new_order@entry=0) at mm/readahead.c:560
#11 0xffffffff8132c9c9 in do_sync_mmap_readahead (vmf=0xffffc90000123df0) at mm/filemap.c:3044
#12 filemap_fault (vmf=0xffffc90000123df0) at mm/filemap.c:3136
#13 0xffffffff813850f9 in __do_fault (vmf=vmf@entry=0xffffc90000123df0) at mm/memory.c:4212
#14 0xffffffff81390804 in do_read_fault (vmf=0xffffc90000123df0) at mm/memory.c:4563
#15 do_fault (vmf=0xffffc90000123df0) at mm/memory.c:4692
#16 handle_pte_fault (vmf=0xffffc90000123df0) at mm/memory.c:4964
#17 __handle_mm_fault (vma=vma@entry=0xffff888000a25000, address=address@entry=94422527533530, flags=flags@entry=852)
    at mm/memory.c:5106
#18 0xffffffff8139212a in handle_mm_fault (vma=vma@entry=0xffff888000a25000, address=address@entry=94422527533530,
    flags=flags@entry=852, regs=regs@entry=0xffffc90000123f58) at mm/memory.c:5227
#19 0xffffffff81cc367f in do_user_addr_fault (address=94422527533530, error_code=20, regs=0xffffc90000123f58)
    at arch/x86/mm/fault.c:1428
#20 handle_page_fault (address=94422527533530, error_code=20, regs=0xffffc90000123f58) at arch/x86/mm/fault.c:1519
#21 exc_page_fault (regs=0xffffc90000123f58, error_code=20) at arch/x86/mm/fault.c:1575
#22 0xffffffff81e00b77 in asm_exc_page_fault () at ./arch/x86/include/asm/idtentry.h:570
```

### Virtual Process Memory
