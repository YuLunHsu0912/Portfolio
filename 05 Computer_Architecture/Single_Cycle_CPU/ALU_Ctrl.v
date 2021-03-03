//--------------------------------------------------------------------------------
//Version:     1
//--------------------------------------------------------------------------------
//Writer:      
//----------------------------------------------
//Date:        
//----------------------------------------------
//Description: 
//--------------------------------------------------------------------------------

module ALU_Ctrl(
          funct3_i,
		  funct7_i,
          ALUOp_i,
          ALUCtrl_o
          );
          
//I/O ports 
input      [3-1:0] funct3_i;
input      [7-1:0] funct7_i;
input      [2-1:0] ALUOp_i;

output     [4-1:0] ALUCtrl_o;    
     
//Internal Signals
reg        [4-1:0] ALUCtrl_o;

//Parameter

//Select exact operation
always@(*)
begin
	if(ALUOp_i==2'b00)
	begin
		if(funct3_i==3'b010)
		begin
			ALUCtrl_o=4'b0111;
		end
		else
		begin
			ALUCtrl_o=4'b0010;
		end
	end

	else if(ALUOp_i==2'b01)
	begin
		ALUCtrl_o=4'b0110;	
	end

	else if(ALUOp_i==2'b10)
	begin
		if(funct3_i==3'b000)
		begin
			if(funct7_i==7'b0000000)
			begin
				ALUCtrl_o=4'b0010;
			end
			else
			begin
				ALUCtrl_o=4'b0110;
			end
			
		end
		else if(funct3_i==3'b111)
		begin
			ALUCtrl_o=4'b0000;
		end
		else if(funct3_i==3'b110)
		begin
			ALUCtrl_o=4'b0001;
		end
	end

end
endmodule     





                    
                    