/*
 * DFFRAM128x32_tb.v
 *
 * A testbench for DFFRAM128x32 macro
 *
 * This is free software: you can redistribute it and/or modify
 * it under the terms of the Apache License, Version 2.0 (the "License").
 *
 * DFFRAM is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * Apache License, Version 2.0 for more details.
 *
 * You should have received a copy of the Apache License, Version 2.0
 * along with DFFRAM. If not, see <https://www.apache.org/licenses/LICENSE-2.0>.
 *
 * For further information, please visit .
 *
 */

`timescale 1ns/1ps
 
`default_nettype        none

module DFFRAM128x32_tb;

    // Parameters
    parameter USE_LATCH = 1;
    parameter WSIZE = 4;
    parameter BANKS = 8;

    localparam    AWIDTH = $clog2(BANKS)+4;

    // Inputs
    reg                       CLK;
    reg [WSIZE-1:0]           WE0;
    reg                       EN0;
    reg [AWIDTH-1:0]   A0;
    reg [(WSIZE*8-1):0]       Di0;

    // Outputs
    wire [(WSIZE*8-1):0]      Do0;

    reg VGND;
    reg VPWR;

    // Instantiate the module under test
    DFFRAM128x32 muv (
`ifdef USE_POWER_PINS  
            .VPWR(VPWR),
            .VGND(VGND), 
`endif 
            .CLK(CLK), 
            .WE0(WE0), 
            .EN0(EN0), 
            .A0(A0), 
            .Di0(Di0), 
            .Do0(Do0)
    );

    initial begin
        $dumpfile("DFFRAM128x32_tb.vcd");
        $dumpvars;
    end
    // Clock generation - 50MHz
    always #10 CLK = ~CLK;

    // Read task
    task read_word;
    input   [AWIDTH-1:0]     addr;
    output  [(WSIZE*8-1):0] data;
    begin
        @(posedge CLK);
        #1;
        WE0 = 4'b0000;
        A0 = addr;
        @(posedge CLK);
        @(posedge CLK) data <= Do0;
        #1;
        $display("Read A:%x, D:%x", addr, data);
    end
    endtask

    // Write task
    task write_word;
    input [AWIDTH-1:0]  addr;
    input [(32-1):0]    data;
    input[3:0]          mask;
    begin
        @(posedge CLK);
        #1;
        WE0 = mask;
        A0 = addr;
        Di0 = data;
        @(posedge CLK);
        #1;
        WE0 = 4'b0;
        $display("Wrote a:%x, D:%x, Mask:%b", addr, data, mask);
    end
    endtask

    task check;
    input [31:0] data_read;
    input [31:0] data_expected;
    begin
        if (data_read !== data_expected)
            $display("Test failed. Expected: %h, Got: %h", data_expected, data_read);
        else
            $display("Test passed.");
    end
    endtask

    reg [31:0] data;
    // Test stimulus
    initial begin
        // Power up the Memory
        VPWR = 1;
        VGND = 0;
        
        // Initialize inputs
        CLK = 0;
        EN0 = 1;
        Di0 = 32'h00;
        WE0 = 4'b0;

        // Write and read to/from Bank0
        $display("\n+++Verifying Bank 0+++");
        write_word('h0, 32'h110055BB, 4'b1111);
        write_word('h1, 32'h110055CC, 4'b1111);
        write_word('h2, 32'h110055DD, 4'b1111);
        
        read_word('h0, data);
        check(data, 32'h110055BB);
    
        write_word('h2, 32'h00_00_00_33, 4'b0001);
        write_word('h1, 32'h00_00_33_00, 4'b0010);
        write_word('h0, 32'h00_33_00_00, 4'b0100);

        read_word('h0, data);
        check(data, 32'h113355bb);
        
        read_word('h1, data);
        check(data, 32'h110033cc);
        
        read_word('h2, data);
        check(data, 32'h11005533);
        
        // Write and read to/from Bank1
        $display("\n+++Verifying Bank 1+++");
        write_word('h10, 32'hAA0055BB, 4'b1111);
        write_word('h11, 32'hAA0055CC, 4'b1111);
        write_word('h12, 32'hAA0055DD, 4'b1111);
        
        read_word('h10, data);
        check(data, 32'hAA0055BB);
    
        write_word('h12, 32'h00_00_00_33, 4'b0001);
        write_word('h11, 32'h00_00_33_00, 4'b0010);
        write_word('h10, 32'h00_33_00_00, 4'b0100);

        read_word('h10, data);
        check(data, 32'haa3355bb);
        
        read_word('h11, data);
        check(data, 32'haa0033cc);
        
        read_word('h12, data);
        check(data, 32'haa005533);  

        // Write and read to/from Bank 7
        $display("\n+++Verifying Bank 7+++");
        write_word('h70, 32'hF0F055BB, 4'b1111);
        write_word('h71, 32'hF0F055CC, 4'b1111);
        write_word('h72, 32'hF0F055DD, 4'b1111);
        
        read_word('h70, data);
        check(data, 32'hF0F055BB);
    
        write_word('h72, 32'hAB_00_00_33, 4'b0001);
        write_word('h71, 32'hAB_00_33_00, 4'b0010);
        write_word('h70, 32'hAB_33_00_00, 4'b0100);

        read_word('h70, data);
        check(data, 32'hF0_33_55_bb);
        
        read_word('h71, data);
        check(data, 32'hF0_F0_33_cc);
        
        read_word('h72, data);
        check(data, 32'hF0_F0_55_33);  

        #100;

        // Finish simulation
        $finish;
    end

endmodule