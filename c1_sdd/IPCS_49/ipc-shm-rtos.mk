#
# IPC Shared Memory Driver - Makefile
#
# Copyright 2018-2023 NXP
# All Rights Reserved.
#
# NXP Confidential. This software is owned or controlled by NXP and may only be
# used strictly in accordance with the applicable license terms. By expressly
# accepting such terms or by downloading, installing, activating and/or otherwise
# using the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to be
# bound by the applicable license terms, then you may not retain, install,
# activate or otherwise use the software.

# List of supported OS targets
shm_os_targets := autosar freertos baremetal zephyr xos

# List of supported platforms from ipc-hw
shm_platforms := s32gen1 s32g3xx \
                    s32k3xx s32k396 s32k358 s32k388\
                    s32r41 saf85xx \
                    s32ze \
                    s32n

# Platform and OS target check
shm_platforms := $(strip $(shm_platforms))
shm_os_targets := $(strip $(shm_os_targets))

ifeq ($(filter-out $(SHM_PLATFORM),$(shm_platforms)),$(shm_platforms))
    $(info Supported platforms: $(shm_platforms))
    $(error Undefined platform SHM_PLATFORM = '$(SHM_PLATFORM)')
endif
ifeq ($(filter-out $(SHM_OS_TARGET),$(shm_os_targets)),$(shm_os_targets))
    $(info Supported OS targets: $(shm_os_targets))
    $(error Undefined OS target SHM_OS_TARGET = '$(SHM_OS_TARGET)')
endif

# SHM_DRIVER_PATH check
ifeq (,$(SHM_DRIVER_PATH))
    $(error Environment variable SHM_DRIVER_PATH not set)
endif
ifneq (1,$(words [$(SHM_DRIVER_PATH)]))
    $(error Spaces are not allowed in SHM_DRIVER_PATH)
endif

# Driver includes
SHM_DRIVER_INCLUDES_DIRS := $(SHM_DRIVER_PATH)/src/common \
                            $(SHM_DRIVER_PATH)/src/hw     \
                            $(SHM_DRIVER_PATH)/src/os

# Driver sources lookup paths
SHM_DRIVER_SRC_DIR := $(SHM_DRIVER_PATH)/src/common \
                      $(SHM_DRIVER_PATH)/src/hw/$(SHM_PLATFORM) \
                      $(SHM_DRIVER_PATH)/src/os/$(SHM_OS_TARGET)

SHM_DRIVER_INCLUDE_FILES := \
        $(foreach path, $(SHM_DRIVER_INCLUDES_DIRS),$(wildcard $(path)/*.h))

SHM_DRIVER_SOURCE_FILES := $(foreach path,$(SHM_DRIVER_SRC_DIR),$(wildcard $(path)/*.c))

SHM_DRIVER_OUT_FILES := $(subst .c,.o,$(SHM_DRIVER_SOURCE_FILES))
