'''
Created on Feb 27, 2022

@author: mballance
'''
from enum import Enum, auto
import multiprocessing as mp
from multiprocessing import Pipe
import traceback

from tblink_bfms_rv_tests.ep_io_bfm import EpIoBfm
from tblink_bfms_rv_tests.syn.env_drv import EnvDrv
import tblink_rpc
from tblink_rpc_gw.msg_bfm_cmd import MsgBfmCmd
from tblink_rpc_gw.msg_ctrl_factory import MsgCtrlFactory


class TestBase(object):
    
    def __init__(self):
        self._tp = None
        pass
    
    async def init(self):
        await tblink_rpc.cocotb_compat.init()
        pass
    
    async def run(self):
        pass
    
    async def get_transport(self):
        if self._tp is None:
            # Perform initialization
            self._tp = EnvDrv()
            await self._tp.init()
        return self._tp
    
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
    
remote_proc = None

def remote_process(remote_conn):
    global remote_proc
    # TOOD: remote process needs to tell the main process what it needs it
    # to do.
    # - Send packet
    # - Receive (and forward) packet
    #
    print("remote_process (remote_proc=%s)" % (str(remote_proc)), flush=True)
    
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

async def run(T):
    global remote_proc
    
    t = T()
    
    
    if remote_proc is not None:
        # Running in a remote proc, so this is the real test
        
        await t.init()
        await t.run()
    else: # Base process: connect to testbench BFMs
        
        tp = await t.get_transport()
        
        remote_conn, this_conn = Pipe()
        remote_proc = mp.Process(target=remote_process, args=(remote_conn,))
    
        remote_proc.start()        
        
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
                    
                    await tp.send(pkt)
                    
                    this_conn.send(Pkt(PktKind.RspPkt, data=None))
                    
                elif obj.kind == PktKind.ReqPktRecv:
                    print("== PktKind.ReqPktRecv")

                    rsp = await tp.recv()
                    
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
    