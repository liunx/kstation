#!/bin/bash

DEBUG=$1

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

PARAMS=""

if [ "$DEBUG" == "gdb" ] ; then
    PARAMS="gdb --args"
fi

exec $PARAMS qemu-system-aarch64 \
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
    -chardev socket,id=char0,path=${SOCK_PATH} \
    -device vhost-user-fs-pci,chardev=char0,tag=myfs \
    -chardev socket,path=/tmp/vi2c.sock0,id=vi2c \
    -device vhost-user-i2c-pci,chardev=vi2c,id=i2c \
    -object memory-backend-memfd,id=mem,size=${MEM_SIZE},share=on \
    -numa node,memdev=mem \
    -device virtio-blk-device,drive=hd0 ${EXTRA_ARGS}
