module DFFRAM_tb;

  // Parameters
  parameter USE_LATCH = 1;
  parameter WSIZE = 4;
  parameter BANKS = 2;

  localparam    AWIDTH = $clog2(BANKS)+4;

  // Inputs
  reg                       CLK;
  reg [WSIZE-1:0]           WE0;
  reg                       EN0;
  reg [$clog2(BANKS)+3:0]   A0;
  reg [(WSIZE*8-1):0]       Di0;

  // Outputs
  wire [(WSIZE*8-1):0]      Do0;

    // Instantiate the module under test
    DFFRAM #(.USE_LATCH(USE_LATCH), .WSIZE(WSIZE), .BANKS(BANKS))
    muv (.CLK(CLK), .WE0(WE0), .EN0(EN0), .A0(A0), .Di0(Di0), .Do0(Do0));

    initial begin
        $dumpfile("DFFRAM_tb.vcd");
        $dumpvars;
    end
    // Clock generation - 50MHz
    always #10 CLK = ~CLK;

    // Read task
    task read_word;
    input   [WSIZE-1:0]     addr;
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

    reg [31:0] data;
    // Test stimulus
    initial begin
    // Initialize inputs
    CLK = 0;
    EN0 = 1;
    Di0 = 32'h00;
    WE0 = 4'b0;

    write_word(7'h0, 32'hAA0055BB, 4'b11111);
    write_word(7'h1, 32'hAA0055CC, 4'b11111);
    write_word(7'h2, 32'hAA0055DD, 4'b11111);
    read_word(7'h0, data);
    // Check the output
    if (data !== 32'hAA0055BB)
        $display("Test failed. Expected: %h, Got: %h", 32'hAA0055BB, data);
    else
        $display("Test passed.");

    write_word(7'h2, 32'h00_00_00_33, 4'b0001);
    write_word(7'h1, 32'h00_00_33_00, 4'b0010);
    write_word(7'h0, 32'h00_33_00_00, 4'b0100);

    read_word(7'h0, data);
    read_word(7'h1, data);
    read_word(7'h2, data);
    
    
    #100;

    // Finish simulation
    $finish;
    end

endmodule