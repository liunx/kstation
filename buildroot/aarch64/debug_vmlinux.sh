#!/bin/bash

export PATH=${PWD}/host/bin:${PATH}

GDB=aarch64-buildroot-linux-gnu-gdb

exec ${GDB} --ex "target remote localhost:8848" build/linux-5.15.18/vmlinux

