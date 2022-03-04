'''
Created on Feb 27, 2022

@author: mballance
'''
import tblink_rpc
from tblink_bfms_rv_tests.ep_io_bfm import EpIoBfm

class TestBase(object):
    
    def __init__(self):
        self.bfm2ctrl = None
        self.ctrl2bfm = None
        pass
    
    async def init(self):
        await tblink_rpc.cocotb_compat.init()
        self.bfm2ctrl = tblink_rpc.cocotb_compat.find_ifinst(".*u_bfm2ctrl")
        self.ctrl2bfm = tblink_rpc.cocotb_compat.find_ifinst(".*u_ctrl2bfm")
        self.ep_bfm = EpIoBfm(self.bfm2ctrl, self.ctrl2bfm)
        pass
    
    async def run(self):
        pass