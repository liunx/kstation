#!/bin/bash

export PATH=${PWD}/host/bin:${PATH}
SOCK_PATH=/tmp/vhost-fs.sock
MEM_SIZE=2G
QEMU=qemu-system-aarch64

BOOT_OPTS="-M virt -m ${MEM_SIZE} -cpu neoverse-n1 -nographic -smp 1 -kernel images/Image -append \"rootwait root=/dev/vda console=ttyAMA0\" -netdev user,id=eth0 -device virtio-net-device,netdev=eth0 -chardev socket,id=char0,path=${SOCK_PATH} -device vhost-user-fs-pci,chardev=char0,tag=myfs -object memory-backend-memfd,id=mem,size=${MEM_SIZE},share=on -numa node,memdev=mem -drive file=images/rootfs.ext4,if=none,format=raw,id=hd0 -device virtio-blk-device,drive=hd0"

SERIAL_OPTS="-chardev socket,id=kdb,port=1234,server=on,wait=off,host=0.0.0.0 -device pci-serial,chardev=kdb"

DEBUG_OPTS=""
if [ "$1" == "gdb" ]; then
    DEBUG_OPTS="-gdb tcp::8848"
fi


virtiofsd \
    --announce-submounts \
    --sandbox none \
    --socket-path=${SOCK_PATH} \
    --shared-dir=${HOME}/Work \
    --cache=auto &
sleep 1

bash -c "${QEMU} ${BOOT_OPTS} ${SERIAL_OPTS} ${DEBUG_OPTS}"

