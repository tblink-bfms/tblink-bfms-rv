import cocotb
import rv_bfms
from tblink_rpc_core.tblink import TbLink
from tblink.impl.iftype_rgy import IftypeRgy
import traceback


@cocotb.test()
async def entry(dut):
    print("entry", flush=True)
    tblink = TbLink.inst()
    
    def mk_ev():
        return cocotb.triggers.Event()
    
    tblink.mk_ev = mk_ev
    
    from cocotb import scheduler
    event_loop_orig = scheduler._event_loop
    def new_event_loop(self):
        nonlocal event_loop_orig
        print("--> new_event_loop")
        event_loop_orig(self)
        print("<-- new_event_loop")
        
    print("scheduler=%s" % str(scheduler))
    scheduler._event_loop = new_event_loop

    # Don't know precisely the order in 
    # which Cocotb and TbLink will be loaded.
    #
    # Spin for a few deltas waiting for the
    # default endpoint to register
    for i in range(16):
        dflt = tblink.getDefaultEP()
        if dflt is not None:
            print("Python: Found default EP", flush=True)
            break
        else:
            print("Python: Waiting for default EP", flush=True)
            await cocotb.triggers.Timer(0, 'ns')

    print("Python: dflt=%s" % str(dflt), flush=True)

    # >> User calls library 'init'

    # TODO: Use 'launcher' to connect to the existing endpoint
    launcher = tblink.findLaunchType("connect.native.loopback")
    params = launcher.newLaunchParams()
    ep,err = launcher.launch(params)
    
    if ep is None:
        raise Exception("Failed to connect: %s" % err)
    
    ep.init()
    
    ev = cocotb.triggers.Event()
    
    def event_l(e):
        nonlocal ev
        print("Python Main: event %s" % str(ev))
        ev.set()
    
    l = ep.addListener(event_l)

    print("--> Python is_init")
    while True:
        ret = ep.is_init()
        
        if ret == 1:
            break
        elif ret == -1:
            raise Exception("Failed during init")
        else:
            print("--> init: ev.wait")
            await ev.wait()
            ev.clear()
            print("<-- init: ev.wait")
    print("<-- Python is_init")
            

    # TODO: Register BFM types with the endpoint

    # TODO: not the best name...    
    IftypeRgy.inst().endpoint_added(ep)
    
    
    print("Registered Types")
    for iftype in ep.getInterfaceTypes():
        print("iftype: %s" % iftype.name())

    # TODO: Complete build stage. This ensures we know about all peer-registered instances
    if ep.build_complete() == -1:
        raise Exception("Build-complete failed")
    
    for _ in range(10):
        print("--> is_build_complete", flush=True)
        code = ep.is_build_complete()
        print("<-- is_build_complete %d" % code, flush=True)
        if code == 0:
            print("--> process_one_message_a: is_build_complete")
            await ev.wait()
            ev.clear()
            print("<-- process_one_message_a: is_build_complete")
#            await cocotb.triggers.Timer(0, 'ns')
#            ep.add_time_callback(0, delta_cb)
#            await ev.wait()
#            ev.clear()
#            ep.process_one_message()
        elif code == -1:
            raise Exception("Is-build-complete failed")
        else:
            break
        
    if ep.is_build_complete() != 1:
        raise Exception("Time-out during is-build-complete")
    else:
        print("Python BUILD_COMPLETE")
    
    # << User calls library 'init'

    # At this point, we know what BFMs exist in the HDL environment
    # Use the Python facade to construct user-specified classes
    bfms = IftypeRgy.inst().build_bfms(ep)

    try:
        print("--> bfms (%s)" % str(bfms))
        for b in bfms:
            print("BFM: %s" % b.inst_name())
        print("<-- bfms (%s)" % str(bfms))
    except Exception as e:
        print("Exception: %s" % str(e))
        
    bfm = bfms[0]
            
    
    # inst_name = ""
    # for ifinst in ep.getPeerInterfaceInsts():
    #     print("ifinst: %s" % ifinst.name())
    #     if ifinst.name().endswith(".u_bfm"):
    #         inst_name = ifinst.name()
    #         break
    #
    #
    # def req_f(*args):
    #     print("req_f: %s" % str(args))
    #
    # iftype = ep.findInterfaceType("rv_bfms.initiator")
    # ifinst = ep.defineInterfaceInst(
    #     iftype,
    #     inst_name,
    #     True,
    #     req_f)
    #
    # print("ifinst: %s" % str(ifinst))

    # >> User code

    # TODO: User needs to create BFM instances. Maybe based on peer-registered instances?

    # << User code

    # >> User calls library 'complete'

    # TODO: Complete connection stage. Only really used for validation. 
    print("--> Python connect_complete")
    if ep.connect_complete() == -1:
        raise Exception("Connect-complete failed")
    print("<-- Python connect_complete")
    
    while True:
        print("--> is_connect_complete", flush=True)
        code = ep.is_connect_complete()
        print("<-- is_connect_complete %d" % code, flush=True)
        if code == 0:
            print("--> process_one_message_a: is_connect_complete")
            await ev.wait()
            ev.clear()
#            await ep.process_one_message_a()
            print("<-- process_one_message_a: is_connect_complete")
#            await cocotb.triggers.Timer(0, 'ns')
#            ep.process_one_message()
        elif code == -1:
            raise Exception("Is-connect-complete failed")
        else:
            break

    # << User calls library 'complete'
    
    for i in range(10):
        await bfm.send(i)
        

    # req_m = iftype.findMethod("req")
    #
    # invoke_ev = cocotb.triggers.Event()
    # def invoke_ack(rval):
    #     nonlocal invoke_ev
    #     print("invoke_ack", flush=True)
    #     invoke_ev.set()
    #
    # for i in range(10):   
    #     params = ifinst.mkValVec()
    #     params.push_back(ifinst.mkValIntU(i, 32))
    #
    #     print("--> invoke_nb(%d)" % i, flush=True)
    #     ifinst.invoke_nb(req_m, params, invoke_ack)
    #     print("<-- invoke_nb(%d)" % i, flush=True)
    #
    #     print("--> wait_ack", flush=True)
    #     await invoke_ev.wait()
    #     invoke_ev.clear()
    #     print("<-- wait_ack", flush=True)
    #
    #     await cocotb.triggers.Timer(100, "ns")
    #
    # for ifinst in dflt.getInterfaceInsts():
    #     pass
    #

    print("--> wait 10ns", flush=True)
    await cocotb.triggers.Timer(10, "ns")
    print("<-- wait 10ns", flush=True)
#    ifinst = dflt.findInterfaceInst(
    pass


