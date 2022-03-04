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
        self._req_f = None
        self._req_q = []
        self._req_ev = tblink_rpc.event()
        
    async def recv(self):
        while len(self._req_q) == 0:
            await self._req_ev.wait()
            self._req_ev.clear()
        return self._req_q.pop(0)
        
    def set_req_f(self, req_f):
        self._req_f = req_f
        
    @tblink_rpc.impfunc
    def _req(self, data : ctypes.c_uint64):
        if self._req_f is not None:
            self._req_f(data)
        else:
            self._req_q.append(data)
            self._req_ev.set()
    
    @tblink_rpc.exptask
    async def _rsp(self):
        pass
        
    @tblink_rpc.impfunc
    def _reset(self):
        self._is_reset = True
        self._reset_ev.set()

