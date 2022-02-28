
import cocotb
import tblink_rpc
import rv_bfms
from tblink_bfms_rv_tests.syn.test_base import TestBase
from tblink_rpc_gw.transport.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.transport.msg_ctrl_factory import MsgCtrlFactory

class SmokeTest(TestBase):

    async def run(self):
        msg = MsgBfmCmd(1, 0 , 1, [1, 2, 3, 4])
        await self.bfm2ctrl.send(msg.pack())
        msg = MsgCtrlFactory.mkRelease(1)
        await self.bfm2ctrl.send(msg.pack())
#        rsp = await self.ep_bfm.send(msg)
        await cocotb.triggers.Timer(10, 'us')
        await super().run()

@cocotb.test()
async def entry(dut):
    print("Hello World")
    t = SmokeTest()
    await t.init()
    await t.run()
    