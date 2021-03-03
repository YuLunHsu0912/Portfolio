//--------------------------------------------------------------------------------
//Version:     1
//--------------------------------------------------------------------------------
//Writer:      
//----------------------------------------------
//Date:        
//----------------------------------------------
//Description: 
//--------------------------------------------------------------------------------
module Simple_Single_CPU(
        clk_i,
		nrst_i
		);
		
//I/O port
input			clk_i;
input			nrst_i;  // negative reset

//Internal Signles
//reg  [31:0] pc_current;
wire [31:0] pc_in;
wire [31:0] pc_out;
wire [31:0] add1_mux;
wire [31:0] instr_o;
wire	[1:0]	ALU_op;
wire		ALUSrc;
wire		RegWrite;
wire		Branch;
wire		MemRead;
wire		MemWrite;
wire		MemtoReg;
wire		[3:0] ALUCtrl;
wire		[63:0] signed_extend;
wire		[63:0] mux_register;
wire		[63:0] data1;
wire		[63:0] data2;
wire		[63:0] realdata2;
wire		[63:0]  Address;
wire		zero;
wire		[63:0] memory_mux;
wire		[63:0] shift_add;
wire		[31:0] add2_mux;
// decoder
/*
always@(posedge clk_i or posedge nrst_i)
begin
	if(nrst_i)
	begin		
	pc_current<=32'd0;
	end
end
assign pc_in=pc_current;*/
//Greate componentes
ProgramCounter PC(
        .clk_i(clk_i),      
	    .nrst_i(nrst_i),     
	    .pc_in_i(pc_in) ,   
	    .pc_out_o(pc_out) 
	    );

// adder for program counter
Adder Adder1(
        .src1_i(pc_out),     
	    .src2_i(32'd4),     
	    .sum_o(add1_mux)    
	    );
	
Instr_Memory IM(
        .pc_addr_i(pc_out),  
	    .instr_o(instr_o)    
	    );

Decoder Decoder(
        .instr_op_i(instr_o[6:0]), 
	    .RegWrite_o(RegWrite), 
	    .ALU_op_o(ALU_op),   
	    .ALUSrc_o(ALUSrc),      
		.Branch_o(Branch),
		.MemRead_o(MemRead),
		.MemWrite_o(MemWrite),
		.MemtoReg_o(MemtoReg)
	    );	
	
Reg_File Registers(
        .clk_i(clk_i),      
	    .nrst_i(nrst_i) ,     
        .RSaddr_i(instr_o[19:15]) ,  
        .RTaddr_i(instr_o[24:20]) ,  
        .RDaddr_i(instr_o[11:7]) ,  
        .RDdata_i(mux_register)  , 
        .RegWrite_i (RegWrite),
        .RSdata_o(data1) ,  
        .RTdata_o(data2)   
        );
	


ALU_Ctrl AC(
        .funct3_i(instr_o[14:12]),
		.funct7_i(instr_o[31:25]),		
        .ALUOp_i(ALU_op),   
        .ALUCtrl_o(ALUCtrl) 
        );
	
Imm_Gen IG(
    .instr_i(instr_o),
    .signed_extend_o(signed_extend)
    );

MUX_2to1 #(.size(64)) Mux_ALUSrc(
        .data0_i(data2),
        .data1_i(signed_extend),
        .select_i(ALUSrc),
        .data_o(realdata2)
        );	
		
ALU ALU(
        .src1_i(data1),
	    .src2_i(realdata2),
	    .ctrl_i(ALUCtrl),
	    .result_o(Address),
		.zero_o(zero)
	    );
	
Data_Memory Data_Memory(
	.clk_i(clk_i),
	.addr_i(Address),
	.data_i(data2),
	.MemRead_i(MemRead),
	.MemWrite_i(MemWrite),
	.data_o(memory_mux)
	);
	

		
Shift_Left_One_64 Shifter(
        .data_i(signed_extend[63:0]),
        .data_o(shift_add[63:0])
        ); 		

Adder Adder2(
        .src1_i(pc_out),     
	    .src2_i(shift_add[31:0]),     
	    .sum_o(add2_mux)      
	    );
		
MUX_2to1 #(.size(32)) Mux_PC_Source(
        .data0_i(add1_mux),
        .data1_i(add2_mux),
        .select_i(Branch&zero),
        .data_o(pc_in)
        );	

MUX_2to1 #(.size(64)) Mux_Write_Back(
        .data0_i(Address),
        .data1_i(memory_mux),
        .select_i(MemtoReg),
        .data_o(mux_register)
        );	

endmodule
		  


