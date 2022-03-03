
import cocotb
import tblink_rpc
import rv_bfms
from tblink_bfms_rv_tests.syn.test_base import TestBase
from tblink_rpc_gw.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.msg_ctrl_factory import MsgCtrlFactory
import multiprocessing as mp
from multiprocessing import Pipe
from enum import Enum, auto
from tblink_bfms_rv_tests.syn.env_drv import EnvDrv

class SmokeTest(TestBase):

    async def run(self):
        msg = MsgBfmCmd(1, 0 , 1, [1, 2, 3, 4])
        await self.bfm2ctrl.send(msg.pack())
        msg = MsgCtrlFactory.mkRelease(1)
        await self.bfm2ctrl.send(msg.pack())
#        rsp = await self.ep_bfm.send(msg)
        await cocotb.triggers.Timer(10, 'us')
        await super().run()
        
class PktKind(Enum):
    Data = auto()
    Term = auto()
        
class Pkt(object):
    
    def __init__(self, kind, data=None, exc=None):
        self.kind = kind
        self.data = data
        self.exc = exc
        pass
    
    pass
        
def remote_process(remote_conn):
    print("remote_process", flush=True)
    try:
        print("--> Send Pkt", flush=True)
        remote_conn.send(Pkt(PktKind.Data, MsgCtrlFactory.mkGetTimeReq(0)))
        print("<-- Send Pkt", flush=True)
        
        print("--> Recv Pkt", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv Pkt", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        print("--> Send Pkt", flush=True)
        remote_conn.send(Pkt(PktKind.Data, MsgCtrlFactory.mkSetTimer(1, 1000)))
        print("<-- Send Pkt", flush=True)
        
        print("--> Recv Pkt", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv Pkt", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        print("--> Send Pkt", flush=True)
        remote_conn.send(Pkt(PktKind.Data, MsgCtrlFactory.mkRelease(2)))
        print("<-- Send Pkt", flush=True)
        
        print("--> Recv Pkt", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv Pkt", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        pass
        remote_conn.send(Pkt(PktKind.Term, exc=None))
    except Exception as e:
        remote_conn.send(Pkt(PktKind.Term, exc=e))
        
remote_proc = None

def atexit_cleanup(proc):
    print("atexit_cleanup")

@cocotb.test()
async def entry(dut):
    print("Hello World")
    
    condition = False
   
    # If condition is true, then we're running the 
    # actual test code (in a separate process)
    if condition:
        t = SmokeTest()
        
        await t.init()
        await t.run()
        
    else:
        global remote_proc
        import atexit
        drv = EnvDrv()
        
        await drv.init()
        
        # TODO: Need to create and run a remote cocotb
        remote_conn, this_conn = Pipe()
        remote_proc = mp.Process(target=remote_process, args=(remote_conn,))
    
        remote_proc.start()
        
        atexit.register(atexit_cleanup, remote_proc)
        
        while True:
            print("--> poll", flush=True)
            ret = this_conn.poll(1)
            print("<-- poll", flush=True)
            
            print("ret=%s" % str(ret))
            
            if ret:
                obj = this_conn.recv()
                
                if obj.kind == PktKind.Term:
                    print("Got term")
                    break
                elif obj.kind == PktKind.Data:
                    # Send/Recv data
                    print("--> Send to BFM", flush=True)
                    print("obj.data=%s obj.data.pack=%s" % (str(obj.data), str(obj.data.pack())))
                    rsp = await drv.ep_bfm.send(obj.data)
                    print("<-- Send to BFM", flush=True)
                    print("--> Send to Remote", flush=True)
                    this_conn.send(Pkt(PktKind.Data, data=rsp))
                    print("<-- Send to Remote", flush=True)
            else:
                if not remote_proc.is_alive():
                    print("Process closed")
                    break
                else:
                    print("Process running")
        
        remote_proc.join()
        
        # TODO: poll pipe and interact with remote
        pass


    # Start remote-service code
    
    # Wait for remote to complete
        
    