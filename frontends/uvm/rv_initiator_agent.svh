/****************************************************************************
 * rv_initiator_agent.svh
 ****************************************************************************/

typedef class rv_initiator_driver;
  
/**
 * Class: rv_initiator_agent
 * 
 * TODO: Add class documentation
 */
class rv_initiator_agent #(int WIDTH=32) extends uvm_component;
	`uvm_component_utils(rv_initiator_agent)
	
	rv_initiator_driver #(WIDTH)				m_driver;

	function new(string name, uvm_component parent);
		super.new(name, parent);
	endfunction
	
	function void build_phase(uvm_phase phase);
		m_driver = new("m_driver", this);
	endfunction
	
	function void connect_phase(uvm_phase phase);
	endfunction

endclass


