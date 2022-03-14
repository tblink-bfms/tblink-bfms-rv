
from enum import Enum, auto
from multiprocessing import Pipe
import traceback
from typing import List, Dict

import cocotb

import multiprocessing as mp
import rv_bfms
from tblink_bfms_rv_tests.syn import test_base
from tblink_bfms_rv_tests.syn.env_drv import EnvDrv
import tblink_rpc
from tblink_rpc_gw.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.msg_ctrl_factory import MsgCtrlFactory
import tblink_rpc_gw.test as gwt
from tblink_rpc import cocotb_compat


class SmokeTest(gwt.TestBase):
    
    def __init__(self):
        self._tp = None
        self._u_dut = None
    
    async def init(self):
        print("Smoke.init")
        await tblink_rpc.cocotb_compat.init()
        pass

    async def run(self):
        print("Smoke.run")
#        msg = MsgBfmCmd(1, 0 , 1, [1, 2, 3, 4])
#        await self.bfm2ctrl.send(msg.pack())
#        msg = MsgCtrlFactory.mkRelease(1)
#        await self.bfm2ctrl.send(msg.pack())
#        rsp = await self.ep_bfm.send(msg)

        for ifinst in cocotb_compat.ifinsts():
            print("InterfaceInst: %s" % str(ifinst))
            
        self._u_dut = tblink_rpc.cocotb_compat.find_ifinst(".*u_dut")
        self._u_dut._is_reset = True

        print("--> send")        
        await self._u_dut.send([1, 2, 3, 4])
        print("<-- send")        
            
        print("--> SLEEP")
        await cocotb.triggers.Timer(10, 'us')
        print("<-- SLEEP")
        print("--> SLEEP")
        await cocotb.triggers.Timer(10, 'us')
        print("<-- SLEEP")
#        await super().run()
        
    async def get_transport(self):
        if self._tp is None:
            # Perform initialization
            self._tp = EnvDrv()
            await self._tp.init()
        return self._tp
    
    def get_ifinst_info(self) -> List[Dict]:
        return [
            dict(name="smoke_initiator_tb.u_dut", addr=1, iftype="rv_bfms.initiator", is_mirror=False)
            ]
        
@cocotb.test()
async def entry(dut):
    print("Hello World")
    
    t = await SmokeTest.run_main(SmokeTest)
