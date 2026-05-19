/**
 * IPC Shared Memory Driver - API Implementation
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
#include "ipc-os.h"
#include "ipc-hw.h"
#include "ipc-queue.h"

/*
 * SOURCE FILE VERSION INFORMATION
 */
#define IPC_SHM_VENDOR_ID_C                    43
#define IPC_SHM_AR_RELEASE_MAJOR_VERSION_C     4
#define IPC_SHM_AR_RELEASE_MINOR_VERSION_C     7
#define IPC_SHM_AR_RELEASE_REVISION_VERSION_C  0
#define IPC_SHM_SW_MAJOR_VERSION_C             4
#define IPC_SHM_SW_MINOR_VERSION_C             0
#define IPC_SHM_SW_PATCH_VERSION_C             1

/*
 * FILE VERSION CHECKS
 */
/* Check if ipc-shm.c file and ipc-shm.h file are of the same vendor */
#if (IPC_SHM_VENDOR_ID_C != IPC_SHM_VENDOR_ID)
	#error "ipc-shm.c and ipc-shm.h have different vendor IDs"
#endif
/* Check if ipc-shm.c file and ipc-shm.h file are of the same Autosar version */
#if ((IPC_SHM_AR_RELEASE_MAJOR_VERSION_C != IPC_SHM_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_MINOR_VERSION_C != IPC_SHM_AR_RELEASE_MINOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_REVISION_VERSION_C != IPC_SHM_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-shm.c and ipc-shm.h are different"
#endif
/* Check if ipc-shm.c file and ipc-shm.h file are of the same software version */
#if ((IPC_SHM_SW_MAJOR_VERSION_C != IPC_SHM_SW_MAJOR_VERSION) || \
	(IPC_SHM_SW_MINOR_VERSION_C != IPC_SHM_SW_MINOR_VERSION) || \
	(IPC_SHM_SW_PATCH_VERSION_C != IPC_SHM_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-shm.c and ipc-shm.h are different"
#endif

/* Check if ipc-shm.c file and ipc-os.h file are of the same vendor */
#if (IPC_SHM_VENDOR_ID_C != IPC_OS_VENDOR_ID)
	#error "ipc-shm.c and ipc-os.h have different vendor IDs"
#endif
/* Check if ipc-shm.c file and ipc-os.h file are of the same Autosar version */
#if ((IPC_SHM_AR_RELEASE_MAJOR_VERSION_C != IPC_OS_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_MINOR_VERSION_C != IPC_OS_AR_RELEASE_MINOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_REVISION_VERSION_C != IPC_OS_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-shm.c and ipc-os.h are different"
#endif
/* Check if ipc-shm.c file and ipc-os.h file are of the same software version */
#if ((IPC_SHM_SW_MAJOR_VERSION_C != IPC_OS_SW_MAJOR_VERSION) || \
	(IPC_SHM_SW_MINOR_VERSION_C != IPC_OS_SW_MINOR_VERSION) || \
	(IPC_SHM_SW_PATCH_VERSION_C != IPC_OS_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-shm.c and ipc-os.h are different"
#endif

/* Check if ipc-shm.c file and ipc-hw.h file are of the same vendor */
#if (IPC_SHM_VENDOR_ID_C != IPC_HW_VENDOR_ID)
	#error "ipc-shm.c and ipc-hw.h have different vendor IDs"
#endif
/* Check if ipc-shm.c file and ipc-hw.h file are of the same Autosar version */
#if ((IPC_SHM_AR_RELEASE_MAJOR_VERSION_C != IPC_HW_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_MINOR_VERSION_C != IPC_HW_AR_RELEASE_MINOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_REVISION_VERSION_C != IPC_HW_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-shm.c and ipc-hw.h are different"
#endif
/* Check if ipc-shm.c file and ipc-hw.h file are of the same software version */
#if ((IPC_SHM_SW_MAJOR_VERSION_C != IPC_HW_SW_MAJOR_VERSION) || \
	(IPC_SHM_SW_MINOR_VERSION_C != IPC_HW_SW_MINOR_VERSION) || \
	(IPC_SHM_SW_PATCH_VERSION_C != IPC_HW_SW_PATCH_VERSION))
	#error "Software Version Numbers of ipc-shm.c and ipc-hw.h are different"
#endif

/* Check if ipc-shm.c file and ipc-queue.h file are of the same vendor */
#if (IPC_SHM_VENDOR_ID_C != IPC_QUEUE_VENDOR_ID)
	#error "ipc-shm.c and ipc-queue.h have different vendor IDs"
#endif
/* Check if ipc-shm.c file and ipc-queue.h file are of the same Autosar version */
#if ((IPC_SHM_AR_RELEASE_MAJOR_VERSION_C != IPC_QUEUE_AR_RELEASE_MAJOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_MINOR_VERSION_C != IPC_QUEUE_AR_RELEASE_MINOR_VERSION) || \
	(IPC_SHM_AR_RELEASE_REVISION_VERSION_C != IPC_QUEUE_AR_RELEASE_REVISION_VERSION))
	#error "AutoSar Version Numbers of ipc-shm.c and ipc-queue.h are different"
#endif
/* Check if ipc-shm.c file and ipc-queue.h file are of the same software version */
#if ((IPC_SHM_SW_MAJOR_VERSION_C != IPC_QUEUE_SW_MAJOR_VERSION) || \
	(IPC_SHM_SW_MINOR_VERSION_C != IPC_QUEUE_SW_MINOR_VERSION) || \
	(IPC_SHM_SW_PATCH_VERSION_C != IPC_QUEUE_SW_PATCH_VERSION))
#error "Software Version Numbers of ipc-shm.c and ipc-queue.h are different"
#endif

/* magic number to indicate the driver is initialized */
#define IPC_SHM_STATE_READY 0x3252455646435049ULL
#define IPC_SHM_STATE_CLEAR 0u

/* magic number to indicate the unmanaged channel integrity */
#define IPC_UCHAN_SENTINEL 0x55435049UL

/**
 * enum IPCS_SHM_INSTANCE_STATE_E - used for IPC instance status
 * @IPC_SHM_INSTANCE_USED:	instance is used
 * @IPC_SHM_INSTANCE_FREE:	instance is free and can be used
 * @IPC_SHM_INSTANCE_ERROR: there are some errors
 */
enum IPCS_SHM_INSTANCE_STATE_E {
	IPC_SHM_INSTANCE_USED = 0u,
	IPC_SHM_INSTANCE_FREE = 1u,
	IPC_SHM_INSTANCE_ERROR = 2u,
};

/**
 * struct IPCS_SHM_POOL_ADDR_TYPE - struct stores temporary addresses of local/remote
 *                            memory
 * @local_pool_shm:  address of local buffer pool
 * @remote_pool_shm: address of remote buffer pool
 */
struct IPCS_SHM_POOL_ADDR_TYPE {
	uintptr_t local_pool_shm;
	uintptr_t remote_pool_shm;
};

/**
 * struct IPCS_SHM_BD_TYPE - buffer descriptor (store buffer location and data size)
 * @pool_id:	index of buffer pool
 * @buf_id:	index of buffer from buffer pool
 * @data_size:	size of data written in buffer
 */
struct IPCS_SHM_BD_TYPE {
	sint16 pool_id;
	uint16 buf_id;
	uint32 data_size;
};

/**
 * struct IPCS_SHM_POOL_TYPE - buffer pool private data
 * @num_bufs:		number of buffers in pool
 * @buf_size:		size of buffers
 * @shm_size:		size of shared memory mapped by this pool (queue + bufs)
 * @local_pool_addr:	address of local buffer pool
 * @remote_pool_addr:	address of remote buffer pool
 * @bd_queue:		queue containing BDs of free buffers
 *
 * bd_queue has two rings: one for pushing BDs (release ring) and one for
 * popping BDs (acquire ring).
 * Local IPC pushes BDs into release ring when local app finishes processing a
 * received buffer and calls ipcsShmReleaseBuf(). Remote IPC pops BDs from its
 * acquire ring (our release ring) when remote app calls ipcsShmAcquireBuf()
 * to prepare for a Tx operation.
 *
 * The relation between local and remote bd_queue rings is:
 *     local acquire ring == remote release ring
 *     local release ring == remote acquire ring
 */
struct IPCS_SHM_POOL_TYPE {
	uint16 num_bufs;
	uint32 buf_size;
	uint32 shm_size;
	uintptr_t local_pool_addr;
	uintptr_t remote_pool_addr;
	struct IPCS_QUEUE_TYPE bd_queue;
};

/**
 * struct IPCS_MANAGED_CHANNEL_TYPE - managed channel private data
 * @bd_queue:	queue containing BDs of sent/received buffers
 * @num_pools:	number of buffer pools
 * @pools:	buffer pools private data
 * @rx_cb:	receive callback
 * @cb_arg:	optional receive callback argument
 *
 * bd_queue has two rings: one for pushing BDs (Tx ring) and one for popping
 * BDs (Rx ring).
 * Local IPC device reads BDs pushed into bd_queue by remote IPC and remote
 * IPC device reads BDs pushed into bd_queue by local IPC.
 *
 * The relation between local and remote bd_queue rings is:
 *     local Tx ring == remote Rx ring
 *     local Rx ring == remote Tx ring
 */
struct IPCS_MANAGED_CHANNEL_TYPE {
	struct IPCS_QUEUE_TYPE bd_queue;
	uint8 num_pools;
	struct IPCS_SHM_POOL_TYPE pools[IPC_SHM_MAX_POOLS];
	void (*rx_cb)(void *cb_arg, const uint8 instance, sint32 chan_id,
			void *buf, uint32 size);
	void *cb_arg;
};

/**
 * struct IPCS_CHANNEL_UMEM_TYPE - unmanaged channel memory control structure
 * @sentinel:	magic word to ensure unmanaged channel integrity
 * @tx_count:	local channel Tx counter (it wraps around at max uint32)
 * @mem:	local channel unmanaged memory buffer
 *
 * tx_count is used by remote peer in Rx intr handler to determine if this
 * channel had a Tx operation and decide whether to call the app Rx callback.
 */
struct IPCS_CHANNEL_UMEM_TYPE {
	uint32 sentinel;
	volatile uint32 tx_count;
	uint8 mem[];
};

/**
 * struct IPCS_UNMANAGED_CHANNEL_TYPE - unmanaged channel private data
 * @size:		unmanaged channel memory size requested by app
 * @local_umem:		local channel unmanaged memory
 * @remote_umem:	remote channel unmanaged memory
 * @remote_tx_count:	copy of remote Tx counter
 * @rx_cb:		receive callback
 * @cb_arg:		optional receive callback argument
 */
struct IPCS_UNMANAGED_CHANNEL_TYPE {
	uint32 size;
	struct IPCS_CHANNEL_UMEM_TYPE *local_mem;
	struct IPCS_CHANNEL_UMEM_TYPE *remote_mem;
	uint32 remote_tx_count;
	void (*rx_cb)(void *cb_arg, const uint8 instance, sint32 chan_id,
			void *buf);
	void *cb_arg;
};

/**
 * struct IPCS_SHM_CHANNEL_TYPE - ipc channel private data
 * @id:		channel id
 * @type:	channel type (see IPCS_SHM_CHANNEL_TYPE_E)
 * @ch:		managed/unmanaged channel private data
 */
struct IPCS_SHM_CHANNEL_TYPE {
	sint32 id;
	enum IPCS_SHM_CHANNEL_TYPE_E type;
	union {
		struct IPCS_MANAGED_CHANNEL_TYPE mng;
		struct IPCS_UNMANAGED_CHANNEL_TYPE umng;
	} ch;
};

/**
 * struct IPCS_SHM_GLOBAL_TYPE - ipc shm global data shared with remote
 * @state:		state to indicate whether local is initialized
 *
 * Global data is located at beginning of local/remote shared memory so the size
 * of this struct should chosen so that memory alignment is preserved.
 */
struct IPCS_SHM_GLOBAL_TYPE {
	uint64 state;
};

/**
 * struct IPCS_SHM_PRIV_TYPE - ipc shm private data
 * @shm_size:		local/remote shared memory size
 * @num_channels:	number of shared memory channels
 * @channels:		ipc channels private data
 * @global:		local global data shared with remote
 */
struct IPCS_SHM_PRIV_TYPE {
	uint32 shm_size;
	uint8 num_channels;
	struct IPCS_SHM_CHANNEL_TYPE channels[IPC_SHM_MAX_CHANNELS];
	struct IPCS_SHM_GLOBAL_TYPE *global;
};

/* ipc shm private data */
static struct IPCS_SHM_PRIV_TYPE ipc_shm_priv_data[IPC_SHM_MAX_INSTANCES];

/* get channel with validation (can be used in API functions) */
static inline struct IPCS_SHM_CHANNEL_TYPE *getChannel(const uint8 instance,
		sint32 chan_id)
{
	struct IPCS_SHM_CHANNEL_TYPE *channel = NULL;

	if ((chan_id < 0)
		|| (chan_id >= (sint32)ipc_shm_priv_data[instance].num_channels)) {
		channel = NULL;
	} else {
		channel = &ipc_shm_priv_data[instance].channels[chan_id];
	}

	return channel;
}

/* get managed channel with validation */
static inline struct IPCS_MANAGED_CHANNEL_TYPE *getManagedChan(
		const uint8 instance, sint32 chan_id)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *channel = NULL;
	struct IPCS_SHM_CHANNEL_TYPE *chan = getChannel(instance, chan_id);

	if ((chan == NULL) || (chan->type != IPC_SHM_MANAGED)) {
		channel = NULL;
	} else {
		channel = &chan->ch.mng;
	}

	return channel;
}

/* get unmanaged channel with validation */
static inline struct IPCS_UNMANAGED_CHANNEL_TYPE *getUnmanagedChan(
		const uint8 instance, sint32 chan_id)
{
	struct IPCS_UNMANAGED_CHANNEL_TYPE *channel = NULL;
	struct IPCS_SHM_CHANNEL_TYPE *chan = getChannel(instance, chan_id);

	if ((chan == NULL) || (chan->type != IPC_SHM_UNMANAGED)) {
		channel = NULL;
	} else {
		channel = &chan->ch.umng;
	}

	return channel;
}

/* check integrity of uchan: the boundaries have not been altered */
static sint32 ipcsCheckUchanIntegrity(const struct IPCS_UNMANAGED_CHANNEL_TYPE *uchan)
{
	sint32 err = -IPC_SHM_E_INTEGRITY;

	if ((uchan->local_mem->sentinel == (uint32)IPC_UCHAN_SENTINEL)
			&& (uchan->remote_mem->sentinel == (uint32)IPC_UCHAN_SENTINEL))
		err = IPC_SHM_E_OK;

	return err;
}

/* check integrity of mchan: the boundaries have not been altered */
static sint32 ipcsCheckMchanIntegrity(struct IPCS_MANAGED_CHANNEL_TYPE *mchan)
{
	sint32 err = IPC_SHM_E_OK;
	uint8 pool_id;
	struct IPCS_SHM_POOL_TYPE *pool = NULL;

	if (IPC_SHM_E_OK == ipcsQueueCheckIntegrity(&mchan->bd_queue)) {
		/* check all the pool bd boundaries */
		for (pool_id = 0; pool_id < mchan->num_pools; pool_id++) {
			pool = &mchan->pools[pool_id];
			if (IPC_SHM_E_OK != ipcsQueueCheckIntegrity(&pool->bd_queue))
				err = -IPC_SHM_E_INTEGRITY;
		}
	} else {
		err = -IPC_SHM_E_INTEGRITY;
	}
	return err;
}

/**
 * ipcsChannelRx() - handle Rx for a single channel
 * @instance:	instance id
 * @chan_id:	channel id
 * @budget:	available work budget (number of messages to be processed)
 *
 * Return:	work done
 */
static sint32 ipcsChannelRx(const uint8 instance, sint32 chan_id, sint32 budget)
{
	struct IPCS_SHM_CHANNEL_TYPE *chan =
			&ipc_shm_priv_data[instance].channels[chan_id];
	struct IPCS_MANAGED_CHANNEL_TYPE *mchan = &chan->ch.mng;
	struct IPCS_UNMANAGED_CHANNEL_TYPE *uchan = &chan->ch.umng;
	struct IPCS_SHM_POOL_TYPE *pool;
	struct IPCS_SHM_BD_TYPE bd;
	uintptr_t buf_addr;
	uint32 buf_offset;
	uint32 remote_tx_count;
	sint32 result = 0;
	sint32 work = 0;

	/* unmanaged channels: call Rx callback if channel Tx counter changed */
	if (chan->type == IPC_SHM_UNMANAGED) {

		/* flush and invalidate dcache */
		ipcsHwFlushCacheLocal(instance);
		ipcsHwFlushCacheRemote(instance);

		if (IPC_SHM_E_OK == ipcsCheckUchanIntegrity(uchan)) {
			remote_tx_count = uchan->remote_mem->tx_count;

			/* call Rx cb if remote Tx counter changed */
			if (remote_tx_count != uchan->remote_tx_count) {

				/* save new remote Tx counter */
				uchan->remote_tx_count = remote_tx_count;

				uchan->rx_cb(uchan->cb_arg, instance, chan->id,
						(void *)uchan->remote_mem->mem);

				work = budget;
			}
		}
	} else {
		/* managed channels: process incoming BDs in the limit of budget */
		while (work < budget) {
			result = ipcsQueuePop(&mchan->bd_queue, &bd);
			if (result != IPC_SHM_E_OK) {
				break;
			}
			pool = &mchan->pools[bd.pool_id];
			buf_offset = pool->buf_size * bd.buf_id;
			buf_addr = pool->remote_pool_addr + buf_offset;

			mchan->rx_cb(mchan->cb_arg, instance, chan->id,
					(void *)buf_addr, bd.data_size);
			work++;
		}
	}

	return work;
}

/**
 * ipcsInstanceIsFree() - determine if the instance is used or not
 * @instance:	instance id
 *
 * This function return the state of instance.
 *
 * Return: IPC_SHM_INSTANCE_FREE if instance is free,
 *     IPC_SHM_INSTANCE_USED otherwise or
 *     IPC_SHM_INSTANCE_ERROR if there is errors
 */
static uint8 ipcsInstanceIsFree(const uint8 instance)
{
	uint8 err = (uint8)IPC_SHM_INSTANCE_ERROR;

	if (instance < IPC_SHM_MAX_INSTANCES) {
		if ((ipc_shm_priv_data[instance].global == NULL)
			|| (ipc_shm_priv_data[instance].global->state
				== (uint64)IPC_SHM_STATE_CLEAR)) {
			err = (uint8)IPC_SHM_INSTANCE_FREE;
		} else {
			err = (uint8)IPC_SHM_INSTANCE_USED;
		}
	}

	return err;
}

/**
 * ipcsShmRx() - shm Rx handler, called from softirq
 * @instance:	instance id
 * @budget:	available work budget (number of messages to be processed)
 *
 * This function handles all channels using a fair handling algorithm: all
 * channels are treated equally and no channel is starving.
 *
 * Return:	work done
 */
static sint32 ipcsShmRx(const uint8 instance, sint32 budget)
{
	uint8 num_chans = ipc_shm_priv_data[instance].num_channels;
	sint32 chan_budget, chan_work;
	sint32 more_work = 1;
	sint32 work = 0;
	uint8 i = 0;

	/* fair channel handling algorithm */
	while ((work < budget) && (more_work > 0)) {
		chan_budget = (budget - work) / ((sint32)num_chans);
		if (chan_budget == 0) {
			chan_budget = 1;
		}
		more_work = 0;

		/* flush dcache before using it */
		ipcsHwFlushCacheRemote(instance);

		for (i = 0; i < num_chans; i++) {
			chan_work = ipcsChannelRx(instance, (sint32)i, chan_budget);
			work += chan_work;

			if (chan_work == chan_budget)
				more_work = 1;
		}
	}

	return work;
}

/**
 * ipcsBufPoolInit() - init buffer pool
 * @instance:	instance id
 * @chan_id:	channel index
 * @pool_id:	pool index in channel
 * @local_shm:	local pool shared memory address
 * @remote_shm: remote pool shared memory address
 * @cfg:	channel configuration parameters
 *
 * To ensure freedom from interference when writing in shared memory, only one
 * IPC is allowed to write in a BD ring, so the IPC that pushes BDs in the
 * release ring at the end of an Rx operation must also initialize it. That's
 * why local IPC initializes bd_queue with BDs pointing to remote free buffers.
 * Since the shared memory configuration is symmetric and remote base address
 * is known, local IPC can compute the remote BD info.
 *
 * Return: IPC_SHM_E_OK for success, error code otherwise
 */
static sint32 ipcsBufPoolInit(const uint8 instance, sint32 chan_id, sint32 pool_id,
		struct IPCS_SHM_POOL_ADDR_TYPE mng_pool, const struct IPCS_SHM_POOL_CFG_TYPE *cfg)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan
		= &ipc_shm_priv_data[instance].channels[chan_id].ch.mng;
	struct IPCS_SHM_POOL_TYPE *pool = &chan->pools[pool_id];
	struct IPCS_SHM_BD_TYPE bd;
	uintptr_t local_shm = mng_pool.local_pool_shm;
	uintptr_t remote_shm = mng_pool.remote_pool_shm;
	uint32 queue_mem_size = 0u;
	uint16 i = 0u;
	sint32 err = -IPC_SHM_E_INVAL;

	if (cfg->num_bufs <= IPC_SHM_MAX_BUFS_PER_POOL) {
		pool->num_bufs = cfg->num_bufs;
		pool->buf_size = cfg->buf_size;

		/* init pool bd_queue with push ring mapped at the start of local
		 * pool shm and pop ring mapped at start of remote pool shm
		 */
		err = ipcsQueueInit(&pool->bd_queue, pool->num_bufs,
			(uint8)sizeof(struct IPCS_SHM_BD_TYPE), local_shm, remote_shm);
		if (err == IPC_SHM_E_OK) {
			/* init local/remote buffer pool addrs */
			queue_mem_size = ipcsQueueMemSize(&pool->bd_queue);

			/* init actual local buffer pool addr */
			pool->local_pool_addr = local_shm + queue_mem_size;

			/* init actual remote buffer pool addr */
			pool->remote_pool_addr = remote_shm + queue_mem_size;

			pool->shm_size = queue_mem_size + (cfg->buf_size * cfg->num_bufs);

			/* check if pool fits into shared memory */
			if ((local_shm + pool->shm_size)
					> (ipcsOsGetLocalShm(instance)
						+ ipc_shm_priv_data[instance].shm_size)) {
				err = -IPC_SHM_E_NOMEM;
			} else {
				/* populate bd_queue with free BDs from remote pool */
				for (i = 0; i < pool->num_bufs; i++) {
					bd.pool_id = (sint16) pool_id;
					bd.buf_id = i;
					bd.data_size = 0;

					err = ipcsQueuePush(&pool->bd_queue, &bd);
					if (err != IPC_SHM_E_OK) {
						break;
					}
				}
			}
		}
	}

	return err;
}

/**
 * ipcsGetTotalBufPerChan() - get total buffers of an managed channel
 *
 * @instance: instance id
 * @chan_id:  channel id
 * @cfg:      managed channel configuration
 *
 * Return: total buffers, 0 if error
 */
static uint32 ipcsGetTotalBufPerChan(const uint8 instance, sint32 chan_id,
		const struct IPCS_SHM_MANAGED_CFG_TYPE *cfg)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan =
		&ipc_shm_priv_data[instance].channels[chan_id].ch.mng;
	const struct IPCS_SHM_POOL_CFG_TYPE *pool_cfg;
	uint32 prev_buf_size = 0u;
	uint32 total_bufs = 0u;
	sint32 err = -IPC_SHM_E_INVAL;
	uint8 i = 0;

	if ((cfg->num_pools > 0u) && (cfg->num_pools <= IPC_SHM_MAX_POOLS)) {
		err = IPC_SHM_E_OK;
		/* save managed channel parameters */
		chan->rx_cb = cfg->rx_cb;
		chan->cb_arg = cfg->cb_arg;
		chan->num_pools = cfg->num_pools;

		/* check that pools are sorted in ascending order by buf size
		 * and count total number of buffers from all pools
		 */
		for (i = 0; i < chan->num_pools; i++) {
			pool_cfg = &cfg->pools[i];

			if (pool_cfg->buf_size < prev_buf_size) {
				err = -IPC_SHM_E_INVAL;
			} else {
				prev_buf_size = pool_cfg->buf_size;
				total_bufs += pool_cfg->num_bufs;
			}
			if ((err != IPC_SHM_E_OK)
					|| (total_bufs > IPC_SHM_MAX_BUFS_PER_CHANNEL)) {
				err = -IPC_SHM_E_INVAL;
				break;
			}
		}
	}

	if (err != IPC_SHM_E_OK) {
		total_bufs = 0u;
	}

	return total_bufs;
}

/**
 * managedChannelInit() - initialize managed channel
 *
 * @instance:   instance id
 * @chan_id:    channel id
 * @local_shm:  local shared memory
 * @remote_shm: remote shared memort
 * @cfg:        managed channel configuration
 *
 * Return: IPC_SHM_E_OK for success, error code otherwise
 */
static sint32 managedChannelInit(const uint8 instance, sint32 chan_id,
		uintptr_t local_shm, uintptr_t remote_shm,
		const struct IPCS_SHM_MANAGED_CFG_TYPE *cfg)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan =
		&ipc_shm_priv_data[instance].channels[chan_id].ch.mng;
	struct IPCS_SHM_POOL_ADDR_TYPE mng_pool_addr
			= { .local_pool_shm = (uintptr_t)NULL,
				.remote_pool_shm = (uintptr_t)NULL};
	uint32 total_bufs = ipcsGetTotalBufPerChan(instance, chan_id, cfg);
	uint32 queue_mem_size = 0u;
	sint32 err = -IPC_SHM_E_INVAL;
	uint8 i = 0;

	if (total_bufs != 0u) {
		/* init channel bd_queue with push ring mapped at the start of local
		 * channel shm and pop ring mapped at start of remote channel shm
		 */
		err = ipcsQueueInit(&chan->bd_queue, (uint16)total_bufs,
					(uint8)sizeof(struct IPCS_SHM_BD_TYPE),
					local_shm, remote_shm);

		if (err == IPC_SHM_E_OK) {
			/* init&map buffer pools after channel bd_queue */
			queue_mem_size = ipcsQueueMemSize(&chan->bd_queue);
			mng_pool_addr.local_pool_shm = local_shm + queue_mem_size;
			mng_pool_addr.remote_pool_shm = remote_shm + queue_mem_size;

			/* check if pool fits into shared memory */
			if ((mng_pool_addr.local_pool_shm)
					> (ipcsOsGetLocalShm(instance)
						+ ipc_shm_priv_data[instance].shm_size)) {
				err = -IPC_SHM_E_NOMEM;
			} else {
				for (i = 0; i < chan->num_pools; i++) {
					err = ipcsBufPoolInit(instance, chan_id, (sint32)i,
						mng_pool_addr, &cfg->pools[i]);
					if (err != IPC_SHM_E_OK) {
						break;
					}

					/* compute next pool local
					 * and remote shm base address
					 */
					mng_pool_addr.local_pool_shm
							+= chan->pools[i].shm_size;
					mng_pool_addr.remote_pool_shm
							+= chan->pools[i].shm_size;
				}
			}
		}
	}

	return err;
}

/**
 * unmanagedChannelInit() - initialize unmanaged channel
 *
 * @instance:   instance id
 * @chan_id:    channel id
 * @local_shm:  local shared memory
 * @remote_shm: remote shared memort
 * @cfg:        unmanaged channel configuration
 *
 * Return: IPC_SHM_E_OK for success, error code otherwise
 */
static sint32 unmanagedChannelInit(const uint8 instance, sint32 chan_id,
		uintptr_t local_shm, uintptr_t remote_shm,
		const struct IPCS_SHM_UNMANAGED_CFG_TYPE *cfg)
{
	struct IPCS_UNMANAGED_CHANNEL_TYPE *chan
		= &ipc_shm_priv_data[instance].channels[chan_id].ch.umng;
	sint32 err = -IPC_SHM_E_INVAL;

	if (cfg->size <= IPC_SHM_MAX_UMNG_SIZE) {
		/* save unmanaged channel parameters */
		chan->size = cfg->size;
		chan->rx_cb = cfg->rx_cb;
		chan->cb_arg = cfg->cb_arg;

		chan->local_mem = (struct IPCS_CHANNEL_UMEM_TYPE *) local_shm;
		chan->remote_mem = (struct IPCS_CHANNEL_UMEM_TYPE *) remote_shm;

		chan->local_mem->sentinel = (uint32)IPC_UCHAN_SENTINEL;
		chan->local_mem->tx_count = 0;
		chan->remote_tx_count = 0;
		err = IPC_SHM_E_OK;
	}

	return err;
}

/**
 * ipcsShmInitChannel() - initialize a shared memory IPC channel
 * @instance:	instance id
 * @chan_id:	channel index
 * @local_shm:	local channel shared memory address
 * @remote_shm: remote channel shared memory address
 * @cfg:	channel configuration parameters
 *
 * Return: 0 for success, error code otherwise
 */
static sint32 ipcsShmInitChannel(const uint8 instance, sint32 chan_id,
		uintptr_t local_shm, uintptr_t remote_shm,
		const struct IPCS_SHM_CHANNEL_CFG_TYPE *cfg)
{
	struct IPCS_SHM_CHANNEL_TYPE *chan =
			&ipc_shm_priv_data[instance].channels[chan_id];
	sint32 err = -IPC_SHM_E_INVAL;

	if (cfg != NULL) {
		/* save common channel parameters */
		chan->id = chan_id;
		chan->type = cfg->type;

		if (cfg->type == IPC_SHM_MANAGED) {
			if ((cfg->ch.managed.rx_cb == NULL)
				|| (cfg->ch.managed.pools == NULL)) {
				err = -IPC_SHM_E_INVAL;
			} else {
				err = managedChannelInit(instance, chan_id, local_shm,
						remote_shm, &cfg->ch.managed);
			}
		} else if (cfg->type == IPC_SHM_UNMANAGED) {
			if (cfg->ch.unmanaged.rx_cb == NULL) {
				err = -IPC_SHM_E_INVAL;
			} else {
				err = unmanagedChannelInit(instance, chan_id, local_shm,
						remote_shm, &cfg->ch.unmanaged);
			}
		} else {
			err = -IPC_SHM_E_INVAL;
		}
	}

	return err;
}

/**
 * getChanMemmapSize() - Get channel local mapped memory size
 *
 * @instance: instance id
 * @chan_id:  channel id
 *
 * Return: Channel memory size
 */
static uint32 getChanMemmapSize(const uint8 instance, sint32 chan_id)
{
	struct IPCS_SHM_CHANNEL_TYPE *chan =
			&ipc_shm_priv_data[instance].channels[chan_id];
	struct IPCS_MANAGED_CHANNEL_TYPE *mchan;
	uint32 mapped_mem_size = 0u;
	uint8 i = 0u;

	/* unmanaged channels: control structure size + channel memory size */
	if (chan->type == IPC_SHM_UNMANAGED) {
		mapped_mem_size = (uint32)(sizeof(struct IPCS_CHANNEL_UMEM_TYPE) +
			chan->ch.umng.size);
	} else {
		/* managed channels: size of BD queue + size of buf pools */
		mchan = &chan->ch.mng;
		mapped_mem_size = ipcsQueueMemSize(&mchan->bd_queue);
		for (i = 0; i < mchan->num_pools; i++) {
			mapped_mem_size += mchan->pools[i].shm_size;
		}
	}

	return mapped_mem_size;
}

/**
 * ipcsShmInitChannels() - initialize all shared memory IPC channel
 *
 * @instance: instance id
 * @cfg:      ipc-shm instance configuration
 *
 * Return: 0 for success, error code otherwise
 */
static sint32 ipcsShmInitChannels(uint8 instance,
	const struct IPCS_SHM_CFG_TYPE *cfg)
{
	uintptr_t local_shm = ipcsOsGetLocalShm(instance);
	uintptr_t local_chan_shm;
	uintptr_t remote_chan_shm;
	uint32 chan_offset = (uint32)sizeof(struct IPCS_SHM_GLOBAL_TYPE);
	uint32 chan_size;
	uint8 i = 0;
	sint32 err = -IPC_SHM_E_INVAL;

	/* global data stored at
	 * beginning of local shared memory
	 */
	ipc_shm_priv_data[instance].global
		= (struct IPCS_SHM_GLOBAL_TYPE *)local_shm;

	/* init channels */
	local_chan_shm = local_shm + (uintptr_t) chan_offset;
	remote_chan_shm = ipcsOsGetRemoteShm(instance) + (uintptr_t) chan_offset;
	for (i = 0; i < ipc_shm_priv_data[instance].num_channels; i++) {
		err = ipcsShmInitChannel(instance, (sint32)i, local_chan_shm,
				remote_chan_shm, &cfg->channels[i]);
		if (err == IPC_SHM_E_OK) {
			/* compute next channel local
			 * remote shm base address
			 */
			chan_size = getChanMemmapSize(instance, (sint32)i);
			local_chan_shm += chan_size;
			remote_chan_shm += chan_size;
		} else {
			ipcsOsFree(instance);
			ipcsHwFree(instance);
			break;
		}
	}

	return err;
}

/**
 * ipcsShmInitInstance() - Initialize only one instance shared memory device
 *
 * @instance: instance id
 * @cfg:      ipc-shm instance configuration
 *
 * Return IPC_SHM_E_OK on success, error code otherwise
 */
static sint32 ipcsShmInitInstance(uint8 instance,
	const struct IPCS_SHM_CFG_TYPE *cfg)
{
	sint32 err = -IPC_SHM_E_INVAL;

	if ((cfg != NULL)
		&& (cfg->local_shm_addr != (uintptr_t) NULL)
			&& (cfg->remote_shm_addr != (uintptr_t) NULL)
				&& (cfg->num_channels > 0u)
					&& (cfg->num_channels <= IPC_SHM_MAX_CHANNELS)) {
		/* save api params */
		ipc_shm_priv_data[instance].shm_size = cfg->shm_size;
		ipc_shm_priv_data[instance].num_channels = cfg->num_channels;

		/* pass interrupt and core data to hw */
		err = ipcsHwInit(instance, cfg);
		if (err == IPC_SHM_E_OK) {
			/* init OS specific resources */
			err = ipcsOsInit(instance, cfg, ipcsShmRx);
			if (err != IPC_SHM_E_OK) {
				ipcsHwFree(instance);
			} else {
				err = ipcsShmInitChannels(instance, cfg);
				if (err == IPC_SHM_E_OK) {
					/* clear interrupt flags */
					ipcsHwIrqClear(instance);

					/* enable interrupt notifications */
					ipcsHwIrqEnable(instance);

					ipc_shm_priv_data[instance].global->state
							= IPC_SHM_STATE_READY;

					/* flush and invalidate dcache */
					ipcsHwFlushCacheLocal(instance);
				}
			}
		}
	}

	return err;
}

void ipcsShmFree(void)
{
	uint8 i = 0;

	/* check if instance must be free */
	for (i = 0; i < IPC_SHM_MAX_INSTANCES; i++) {
		if (ipcsInstanceIsFree(i) == (uint8)IPC_SHM_INSTANCE_USED) {

			/* reset state */
			ipc_shm_priv_data[i].global->state =
				IPC_SHM_STATE_CLEAR;
			ipc_shm_priv_data[i].global = NULL;

			/* flush and invalidate dcache */
			ipcsHwFlushCacheLocal(i);

			/* disable hardirq */
			ipcsHwIrqDisable(i);

			ipcsOsFree(i);
			ipcsHwFree(i);
		}
	}
}

void *ipcsShmAcquireBuf(const uint8 instance, sint32 chan_id, uint32 mem_size)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan;
	struct IPCS_SHM_POOL_TYPE *pool = NULL;
	struct IPCS_SHM_BD_TYPE bd = {.pool_id = 0, .buf_id = 0u, .data_size = 0u};
	uintptr_t buf_addr = (uintptr_t)NULL;
	uint8 pool_id;

	/* flush and invalidate dcache */
	ipcsHwFlushCacheLocal(instance);
	ipcsHwFlushCacheRemote(instance);

	/* check if instance is valid */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		chan = getManagedChan(instance, chan_id);

		if ((chan == NULL) || (mem_size == 0u)
				|| (IPC_SHM_E_OK != ipcsCheckMchanIntegrity(chan))) {
			buf_addr = (uintptr_t)NULL;
		} else {
			/* find first non-empty pool that accommodates the requested size */
			for (pool_id = 0; pool_id < chan->num_pools; pool_id++) {
				pool = &chan->pools[pool_id];

				/* check if pool buf size covers the requested size */
				if (mem_size > pool->buf_size)
					continue;

				/* check if pool has any free buffers left */
				if (ipcsQueuePop(&pool->bd_queue, &bd) == 0)
					break;
			}

			if (pool_id == chan->num_pools) {
				buf_addr = (uintptr_t)NULL;
			} else {
				buf_addr = pool->local_pool_addr +
					(uint32)(bd.buf_id * pool->buf_size);
			}
		}
	}

	return (void *)buf_addr;
}

sint32 ipcsShmInit(const struct IPCS_SHM_INSTANCES_CFG_TYPE *cfg)
{
	uint8 i = 0;
	sint32 err = -IPC_SHM_E_INVAL;

	if (cfg != NULL) {
		if ((cfg->num_instances > IPC_SHM_MAX_INSTANCES)
				|| (cfg->num_instances == 0u)) {
			err = -IPC_SHM_E_INVAL;
		} else {
			/* init all instances */
			for (i = 0; i < cfg->num_instances; i++) {
				err = ipcsShmInitInstance(i, &cfg->shm_cfg[i]);
				if (err != IPC_SHM_E_OK) {
					break;
				}
			}
		}
	}

	return err;
}

/**
 * findPoolForBuf() - Find the pool that owns the specified buffer.
 * @chan:	managed channel pointer
 * @buf:	buffer pointer
 * @remote:	flag telling if buffer is from remote OS
 *
 * Return: pool index on success, -1 otherwise
 */
static sint16 findPoolForBuf(struct IPCS_MANAGED_CHANNEL_TYPE *chan,
		uintptr_t buf, sint32 remote)
{
	struct IPCS_SHM_POOL_TYPE *pool;
	uintptr_t addr;
	uint32 pool_size;
	uint8 pool_id;
	sint16 pool_index = -1;

	for (pool_id = 0U; pool_id < chan->num_pools; pool_id++) {
		pool = &chan->pools[pool_id];

		if (remote == 1) {
			addr = pool->remote_pool_addr;
		} else {
			addr = pool->local_pool_addr;
		}

		pool_size = pool->num_bufs * pool->buf_size;

		if ((buf >= addr) && (buf < (addr + pool_size))) {
			pool_index = (sint16)pool_id;
			break;
		}
	}

	return pool_index;
}

sint32 ipcsShmReleaseBuf(const uint8 instance, sint32 chan_id, const void *buf)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan;
	struct IPCS_SHM_POOL_TYPE *pool;
	struct IPCS_SHM_BD_TYPE bd;
	sint32 err = -IPC_SHM_E_INVAL;

	/* check if instance is valid */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		chan = getManagedChan(instance, chan_id);
		if ((chan != NULL) && (buf != NULL)) {

			/* flush and invalidate dcache */
			ipcsHwFlushCacheLocal(instance);
			ipcsHwFlushCacheRemote(instance);

			err = ipcsCheckMchanIntegrity(chan);
			if (IPC_SHM_E_OK == err) {
				/* Find the pool that owns the buffer */
				bd.pool_id = findPoolForBuf(chan, (uintptr_t)buf, 1);
				if (bd.pool_id != -1) {
					pool = &chan->pools[bd.pool_id];
					bd.buf_id = (uint16)(((uintptr_t)buf
							- pool->remote_pool_addr) /
							pool->buf_size);
					bd.data_size = 0; /* reset size of written data in buffer */

					err = ipcsQueuePush(&pool->bd_queue, &bd);
				} else {
					err = -IPC_SHM_E_INVAL;
				}
			}
		}
	}

	/* flush and invalidate dcache */
	ipcsHwFlushCacheLocal(instance);

	return err;
}

sint32 ipcsShmTx(const uint8 instance, sint32 chan_id, void *buf, uint32 size)
{
	struct IPCS_MANAGED_CHANNEL_TYPE *chan;
	struct IPCS_SHM_POOL_TYPE *pool;
	struct IPCS_SHM_BD_TYPE bd;
	sint32 err = -IPC_SHM_E_INVAL;

	/* check if instance is used */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		chan = getManagedChan(instance, chan_id);
		if ((chan != NULL) && (buf != NULL) && (size != 0u)) {

			/* flush and invalidate dcache */
			ipcsHwFlushCacheLocal(instance);
			ipcsHwFlushCacheRemote(instance);

			err = ipcsCheckMchanIntegrity(chan);
			if (IPC_SHM_E_OK == err) {
				/* Find the pool that owns the buffer */
				bd.pool_id = findPoolForBuf(chan, (uintptr_t)buf, 0);
				if (bd.pool_id != -1) {
					pool = &chan->pools[bd.pool_id];
					bd.buf_id = (uint16)(((uintptr_t)buf
							- pool->local_pool_addr) / pool->buf_size);
					bd.data_size = size;

					/* push buffer descriptor in queue */
					err = ipcsQueuePush(&chan->bd_queue, &bd);
					if (err == IPC_SHM_E_OK) {
						/* flush and invalidate dcache */
						ipcsHwFlushCacheLocal(instance);

						/* notify remote that data is available */
						ipcsHwIrqNotify(instance);
					}
				} else {
					err = -IPC_SHM_E_INVAL;
				}
			}
		}
	}

	return err;
}

void *ipcsShmUnmanagedAcquire(const uint8 instance, sint32 chan_id)
{
	struct IPCS_UNMANAGED_CHANNEL_TYPE *chan = NULL;
	uint8 *umng_mem = NULL;

	/* check if instance is used */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {

		/* flush and invalidate dcache */
		ipcsHwFlushCacheLocal(instance);
		ipcsHwFlushCacheRemote(instance);

		chan = getUnmanagedChan(instance, chan_id);
		if ((chan != NULL) && (IPC_SHM_E_OK == ipcsCheckUchanIntegrity(chan))) {
			umng_mem = chan->local_mem->mem;
		}
	}

	/* for unmanaged channels return entire channel memory */
	return (void *)umng_mem;
}

sint32 ipcsShmUnmanagedTx(const uint8 instance, sint32 chan_id)
{
	struct IPCS_UNMANAGED_CHANNEL_TYPE *chan = NULL;
	sint32 err = -IPC_SHM_E_INVAL;

	/* check if instance is used */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		chan = getUnmanagedChan(instance, chan_id);
		if (chan != NULL) {

			/* flush and invalidate dcache */
			ipcsHwFlushCacheLocal(instance);
			ipcsHwFlushCacheRemote(instance);

			err = ipcsCheckUchanIntegrity(chan);
			if (IPC_SHM_E_OK == err) {
				chan->local_mem->tx_count++;

				/* flush and invalidate dcache */
				ipcsHwFlushCacheLocal(instance);

				ipcsHwIrqNotify(instance);
			}
		}
	}

	return err;
}

sint32 ipcsShmIsRemoteReady(const uint8 instance)
{
	struct IPCS_SHM_GLOBAL_TYPE *remote_global;
	sint32 err = -IPC_SHM_E_INVAL;

	/* flush and invalidate dcache */
	ipcsHwFlushCacheRemote(instance);

	/* check if instance is used */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		/* global data of remote at beginning of remote shared memory */
		remote_global = (struct IPCS_SHM_GLOBAL_TYPE *)ipcsOsGetRemoteShm(
				instance);

		if (remote_global->state != IPC_SHM_STATE_READY) {
			err = -IPC_SHM_E_NOT_READY;
		} else {
			err = IPC_SHM_E_OK;
		}
	}

	return err;
}

sint32 ipcsShmPollChannels(const uint8 instance)
{
	struct IPCS_SHM_GLOBAL_TYPE *remote_global;
	sint32 err = -IPC_SHM_E_INVAL;

	/* flush and invalidate dcache */
	ipcsHwFlushCacheRemote(instance);

	/* check if instance is used */
	if (ipcsInstanceIsFree(instance) == (uint8)IPC_SHM_INSTANCE_USED) {
		/* global data of remote at beginning of remote shared memory */
		remote_global = (struct IPCS_SHM_GLOBAL_TYPE *)ipcsOsGetRemoteShm(
				instance);

		/* check if remote is ready before polling */
		if (remote_global->state != IPC_SHM_STATE_READY) {
			err = -IPC_SHM_E_NOT_READY;
		} else {
			err = ipcsOsPollChannels(instance);
		}
	}

	return err;
}

#if defined(__cplusplus)
}
#endif
