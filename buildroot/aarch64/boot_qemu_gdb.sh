#!/bin/sh

export PATH=${PWD}/host/bin:${PATH}
MEM_SIZE=2G

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
    -gdb tcp::8848 \
    $@
