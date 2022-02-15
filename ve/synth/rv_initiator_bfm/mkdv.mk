MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
SYNTH_DIR:=$(dir $(MKDV_MK))
MKDV_TOOL ?= openlane
#TBLINK_RPC_UVM_FILES := $(shell python3 -m tblink_rpc_hdl files sv-uvm)
#TBLINK_RPC_UVM_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin)

#DPI_LIBS += $(TBLINK_RPC_UVM_PLUGIN)
#MKDV_BUILD_DEPS += gen-bfms
#MKDV_VL_SRCS += $(TBLINK_RPC_UVM_FILES)
MKDV_VL_SRCS += $(SYNTH_DIR)/../../../backends/rv_initiator_bfm_syn.v
MKDV_VL_SRCS += $(SYNTH_DIR)/../../../packages/tblink-rpc-gw/verilog/rtl/tblink_rpc_ep.v
MKDV_VL_SRCS += $(SYNTH_DIR)/../../../packages/tblink-rpc-gw/verilog/rtl/tblink_rpc_rvdemux.v
MKDV_VL_SRCS += $(SYNTH_DIR)/../../../packages/tblink-rpc-gw/verilog/rtl/tblink_rpc_rvmux.v
MKDV_VL_SRCS += $(SYNTH_DIR)/../../../packages/fw-rv-comps/verilog/rtl/fw_rv_buffer.v
TOP_MODULE=rv_initiator_bfm_syn

#MKDV_RUN_ARGS += +tblink.launch=sv.loopback +UVM_TESTNAME=smoke_uvm_test


include $(SYNTH_DIR)/../../common/defs_rules.mk

RULES := 1

include $(SYNTH_DIR)/../../common/defs_rules.mk

$(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sv.sv : gen-bfms

.PHONY: gen-bfms
gen-bfms: 
	$(Q)$(PACKAGES_DIR)/python/bin/python3 -m tblink_bfms gen \
		-o bfm $(TBLINK_BFMS_RVDIR)/rv_bfms.yaml \
		$(TBLINK_BFMS_RVDIR)/frontends \
		$(TBLINK_BFMS_RVDIR)/backends


