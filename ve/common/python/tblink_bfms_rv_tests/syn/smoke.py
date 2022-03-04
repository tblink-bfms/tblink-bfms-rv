
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
import traceback

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
    ReqPktSend = auto()
    ReqPktRecv = auto()
    RspPkt = auto()
    Term = auto()
        
class Pkt(object):
    
    def __init__(self, kind, data=None, exc=None):
        self.kind = kind
        self.data = data
        self.exc = exc
        pass
    
    pass
        
def remote_process(remote_conn):
    # TOOD: remote process needs to tell the main process what it needs it
    # to do.
    # - Send packet
    # - Receive (and forward) packet
    #
    print("remote_process", flush=True)
    try:
        print("[0] --> Send SendPkt Req", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktSend, MsgCtrlFactory.mkGetTimeReq(0)))
        print("[0] <-- Send SendPkt Req", flush=True)
        
        print("[0] --> Recv SendPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("[0] <-- Recv SendPkt Resp", flush=True)
        
        print("[1] --> Send RecvPkt", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktRecv))
        print("[1] <-- Send RecvPkt", flush=True)
        
        print("[1] --> Recv RecvPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("[1] <-- Recv RecvPkt Resp", flush=True)
        print("[1] pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)

        # Set Timer
        print("[2] --> Send SendPkt Req", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktSend, MsgCtrlFactory.mkSetTimer(1, 1000)))
        print("[2] <-- Send SendPkt Req", flush=True)
        
        print("[2] --> Recv SendPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("[2] <-- Recv SendPkt Resp", flush=True)
        
        print("[3] --> Send RecvPkt", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktRecv))
        print("[3] <-- Send RecvPkt", flush=True)
        
        print("[3] --> Recv RecvPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("[3] <-- Recv RecvPkt Resp", flush=True)
        print("[3] pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
      
        print("--> Send SendPkt Req", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktSend, MsgCtrlFactory.mkRelease(2)))
        print("<-- Send SendPkt Req", flush=True)
        
        print("--> Recv SendPkt Rsp", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv SendPkt Rsp", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        print("--> Send RecvPkt", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktRecv))
        print("<-- Send RecvPkt", flush=True)
        
        print("--> Recv RecvPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv RecvPkt Resp", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        print("== Wait for wakeup")
        
        print("--> Send RecvPkt", flush=True)
        remote_conn.send(Pkt(PktKind.ReqPktRecv))
        print("<-- Send RecvPkt", flush=True)
        
        print("--> Recv RecvPkt Resp", flush=True)
        pkt = remote_conn.recv()
        print("<-- Recv RecvPkt Resp", flush=True)
        print("pkt: %s %s" % (str(pkt), str(pkt.data.pack())), flush=True)
        
        pass
        remote_conn.send(Pkt(PktKind.Term, exc=None))
    except Exception as e:
        traceback.print_exc()
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
        
        # States:
        # - Released
        #   - Wait for event back from hardware
        #   - 
        # - Waiting
        #   - Hardware is waitinf for message from EP
        #   - We must also wait for message from EP
        #   - Send received message, wait for response
        
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
                elif obj.kind == PktKind.ReqPktSend:
                    print("== PktKind.ReqPktSend")
                    pkt = obj.data
                    
                    await drv.bfm2ctrl.send(pkt.pack())
                    
                    this_conn.send(Pkt(PktKind.RspPkt, data=None))
                    
                elif obj.kind == PktKind.ReqPktRecv:
                    print("== PktKind.ReqPktRecv")

                    # TODO: need a message-decode loop here                    
                    
                    # Receive destination
                    dst = await drv.ctrl2bfm.recv()
                    
                    print("dst=%d" % dst)
                    
                    # Receive size
                    size = await drv.ctrl2bfm.recv()
                    size += 1
                    
                    print("size=%d" % size)

                    payload = []
                    for _ in range(size):
                        data = await drv.ctrl2bfm.recv()
                        payload.append(data)
                        print("data=%d" % data)
                        
                    rsp = MsgBfmCmd(0, payload[1], payload[0])
                    rsp.payload.extend(payload[2:])
                    
                    this_conn.send(Pkt(PktKind.RspPkt, data=rsp))
                else:
                    print("== Unknown request")
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
        
    