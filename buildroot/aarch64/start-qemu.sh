#!/bin/bash

export PATH=${PWD}/host/bin:${PATH}
SOCK_PATH=/tmp/vhost-fs.sock
MEM_SIZE=2G
QEMU=qemu-system-aarch64
CONSOLE="-nographic"

BASE_OPTS="-M virt -m ${MEM_SIZE} -cpu neoverse-n1 -smp 1 -kernel images/Image -append \"rootwait root=/dev/vda console=ttyAMA0\" -netdev user,id=eth0 -device virtio-net-device,netdev=eth0 -chardev socket,id=char0,path=${SOCK_PATH} -device vhost-user-fs-pci,chardev=char0,tag=myfs -object memory-backend-memfd,id=mem,size=${MEM_SIZE},share=on -numa node,memdev=mem -drive file=images/rootfs.ext4,if=none,format=raw,id=hd0 -device virtio-blk-device,drive=hd0"

SERIAL_OPTS="-chardev socket,id=kdb,port=1234,server=on,wait=off,host=0.0.0.0 -device pci-serial,chardev=kdb"
MISC_OPTS="-device pci-testdev"
VHOST_RNG="-chardev socket,path=/tmp/rng.sock0,id=rng0 -device vhost-user-rng-pci,chardev=rng0"
VHOST_OPTS="${VHOST_RNG}"

DEBUG_OPTS=""
GDB_RUN=""
if [ "$1" == "qdb" ]; then
    DEBUG_OPTS="-gdb tcp::8848"
elif [ "$1" == "gdb" ]; then
    GDB_RUN="gdb --args"
    CONSOLE="${CONSOLE} -serial telnet::1688,server=on,wait=off"
fi


virtiofsd \
    --announce-submounts \
    --sandbox none \
    --socket-path=${SOCK_PATH} \
    --shared-dir=${PWD} \
    --cache=auto &
sleep 1

bash -c "${GDB_RUN} ${QEMU} ${CONSOLE} ${BASE_OPTS} ${VHOST_OPTS} ${MISC_OPTS} ${DEBUG_OPTS} ${SERIAL_OPTS}"

