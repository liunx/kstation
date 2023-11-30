### rdmsrl_safe(MSR_IA32_CR_PAT, &host_pat)

* 在当前的处理器中，memory type是根据PAT和MTTR两者来选择的, 具体的映射关系见IA32手册第三卷的10.5.2.2 Selecting Memory Types for Pentium III and More Recent Processor Families 对于memory type的描述，请参考IA32中的5种caching type(也叫memory type)

* 对于MTRRs和PAT
    * MTRRs: The memory type range registers (MTRRs) provide a mechanism for associating the memory types with physical-address ranges in system memory.
    * PAT: The Page Attribute Table (PAT) extends the IA-32 architecture’s page-table format to allow memory types to be assigned to regions of physical memory based on linear address mappings.     

    简单来说PAT是作用于页表上的，基于虚拟地址的。而MTRRs是作用于物理地址上的.

### boot_cpu_has(X86_FEATURE_XSAVE)

* Performs a full or partial save of processor state components to the XSAVE area located at the memory address specified by the destination operand. The implicit EDX:EAX register pair specifies a 64-bit instruction mask. The specific state components saved correspond to the bits set in the requested-feature bitmap (RFBM), which is the logical-AND of EDX:EAX and XCR0.

* The format of the XSAVE area is detailed in Section 13.4, “XSAVE Area,” of Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1. Like FXRSTOR and FXSAVE, the memory format used for x87 state depends on a REX.W prefix; see Section 13.5.1, “x87 State” of Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1.

### vmx_setup_l1d_flush(vmentry_l1d_flush_param)

L1 Terminal Fault is a hardware vulnerability which allows unprivileged speculative access to data which is available in the Level 1 Data Cache when the page table entry controlling the virtual address, which is used for the access, has the Present bit cleared or other reserved bits set.

[L1TF - L1 Terminal Fault](https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/l1tf.html)

### IA32_EFER
Extended Feature Enable Register (EFER) is a model-specific register added in the AMD K6 processor, to allow enabling the SYSCALL/SYSRET instruction, and later for entering and exiting long mode. This register becomes architectural in AMD64 and has been adopted by Intel. Its MSR number is 0xC0000080.

see [CPU Registers x86-64](https://wiki.osdev.org/CPU_Registers_x86-64#IA32_EFER) for detail.

### TDP (Two Dimensional Paging) MMU

[Introduce the TDP MMU](https://lwn.net/Articles/832835/)

### Create VM

* kvm_create_vm

    ```c
    Breakpoint 4, kvm_create_vm (fdname=0xffffc90000187e63 "10", type=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1140
    1140            __module_get(kvm_chardev_ops.owner);
    (gdb) bt
    #0  kvm_create_vm (fdname=0xffffc90000187e63 "10", type=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1140
    #1  kvm_dev_ioctl_create_vm (type=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4963
    #2  kvm_dev_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:5005
    #3  0xffffffff811fbde7 in vfs_ioctl (arg=0, cmd=<optimized out>, filp=0xffff888100dd4100) at fs/ioctl.c:51
    #4  __do_sys_ioctl (arg=0, cmd=<optimized out>, fd=<optimized out>) at fs/ioctl.c:870
    #5  __se_sys_ioctl (arg=0, cmd=<optimized out>, fd=<optimized out>) at fs/ioctl.c:856
    #6  __x64_sys_ioctl (regs=<optimized out>) at fs/ioctl.c:856
    #7  0xffffffff8172f590 in do_syscall_x64 (nr=<optimized out>, regs=0xffffc90000187f58) at arch/x86/entry/common.c:50
    #8  do_syscall_64 (regs=0xffffc90000187f58, nr=<optimized out>) at arch/x86/entry/common.c:80
    #9  0xffffffff8180009b in entry_SYSCALL_64 () at arch/x86/entry/entry_64.S:120
    ```

* vmx_hardware_enable

    ```c
    Breakpoint 2, vmx_hardware_enable () at arch/x86/kvm/vmx/vmx.c:2485
    2485            int cpu = raw_smp_processor_id();
    (gdb) bt
    #0  vmx_hardware_enable () at arch/x86/kvm/vmx/vmx.c:2485
    #1  0xffffffff810417a4 in kvm_arch_hardware_enable () at arch/x86/kvm/x86.c:12204
    #2  0xffffffff81021853 in hardware_enable_nolock (junk=<optimized out>)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:5055
    #3  0xffffffff811549b4 in smp_call_function_many_cond (mask=mask@entry=0xffffffff81ee4ac0 <__cpu_online_mask>,
        func=func@entry=0xffffffff81021820 <hardware_enable_nolock>, info=info@entry=0x0 <fixed_percpu_data>,
        scf_flags=scf_flags@entry=3, cond_func=cond_func@entry=0x0 <fixed_percpu_data>) at kernel/smp.c:978
    #4  0xffffffff81154c4c in on_each_cpu_cond_mask (cond_func=cond_func@entry=0x0 <fixed_percpu_data>,
        func=func@entry=0xffffffff81021820 <hardware_enable_nolock>, info=info@entry=0x0 <fixed_percpu_data>,
        wait=wait@entry=true, mask=0xffffffff81ee4ac0 <__cpu_online_mask>) at kernel/smp.c:1155
    #5  0xffffffff81026d38 in on_each_cpu (wait=1, info=0x0 <fixed_percpu_data>,
        func=0xffffffff81021820 <hardware_enable_nolock>) at ./include/linux/smp.h:71
    #6  hardware_enable_all () at arch/x86/kvm/../../../virt/kvm/kvm_main.c:5117
    #7  kvm_create_vm (fdname=0xffffc9000017fe63 "10", type=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1205
    #8  kvm_dev_ioctl_create_vm (type=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4963
    #9  kvm_dev_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:5005
    ```
    ***NOTE:***

    1. KVM_X86_OP(hardware_enable) --> static_call(kvm_x86_hardware_enable)(...)
    2. intel PT (Processor Trace)

* kvm_cpu_vmxon(vmxarea)

    对于Intel x86处理器，在打开VMX（Virtual Machine Extension），即执行VMXON指令的时候需要提供一个4KB对齐的内存区间，称作VMXON region，该区域的物理地址作为VMXON指令的操作数。该内存区间用于支持逻辑CPU的VMX功能，该区域在VMXON和VMXOFF之间一直都会被VMX硬件所使用。

### Create VCPU

* vmx_vcpu_create

    ```c
    Breakpoint 3, vmx_vcpu_create (vcpu=0xffff888100eb8000) at arch/x86/kvm/vmx/vmx.c:7317
    7317            INIT_LIST_HEAD(&vmx->pi_wakeup_list);
    (gdb) bt
    #0  vmx_vcpu_create (vcpu=0xffff888100eb8000) at arch/x86/kvm/vmx/vmx.c:7317
    #1  0xffffffff81041436 in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/x86.c:11951
    #2  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc9000025d000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #3  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

* alloc_vmx_cpu

    ```c
    Breakpoint 1, alloc_vmcs_cpu (shadow=shadow@entry=false, cpu=0, flags=flags@entry=4197568)
        at arch/x86/kvm/vmx/vmx.c:2767
    2767            pages = __alloc_pages_node(node, flags, 0);
    (gdb) bt
    #0  alloc_vmcs_cpu (shadow=shadow@entry=false, cpu=0, flags=flags@entry=4197568) at arch/x86/kvm/vmx/vmx.c:2767
    #1  0xffffffff8107d0ff in alloc_vmcs (shadow=false) at arch/x86/kvm/vmx/vmx.h:702
    #2  alloc_loaded_vmcs (loaded_vmcs=loaded_vmcs@entry=0xffff888100ec1a70) at arch/x86/kvm/vmx/vmx.c:2806
    #3  0xffffffff8107f45c in vmx_vcpu_create (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:7348
    #4  0xffffffff81041436 in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11951
    #5  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc90000265000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #6  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

* vmx_vcpu_load_vmcs

    ```c
    Breakpoint 1, vmx_vcpu_load_vmcs (vcpu=vcpu@entry=0xffff888100ec0000, cpu=cpu@entry=0,
        buddy=buddy@entry=0x0 <fixed_percpu_data>) at arch/x86/kvm/vmx/vmx.c:1351
    1351            bool already_loaded = vmx->loaded_vmcs->cpu == cpu;
    (gdb) bt
    #0  vmx_vcpu_load_vmcs (vcpu=vcpu@entry=0xffff888100ec0000, cpu=cpu@entry=0,
        buddy=buddy@entry=0x0 <fixed_percpu_data>) at arch/x86/kvm/vmx/vmx.c:1351
    #1  0xffffffff8107cf84 in vmx_vcpu_load (vcpu=0xffff888100ec0000, cpu=0) at arch/x86/kvm/vmx/vmx.c:1422
    #2  0xffffffff8103a9ed in kvm_arch_vcpu_load (vcpu=vcpu@entry=0xffff888100ec0000, cpu=cpu@entry=0)
        at arch/x86/kvm/x86.c:4710
    #3  0xffffffff810213e2 in vcpu_load (vcpu=vcpu@entry=0xffff888100ec0000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:226
    #4  0xffffffff8104146b in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11959
    #5  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc90000459000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #6  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

### VCPU Run

* __vmx_vcpu_run

    ```c
    Breakpoint 3, __vmx_vcpu_run () at arch/x86/kvm/vmx/vmenter.S:47
    47              push %_ASM_BP
    (gdb) bt
    #0  __vmx_vcpu_run () at arch/x86/kvm/vmx/vmenter.S:47
    #1  0xffffffff8172f759 in vmx_vcpu_enter_exit (vcpu=vcpu@entry=0xffff888100ec0000, vmx=vmx@entry=0xffff888100ec0000,
        flags=1) at arch/x86/kvm/vmx/vmx.c:7121
    #2  0xffffffff8107bfb8 in vmx_vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:7222
    #3  0xffffffff8103f65e in vcpu_enter_guest (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10809
    #4  vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:11008
    #5  kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11229
    #6  0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
    ```

### KVM MMU

* __kvm_mmu_create

    ```c
    Breakpoint 1, __kvm_mmu_create (vcpu=vcpu@entry=0xffff888100eb8000, mmu=mmu@entry=0xffff888100eb8410)
        at arch/x86/kvm/mmu/mmu.c:5762
    5762            mmu->root.hpa = INVALID_PAGE;
    (gdb) bt
    #0  __kvm_mmu_create (vcpu=vcpu@entry=0xffff888100eb8000, mmu=mmu@entry=0xffff888100eb8410)
        at arch/x86/kvm/mmu/mmu.c:5762
    #1  0xffffffff8106e39f in kvm_mmu_create (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5825
    #2  0xffffffff81041273 in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/x86.c:11883
    #3  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc900001a9000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #4  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

* kvm_init_mmu

    ```c
    Breakpoint 2, init_kvm_tdp_mmu (cpu_role=..., vcpu=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5035
    5035            union kvm_mmu_page_role root_role = kvm_calc_tdp_mmu_root_page_role(vcpu, cpu_role);
    (gdb) bt
    #0  init_kvm_tdp_mmu (cpu_role=..., vcpu=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5035
    #1  kvm_init_mmu (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5248
    #2  0xffffffff8104148f in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/x86.c:11962
    #3  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc900001b1000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #4  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

* kvm_set_memory_region

    ```c
    Breakpoint 3, __kvm_set_memory_region (kvm=kvm@entry=0xffffc900003d9000, mem=mem@entry=0xffffc9000018fdd0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1535
    1535            if (mem->flags & ~valid_flags)
    (gdb) bt
    #0  __kvm_set_memory_region (kvm=kvm@entry=0xffffc900003d9000, mem=mem@entry=0xffffc9000018fdd0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1535
    #1  0xffffffff81028c75 in kvm_set_memory_region (mem=0xffffc9000018fdd0, kvm=0xffffc900003d9000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2030
    #2  kvm_vm_ioctl_set_memory_region (mem=0xffffc9000018fdd0, kvm=0xffffc900003d9000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2042
    #3  kvm_vm_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=140722315496952)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4695
    ```

    ```c
    Breakpoint 2, __kvm_set_memory_region (kvm=kvm@entry=0xffffc900003d9000, mem=mem@entry=0xffffc900003f7cd8)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1535
    1535            if (mem->flags & ~valid_flags)
    (gdb) bt
    #0  __kvm_set_memory_region (kvm=kvm@entry=0xffffc900003d9000, mem=mem@entry=0xffffc900003f7cd8)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:1535
    #1  0xffffffff81030f61 in __x86_set_memory_region (kvm=kvm@entry=0xffffc900003d9000, id=id@entry=32765,
        gpa=gpa@entry=4276092928, size=size@entry=4096) at arch/x86/kvm/x86.c:12563
    #2  0xffffffff8107f7be in alloc_apic_access_page (kvm=0xffffc900003d9000) at arch/x86/kvm/vmx/vmx.c:3815
    #3  vmx_vcpu_create (vcpu=0xffff888100eb8000) at arch/x86/kvm/vmx/vmx.c:7388
    #4  0xffffffff81041436 in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/x86.c:11951
    #5  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc900003d9000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #6  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

* Setup MMU (Set CR3)

    ```c
    Breakpoint 8, construct_eptp (root_level=4, root_hpa=4309368832, vcpu=0xffff888100eb8000)
        at arch/x86/kvm/vmx/vmx.c:3263
    3263            eptp |= (root_level == 5) ? VMX_EPTP_PWL_5 : VMX_EPTP_PWL_4;
    (gdb) bt
    #0  construct_eptp (root_level=4, root_hpa=4309368832, vcpu=0xffff888100eb8000) at arch/x86/kvm/vmx/vmx.c:3263
    #1  vmx_load_mmu_pgd (vcpu=0xffff888100eb8000, root_hpa=4309368832, root_level=4) at arch/x86/kvm/vmx/vmx.c:3282
    #2  0xffffffff8106db04 in kvm_mmu_load_pgd (vcpu=0xffff888100eb8000) at ./arch/x86/kvm/mmu.h:152
    #3  kvm_mmu_load (vcpu=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5309
    #4  kvm_mmu_load (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/mmu/mmu.c:5290
    #5  0xffffffff8103fb84 in kvm_mmu_reload (vcpu=0xffff888100eb8000) at arch/x86/kvm/mmu.h:128
    #6  vcpu_enter_guest (vcpu=0xffff888100eb8000) at arch/x86/kvm/x86.c:10720
    #7  vcpu_run (vcpu=0xffff888100eb8000) at arch/x86/kvm/x86.c:11008
    #8  kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100eb8000) at arch/x86/kvm/x86.c:11229
    #9  0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

* Handle a TDP Page Fault

    ```c
    Breakpoint 5, tdp_mmu_map_handle_target_level (iter=0xffffc9000081fab8, fault=0xffffc9000081fc20,
        vcpu=0xffff888100ec0000) at arch/x86/kvm/mmu/tdp_mmu.c:1066
    1066            struct kvm_mmu_page *sp = sptep_to_sp(rcu_dereference(iter->sptep));
    (gdb) bt
    #0  tdp_mmu_map_handle_target_level (iter=0xffffc9000081fab8, fault=0xffffc9000081fc20, vcpu=0xffff888100ec0000)
        at arch/x86/kvm/mmu/tdp_mmu.c:1066
    #1  kvm_tdp_mmu_map (vcpu=vcpu@entry=0xffff888100ec0000, fault=fault@entry=0xffffc9000081fc20)
        at arch/x86/kvm/mmu/tdp_mmu.c:1224
    #2  0xffffffff8106aa69 in direct_page_fault (vcpu=vcpu@entry=0xffff888100ec0000, fault=fault@entry=0xffffc9000081fc20)
        at arch/x86/kvm/mmu/mmu.c:4267
    #3  0xffffffff8106afa4 in kvm_tdp_page_fault (vcpu=vcpu@entry=0xffff888100ec0000,
        fault=fault@entry=0xffffc9000081fc20) at arch/x86/kvm/mmu/mmu.c:4351
    #4  0xffffffff8106b13d in kvm_mmu_do_page_fault (prefetch=false, err=4, cr2_or_gpa=1072188680,
        vcpu=0xffff888100ec0000) at arch/x86/kvm/mmu/mmu_internal.h:290
    #5  kvm_mmu_page_fault (vcpu=vcpu@entry=0xffff888100ec0000, cr2_or_gpa=1072188680, error_code=4294967300,
        insn=insn@entry=0x0 <fixed_percpu_data>, insn_len=insn_len@entry=0) at arch/x86/kvm/mmu/mmu.c:5550
    #6  0xffffffff8107960a in handle_ept_violation (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:5701
    #7  0xffffffff810845d4 in __vmx_handle_exit (exit_fastpath=EXIT_FASTPATH_NONE, vcpu=0xffff888100ec0000)
        at arch/x86/kvm/vmx/vmx.c:6480
    #8  vmx_handle_exit (vcpu=0xffff888100ec0000, exit_fastpath=EXIT_FASTPATH_NONE) at arch/x86/kvm/vmx/vmx.c:6497
    #9  0xffffffff8103f7a5 in vcpu_enter_guest (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10905
    #10 vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:11008
    #11 kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11229
    #12 0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

### Interrupt Virtualization

* KVM_CREATE_IRQCHIP

    ```c
    Breakpoint 1, kvm_arch_vm_ioctl (filp=<optimized out>, ioctl=ioctl@entry=44640, arg=arg@entry=0)
        at arch/x86/kvm/x86.c:6711
    6711                    if (kvm->created_vcpus)
    (gdb) bt
    #0  kvm_arch_vm_ioctl (filp=<optimized out>, ioctl=ioctl@entry=44640, arg=arg@entry=0) at arch/x86/kvm/x86.c:6711
    #1  0xffffffff8102934f in kvm_vm_ioctl (filp=<optimized out>, ioctl=44640, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4851
    #2  0xffffffff811fbde7 in vfs_ioctl (arg=0, cmd=<optimized out>, filp=0xffff888100d28800) at fs/ioctl.c:51
    #3  __do_sys_ioctl (arg=0, cmd=<optimized out>, fd=<optimized out>) at fs/ioctl.c:870
    #4  __se_sys_ioctl (arg=0, cmd=<optimized out>, fd=<optimized out>) at fs/ioctl.c:856
    #5  __x64_sys_ioctl (regs=<optimized out>) at fs/ioctl.c:856
    #6  0xffffffff8172f590 in do_syscall_x64 (nr=<optimized out>, regs=0xffffc9000017ff58) at arch/x86/entry/common.c:50
    #7  do_syscall_64 (regs=0xffffc9000017ff58, nr=<optimized out>) at arch/x86/entry/common.c:80
    #8  0xffffffff8180009b in entry_SYSCALL_64 () at arch/x86/entry/entry_64.S:120
    #9  0x0000000000000001 in fixed_percpu_data ()
    #10 0x0000000000000000 in ?? ()
    (gdb) n
    6714                    r = kvm_pic_init(kvm);
    (gdb) n
    6715                    if (r)
    (gdb)
    6718                    r = kvm_ioapic_init(kvm);
    (gdb)
    ```

* apic_timer_expired

    ```c
    Breakpoint 1, apic_timer_expired (apic=apic@entry=0xffff888100f5a200, from_timer_fn=from_timer_fn@entry=true)
        at arch/x86/kvm/lapic.c:1755
    1755            if (from_timer_fn)
    (gdb) bt
    #0  apic_timer_expired (apic=apic@entry=0xffff888100f5a200, from_timer_fn=from_timer_fn@entry=true)
        at arch/x86/kvm/lapic.c:1755
    #1  0xffffffff810544cb in apic_timer_fn (data=0xffff888100f5a210) at arch/x86/kvm/lapic.c:2567
    #2  0xffffffff8113fa97 in __run_hrtimer (now=<synthetic pointer>, flags=2, timer=0xffff888100f5a210,
        base=0xffff88813bc1ca00, cpu_base=0xffff88813bc1c9c0) at kernel/time/hrtimer.c:1685
    #3  __hrtimer_run_queues (cpu_base=cpu_base@entry=0xffff88813bc1c9c0, now=163156241389, flags=flags@entry=2,
        active_mask=active_mask@entry=15) at kernel/time/hrtimer.c:1749
    #4  0xffffffff8114058b in hrtimer_interrupt (dev=<optimized out>) at kernel/time/hrtimer.c:1811
    #5  0xffffffff810b8c93 in local_apic_timer_interrupt () at arch/x86/kernel/apic/apic.c:1096
    #6  __sysvec_apic_timer_interrupt (regs=<optimized out>) at arch/x86/kernel/apic/apic.c:1113
    #7  0xffffffff8174921b in sysvec_apic_timer_interrupt (regs=0xffffffff81e03d88) at arch/x86/kernel/apic/apic.c:1107
    #8  0xffffffff81800d4b in asm_sysvec_apic_timer_interrupt () at ./arch/x86/include/asm/idtentry.h:649
    ```

* kvm_cpu_has_pending_timer

    ```c
    Breakpoint 2, kvm_cpu_has_pending_timer (vcpu=vcpu@entry=0xffff888100ec8000) at arch/x86/kvm/irq.c:28
    28                      r = apic_has_pending_timer(vcpu);
    (gdb) bt
    #0  kvm_cpu_has_pending_timer (vcpu=vcpu@entry=0xffff888100ec8000) at arch/x86/kvm/irq.c:28
    #1  0xffffffff81022be2 in kvm_vcpu_check_block (vcpu=vcpu@entry=0xffff888100ec8000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3409
    #2  0xffffffff8102813b in kvm_vcpu_block (vcpu=vcpu@entry=0xffff888100ec8000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3442
    #3  0xffffffff81028209 in kvm_vcpu_halt (vcpu=0xffff888100ec8000) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3535
    #4  0xffffffff8103f566 in vcpu_block (vcpu=<optimized out>) at arch/x86/kvm/x86.c:10937
    #5  vcpu_run (vcpu=0xffff888100ec8000) at arch/x86/kvm/x86.c:11010
    #6  kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec8000) at arch/x86/kvm/x86.c:11229
    #7  0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

### KVM EPT Memory Virtualization

* arch/x86/kvm/mmu/mmu.c:kvm_mmu_vendor_module_init(...)

    ```c
    int kvm_mmu_vendor_module_init(void)
    {
        ...
        // a) build pte_list_desc structure
        pte_list_desc_cache = kmem_cache_create("pte_list_desc",
                            sizeof(struct pte_list_desc),
                            0, SLAB_ACCOUNT, NULL);
        if (!pte_list_desc_cache)
            goto out;

        // b) build kvm_mmu_page_header for kvm_mmu_page structure
        mmu_page_header_cache = kmem_cache_create("kvm_mmu_page_header",
                            sizeof(struct kvm_mmu_page),
                            0, SLAB_ACCOUNT, NULL);
        if (!mmu_page_header_cache)
            goto out;

        if (percpu_counter_init(&kvm_total_used_mmu_pages, 0, GFP_KERNEL))
            goto out;

        // c) register shrinker hook for memory reclaim
        ret = register_shrinker(&mmu_shrinker, "x86-mmu");
        ...
    }

    ```

* arch/x86/kvm/mmu/mmu.c:kvm_mmu_create(...)

    ```c
    int kvm_mmu_create(struct kvm_vcpu *vcpu)
    {
        int ret;

        vcpu->arch.mmu_pte_list_desc_cache.kmem_cache = pte_list_desc_cache;
        vcpu->arch.mmu_pte_list_desc_cache.gfp_zero = __GFP_ZERO;

        vcpu->arch.mmu_page_header_cache.kmem_cache = mmu_page_header_cache;
        vcpu->arch.mmu_page_header_cache.gfp_zero = __GFP_ZERO;

        vcpu->arch.mmu_shadow_page_cache.gfp_zero = __GFP_ZERO;

        vcpu->arch.mmu = &vcpu->arch.root_mmu;
        vcpu->arch.walk_mmu = &vcpu->arch.root_mmu;

        ret = __kvm_mmu_create(vcpu, &vcpu->arch.guest_mmu);
        if (ret)
            return ret;

        ret = __kvm_mmu_create(vcpu, &vcpu->arch.root_mmu);
        ...
    }
    ```

* tdp_mmu_alloc_sp

    ```c
    Breakpoint 3, tdp_mmu_alloc_sp (vcpu=0xffff888100eb0000) at arch/x86/kvm/mmu/tdp_mmu.c:278
    278             sp = kvm_mmu_memory_cache_alloc(&vcpu->arch.mmu_page_header_cache);
    (gdb) bt
    #0  tdp_mmu_alloc_sp (vcpu=0xffff888100eb0000) at arch/x86/kvm/mmu/tdp_mmu.c:278
    #1  kvm_tdp_mmu_map (vcpu=vcpu@entry=0xffff888100eb0000, fault=fault@entry=0xffffc900003cbc20)
        at arch/x86/kvm/mmu/tdp_mmu.c:1205
    #2  0xffffffff8106aa69 in direct_page_fault (vcpu=vcpu@entry=0xffff888100eb0000, fault=fault@entry=0xffffc900003cbc20)
        at arch/x86/kvm/mmu/mmu.c:4267
    #3  0xffffffff8106afa4 in kvm_tdp_page_fault (vcpu=vcpu@entry=0xffff888100eb0000,
        fault=fault@entry=0xffffc900003cbc20) at arch/x86/kvm/mmu/mmu.c:4351
    #4  0xffffffff8106b13d in kvm_mmu_do_page_fault (prefetch=false, err=16, cr2_or_gpa=4294967280,
        vcpu=0xffff888100eb0000) at arch/x86/kvm/mmu/mmu_internal.h:290
    #5  kvm_mmu_page_fault (vcpu=vcpu@entry=0xffff888100eb0000, cr2_or_gpa=4294967280, error_code=4294967312,
        insn=insn@entry=0x0 <fixed_percpu_data>, insn_len=insn_len@entry=0) at arch/x86/kvm/mmu/mmu.c:5550
    #6  0xffffffff8107960a in handle_ept_violation (vcpu=0xffff888100eb0000) at arch/x86/kvm/vmx/vmx.c:5701
    #7  0xffffffff810845d4 in __vmx_handle_exit (exit_fastpath=EXIT_FASTPATH_NONE, vcpu=0xffff888100eb0000)
        at arch/x86/kvm/vmx/vmx.c:6480
    #8  vmx_handle_exit (vcpu=0xffff888100eb0000, exit_fastpath=EXIT_FASTPATH_NONE) at arch/x86/kvm/vmx/vmx.c:6497
    #9  0xffffffff8103f7a5 in vcpu_enter_guest (vcpu=0xffff888100eb0000) at arch/x86/kvm/x86.c:10905
    #10 vcpu_run (vcpu=0xffff888100eb0000) at arch/x86/kvm/x86.c:11008
    #11 kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100eb0000) at arch/x86/kvm/x86.c:11229
    #12 0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

* __gfn_to_pfn_memslot

    ```c
    Breakpoint 5, __gfn_to_pfn_memslot (hva=0x0 <fixed_percpu_data>, writable=0x0 <fixed_percpu_data>, write_fault=true,
        async=0x0 <fixed_percpu_data>, atomic=false, gfn=1043968, slot=0xffff888100ddf800)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    2701            unsigned long addr = __gfn_to_hva_many(slot, gfn, NULL, write_fault);
    (gdb) bt
    #0  __gfn_to_pfn_memslot (hva=0x0 <fixed_percpu_data>, writable=0x0 <fixed_percpu_data>, write_fault=true,
        async=0x0 <fixed_percpu_data>, atomic=false, gfn=1043968, slot=0xffff888100ddf800)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    #1  gfn_to_pfn_memslot (gfn=1043968, slot=0xffff888100ddf800) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2739
    #2  gfn_to_pfn (gfn=gfn@entry=1043968, kvm=kvm@entry=0xffffc900001b1000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2757
    #3  gfn_to_page (kvm=kvm@entry=0xffffc900001b1000, gfn=gfn@entry=1043968)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2795
    #4  0xffffffff8107f7d7 in alloc_apic_access_page (kvm=0xffffc900001b1000) at arch/x86/kvm/vmx/vmx.c:3822
    #5  vmx_vcpu_create (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:7388
    #6  0xffffffff81041436 in kvm_arch_vcpu_create (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11951
    #7  0xffffffff81029168 in kvm_vm_ioctl_create_vcpu (id=<optimized out>, kvm=0xffffc900001b1000)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:3932
    #8  kvm_vm_ioctl (filp=<optimized out>, ioctl=44609, arg=0) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4676
    ```

    ```c
    Breakpoint 5, __gfn_to_pfn_memslot (hva=0x0 <fixed_percpu_data>, writable=0x0 <fixed_percpu_data>, write_fault=true,
        async=0x0 <fixed_percpu_data>, atomic=false, gfn=1043968, slot=0xffff888100ddf800)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    2701            unsigned long addr = __gfn_to_hva_many(slot, gfn, NULL, write_fault);
    (gdb) bt
    #0  __gfn_to_pfn_memslot (hva=0x0 <fixed_percpu_data>, writable=0x0 <fixed_percpu_data>, write_fault=true,
        async=0x0 <fixed_percpu_data>, atomic=false, gfn=1043968, slot=0xffff888100ddf800)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    #1  gfn_to_pfn_memslot (gfn=1043968, slot=0xffff888100ddf800) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2739
    #2  gfn_to_pfn (gfn=gfn@entry=1043968, kvm=<optimized out>) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2757
    #3  gfn_to_page (kvm=<optimized out>, gfn=gfn@entry=1043968) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2795
    #4  0xffffffff8107baff in vmx_set_apic_access_page_addr (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:6667
    #5  vmx_set_apic_access_page_addr (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:6653
    #6  0xffffffff8103fec7 in kvm_vcpu_reload_apic_access_page (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10533
    #7  vcpu_enter_guest (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10651
    #8  vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:11008
    #9  kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11229
    #10 0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

    ```c
    Breakpoint 5, __gfn_to_pfn_memslot (slot=slot@entry=0xffff888100e32200, gfn=1048575, atomic=atomic@entry=false,
        async=async@entry=0xffffc900001cfaff, write_fault=false, writable=writable@entry=0xffffc900001cfc58,
        hva=0xffffc900001cfc50) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    2701            unsigned long addr = __gfn_to_hva_many(slot, gfn, NULL, write_fault);
    (gdb) bt
    #0  __gfn_to_pfn_memslot (slot=slot@entry=0xffff888100e32200, gfn=1048575, atomic=atomic@entry=false,
        async=async@entry=0xffffc900001cfaff, write_fault=false, writable=writable@entry=0xffffc900001cfc58,
        hva=0xffffc900001cfc50) at arch/x86/kvm/../../../virt/kvm/kvm_main.c:2701
    #1  0xffffffff81061fa0 in kvm_faultin_pfn (vcpu=vcpu@entry=0xffff888100ec0000, fault=fault@entry=0xffffc900001cfc20)
        at arch/x86/kvm/mmu/mmu.c:4173
    #2  0xffffffff8106aa1a in direct_page_fault (vcpu=vcpu@entry=0xffff888100ec0000, fault=fault@entry=0xffffc900001cfc20)
        at arch/x86/kvm/mmu/mmu.c:4248
    #3  0xffffffff8106afa4 in kvm_tdp_page_fault (vcpu=vcpu@entry=0xffff888100ec0000,
        fault=fault@entry=0xffffc900001cfc20) at arch/x86/kvm/mmu/mmu.c:4351
    #4  0xffffffff8106b13d in kvm_mmu_do_page_fault (prefetch=false, err=16, cr2_or_gpa=4294967280,
        vcpu=0xffff888100ec0000) at arch/x86/kvm/mmu/mmu_internal.h:290
    #5  kvm_mmu_page_fault (vcpu=vcpu@entry=0xffff888100ec0000, cr2_or_gpa=4294967280, error_code=4294967312,
        insn=insn@entry=0x0 <fixed_percpu_data>, insn_len=insn_len@entry=0) at arch/x86/kvm/mmu/mmu.c:5550
    #6  0xffffffff8107960a in handle_ept_violation (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:5701
    #7  0xffffffff810845d4 in __vmx_handle_exit (exit_fastpath=EXIT_FASTPATH_NONE, vcpu=0xffff888100ec0000)
        at arch/x86/kvm/vmx/vmx.c:6480
    #8  vmx_handle_exit (vcpu=0xffff888100ec0000, exit_fastpath=EXIT_FASTPATH_NONE) at arch/x86/kvm/vmx/vmx.c:6497
    #9  0xffffffff8103f7a5 in vcpu_enter_guest (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10905
    #10 vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:11008
    #11 kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11229
    #12 0xffffffff81023d9b in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=0)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087
    ```

* kvm_set_cr3

    ```c
    Breakpoint 4, kvm_set_cr3 (vcpu=0xffff888100ec0000, cr3=0) at arch/x86/kvm/x86.c:1251
    1251            if (pcid_enabled) {
    (gdb) bt
    #0  kvm_set_cr3 (vcpu=0xffff888100ec0000, cr3=0) at arch/x86/kvm/x86.c:1251
    #1  0xffffffff81037fd8 in emulator_set_cr (ctxt=<optimized out>, cr=<optimized out>, val=<optimized out>)
        at arch/x86/kvm/x86.c:7941
    #2  0xffffffff81045228 in rsm_enter_protected_mode (ctxt=ctxt@entry=0xffff888100ec8000, cr0=cr0@entry=17,
        cr3=cr3@entry=0, cr4=cr4@entry=0) at arch/x86/kvm/emulate.c:2418
    #3  0xffffffff81049c0e in rsm_load_state_64 (smstate=<optimized out>, ctxt=<optimized out>)
        at arch/x86/kvm/emulate.c:2568
    #4  em_rsm (ctxt=0xffff888100ec8000) at arch/x86/kvm/emulate.c:2649
    #5  0xffffffff8104e9d4 in x86_emulate_insn (ctxt=0xffff888100ec0000, ctxt@entry=0xffff888100ec8000)
        at arch/x86/kvm/emulate.c:5634
    #6  0xffffffff8103dd35 in x86_emulate_instruction (vcpu=vcpu@entry=0xffff888100ec0000, cr2_or_gpa=cr2_or_gpa@entry=0,
        emulation_type=2, insn=insn@entry=0x0 <fixed_percpu_data>, insn_len=insn_len@entry=0) at arch/x86/kvm/x86.c:8933
    #7  0xffffffff8103e213 in kvm_emulate_instruction (emulation_type=<optimized out>, vcpu=0xffff888100ec0000)
        at arch/x86/kvm/x86.c:9012
    #8  handle_ud (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:7400
    #9  0xffffffff81083c22 in handle_exception_nmi (vcpu=0xffff888100ec0000) at arch/x86/kvm/vmx/vmx.c:5118
    #10 0xffffffff810845d4 in __vmx_handle_exit (exit_fastpath=EXIT_FASTPATH_NONE, vcpu=0xffff888100ec0000)
        at arch/x86/kvm/vmx/vmx.c:6480
    #11 vmx_handle_exit (vcpu=0xffff888100ec0000, exit_fastpath=EXIT_FASTPATH_NONE) at arch/x86/kvm/vmx/vmx.c:6497
    #12 0xffffffff8103f7a5 in vcpu_enter_guest (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:10905
    #13 vcpu_run (vcpu=0xffff888100ec0000) at arch/x86/kvm/x86.c:11008
    #14 kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff888100ec0000) at arch/x86/kvm/x86.c:11229
    ```

### KVM EPT

* mmu_alloc_direct_roots

    ```c
    Breakpoint 3, mmu_alloc_direct_roots (vcpu=0xffff8881017e0000) at arch/x86/kvm/mmu/mmu.c:3557
    3557            r = make_mmu_pages_available(vcpu);
    (gdb) bt
    #0  mmu_alloc_direct_roots (vcpu=0xffff8881017e0000) at arch/x86/kvm/mmu/mmu.c:3557
    #1  kvm_mmu_load (vcpu=vcpu@entry=0xffff8881017e0000) at arch/x86/kvm/mmu/mmu.c:5301
    #2  0xffffffff8107e0ae in kvm_mmu_reload (vcpu=0xffff8881017e0000) at arch/x86/kvm/mmu.h:128
    #3  vcpu_enter_guest (vcpu=vcpu@entry=0xffff8881017e0000) at arch/x86/kvm/x86.c:10720
    #4  0xffffffff81081285 in vcpu_run (vcpu=0xffff8881017e0000) at arch/x86/kvm/x86.c:11008
    #5  kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff8881017e0000) at arch/x86/kvm/x86.c:11229
    ```

    ```c
    root = kvm_tdp_mmu_get_vcpu_root_hpa(vcpu);
    ///////////////////////////////////////////
    hpa_t kvm_tdp_mmu_get_vcpu_root_hpa(struct kvm_vcpu *vcpu)
    {
        ...
        /*
        * Check for an existing root before allocating a new one.  Note, the
        * role check prevents consuming an invalid root.
        */
        for_each_tdp_mmu_root(kvm, root, kvm_mmu_role_as_id(role)) {
            if (root->role.word == role.word &&
                kvm_tdp_mmu_get_root(root))
                goto out;
        }

        root = tdp_mmu_alloc_sp(vcpu);
        tdp_mmu_init_sp(root, NULL, 0, role);
        ...
    out:
        return __pa(root->spt);
    }
    ```

* kvm_set_cr3

    ```c
    Breakpoint 4, kvm_set_cr3 (vcpu=0xffff8881017d8000, cr3=0) at arch/x86/kvm/x86.c:1251
    1251            if (pcid_enabled) {
    (gdb) bt
    #0  kvm_set_cr3 (vcpu=0xffff8881017d8000, cr3=0) at arch/x86/kvm/x86.c:1251
    #1  0xffffffff8107862b in emulator_set_cr (ctxt=<optimized out>, cr=<optimized out>, val=<optimized out>)
        at arch/x86/kvm/x86.c:7941
    #2  0xffffffff8108916b in rsm_enter_protected_mode (ctxt=ctxt@entry=0xffff8881017e0000, cr0=cr0@entry=17,
        cr3=cr3@entry=0, cr4=cr4@entry=0) at arch/x86/kvm/emulate.c:2418
    #3  0xffffffff81090347 in rsm_load_state_64 (smstate=0xffffc9000044f940 "\020", ctxt=0xffff8881017e0000)
        at arch/x86/kvm/emulate.c:2568
    #4  em_rsm (ctxt=0xffff8881017e0000) at arch/x86/kvm/emulate.c:2649
    #5  0xffffffff81095051 in x86_emulate_insn (ctxt=ctxt@entry=0xffff8881017e0000) at arch/x86/kvm/emulate.c:5634
    #6  0xffffffff8107bba1 in x86_emulate_instruction (vcpu=vcpu@entry=0xffff8881017d8000,
        cr2_or_gpa=cr2_or_gpa@entry=0, emulation_type=2, insn=insn@entry=0x0 <fixed_percpu_data>,
        insn_len=insn_len@entry=0) at arch/x86/kvm/x86.c:8933
    #7  0xffffffff8107c174 in kvm_emulate_instruction (emulation_type=<optimized out>, vcpu=0xffff8881017d8000)
        at arch/x86/kvm/x86.c:9012
    #8  handle_ud (vcpu=vcpu@entry=0xffff8881017d8000) at arch/x86/kvm/x86.c:7400
    #9  0xffffffff810f1baf in handle_exception_nmi (vcpu=0xffff8881017d8000) at arch/x86/kvm/vmx/vmx.c:5118
    #10 0xffffffff810f3723 in __vmx_handle_exit (exit_fastpath=<optimized out>, vcpu=0xffff8881017d8000)
        at arch/x86/kvm/vmx/vmx.c:6480
    #11 vmx_handle_exit (vcpu=0xffff8881017d8000, exit_fastpath=EXIT_FASTPATH_NONE) at arch/x86/kvm/vmx/vmx.c:6497
    #12 0xffffffff8107ddb5 in vcpu_enter_guest (vcpu=vcpu@entry=0xffff8881017d8000) at arch/x86/kvm/x86.c:10905
    #13 0xffffffff81081285 in vcpu_run (vcpu=0xffff8881017d8000) at arch/x86/kvm/x86.c:11008
    #14 kvm_arch_vcpu_ioctl_run (vcpu=vcpu@entry=0xffff8881017d8000) at arch/x86/kvm/x86.c:11229
    #15 0xffffffff8104297e in kvm_vcpu_ioctl (filp=<optimized out>, ioctl=<optimized out>, arg=<optimized out>)
        at arch/x86/kvm/../../../virt/kvm/kvm_main.c:4087

    ```
