'''
Created on Nov 13, 2021

@author: mballance
'''
import tblink_rpc
import ctypes

@tblink_rpc.iftype("rv_bfms.initiator")
class RvInitiatorBfm(object):
    
    def __init__(self):
        self.ev = tblink_rpc.event()
        
    async def send(self, data):
        self.ev.clear()
        print("--> self.req", flush=True)
        await self.req(data)
        print("<-- self.req", flush=True)
        
        if not self.ev.is_set():
            print("--> await", flush=True)
            await self.ev.wait()
            print("<-- await", flush=True)

    @tblink_rpc.exptask
    async def req(self, data : ctypes.c_uint64):
        pass
    
    @tblink_rpc.impfunc
    def rsp(self):
        print("--> rsp", flush=True)
        self.ev.set()
        print("<-- rsp", flush=True)
    
    pass