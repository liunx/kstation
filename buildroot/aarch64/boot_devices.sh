#!/bin/sh

export PATH=${PWD}/host/bin:${PATH}
SOCK_PATH=/tmp/vhost-fs.sock
MEM_SIZE=2G

virtiofsd \
    --announce-submounts \
    --sandbox none \
    --socket-path=${SOCK_PATH} \
    --shared-dir=${PWD} \
    --cache=auto &
sleep 1

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
    -chardev socket,id=char0,path=${SOCK_PATH} \
    -device vhost-user-fs-pci,chardev=char0,tag=myfs \
    -object memory-backend-memfd,id=mem,size=${MEM_SIZE},share=on \
    -numa node,memdev=mem \
    -drive file=images/rootfs.ext4,if=none,format=raw,id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -object can-bus,id=canbus0 \
    -device kvaser_pci,canbus=canbus0 \
    -device pci-testdev \
    $@
