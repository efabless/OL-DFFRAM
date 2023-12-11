#!/bin/bash
arg1=$1
mkdir -p $1
cp $1.json $1

cp README.md $1

mkdir -p $1/verify/utb

cp verify/utb/Makefile verify/utb/sky130_fd_sc_hd.v verify/utb/primitives.v verify/utb/hd_cells.v verify/utb/DFFRAM_tb.v verify/utb/$1_tb.v $1/verify/utb

mkdir -p $1/timing/lib/max $1/timing/lib/min $1/timing/lib/nom

cp timing/lib/max/$1.* $1/timing/lib/max
cp timing/lib/min/$1.* $1/timing/lib/min
cp timing/lib/nom/$1.* $1/timing/lib/nom

mkdir $1/timing/pt-etm

cp -r timing/pt-etm/$1 timing/pt-etm/signoff.sdc $1/timing/pt-etm

mkdir -p $1/timing/sdf/max $1/timing/sdf/min $1/timing/sdf/nom

cp timing/sdf/max/$1.* $1/timing/sdf/max
cp timing/sdf/min/$1.* $1/timing/sdf/min
cp timing/sdf/nom/$1.* $1/timing/sdf/nom

mkdir -p $1/timing/spef

cp timing/spef/$1.* $1/timing/spef
cp timing/spef/$1.* $1/timing/spef
cp timing/spef/$1.* $1/timing/spef

mkdir -p $1/layout/gds $1/layout/mag $1/layout/lef

cp layout/gds/$1.* $1/layout/gds
cp layout/mag/$1.* $1/layout/mag
cp layout/lef/$1.* $1/layout/lef

mkdir -p $1/hdl/gl $1/hdl/rtl/bus_wrapper $1/hdl/sim

cp hdl/gl/$1.* $1/hdl/gl
cp hdl/rtl/$1.* hdl/rtl/DFFRAM.v $1/hdl/rtl
cp hdl/rtl/bus_wrapper/$1_ahbl.v $1/hdl/rtl/bus_wrapper
cp hdl/sim/$1.* $1/hdl/sim

cp -r doc $1

mkdir -p $1/PnR

cp -r PnR/$1 $1/PnR

cd $1 

tar czf $2.tar.gz *
