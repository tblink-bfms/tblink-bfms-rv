/****************************************************************************
 * rv_initiator_driver.svh
 ****************************************************************************/

/**
 * Class: rv_initiator_driver
 * 
 * TODO: Add class documentation
 */
class rv_initiator_driver #(int WIDTH=32) extends uvm_component;
	IInterfaceInst				m_ifinst;
	rv_initiator_bfm_impl #(WIDTH)          m_impl;
	semaphore								m_rsp_s = new(0);

	function new(string name, uvm_component parent);
		super.new(name, parent);
	endfunction
	
	// Public API
	task send(bit[WIDTH-1:0] data);
		m_impl.req(data);
		m_rsp_s.get(1);
	endtask

	// TODO: shouldn't need this
	virtual function void req(int unsigned data);
	endfunction
	
	// Implementation
	virtual function void rsp();
		m_rsp_s.put(1);
	endfunction
	
	function void build_phase(uvm_phase phase);
		string ifinst_path;
		IEndpoint	   ep;
		IInterfaceType iftype;
		IInterfaceInst ifinst;
		
		$display("rv_initiator_driver build phase");

		if (!uvm_config_db #(IEndpoint)::get(this, "", "IEndpoint", ep)) begin
			`uvm_fatal("rv_initiator_driver", "No endpoint registered");
			return;
		end
		
		if (!uvm_config_db #(string)::get(this, "", "IInterfaceInst", ifinst_path)) begin
			`uvm_fatal("rv_initiator_driver", "No interface path specified");
			return;
		end
		
		iftype = rv_initiator_bfm_impl #(WIDTH)::define_type(ep);
		
		m_impl = new(this);
		
		ifinst = ep.defineInterfaceInst(
				iftype,
				ifinst_path,
				1,
				m_impl);
		
	endfunction


endclass


