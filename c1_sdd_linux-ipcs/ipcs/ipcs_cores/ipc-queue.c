/**
 * IPC Shared Memory Driver - queue implementation
 *
 * Copyright 2018-2019,2022-2023 NXP
 * All Rights Reserved.
 *
 * NXP Confidential. This software is owned or controlled by NXP and may only be
 * used strictly in accordance with the applicable license terms. By expressly
 * accepting such terms or by downloading, installing, activating and/or otherwise
 * using the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to be
 * bound by the applicable license terms, then you may not retain, install,
 * activate or otherwise use the software.
 */
#if defined(__cplusplus)
extern "C"{
#endif

#include "ipc-shm.h"
#include "ipc-queue.h"
#include "ipc-util.h"

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_QUEUE_VENDOR_ID_C                    43
#define IPC_QUEUE_AR_RELEASE_MAJOR_VERSION_C     4
#define IPC_QUEUE_AR_RELEASE_MINOR_VERSION_C     7
#define IPC_QUEUE_AR_RELEASE_REVISION_VERSION_C  0
#define IPC_QUEUE_SW_MAJOR_VERSION_C             4
#define IPC_QUEUE_SW_MINOR_VERSION_C             0
#define IPC_QUEUE_SW_PATCH_VERSION_C             1

/*
 * FILE VERSION CHECKS
 */
/* Check if ipc-queue.c file and ipc-shm.h file are of the same vendor */
#if (IPC_QUEUE_VENDOR_ID_C != IPC_SHM_VENDOR_ID)
	#error "ipc-queue.c and ipc-shm.h have different vendor IDs"
#endif
/* Check if ipc-queue.c file and ipc-shm.h file are of the same Autosar version */
#if ((IPC_QUEUE_AR_RELEASE_MAJOR_VERSION_C != IPC_SHM_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_MINOR_VERSION_C != IPC_SHM_AR_RELEASE_MINOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_REVISION_VERSION_C != IPC_SHM_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-queue.c and ipc-shm.h are different"
#endif
/* Check if ipc-queue.c file and ipc-shm.h file are of the same software version */
#if ((IPC_QUEUE_SW_MAJOR_VERSION_C != IPC_SHM_SW_MAJOR_VERSION) || \
	(IPC_QUEUE_SW_MINOR_VERSION_C != IPC_SHM_SW_MINOR_VERSION) || \
	(IPC_QUEUE_SW_PATCH_VERSION_C != IPC_SHM_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-queue.c and ipc-shm.h are different"
#endif

/* Check if ipc-queue.c file and ipc-queue.h file are of the same vendor */
#if (IPC_QUEUE_VENDOR_ID_C != IPC_QUEUE_VENDOR_ID)
	#error "ipc-queue.c and ipc-queue.h have different vendor IDs"
#endif
/* Check if ipc-queue.c file and ipc-queue.h file are of the same Autosar version */
#if ((IPC_QUEUE_AR_RELEASE_MAJOR_VERSION_C != IPC_QUEUE_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_MINOR_VERSION_C != IPC_QUEUE_AR_RELEASE_MINOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_REVISION_VERSION_C != IPC_QUEUE_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-queue.c and ipc-queue.h are different"
#endif
/* Check if ipc-queue.c file and ipc-queue.h file are of the same software version */
#if ((IPC_QUEUE_SW_MAJOR_VERSION_C != IPC_QUEUE_SW_MAJOR_VERSION) || \
	(IPC_QUEUE_SW_MINOR_VERSION_C != IPC_QUEUE_SW_MINOR_VERSION) || \
	(IPC_QUEUE_SW_PATCH_VERSION_C != IPC_QUEUE_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-queue.c and ipc-queue.h are different"
#endif

/* Check if ipc-queue.c file and ipc-util.h file are of the same vendor */
#if (IPC_QUEUE_VENDOR_ID_C != IPC_UTIL_VENDOR_ID)
	#error "ipc-queue.c and ipc-util.h have different vendor IDs"
#endif
/* Check if ipc-queue.c file and ipc-util.h file are of the same Autosar version */
#if ((IPC_QUEUE_AR_RELEASE_MAJOR_VERSION_C != IPC_UTIL_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_MINOR_VERSION_C != IPC_UTIL_AR_RELEASE_MINOR_VERSION) || \
	(IPC_QUEUE_AR_RELEASE_REVISION_VERSION_C != IPC_UTIL_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-queue.c and ipc-util.h are different"
#endif
/* Check if ipc-queue.c file and ipc-util.h file are of the same software version */
#if ((IPC_QUEUE_SW_MAJOR_VERSION_C != IPC_UTIL_SW_MAJOR_VERSION) || \
	(IPC_QUEUE_SW_MINOR_VERSION_C != IPC_UTIL_SW_MINOR_VERSION) || \
	(IPC_QUEUE_SW_PATCH_VERSION_C != IPC_UTIL_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-queue.c and ipc-util.h are different"
#endif

/* magic number to indicate the queue integrity */
#define IPC_QUEUE_SENTINEL 0x474E495246435049ULL

/**
 * ipcsQueuePop() - removes element from queue
 * @queue:	[IN] queue pointer
 * @buf:	[OUT] pointer where to copy the removed element
 *
 * Element is removed from pop ring that is mapped in remote shared memory and
 * it corresponds to the remote push ring.
 *
 * Return:	IPC_SHM_E_OK on success, error code otherwise
 */
sint32 ipcsQueuePop(struct IPCS_QUEUE_TYPE *queue, void *buf)
{
	uint32 write; /* cache write index for thread-safety */
	uint32 read; /* cache read index for thread-safety */
	void *src;
	sint32 err = -IPC_SHM_E_INVAL;

	if ((queue != NULL) && (buf != NULL)) {
		write = queue->pop_ring->write;

		/* read indexes of push/pop rings are swapped (interference freedom) */
		read = queue->push_ring->read;

		/* check if queue is empty */
		if (read == write) {
			err = -IPC_SHM_E_NO_QUEUE;
		} else {
			/* copy queue element in buffer */
			src = &queue->pop_ring->data[read * queue->elem_size];
			ipcsMemcpy(buf, src, queue->elem_size);

			/* increment read index with wrap around */
			queue->push_ring->read = (read + 1u) % queue->elem_num;
			err = IPC_SHM_E_OK;
		}
	}

	return err;
}

/**
 * ipcsQueuePush() - pushes element into the queue
 * @queue:	[IN] queue pointer
 * @buf:	[IN] pointer to element to be pushed into the queue
 *
 * Element is pushed into the push ring that is mapped in local shared memory
 * and corresponds to the remote pop ring.
 *
 * Return:	IPC_SHM_E_OK on success, error code otherwise
 */
sint32 ipcsQueuePush(struct IPCS_QUEUE_TYPE *queue, const void *buf)
{
	uint32 write; /* cache write index for thread-safety */
	uint32 read; /* cache read index for thread-safety */
	void *dst;
	sint32 err = -IPC_SHM_E_INVAL;

	if ((queue != NULL) && (buf != NULL)) {
		write = queue->push_ring->write;

		/* read indexes of push/pop rings are swapped (interference freedom) */
		read = queue->pop_ring->read;

		/* check if queue is full ([write + 1 == read] because of sentinel) */
		if (((write + 1u) % queue->elem_num) == read) {
			err = -IPC_SHM_E_NOMEM;
		} else {
			/* copy element from buffer in queue */
			dst = &queue->push_ring->data[write * queue->elem_size];
			ipcsMemcpy(dst, buf, queue->elem_size);

			/* increment write index with wrap around */
			queue->push_ring->write = (write + 1u) % queue->elem_num;

			err = IPC_SHM_E_OK;
		}
	}

	return err;
}

/**
 * ipcsQueueInit() - initializes queue and maps push/pop rings in memory
 * @queue:		[IN] queue pointer
 * @elem_num:		[IN] number of elements in queue
 * @elem_size:		[IN] element size in bytes (8-byte multiple)
 * @push_ring_addr:	[IN] local addr where to map the push buffer ring
 * @pop_ring_addr:	[IN] remote addr where to map the pop buffer ring
 *
 * Element size must be 8-byte multiple to ensure memory alignment.
 *
 * Queue will add one additional sentinel element to its size for lock-free
 * single-producer - single-consumer thread-safety.
 *
 * Return: IPC_SHM_E_OK on success, error code otherwise
 */
sint32 ipcsQueueInit(struct IPCS_QUEUE_TYPE *queue,
		uint16 elem_num, uint8 elem_size,
		uintptr_t push_ring_addr, uintptr_t pop_ring_addr)
{
	sint32 err = -IPC_SHM_E_INVAL;

	if ((queue != NULL) && (push_ring_addr != (uintptr_t)NULL) &&
		(pop_ring_addr != (uintptr_t)NULL) && (elem_num != 0u) &&
		(elem_size != 0u) && ((elem_size % 8u) == 0u)) {
		/* add 1 sentinel element in queue for lock-free thread-safety */
		queue->elem_num = elem_num + 1u;

		queue->elem_size = elem_size;

		/* map and init push ring in local memory */
		queue->push_ring = (struct IPCS_RING_TYPE *) push_ring_addr;

		/* add sentinel to detect integrity */
		queue->push_ring->sentinel = IPC_QUEUE_SENTINEL;

		queue->push_ring->write = 0;
		queue->push_ring->read = 0;

		/* map pop ring in remote memory (init is done by remote) */
		queue->pop_ring = (struct IPCS_RING_TYPE *) pop_ring_addr;
		err = IPC_SHM_E_OK;
	}

	return err;
}

/**
 * ipcsQueueCheckIntegrity() - check if the sentinel was not overwritten
 * @queue:	[IN] queue pointer
 *
 * Check if the sentinel was not overwritten
 *
 * Return:	IPC_SHM_E_OK on success, error code otherwise
 */
sint32 ipcsQueueCheckIntegrity(struct IPCS_QUEUE_TYPE *queue)
{
	sint32 err = -IPC_SHM_E_INTEGRITY;

	if ((IPC_QUEUE_SENTINEL == queue->pop_ring->sentinel) &&
			(IPC_QUEUE_SENTINEL == queue->push_ring->sentinel))
		err = IPC_SHM_E_OK;

	return err;
}

#if defined(__cplusplus)
}
#endif
