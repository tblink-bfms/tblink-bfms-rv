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
        self._is_reset = False
        self._reset_ev = tblink_rpc.event()
        
    async def send(self, data):
        print("send: %s" % str(data))
        
        if not self._is_reset:
            await self._reset_ev.wait()
            
        if not isinstance(data, list):
            data = [data]

        i = 0
        while i < len(data):
            self.ev.clear()
            
            if i == 0 and len(data) > 1:
                # Send two values initially
                print("--> Calling _req2", flush=True)
                await self._req2(data[i], data[i+1])
                print("<-- Calling _req2", flush=True)
                i += 1
            else:
                await self._req(data[i])
                
            if not self.ev.is_set():
                print("--> await", flush=True)
                await self.ev.wait()
                self.ev.clear()
                print("<-- await", flush=True)
                
            i += 1
                
        if len(data) > 1:
            await self.ev.wait()
            self.ev.clear()
            

    @tblink_rpc.exptask
    async def _req(self, data : ctypes.c_uint64):
        print("_req called")
        pass
    
    @tblink_rpc.exptask
    async def _req2(self, 
                    data1 : ctypes.c_uint64,
                    data2 : ctypes.c_uint64):
        print("_req2 called")
        pass
    
    @tblink_rpc.impfunc
    def _rsp(self):
        print("--> rsp", flush=True)
        self.ev.set()
        print("<-- rsp", flush=True)
        
    @tblink_rpc.impfunc
    def _reset(self):
        self._is_reset = True
        self._reset_ev.set()
    
    pass