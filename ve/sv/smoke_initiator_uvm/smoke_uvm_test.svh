
/****************************************************************************
 * smoke_uvm_test.svh
 ****************************************************************************/

  
/**
 * Class: smoke_uvm_test
 * 
 * TODO: Add class documentation
 */
class smoke_uvm_test extends uvm_test;
	`uvm_component_utils(smoke_uvm_test)
	
	IEndpoint						m_ep;
	rv_initiator_agent #(32)					m_rv_initiator_agent;

	function new(string name, uvm_component parent=null);
		super.new(name, parent);
		$display("smoke_uvm_test::new");
	endfunction

	function void build_phase(uvm_phase phase);
		TbLink tblink = TbLink::inst();
		IEndpoint ep = tblink.get_default_ep();
		SVEndpointLoopback ep_loopback;
		
		$display("test::build_phase");
		
		if (ep == null) begin
			`uvm_fatal("loopback_smoke_test", "No default endpoint");
			return;
		end
		
		if ($cast(ep_loopback, ep)) begin
			// The HDL endpoint is set as the default. 
			// We want the HVL endpoint
			m_ep = ep_loopback.m_peer_ep;
		end else begin
			m_ep = ep;
		end
		
		uvm_config_db #(IEndpoint)::set(this, "*", "IEndpoint", m_ep);
		
		m_rv_initiator_agent = new("m_rv_initiator_agent", this);
		
		if (m_ep.build_complete() == -1) begin
			`uvm_fatal("loopback_smoke_test", "tblink failed to complete build");
		end

	endfunction

	function void connect_phase(uvm_phase phase);
		if (m_ep.connect_complete() == -1) begin
			`uvm_fatal("loopback_smoke_test", "tblink failed to complete connect");
		end
	endfunction
	
	task run_phase(uvm_phase phase);
		$display("--> run_phase");
		phase.raise_objection(this, "Main", 1);
		phase.drop_objection(this, "Main", 1);
		$display("<-- run_phase");
	endtask
	
endclass


