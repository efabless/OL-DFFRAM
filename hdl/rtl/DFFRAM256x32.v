module DFFRAM256x32  (
	input   wire            CLK,  
    input   wire [3:0]      WE0,  
    input                   EN0,  
    input   wire [7:0]      A0,   
    input   wire [31:0]     Di0,  
    output  wire [31:0]     Do0
);

    DFFRAM  #( .USE_LATCH(1), .WSIZE(4), .BANKS(16) ) RAM (
	    .CLK(CLK),  
        .WE0(WE0),  
        .EN0(EN0),  
        .A0(A0),   
        .Di0(Di0),  
        .Do0(Do0)
    );

endmodule