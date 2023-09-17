SIM-RTL-128:
	iverilog -o ram128-rtl.vvp DFFRAM128x32_tb.v ../../hdl/rtl/DFFRAM128x32.v ../../hdl/rtl/DFFRAM.v hd_cells.v primitives.v
	./ram128-rtl.vvp

SIM_GL_128:
	iverilog -o ram128-rtl.vvp DFFRAM128x32_tb.v ../../hdl/gl/DFFRAM128x32.v hd_cells.v primitives.v
	./ram128-gl.vvp

SIM-RTL-256:
	iverilog -o ram256-rtl.vvp DFFRAM256x32_tb.v ../../hdl/rtl/DFFRAM256x32.v ../../hdl/rtl/DFFRAM.v hd_cells.v primitives.v
	./ram256-rtl.vvp

SIM_GL_256:
	iverilog -o ram256-rtl.vvp DFFRAM256x32_tb.v ../../hdl/gl/DFFRAM256x32.v hd_cells.v primitives.v
	./ram256-gl.vvp