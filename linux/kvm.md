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
