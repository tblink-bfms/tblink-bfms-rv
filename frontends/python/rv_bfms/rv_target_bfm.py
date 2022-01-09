'''
Created on Nov 13, 2021

@author: mballance
'''
import tblink_rpc
import ctypes

@tblink_rpc.iftype("rv_bfms.target")
class RvTargetBfm(object):
    
    def __init__(self):
        self.ev = tblink_rpc.event()
        self._is_reset = False
        self._reset_ev = tblink_rpc.event()
        
    # async def send(self, data):
    #
    #     if not self._is_reset:
    #         await self._reset_ev.wait()
    #
    #     self.ev.clear()
    #     print("--> self.req", flush=True)
    #     await self.req(data)
    #     print("<-- self.req", flush=True)
    #
    #     if not self.ev.is_set():
    #         print("--> await", flush=True)
    #         await self.ev.wait()
    #         print("<-- await", flush=True)

    @tblink_rpc.impfunc
    async def _req(self, data : ctypes.c_uint64):
        pass
    
    @tblink_rpc.exptask
    def _rsp(self):
        pass
        
    @tblink_rpc.impfunc
    def _reset(self):
        self._is_reset = True
        self._reset_ev.set()
    pass