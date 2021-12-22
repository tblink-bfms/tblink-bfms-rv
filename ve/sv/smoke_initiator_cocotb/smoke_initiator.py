import tblink_rpc_cocotb
import cocotb
import rv_bfms

@cocotb.test()
async def entry(dut):
    await tblink_rpc_cocotb.init()
    
    rv_bfm = tblink_rpc_cocotb.find_ifinst(".*u_bfm")
    
    for i in range(10):
        await rv_bfm.send(i)
    

