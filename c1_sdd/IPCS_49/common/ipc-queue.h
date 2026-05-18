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
#ifndef IPC_QUEUE_H
#define IPC_QUEUE_H

#if defined(__cplusplus)
extern "C"{
#endif

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_QUEUE_VENDOR_ID                    43
#define IPC_QUEUE_AR_RELEASE_MAJOR_VERSION     4
#define IPC_QUEUE_AR_RELEASE_MINOR_VERSION     7
#define IPC_QUEUE_AR_RELEASE_REVISION_VERSION  0
#define IPC_QUEUE_SW_MAJOR_VERSION             4
#define IPC_QUEUE_SW_MINOR_VERSION             0
#define IPC_QUEUE_SW_PATCH_VERSION             1

/**
 * struct IPCS_RING_TYPE - memory mapped circular buffer ring
 * @sentinel: a magic word to ensure ring integrity
 * @write:	write index, position used to store next byte in the buffer
 * @read:	read index, read next byte from this position
 * @data:	circular buffer
 */
struct IPCS_RING_TYPE {
	uint64 sentinel;
	volatile uint32 write;
	volatile uint32 read;
	uint8 data[];
};

/**
 * struct IPCS_QUEUE_TYPE - Dual-Ring Shared-Memory Lock-Free FIFO Queue
 * @elem_num:	number of elements in queue
 * @elem_size:  element size in bytes (8-byte multiple)
 * @push_ring:	push buffer ring mapped in local shared memory
 * @pop_ring:	pop buffer ring mapped in remote shared memory
 *
 * This queue has two buffer rings one for pushing data and one for popping
 * data and works in conjunction with a complementary queue configured by
 * another IPC device (called remote) where the push/pop rings are reversed:
 *     local push_ring == remote pop_ring
 *     local pop_ring == remote push_ring
 *
 * The queue has freedom from interference between local and remote memory
 * domains by executing all write operations only in local memory (push_ring).
 * Read indexes of push_ring and pop_ring are swapped to avoid writing read
 * index in remote memory when doing pop operations.
 *
 * The queue is thread safe as long as only one thread is pushing and only one
 * thread is popping: Single-Producer - Single-Consumer. This thread safety
 * is lock-free and needs one additional sentinel element in rings between
 * write and read index that is never written.
 */
struct IPCS_QUEUE_TYPE {
	uint16 elem_num;
	uint8 elem_size;
	struct IPCS_RING_TYPE *push_ring;
	struct IPCS_RING_TYPE *pop_ring;
};

sint32 ipcsQueueInit(struct IPCS_QUEUE_TYPE *queue, uint16 elem_num,
	uint8 elem_size, uintptr_t push_ring_addr, uintptr_t pop_ring_addr);
sint32 ipcsQueuePush(struct IPCS_QUEUE_TYPE *queue, const void *buf);
sint32 ipcsQueuePop(struct IPCS_QUEUE_TYPE *queue, void *buf);
sint32 ipcsQueueCheckIntegrity(struct IPCS_QUEUE_TYPE *queue);

/**
 * ipcsQueueMemSize() - return queue footprint in local mapped memory
 * @queue:	[IN] queue pointer
 *
 * Return local mapped memory footprint: local ring control data + ring buffer.
 *
 * Return:	size of local mapped memory occupied by queue
 */
static inline uint32 ipcsQueueMemSize(struct IPCS_QUEUE_TYPE *queue)
{
	/* local ring control room + ring size */
	return (uint32)sizeof(struct IPCS_RING_TYPE)
		+ ((uint32)queue->elem_num * (uint32)queue->elem_size);
}

#if defined(__cplusplus)
}
#endif

#endif /* IPC_QUEUE_H */
