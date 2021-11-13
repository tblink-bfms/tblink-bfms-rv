/****************************************************************************
 * smoke_uvm_tb.sv
 ****************************************************************************/
`include "rv_macros.svh"
`ifdef NEED_TIMESCALE
`timescale 1ns/1ns
`endif
  
/**
 * Module: smoke_uvm_tb
 * 
 * TODO: Add module documentation
 */
module smoke_uvm_tb(input clock);
	import uvm_pkg::*;
	import smoke_uvm_pkg::*;
	
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
	
	wire reset = 0;
	
	`RV_WIRES(rv_, 32);
	
	rv_initiator_bfm #(
			.WIDTH(32)
			) u_bfm (
				.clock(clock),
				.reset(reset),
				`RV_CONNECT(i_, rv_)
			);
	
	initial begin
		run_test();
	end


endmodule


