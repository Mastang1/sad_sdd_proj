# -*- coding: utf-8 -*-
"""PlantUML activity bodies for Linux chapter 6 (slug -> body without @startuml)."""

from __future__ import annotations

HEADER = """\
@startuml
!pragma layout smetana
skinparam conditionStyle insideDiamond
skinparam linetype ortho
"""

# slug: body lines between start and stop (inclusive)
FLOWS: dict[str, str] = {
    # --- 6.3 full-kernel OSAL ---
    "linux_6_3_1_ipcsShmSoftirq": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if ((priv.id[i].state == DISABLED) || (priv.id[i].irq_num == IPC_IRQ_NONE)?) then (yes)
  else (no)
    repeat
      :work = priv.rx_cb(i, budget);
      if (work >= budget?) then (yes)
        :tasklet_schedule(&ipc_shm_rx_tasklet);
      else (no)
      endif
    repeat while (work >= budget?) is (yes)
    :ipcsHwIrqEnable(i);
  endif
  :i++;
endwhile (no)
stop
""",
    "linux_6_3_2_ipcsShmHardirq": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if ((priv.id[i].state == DISABLED) || (priv.id[i].irq_num == IPC_IRQ_NONE)?) then (yes)
  else (no)
    :ipcsHwIrqDisable(i);
    :ipcsHwIrqClear(i);
  endif
  :i++;
endwhile (no)
:tasklet_schedule(&ipc_shm_rx_tasklet);;
:return IRQ_HANDLED;
stop
""",
    "linux_6_3_3_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL;
  stop
else (no)
endif
if ((instance invalid)?) then (yes)
  :return -EINVAL;
  stop
else (no)
endif
:request_mem_region local; ioremap local_virt_shm;
if (local map failed?) then (yes)
  :return err; stop
else (no)
endif
:request_mem_region remote; ioremap remote_virt_shm;
if (remote map failed?) then (yes)
  :unmap local; return err; stop
else (no)
endif
:save shm_size phys addrs; priv.rx_cb = rx_cb;
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :irq_num = IPC_IRQ_NONE;
else (no)
  :of_find_compatible_node MSCM; of_irq_get;
  if (mscm missing?) then (yes)
    :err; goto unmap; stop
  else (no)
  endif
endif
if (duplicate irq already registered?) then (yes)
  :state = ENABLED; return 0; stop
else (no)
endif
:irq_num_init[instance] = irq_num;
if (irq_num != IPC_IRQ_NONE?) then (yes)
  :request_irq(ipcsShmHardirq);
  if (request_irq failed?) then (yes)
    :goto unmap; stop
  else (no)
  endif
else (no)
endif
:state = ENABLED; return 0;
stop
""",
    "linux_6_3_4_ipcsOsFree": """
start
:state = DISABLED;
:ipcsHwIrqDisable(instance);
:tasklet_kill(&ipc_shm_rx_tasklet);
if (irq_num_init[instance] != 0?) then (yes)
  :free_irq;
  :irq_num_init[instance] = 0;
else (no)
endif
:iounmap remote; release_mem_region remote;
:iounmap local; release_mem_region local;
stop
""",
    "linux_6_3_5_ipcsOsGetLocalShm": """
start
:return priv.id[instance].local_virt_shm;
stop
""",
    "linux_6_3_6_ipcsOsGetRemoteShm": """
start
:return priv.id[instance].remote_virt_shm;
stop
""",
    "linux_6_3_7_ipcsOsMapIntc": """
start
:node = of_find_compatible_node(DT_INTC_NODE_COMP);
if (node == NULL?) then (yes)
  :return NULL;
  stop
else (no)
endif
:of_address_to_resource; of_node_put;
if (err?) then (yes)
  :return NULL;
  stop
else (no)
endif
:return ioremap(res.start, resource_size);
stop
""",
    "linux_6_3_8_ipcsOsUnmapIntc": """
start
:iounmap(addr);
stop
""",
    "linux_6_3_9_ipcsOsPollChannels": """
start
if (irq_num == IPC_IRQ_NONE?) then (yes)
  if (rx_cb != NULL?) then (yes)
    :return rx_cb(instance, IPC_SOFTIRQ_BUDGET);;
  else (no)
    :return -EINVAL;
  endif
else (no)
  :return -EOPNOTSUPP;
endif
stop
""",
    "linux_6_3_10_shm_mod_init": """
start
:shm_dbg driver version init;
:return 0;
stop
""",
    "linux_6_3_11_shm_mod_exit": """
start
:shm_dbg driver version exit;
stop
""",
    # --- 6.4 UIO user proxy ---
    "linux_6_4_1_line_from_file": """
start
:file = fopen(filename, "r");
if (file == NULL?) then (yes)
  :return -ENONET;
  stop
else (no)
endif
:s = fgets(buf, IPC_SHM_UIO_BUF_LEN, file);
if (s == NULL?) then (yes)
  :return -EIO;
  stop
else (no)
endif
:strip first line at newline; fclose(file);
:return 0;
stop
""",
    "linux_6_4_2_line_match": """
start
:err = line_from_file(filename, linebuf);
if (err != 0?) then (yes)
  :return err;
  stop
else (no)
endif
if (strncmp(linebuf, filter) != 0?) then (yes)
  :return EINVAL;
else (no)
  :return 0;
endif
stop
""",
    "linux_6_4_3_get_uio_dev_name": """
start
:sprintf uio_name instance_N;
:nentries = scandir(IPC_SHM_UIO_DIR);
if (nentries < 0?) then (yes)
  :return -EIO;
  stop
else (no)
endif
while (count > 0?) is (yes)
  :match sysfs name and version via line_match;
  if (matched?) then (yes)
    :copy dev_name;
    break
  else (no)
  endif
  :count--;
endwhile (no)
:free name_list entries;
if (found?) then (yes)
  :return 0;
else (no)
  :return -ENONET;
endif
stop
""",
    "linux_6_4_4_ipcsShmSoftirq": """
start
while (forever?) is (yes)
  if (rx_cb != NULL?) then (yes)
    :read(uio_fd, irq_count) block until kernel IRQ;
  else (no)
  endif
  repeat
    :work = rx_cb(instance, budget);
    if (work >= budget?) then (yes)
      :sched_yield();
    else (no)
    endif
  repeat while (work >= budget?) is (yes)
  :ipcsHwIrqEnable(instance);
endwhile (no)
stop
""",
    "linux_6_4_5_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:save shm_size rx_cb instance;
if (ipc_files_opened == CLEAR?) then (yes)
  :open module; finit_module;
  :open ipc-cdev-uio; open /dev/mem;
  :ipc_files_opened = SET;
else (no)
endif
:mmap local shm via /dev/mem page aligned;
if (local MAP_FAILED?) then (yes)
  :err; goto cleanup; stop
else (no)
endif
:mmap remote shm;
if (remote MAP_FAILED?) then (yes)
  :munmap local; err; stop
else (no)
endif
:write IPCS_UIO_CDEV_DATA_TYPE to cdev;
if (write failed?) then (yes)
  :munmap remote/local; err; stop
else (no)
endif
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :state = ENABLED; return 0; stop
else (no)
endif
:get_uio_dev_name; open /dev/uioX;
if (open UIO failed?) then (yes)
  :munmap; err; stop
else (no)
endif
:pthread_create(ipcsShmSoftirq, SCHED_FIFO max priority);
if (pthread_create failed?) then (yes)
  :close uio; munmap; err; stop
else (no)
endif
:state = ENABLED; return 0;
stop
""",
    "linux_6_4_6_ipcsOsFree": """
start
:state = DISABLED;
if (irq_num != IPC_IRQ_NONE?) then (yes)
  :ipcsHwIrqDisable; pthread_cancel/join irq thread;
  :close uio_fd;
else (no)
endif
:munmap remote and local;
if (any instance still ENABLED?) then (yes)
  :return;
  stop
else (no)
endif
:close cdev and mem; delete_module ipc-shm-uio;
stop
""",
    "linux_6_4_7_ipcsOsGetLocalShm": """
start
:return (uintptr_t)ipc_os_priv.id[instance].local_virt_shm;
stop
""",
    "linux_6_4_8_ipcsOsGetRemoteShm": """
start
:return (uintptr_t)ipc_os_priv.id[instance].remote_virt_shm;
stop
""",
    "linux_6_4_9_ipcsOsPollChannels": """
start
if (irq_num == IPC_IRQ_NONE?) then (yes)
  if (rx_cb != NULL?) then (yes)
    :return rx_cb(instance, budget);;
  else (no)
    :return -EINVAL;
  endif
else (no)
  :return -EOPNOTSUPP;
endif
stop
""",
    "linux_6_4_10_ipcsSendUioCmd": """
start
:ret = write(uio_fd, &cmd, sizeof(int));
if (ret != sizeof(int)?) then (yes)
  :shm_dbg failed command;
else (no)
endif
stop
""",
    "linux_6_4_11_ipcsHwIrqEnable": """
start
:ipcsSendUioCmd(uio_fd, IPC_UIO_ENABLE_CMD);
stop
""",
    "linux_6_4_12_ipcsHwIrqDisable": """
start
:ipcsSendUioCmd(uio_fd, IPC_UIO_DISABLE_CMD);
stop
""",
    "linux_6_4_13_ipcsHwIrqNotify": """
start
:ipcsSendUioCmd(uio_fd, IPC_UIO_TRIGGER_CMD);
stop
""",
    "linux_6_4_14_ipcsHwInit": """
start
:return 0 (kernel UIO handles HAL);
stop
""",
    "linux_6_4_15_ipcsHwFree": """
start
:return (no-op user proxy);
stop
""",
    # --- 6.4 UIO kernel backend ---
    "linux_6_4_17_ipcsShmUioOpen": """
start
if (!atomic_dec_and_test(&refcnt)?) then (yes)
  :atomic_inc; return -EBUSY;
else (no)
  :return 0;
endif
stop
""",
    "linux_6_4_18_ipcsShmUioRelease": """
start
:atomic_inc(&refcnt);
:return 0;
stop
""",
    "linux_6_4_19_ipcsShmUioIrqcontrol": """
start
:instance = info->data.instance;
if (cmd == IPC_UIO_DISABLE_CMD?) then (yes)
  :ipcsHwIrqDisable(instance);
elseif (cmd == IPC_UIO_ENABLE_CMD?) then (yes)
  :ipcsHwIrqEnable(instance);
elseif (cmd == IPC_UIO_TRIGGER_CMD?) then (yes)
  :ipcsHwIrqNotify(instance);
else (no)
endif
:return 0;
stop
""",
    "linux_6_4_20_ipcsShmUioHandler": """
start
:instance = info->data.instance;
:ipcsHwIrqDisable(instance);
:ipcsHwIrqClear(instance);
:return IRQ_HANDLED (uio_event_notify user);
stop
""",
    "linux_6_4_21_ipcsUioInit": """
start
:sprintf uio_name instance_N;
:err = ipcsHwInit(instance, cfg);
if (err?) then (yes)
  :return err; stop
else (no)
endif
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :return 0; stop
else (no)
endif
:irq = platform_get_irq(pdev, inter_core_rx_irq);
if (irq < 0?) then (yes)
  :return irq; stop
else (no)
endif
if (duplicate irq?) then (yes)
  :return -EFAULT; stop
else (no)
endif
:fill uio_info handler irqcontrol open release;
:uio_register_device;
if (failed?) then (yes)
  :return err; stop
else (no)
endif
:state = ENABLED; return 0;
stop
""",
    "linux_6_4_22_ipcsCdevOpen": """
start
if (!mutex_trylock(&mmap_device_mutex)?) then (yes)
  :return -EBUSY;
else (no)
endif
:filp->private_data = &ipc_pdev_priv;
:return 0;
stop
""",
    "linux_6_4_23_ipcsCdevRelease": """
start
:mutex_unlock(&mmap_device_mutex);
:filp->private_data = NULL;
:return 0;
stop
""",
    "linux_6_4_24_ipcsCdevWrite": """
start
:copy_from_user IPCS_UIO_CDEV_DATA_TYPE;
if (copy failed?) then (yes)
  :return -EFAULT; stop
else (no)
endif
if (instance >= IPC_SHM_MAX_INSTANCES?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:store data; ipcsUioInit(&data);
if (err?) then (yes)
  :return err; stop
else (no)
endif
:return sizeof(data);
stop
""",
    "linux_6_4_25_ipcsShmUioProbe": """
start
:platform_get_resource MSCM; devm_ioremap;
:create class and cdev ipc-cdev-uio;
:register platform driver;
:return 0;
stop
""",
    "linux_6_4_26_ipcsShmUioRemove": """
start
:unregister UIO devices per instance;
:cdev_del; class_destroy; devm unmap;
:return 0;
stop
""",
    "linux_6_4_27_ipcsOsMapIntc": """
start
:return ipc_pdev_priv.pdev_reg (mapped at probe);
stop
""",
    "linux_6_4_28_ipcsOsUnmapIntc": """
start
:no-op (devm manages MSCM mapping);
stop
""",
    # --- 6.5 CDEV user proxy ---
    "linux_6_5_1_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:save cfg; open/load ipc-shm-cdev module if first use;
:open /dev/mem and /dev/ipc-shm-cdev;
:mmap local and remote shm page aligned;
if (mmap failed?) then (yes)
  :cleanup; return err; stop
else (no)
endif
if (ipc_soft_created == CLEAR?) then (yes)
  :pthread_create global ipcsShmSoftirq thread;;
  :ipc_soft_created = SET;
else (no)
endif
:ioctl SET_INSTANCE; ioctl INIT_INSTANCE with cfg;
if (ioctl failed?) then (yes)
  :munmap; return err; stop
else (no)
endif
:irq_num = cfg->inter_core_rx_irq; state = ENABLED;
:return 0;
stop
""",
    "linux_6_5_2_ipcsOsFree": """
start
:state = DISABLED; munmap instance shm;
if (all instances disabled?) then (yes)
  :pthread_cancel/join softirq; close fds;
  :delete_module;
else (no)
endif
stop
""",
    "linux_6_5_3_ipcsOsGetLocalShm": """
start
:return (uintptr_t)priv.id[instance].local_virt_shm;
stop
""",
    "linux_6_5_4_ipcsOsGetRemoteShm": """
start
:return (uintptr_t)priv.id[instance].remote_virt_shm;
stop
""",
    "linux_6_5_5_ipcsOsPollChannels": """
start
if (irq_num == IPC_IRQ_NONE?) then (yes)
  if (rx_cb != NULL?) then (yes)
    :return rx_cb(instance, budget);;
  else (no)
    :return -EINVAL;
  endif
else (no)
  :return -EOPNOTSUPP;
endif
stop
""",
    "linux_6_5_6_ipcsHwIrqEnable": """
start
:ioctl(IPC_CDEV_CMD_ENABLE_RX_IRQ, instance);
stop
""",
    "linux_6_5_7_ipcsHwIrqDisable": """
start
:ioctl(IPC_CDEV_CMD_DISABLE_RX_IRQ, instance);
stop
""",
    "linux_6_5_8_ipcsHwIrqNotify": """
start
:ioctl(IPC_CDEV_CMD_TRIGGER_TX_IRQ, instance);
stop
""",
    "linux_6_5_9_ipcsHwInit": """
start
:return 0 (kernel CDEV backend owns HAL);
stop
""",
    "linux_6_5_10_ipcsHwFree": """
start
:no-op user proxy;
stop
""",
    # --- 6.5 CDEV kernel backend ---
    "linux_6_5_12_ipcsShmHardirq": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if ((disabled) || (irq_none)?) then (yes)
  else (no)
    :ipcsHwIrqDisable(i);
    :ipcsHwIrqClear(i);
  endif
  :i++;
endwhile (no)
:wait_queue_flag = WAKE; wake_up_interruptible(&wait_queue);
:return IRQ_HANDLED;
stop
""",
    "linux_6_5_13_ipcsOsMapIntc": """
start
:of_find_compatible_node; of_address_to_resource; ioremap;
if (failed?) then (yes)
  :return NULL;
else (no)
  :return mapped addr;
endif
stop
""",
    "linux_6_5_14_ipcsOsUnmapIntc": """
start
:iounmap(addr);
stop
""",
    "linux_6_5_15_ipcsCdevOpen": """
start
if (dev_is_opened?) then (yes)
  :return -EBUSY;
else (no)
  :dev_is_opened++; return 0;
endif
stop
""",
    "linux_6_5_16_ipcsCdevRelease": """
start
:dev_is_opened--;
:return 0;
stop
""",
    "linux_6_5_17_ipcsCdevRead": """
start
:wait_event_interruptible(wait_queue, flag != SLEEP);
:wait_queue_flag = SLEEP;
:return 0;
stop
""",
    "linux_6_5_18_ipcsCdevOsInit": """
start
:ipcsHwInit(instance, cfg);
if (failed?) then (yes)
  :return err; stop
else (no)
endif
if (rx_irq == IPC_IRQ_NONE?) then (yes)
  :irq_num = IPC_IRQ_NONE;
else (no)
  :of_irq_get from MSCM DT;
endif
if (duplicate irq?) then (yes)
  :state = ENABLED; return 0; stop
else (no)
endif
if (irq_num != IPC_IRQ_NONE?) then (yes)
  :request_irq(ipcsShmHardirq);
else (no)
endif
:state = ENABLED; return 0;
stop
""",
    "linux_6_5_19_ipcsCdevIoctl": """
start
if (ioctl_cmd == SET_INSTANCE?) then (yes)
  :target_instance = arg;
elseif (ioctl_cmd == INIT_INSTANCE?) then (yes)
  :copy_from_user cfg; ipcsCdevOsInit(target, cfg);
elseif (ioctl_cmd == DISABLE_RX_IRQ?) then (yes)
  :ipcsHwIrqDisable(arg);
elseif (ioctl_cmd == ENABLE_RX_IRQ?) then (yes)
  :ipcsHwIrqEnable(arg);
elseif (ioctl_cmd == TRIGGER_TX_IRQ?) then (yes)
  :ipcsHwIrqNotify(arg);
else (no)
  :return -ENOTTY;
endif
:return 0;
stop
""",
    "linux_6_5_20_ipcsCdevInit": """
start
:alloc_chrdev_region; class_create; cdev_init/add;
:device_create /dev/ipc-shm-cdev;
:init_waitqueue_head; return 0;
stop
""",
    "linux_6_5_21_ipcsCdevClean": """
start
:foreach instance: ipcsHwIrqDisable; free_irq if needed;
:cdev_del; device_destroy; class_destroy;
:unregister_chrdev_region;
stop
""",
    # --- 6.6 Linux HAL ---
    "linux_6_6_1_ipcsHwGetRxIrq": """
start
:return ipc_hw_priv[instance].mscm_rx_irq;
stop
""",
    "linux_6_6_2_ipcsHwInit": """
start
:addr = ipcsOsMapIntc();
:return _ipcsHwInit(instance, tx_irq, rx_irq, remote, local, addr);
stop
""",
    "linux_6_6_3__ipcsHwInit": """
start
if (mscm_addr == NULL?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:resolve local_core_idx and remote_core_idx from cfg;
:validate trust mask and irq indices;
if (invalid tx/rx same or core conflict?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:map MSI/SPI indices; store mscm tx/rx;
:ipcsHwIrqDisable(instance);
:update MSCM IRCPCFG trusted cores;
if (IRCPCFG locked?) then (yes)
  :return -EACCES;
else (no)
  :return 0;
endif
stop
""",
    "linux_6_6_4_ipcsHwFree": """
start
:ipcsHwIrqClear(instance);
:ipcsOsUnmapIntc(ipc_mscm);
stop
""",
    "linux_6_6_5_ipcsHwIrqEnable": """
start
if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
  :read IRSPRC; writew enable GIC500 routing;;
else (no)
endif
stop
""",
    "linux_6_6_6_ipcsHwIrqDisable": """
start
if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
  :read IRSPRC; writew disable GIC500 routing;;
else (no)
endif
stop
""",
    "linux_6_6_7_ipcsHwIrqNotify": """
start
if (mscm_tx_irq != IPC_IRQ_NONE?) then (yes)
  :writel IRCPnIGRn_INT_EN to remote core MSI;;
else (no)
endif
stop
""",
    "linux_6_6_8_ipcsHwIrqClear": """
start
if (mscm_rx_irq != IPC_IRQ_NONE?) then (yes)
  :writel clear ISR on local core MSI;;
else (no)
endif
stop
""",
    # --- 6.7 scenarios ---
    "linux_scenario_uio_init": """
start
:User ipcsShmInit -> ipcsOsInit;
:Load ipc-shm-uio.ko; open cdev-uio and /dev/mem;
:mmap local/remote SHM;
:write IPCS_UIO_CDEV_DATA_TYPE to cdev;
:Kernel ipcsCdevWrite -> ipcsUioInit;
:Kernel ipcsHwInit and uio_register_device;
:User get_uio_dev_name; open UIO fd;
:User pthread ipcsShmSoftirq (read blocks on IRQ);
stop
""",
    "linux_scenario_cdev_init": """
start
:User ipcsOsInit;
:Load ipc-shm-cdev.ko; open /dev/ipc-shm-cdev;
:mmap SHM; create Rx pthread;
:ioctl SET_INSTANCE + INIT_INSTANCE;
:Kernel ipcsCdevOsInit -> ipcsHwInit; request_irq;
stop
""",
    "linux_scenario_kernel_init": """
start
:In-kernel ipcsShmInit -> ipcsOsInit;
:request_mem_region; ioremap local/remote;
:of_irq_get; request_irq ipcsShmHardirq;
:tasklet ipcsShmSoftirq on RX;
stop
""",
    "linux_scenario_tx_irq": """
start
:User/Core ipcsHwIrqNotify;
if (UIO?) then (yes)
  :write UIO TRIGGER -> irqcontrol -> ipcsHwIrqNotify MSCM;;
else (no)
  :ioctl TRIGGER_TX_IRQ -> ipcsHwIrqNotify MSCM;;
endif
:Remote core receives inter-core interrupt;
stop
""",
    "linux_scenario_rx": """
start
:Remote notifies local MSCM IRQ;
:Kernel ISR ipcsShmHardirq or UioHandler;
:Kernel ipcsHwIrqDisable and ipcsHwIrqClear;
:Kernel wake user via UIO read or wait_queue;
:User read unblocks; rx_cb drains channels;
:User ipcsHwIrqEnable when budget done;
stop
""",
}
