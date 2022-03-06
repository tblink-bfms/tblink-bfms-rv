
import cocotb
import tblink_rpc
import rv_bfms
from tblink_rpc_gw.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.msg_ctrl_factory import MsgCtrlFactory
import multiprocessing as mp
from multiprocessing import Pipe
from enum import Enum, auto
from tblink_bfms_rv_tests.syn.env_drv import EnvDrv
import traceback
from tblink_bfms_rv_tests.syn import test_base
import tblink_rpc_gw.test as gwt

class SmokeTest(gwt.TestBase):
    
    def __init__(self):
        self._tp = None
    
    async def init(self):
        print("Smoke.init")
        await tblink_rpc.cocotb_compat.init()
        pass

    async def run(self):
        msg = MsgBfmCmd(1, 0 , 1, [1, 2, 3, 4])
        await self.bfm2ctrl.send(msg.pack())
        msg = MsgCtrlFactory.mkRelease(1)
        await self.bfm2ctrl.send(msg.pack())
#        rsp = await self.ep_bfm.send(msg)
        await cocotb.triggers.Timer(10, 'us')
        await super().run()
        
    async def get_transport(self):
        if self._tp is None:
            # Perform initialization
            self._tp = EnvDrv()
            await self._tp.init()
        return self._tp
        
@cocotb.test()
async def entry(dut):
    print("Hello World")
    
    t = await SmokeTest.run_main(SmokeTest)
