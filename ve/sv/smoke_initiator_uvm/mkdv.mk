MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
TEST_DIR:=$(dir $(MKDV_MK))
MKDV_TOOL ?= questa
TBLINK_RPC_UVM_FILES := $(shell python3 -m tblink_rpc_hdl files sv-uvm)
TBLINK_RPC_UVM_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin)

DPI_LIBS += $(TBLINK_RPC_UVM_PLUGIN)
MKDV_BUILD_DEPS += gen-bfms
MKDV_VL_SRCS += $(TBLINK_RPC_UVM_FILES)
MKDV_VL_SRCS += $(MKDV_CACHEDIR)/bfm/frontends/uvm/rv_agent_pkg.sv
MKDV_VL_SRCS += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sv.sv
MKDV_VL_SRCS += $(TEST_DIR)/smoke_uvm_pkg.sv
MKDV_VL_SRCS += $(TEST_DIR)/smoke_uvm_tb.sv
TOP_MODULE=smoke_uvm_tb

MKDV_RUN_ARGS += +tblink.launch=sv.loopback +UVM_TESTNAME=smoke_uvm_test


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


