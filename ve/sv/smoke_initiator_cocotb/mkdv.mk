MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
TEST_DIR:=$(dir $(MKDV_MK))
PACKAGES_DIR := $(abspath $(TEST_DIR)/../../../packages)
MKDV_TOOL ?= questa
TBLINK_RPC_UVM_FILES := $(shell python3 -m tblink_rpc_hdl files sv)
TBLINK_RPC_UVM_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin)

MKDV_PLUGINS += cocotb

MKDV_PYTHONPATH += $(TEST_DIR) $(abspath $(TEST_DIR)/../../../frontends/python)
MKDV_COCOTB_MODULE = smoke_initiator

DPI_LIBS += $(TBLINK_RPC_UVM_PLUGIN)
VPI_LIBS += $(TBLINK_RPC_UVM_PLUGIN)
MKDV_BUILD_DEPS += gen-bfms
MKDV_VL_SRCS += $(TBLINK_RPC_UVM_FILES)
MKDV_VL_INCDIRS += $(sort $(dir $(TBLINK_RPC_UVM_FILES)))
MKDV_VL_SRCS += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sv.sv
MKDV_VL_SRCS += $(TEST_DIR)/smoke_initiator_tb.sv
TOP_MODULE=smoke_initiator_tb

VLSIM_CLKSPEC += clock=10ns
VLSIM_OPTIONS += -Wno-fatal

MKDV_RUN_ARGS += +tblink.launch=native.loopback 


include $(TEST_DIR)/../../common/defs_rules.mk

RULES := 1

include $(TEST_DIR)/../../common/defs_rules.mk

$(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sv.sv : gen-bfms

.PHONY: gen-bfms
gen-bfms: 
	$(Q)$(PACKAGES_DIR)/python/bin/python3 -m tblink_bfms gen \
		-o bfm $(TBLINK_BFMS_RVDIR)/rv_bfms.yaml \
		$(TBLINK_BFMS_RVDIR)/frontends \
		$(TBLINK_BFMS_RVDIR)/backends


