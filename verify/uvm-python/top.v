`timescale 1ns/1ps

module top();
    reg 		CLK = 0;
    wire 		RESETn = 1'b1;
    wire 		irq;
    // TODO: Add any IP signals here
        wire [31:0]	HADDR;
        wire 		HWRITE;
        wire 		HSEL = 0;
        wire 		HREADYOUT;
        wire [1:0]	HTRANS=0;
        wire [31:0]	HWDATA;
        wire [31:0]	HRDATA;
        wire 		HREADY;
        wire [2:0]  HSIZE;
    `ifdef RAM128
        DFFRAM128x32_ahbl dut( `ifdef USE_POWER_PINS .VPWR(1'b1), .VGND(1'b0), `endif .HCLK(CLK), .HRESETn(RESETn), .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL), .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA), .HREADY(HREADY),.HREADYOUT(HREADYOUT), .HSIZE(HSIZE));
    `elsif RAM256
        DFFRAM256x32_ahbl dut(`ifdef USE_POWER_PINS .VPWR(1'b1), .VGND(1'b0), `endif .HCLK(CLK), .HRESETn(RESETn), .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL), .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA), .HREADY(HREADY),.HREADYOUT(HREADYOUT), .HSIZE(HSIZE));
    `elsif RAM512
        DFFRAM512x32_ahbl dut(`ifdef USE_POWER_PINS .VPWR(1'b1), .VGND(1'b0), `endif .HCLK(CLK), .HRESETn(RESETn), .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL), .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA), .HREADY(HREADY),.HREADYOUT(HREADYOUT), .HSIZE(HSIZE));
    `endif
    // monitor inside signals
    `ifndef SKIP_WAVE_DUMP
        initial begin
            $dumpfile ({"waves.vcd"});
            $dumpvars(0, top);
        end
    `endif
    always #10 CLK = !CLK; // clk generator
endmodule