/*
	Copyright 2023 AUC Open H/W Lab

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

`timescale              1ns/1ps
`default_nettype        none

module DFFRAM128x32_ahbl (
    `ifdef USE_POWER_PINS
    input wire              VPWR,
    input wire              VGND,
    `endif
    input                   HCLK,
    input                   HRESETn,
    
    input wire              HSEL,
    input wire [31:0]       HADDR,
    input wire [1:0]        HTRANS,
    input wire              HWRITE,
    input wire              HREADY,
    input wire [31:0]       HWDATA,
    input wire [2:0]        HSIZE,
    output wire             HREADYOUT,
    output wire [31:0]      HRDATA
);   

    localparam              AW = 9;            // Address width - byte addressing
    wire                  SRAMCS;
    wire [3:0]            SRAMWEN;
    wire [AW-3:0]         SRAMADDR;
    wire [31:0]           SRAMWDATA;
    wire [31:0]           SRAMRDATA;

    DFFRAM_ahbl#(AW) RAM_ahbl  (
        .HCLK(HCLK),
        .HRESETn(HRESETn),
        .HSEL(HSEL),
        .HADDR(HADDR),
        .HTRANS(HTRANS),
        .HSIZE(HSIZE),
        .HWDATA(HWDATA),
        .HWRITE(HWRITE),
        .HREADY(HREADY),
        .HREADYOUT(HREADYOUT),
        .HRDATA(HRDATA),
        .SRAMCS(SRAMCS),
        .SRAMADDR(SRAMADDR),
        .SRAMWDATA(SRAMWDATA),
        .SRAMRDATA(SRAMRDATA),
        .SRAMWEN(SRAMWEN)
    );

    DFFRAM128x32 DFFRAM128x32 (
        `ifdef USE_POWER_PINS
        .VPWR(VPWR),
        .VGND(VGND),
        `endif
        .CLK(HCLK),
        .EN0(SRAMCS),
        .A0(SRAMADDR),
        .Di0(SRAMWDATA),
        .Do0(SRAMRDATA),
        .WE0(SRAMWEN)
    );

endmodule