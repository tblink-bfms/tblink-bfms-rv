MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
TEST_DIR:=$(dir $(MKDV_MK))
PACKAGES_DIR := $(abspath $(TEST_DIR)/../../../packages)
MKDV_TOOL ?= questa

ifeq (icarus,$(MKDV_TOOL))
  TBLINK_RPC_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin vpi)
  MKDV_VL_SRCS += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_vl.sv
else
  TBLINK_RPC_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin dpi)
  TBLINK_RPC_SV_FILES := $(shell python3 -m tblink_rpc_hdl files sv)
  DPI_LIBS += $(TBLINK_RPC_PLUGIN)
  MKDV_VL_SRCS += $(TBLINK_RPC_SV_FILES)
  MKDV_VL_INCDIRS += $(sort $(dir $(TBLINK_RPC_SV_FILES)))
  MKDV_VL_SRCS += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sv.sv
endif
VPI_LIBS += $(TBLINK_RPC_PLUGIN)

#MKDV_PLUGINS += cocotb

MKDV_PYTHONPATH += $(TEST_DIR) $(abspath $(TEST_DIR)/../../../frontends/python)
MKDV_COCOTB_MODULE = smoke_initiator

MKDV_BUILD_DEPS += gen-bfms
MKDV_VL_SRCS += $(TEST_DIR)/smoke_initiator_tb.sv
TOP_MODULE=smoke_initiator_tb

VLSIM_CLKSPEC += clock=10ns
VLSIM_OPTIONS += -Wno-fatal

#MKDV_RUN_ARGS += +tblink.launch=python.socket 
MKDV_RUN_ARGS += +tblink.launch=python.loopback 
MKDV_RUN_ARGS += +tblink.param+module=tblink_rpc.rt
MKDV_RUN_ARGS += +tblink.param+python=$(PACKAGES_DIR)/python/bin/python3
MKDV_RUN_ARGS += +tblink.class=smoke_initiator.test


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


