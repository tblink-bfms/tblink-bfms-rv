import rv_bfms
from tblink_rpc.component import Component
import tblink_rpc
from tblink_rpc import TimeUnit

class test(Component):
    
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.u_bfm = None
        pass
    
    def connect(self, ep):
        print("connect", flush=True)
        ifinst = self._backend.findPeerIfinst(".*u_bfm")
        print("ifinst: %s" % str(ifinst))
        
        self.u_bfm = self.mkMirrorInst(rv_bfms.RvInitiatorBfm, ifinst.name())
        
        
    async def run(self):
        self.raise_objection()
        print("run")
       
        for i in range(10):
            print("--> send", flush=True)
            await self.u_bfm.send(i+1)
            print("<-- send", flush=True)
        
#        await tblink_rpc.sleep(10, TimeUnit.ns)
        self.drop_objection()

    

