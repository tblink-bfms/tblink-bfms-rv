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

	wire uclock = clock;
	wire cclock;
	
	`RV_WIRES(bfm2ctrl_, 8);
	`RV_WIRES(ctrl2bfm_, 8);
	`RV_WIRES(ctrl2dut_, 8);
	`RV_WIRES(dut2ctrl_, 8);
	
	rv_initiator_bfm_sim #(
			.WIDTH(8)
		) u_bfm2ctrl(
			.clock(		uclock),
			.reset(		reset),
			`RV_CONNECT(i_, bfm2ctrl_)
		);
	rv_target_bfm_sim #(
			.WIDTH(8)
		) u_ctrl2bfm(
			.clock(		uclock),
			.reset(		reset),
			`RV_CONNECT(t_, ctrl2bfm_)
		);
	
	tblink_rpc_ctrl u_ctrl (
		.uclock      (uclock     ), 
		.reset       (reset      ), 
		.cclock      (cclock     ), 
		.hreq_i      (hreq_i     ), 
		`RV_CONNECT(t_, bfm2ctrl_),
		`RV_CONNECT(i_, ctrl2bfm_),
		`RV_CONNECT(neti_, dut2ctrl_),
		`RV_CONNECT(neto_, ctrl2dut_)
		);

	`RV_WIRES(dut2bfm_, 32);
	rv_initiator_bfm_syn #(
			.ADDR(1),
			.WIDTH(32)
		) u_dut (
			.cclock(			cclock),
			.uclock(			uclock),
			.reset(				reset),
			`RV_CONNECT(neti_, ctrl2dut_),
			`RV_CONNECT(neto_, dut2ctrl_),
			`RV_CONNECT(i_, dut2bfm_)
			);
	
	rv_target_bfm_sim #(
			.WIDTH(32)
		) u_dut_bfm(
			.clock(				uclock),
			.reset(				reset),
			`RV_CONNECT(t_, dut2bfm_)
		);
	
endmodule


