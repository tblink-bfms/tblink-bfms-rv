'''
Created on Feb 27, 2022

@author: mballance
'''
from tblink_bfms_rv_tests.ep_io_bfm import EpIoBfm
import tblink_rpc
from tblink_rpc_gw.msg_base import MsgBase
from tblink_rpc_gw.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.test.test_backend_transport import TestBackendTransport


class EnvDrv(TestBackendTransport):
    
    def __init__(self):
        self.bfm2ctrl = None
        self.ctrl2bfm = None
        pass
    
    async def init(self):
        await tblink_rpc.cocotb_compat.init()
        self.bfm2ctrl = tblink_rpc.cocotb_compat.find_ifinst(".*u_bfm2ctrl")
        self.ctrl2bfm = tblink_rpc.cocotb_compat.find_ifinst(".*u_ctrl2bfm")
        pass
    
    async def send(self, pkt : MsgBase):
        await self.bfm2ctrl.send(pkt.pack())
        
    async def recv_b(self) -> int:
        return await self.ctrl2bfm.recv()
