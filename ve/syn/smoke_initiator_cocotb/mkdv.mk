MKDV_MK:=$(abspath $(lastword $(MAKEFILE_LIST)))
TEST_DIR:=$(dir $(MKDV_MK))
PACKAGES_DIR := $(abspath $(TEST_DIR)/../../../packages)
MKDV_TOOL ?= questa

ifeq (icarus,$(MKDV_TOOL))
  TBLINK_RPC_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin vpi)
  BFM_FILES += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sim_vl.sv
  BFM_FILES += $(MKDV_CACHEDIR)/bfm/backends/rv_target_bfm_sim_vl.sv
  VPI_LIBS += $(TBLINK_RPC_PLUGIN)
  FILESPEC = $(TEST_DIR)/filespec_vl.yaml
else
  TBLINK_RPC_PLUGIN := $(shell python3 -m tblink_rpc_hdl simplugin dpi)
  TBLINK_RPC_SV_FILES := $(shell python3 -m tblink_rpc_hdl files sv)
  DPI_LIBS += $(TBLINK_RPC_PLUGIN)
  FILESPEC = $(TEST_DIR)/filespec_sv.yaml
  MKDV_VL_SRCS += $(TBLINK_RPC_SV_FILES)
  MKDV_VL_INCDIRS += $(sort $(dir $(TBLINK_RPC_SV_FILES)))
  BFM_FILES += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_sim_sv.sv
  BFM_FILES += $(MKDV_CACHEDIR)/bfm/backends/rv_target_bfm_sim_sv.sv
endif

BFM_FILES += $(MKDV_CACHEDIR)/bfm/backends/rv_initiator_bfm_syn.v

MKDV_PYTHONPATH += $(TEST_DIR) $(abspath $(TEST_DIR)/../../../frontends/python)

MKDV_BUILD_DEPS += gen-bfms
#MKDV_VL_SRCS += $(TEST_DIR)/smoke_initiator_tb.sv
TOP_MODULE=smoke_initiator_tb

VLSIM_CLKSPEC += clock=10ns
VLSIM_OPTIONS += -Wno-fatal

MKDV_RUN_ARGS += +tblink.launch=python.loopback 
MKDV_RUN_ARGS += +module=tblink_rpc.rt.cocotb

MODULE = tblink_bfms_rv_tests.syn.smoke
export MODULE

include $(TEST_DIR)/../../common/defs_rules.mk
include $(MKDV_CACHEDIR)/files.mk
MKDV_VL_SRCS += $(BFM_FILES)

RULES := 1

include $(TEST_DIR)/../../common/defs_rules.mk

$(MKDV_CACHEDIR)/files.mk : $(FILESPEC)
	$(Q)mkdir -p `dirname $@`
	$(Q)$(PACKAGES_DIR)/python/bin/python3 -m mkdv filespec \
		$^ -t mk -o $@

$(BFM_FILES) : gen-bfms

.PHONY: gen-bfms
gen-bfms: 
	$(Q)$(PACKAGES_DIR)/python/bin/python3 -m tblink_bfms gen \
		-o bfm $(TBLINK_BFMS_RVDIR)/rv_bfms.yaml \
		$(TBLINK_BFMS_RVDIR)/frontends \
		$(TBLINK_BFMS_RVDIR)/backends


