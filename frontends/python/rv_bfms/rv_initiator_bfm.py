'''
Created on Nov 13, 2021

@author: mballance
'''
import tblink
import ctypes

@tblink.iftype("rv_bfms.initiator")
class RvInitiatorBfm(object):
    
    def __init__(self):
        self.ev = tblink.Event()
        
    async def send(self, data):
        self.ev.clear()
        await self.req(data)
        
        if not self.ev.is_set():
            print("--> await")
            await self.ev.wait()
            print("<-- await")

    @tblink.exptask
    async def req(self, data : ctypes.c_uint64):
        pass
    
    @tblink.imptask
    async def rsp(self):
        print("--> rsp")
        self.ev.set()
        print("<-- rsp")
    
    pass