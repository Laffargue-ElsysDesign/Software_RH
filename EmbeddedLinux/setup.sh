#! /bin/bash
PYNQ_DIR=../../PYNQ

cp Files/build.sh $PYNQ_DIR/
cp Files/Makefile $PYNQ_DIR/sdbuild
cp -r Zybo-Z7 $PYNQ_DIR/boards
