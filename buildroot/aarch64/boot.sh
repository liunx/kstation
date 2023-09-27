#!/bin/sh

export PATH="/home/liunx/Work/CloudEdge/Work/build/buildroot/aarch64/host/bin:${PATH}"
SOCK_PATH=/tmp/vhost-fs.sock
MEM_SIZE=2G

virtiofsd \
    --announce-submounts \
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
    -drive file=images/rootfs.ext4,if=none,format=raw,id=hd0 \
    -chardev socket,id=char0,path=${SOCK_PATH} \
    -device vhost-user-fs-pci,chardev=char0,tag=myfs \
    -object memory-backend-memfd,id=mem,size=${MEM_SIZE},share=on \
    -numa node,memdev=mem \
    -device virtio-blk-device,drive=hd0 ${EXTRA_ARGS}
