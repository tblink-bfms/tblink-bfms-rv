TBLINK_BFMS_RV_VE_COMMONDIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
TBLINK_BFMS_RVDIR:=$(abspath $(TBLINK_BFMS_RV_VE_COMMONDIR)/../..)
PACKAGES_DIR := $(TBLINK_BFMS_RVDIR)/packages
DV_MK:=$(shell PATH=$(PACKAGES_DIR)/python/bin:$(PATH) python3 -m mkdv mkfile)

ifneq (1,$(RULES))

MKDV_PYTHONPATH += $(TBLINK_BFMS_RV_VE_COMMONDIR)/python

include $(DV_MK)
else # Rules
include $(DV_MK)

endif

