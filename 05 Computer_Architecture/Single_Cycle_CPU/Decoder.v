//--------------------------------------------------------------------------------
//Version:     1
//--------------------------------------------------------------------------------
//Writer:      Luke
//----------------------------------------------
//Date:        
//----------------------------------------------
//Description: 
//--------------------------------------------------------------------------------

module Decoder(
    instr_op_i,
	RegWrite_o,
	ALU_op_o,
	ALUSrc_o,
	Branch_o,
	MemRead_o,
	MemWrite_o,
	MemtoReg_o
	);
     
//I/O ports
input	[6:0]	instr_op_i;

output			RegWrite_o;
output	[1:0]	ALU_op_o;
output			ALUSrc_o;
output			Branch_o;
output			MemRead_o;
output			MemWrite_o;
output			MemtoReg_o;
 
//Internal Signals
reg	[1:0]		ALU_op_o;
reg				ALUSrc_o;
reg				RegWrite_o;
reg				Branch_o;
reg				MemRead_o;
reg				MemWrite_o;
reg				MemtoReg_o;

//Parameter


//Main function
always@(*)
begin
	case(instr_op_i)
	7'b0110011:begin//R format
		RegWrite_o=1'b1;
		ALU_op_o=2'b10;
		ALUSrc_o=1'b0;
		Branch_o=1'b0;
		MemRead_o=1'b0;
		MemWrite_o=1'b0;
		MemtoReg_o=1'b0;
	end
	7'b0100011:begin//S format
		RegWrite_o=1'b0;
		ALU_op_o=2'b00;
		ALUSrc_o=1'b1;
		Branch_o=1'b0;
		MemRead_o=1'b0;
		MemWrite_o=1'b1;
		MemtoReg_o=1'b0;
	end

	7'b1100011:begin//B format
		RegWrite_o=1'b0;
		ALU_op_o=2'b01;
		ALUSrc_o=1'b0;
		Branch_o=1'b1;
		MemRead_o=1'b0;
		MemWrite_o=1'b0;
		MemtoReg_o=1'b0;
	end

	7'b0000011:begin//LD 
		RegWrite_o=1'b1;
		ALU_op_o=2'b00;
		ALUSrc_o=1'b1;
		Branch_o=1'b0;
		MemRead_o=1'b1;
		MemWrite_o=1'b0;
		MemtoReg_o=1'b1;
	end
	7'b0010011:begin//I format 
		RegWrite_o=1'b1;
		ALU_op_o=2'b00;
		ALUSrc_o=1'b1;
		Branch_o=1'b0;
		MemRead_o=1'b0;
		MemWrite_o=1'b0;
		MemtoReg_o=1'b0;
	end
	default:begin
		
	end
	endcase
	
end

endmodule





                    
                    