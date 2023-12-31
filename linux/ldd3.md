## 第2章 建立和运行模块

### 2.6. 预备知识

moudle.h 包含了大量加载模块需要的函数和符号的定义. 你需要 init.h 来指定你的初始化和清理函数, 如我们在上面的 "hello world" 例子里见到的, 这个我们在下一节中再讲. 大部分模块还包含 moudleparam.h, 使得可以在模块加载时传递参数给模块.

## 第4章 调试技术

### 4.2. 用打印调试

#### 4.2.2. 重定向控制台消息

Linux 在控制台记录策略上允许一些灵活性, 它允许你发送消息到一个指定的虚拟控制台(如果你的控制台使用的是文本屏幕). 缺省地, 这个"控制台"是当前虚拟终端. 为了选择一个不同地虚拟终端来接收消息, 你可对任何控制台设备调用 ioctl(TIOCLINUX). 下面的程序, setconsole, 可以用来选择哪个控制台接收内核消息; 它必须由超级用户运行, 可以从 misc-progs 目录得到.

#### 4.2.3. 消息是如何记录的

printk 函数将消息写入一个 __LOG_BUF_LEN 字节长的环形缓存, 长度值从 4 KB 到 1 MB, 由配置内核时选择. 这个函数接着唤醒任何在等待消息的进程, 就是说, 任何在系统调用中睡眠或者在读取 /proc/kmsg 的进程. 这 2 个日志引擎的接口几乎是等同的, 但是注意, 从 /proc/kmsg 中读取是从日志缓存中消费数据, 然而 syslog 系统调用能够选择地在返回日志数据地同时保留它给其他进程. 通常, 读取 /proc 文件容易些并且是 klogd 的缺省做法. dmesg 命令可用来查看缓存的内容, 不会冲掉它; 实际上, 这个命令将缓存区的整个内容返回给 stdout, 不管它是否已经被读过.