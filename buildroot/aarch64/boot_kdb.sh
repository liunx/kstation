#!/bin/sh

export PATH=${PWD}/host/bin:${PATH}
MEM_SIZE=2G
#-append "rootwait root=/dev/vda console=ttyAMA0 kgdboc=ttyS0 kgdbcon kgdbwait" \

exec qemu-system-aarch64 \
    -M virt \
    -m ${MEM_SIZE} \
    -cpu neoverse-n1 \
    -nographic \
    -smp 1 \
    -kernel images/Image \
    -append "rootwait root=/dev/vda console=ttyAMA0" \
    -netdev user,id=eth0 \
    -device virtio-net-device,netdev=eth0 \
    -drive file=images/rootfs.ext4,if=none,format=raw,id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -chardev socket,id=gdb,port=1234,server=on,wait=off,host=0.0.0.0 \
    -device pci-serial,chardev=gdb \
    $@

