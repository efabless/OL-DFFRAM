# OL-DFFRAM
OpenLane hardened DFFRAM macros. This repo provides three ready to use single port DFFRAM macros:
- 128x32 (512 bytes)
- 256x32 (1024 bytes)
- 512x32 (2048 bytes)

## Read and Write Operations
The DFFRAM adheres to the SRAM read/write operation. The following timing diagram explains its operation.
![DFFRAM RD/WR](doc/static/rd_wr.png)

## Timing Parameters
![DFFRAM RD/WR](doc/static/timing.png)
|Parameters|DFRAM128x32|DFFRAM256x32|DFFRAM512x32|
|----------|-----------|------------|------------|
|T<sub>C</sub> (min)| 25 ns| 25 ns| 30 ns|
|T<sub>1</sub> (min)| 10 ns| 10 ns| 10 ns|
|T<sub>2</sub> (min)| 10 ns| 10 ns| 10 ns|
|T<sub>3</sub> (min)| 10 ns| 10 ns| 10 ns|
|T<sub>4</sub> (max)| 10 ns| 10 ns| 10 ns|
