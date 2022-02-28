/****************************************************************************
 * smoke_initiator_tb.sv
 ****************************************************************************/
`include "rv_macros.svh"
`ifdef NEED_TIMESCALE
`timescale 1ns/1ns
`endif
  
/**
 * Module: smoke_initiator_tb
 * 
 * TODO: Add module documentation
 */
module smoke_initiator_tb(input clock);
	
`ifdef HAVE_HDL_CLOCKGEN
	reg clock_r = 0;
	initial begin
		forever begin
`ifdef NEED_TIMESCALE
			#10;
`else
			#10ns;
`endif
			clock_r <= ~clock_r;
		end
	end
	assign clock = clock_r;
`endif
	
`ifdef IVERILOG
`include "iverilog_control.svh"
`endif
	
	reg reset /*verilator public */ = 0;
	
	reg[7:0] reset_cnt = 0;
	
	always @(posedge clock) begin
		if (reset_cnt == 20) begin
			reset <= 1'b0;
		end else begin
			if (reset_cnt == 1) begin
				reset <= 1'b1;
			end
			reset_cnt <= reset_cnt + 1'b1;
		end
	end
	
	`RV_WIRES(rv_, 32);
	
	rv_initiator_bfm_sim #(
			.WIDTH(32)
			) u_bfm (
				.clock(clock),
				.reset(reset),
				`RV_CONNECT(i_, rv_)
			);

	reg rv_ready_r = 0;
	
	always @(posedge clock) begin
		if (reset) begin
			rv_ready_r <= 0;
		end else begin
			if (rv_ready_r) begin
				rv_ready_r <= 0;
			end else begin
				if (rv_valid) begin
					rv_ready_r <= 1;
				end
			end
		end
	end
	
	assign rv_ready = rv_ready_r;
	
endmodule


