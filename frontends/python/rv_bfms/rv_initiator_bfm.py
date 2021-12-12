'''
Created on Nov 13, 2021

@author: mballance
'''
import tblink
import ctypes

@tblink.iftype("rv_bfms.initiator")
class RvInitiatorBfm(object):
    
    def __init__(self, ep, inst_name):
        pass

    @tblink.expfunc
    def req(self, data : ctypes.c_uint64):
        pass
    
    @tblink.impfunc
    def rsp(self):
        pass
    
    pass