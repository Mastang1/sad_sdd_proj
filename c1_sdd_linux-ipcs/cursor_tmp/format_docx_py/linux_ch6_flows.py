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
  if ((priv.id[i].state != DISABLED) && (priv.id[i].irq_num != IPC_IRQ_NONE)?) then (yes)
    repeat
      :work = priv.rx_cb(i, budget);
      if (work >= budget?) then (yes)
        :tasklet_schedule(&ipc_shm_rx_tasklet);
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
  if ((priv.id[i].state != DISABLED) && (priv.id[i].irq_num != IPC_IRQ_NONE)?) then (yes)
    :ipcsHwIrqDisable(i);
    :ipcsHwIrqClear(i);
  endif
  :i++;
endwhile (no)
:tasklet_schedule(&ipc_shm_rx_tasklet);
:return IRQ_HANDLED;
stop
""",
    "linux_6_3_3_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL;
  stop
endif
if ((instance invalid)?) then (yes)
  :return -EINVAL;
  stop
endif
:request_mem_region(cfg->local_shm_addr, cfg->shm_size, DRIVER_NAME)\nlocal_virt_shm = ioremap(cfg->local_shm_addr, cfg->shm_size);;
if (local map failed?) then (yes)
  :release_mem_region(cfg->local_shm_addr, cfg->shm_size)\nreturn -ENOMEM;;
  stop
endif
:request_mem_region(cfg->remote_shm_addr, cfg->shm_size, DRIVER_NAME)\nremote_virt_shm = ioremap(cfg->remote_shm_addr, cfg->shm_size);;
if (remote map failed?) then (yes)
  :iounmap(local_virt_shm)\nrelease_mem_region(cfg->local_shm_addr, cfg->shm_size)\nreturn -ENOMEM;;
  stop
endif
:priv.id[instance].shm_size = cfg->shm_size\npriv.id[instance].local_shm = cfg->local_shm_addr\npriv.id[instance].remote_shm = cfg->remote_shm_addr\npriv.rx_cb = rx_cb;;
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :irq_num = IPC_IRQ_NONE;
else (no)
  :mscm_node = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP)\nirq_num = of_irq_get(mscm_node, cfg->inter_core_rx_irq);;
  if (mscm missing?) then (yes)
    :iounmap(remote_virt_shm)\niounmap(local_virt_shm)\nrelease_mem_region(cfg->remote_shm_addr, cfg->shm_size)\nrelease_mem_region(cfg->local_shm_addr, cfg->shm_size)\nreturn -ENXIO;;
    stop
  endif
endif
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if (irq_num == irq_num_init[i]?) then (yes)
    :priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED\nreturn 0;;
    stop
  endif
  :i++;
endwhile (no)
:irq_num_init[instance] = irq_num;
if (irq_num != IPC_IRQ_NONE?) then (yes)
  :request_irq(ipcsShmHardirq);
  if (request_irq failed?) then (yes)
    :iounmap(remote_virt_shm)\niounmap(local_virt_shm)\nrelease_mem_region(cfg->remote_shm_addr, cfg->shm_size)\nrelease_mem_region(cfg->local_shm_addr, cfg->shm_size)\nreturn err;;
    stop
  endif
endif
:priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED\nreturn 0;;
stop
""",
    "linux_6_3_4_ipcsOsFree": """
start
:priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;;
:ipcsHwIrqDisable(instance);
:tasklet_kill(&ipc_shm_rx_tasklet);
if (irq_num_init[instance] != 0?) then (yes)
  :free_irq(priv.id[instance].irq_num, &priv);;
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
:err = of_address_to_resource(node, 0, &res)\nof_node_put(node);;
if (err?) then (yes)
  :return NULL;
  stop
else (no)
endif
:return ioremap(res.start, resource_size(&res));;
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
:shm_dbg("%s: %s", DRIVER_NAME, DRIVER_VERSION);
:return 0;
stop
""",
    "linux_6_3_11_shm_mod_exit": """
start
:shm_dbg("%s: %s exit", DRIVER_NAME, DRIVER_VERSION);
stop
""",
    # --- 6.4 UIO user proxy ---
    "linux_6_4_1_line_from_file": """
start
:memset(buf, 0, IPC_UIO_PARAMS_LEN);
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
:i = 0;
while ((*s) && (i < IPC_SHM_UIO_BUF_LEN)?) is (yes)
  if (*s == '\\n'?) then (yes)
    :*s = 0;
    break
  else (no)
  endif
  :s++;
  :i++;
endwhile (no)
:fclose(file);
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
  :return -EINVAL;
else (no)
  :return 0;
endif
stop
""",
    "linux_6_4_3_get_uio_dev_name": """
start
:sprintf(uio_name, "instance_%u", instance);;
:nentries = scandir(IPC_SHM_UIO_DIR);
if (nentries < 0?) then (yes)
  :return -EIO;
  stop
else (no)
endif
while (count > 0?) is (yes)
  :err_name = line_match(name_path, uio_name)\nerr_version = line_match(version_path, DRIVER_VERSION);;
  if (matched?) then (yes)
    :strcpy(dev_name, name_list[count]->d_name);;
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
while (1?) is (yes)
  if (info->rx_cb != NULL?) then (yes)
    :read(info->uio_fd, &irq_count, sizeof(irq_count));
  endif
  repeat
    :work = info->rx_cb(info->instance, IPC_SOFTIRQ_BUDGET);
    :sched_yield();
  repeat while (work >= IPC_SOFTIRQ_BUDGET?) is (yes)
  :ipcsHwIrqEnable(info->instance);
endwhile (no)
stop
""",
    "linux_6_4_5_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL;
  stop
endif
:ipc_os_priv.id[instance].shm_size = cfg->shm_size; ipc_os_priv.id[instance].rx_cb = rx_cb; ipc_os_priv.id[instance].instance = instance;;
if (ipc_os_priv.ipc_files_opened == IPC_STATUS_CLEAR?) then (yes)
  :ipc_uio_module_fd = open(IPC_UIO_MODULE_PATH, O_RDONLY)\nfinit_module(ipc_uio_module_fd, "", 0);;
  if ((ipc_uio_module_fd == -1) || (finit_module != 0)?) then (yes)
    :err = -ENODEV\nclose(ipc_uio_module_fd)\nreturn err;;
    stop
  endif
  :ipc_os_priv.ipc_cdev_fd = open(IPC_UIO_CDEV_NAME, O_RDWR)\nipc_os_priv.dev_mem_fd = open(IPC_UIO_DEV_MEM_NAME, O_RDWR);;
  if ((ipc_cdev_fd == -1) || (dev_mem_fd == -1)?) then (yes)
    :err = -ENODEV\nclose(ipc_os_priv.ipc_cdev_fd)\nclose(ipc_uio_module_fd)\nreturn err;;
    stop
  endif
  :ipc_os_priv.ipc_files_opened = IPC_STATUS_SET;
endif
:page_phys_addr = (cfg->local_shm_addr / page_size) * page_size\nlocal_shm_offset = cfg->local_shm_addr - page_phys_addr\nlocal_shm_map = mmap(NULL, local_shm_offset + cfg->shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, dev_mem_fd, page_phys_addr)\nlocal_virt_shm = local_shm_map + local_shm_offset;;
if (local_shm_map == MAP_FAILED?) then (yes)
  :return -ENOMEM; stop
endif
:page_phys_addr = (cfg->remote_shm_addr / page_size) * page_size\nremote_shm_offset = cfg->remote_shm_addr - page_phys_addr\nremote_shm_map = mmap(NULL, remote_shm_offset + cfg->shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, dev_mem_fd, page_phys_addr)\nremote_virt_shm = remote_shm_map + remote_shm_offset;;
if (remote_shm_map == MAP_FAILED?) then (yes)
  :munmap(local_shm_map); return -ENOMEM; stop
endif
:irq_num = cfg->inter_core_rx_irq\ndata_cfg.instance = instance\ndata_cfg.cfg = *cfg\nerr = write(ipc_os_priv.ipc_cdev_fd, &data_cfg, sizeof(data_cfg));;
if (err < 0?) then (yes)
  :munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size)\nreturn -EINVAL;;
  stop
endif
if (cfg->inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :id[instance].state = IPC_SHM_INSTANCE_ENABLED; return 0; stop
endif
:err = get_uio_dev_name(uio_dev_name, instance)\nsnprintf(dev_uio, sizeof(dev_uio), "/dev/%s", uio_dev_name)\nuio_fd = open(dev_uio, O_RDWR);;
if ((err != 0) || (uio_fd == -1)?) then (yes)
  :munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size)\nreturn -ENODEV;;
  stop
endif
:pthread_attr_init(&irq_thread_attr)\npthread_attr_setschedpolicy(&irq_thread_attr, RX_SOFTIRQ_POLICY)\npthread_attr_setschedparam(&irq_thread_attr, &irq_thread_param)\nerr = pthread_create(&irq_thread_id, &irq_thread_attr, ipcsShmSoftirq, &id[instance]);;
if (err == -1?) then (yes)
  :close(uio_fd)\nmunmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size)\nreturn err;;
  stop
endif
:id[instance].state = IPC_SHM_INSTANCE_ENABLED; return 0;
stop
""",
    "linux_6_4_6_ipcsOsFree": """
start
:ipc_os_priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;;
if (ipc_os_priv.id[instance].irq_num != IPC_IRQ_NONE?) then (yes)
  :ipcsHwIrqDisable(instance)\npthread_cancel(irq_thread_id)\npthread_join(irq_thread_id, &res)\nclose(uio_fd);;
else (no)
endif
:munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size);;
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if (ipc_os_priv.id[i].state == IPC_SHM_INSTANCE_ENABLED?) then (yes)
  :return;
  stop
  endif
  :i++;
endwhile (no)
:close(ipc_cdev_fd)\nclose(dev_mem_fd);;
if (delete_module(IPC_UIO_MODULE_NAME, O_NONBLOCK) != 0?) then (yes)
  :shm_err("Can't unload %s module", IPC_UIO_MODULE_NAME);;
endif
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
  :shm_dbg("Failed to write UIO command %d", cmd);;
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
:return 0;
stop
""",
    "linux_6_4_15_ipcsHwFree": """
start
:return;
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
  :return -EINVAL;
  stop
endif
:return 0;
stop
""",
    "linux_6_4_20_ipcsShmUioHandler": """
start
:instance = info->data.instance;
:ipcsHwIrqDisable(instance);;
:ipcsHwIrqClear(instance);;
:return IRQ_HANDLED;
stop
""",
    "linux_6_4_21_ipcsUioInit": """
start
:sprintf(uio_name, "instance_%u", instance);;
:err = ipcsHwInit(instance, cfg);
if (err != 0?) then (yes)
  :return err;
  stop
endif
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :return 0;
  stop
endif
:irq = platform_get_irq(ipc_pdev, inter_core_rx_irq);
if (irq < 0?) then (yes)
  :return irq;
  stop
endif
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if (irq == irq_num_init[i]?) then (yes)
    :return -EFAULT;
    stop
  endif
  :i++;
endwhile (no)
:irq_num_init[instance] = irq\nuio_id[instance].info.name = uio_name\nuio_id[instance].info.version = IPC_UIO_VERSION\nuio_id[instance].info.handler = ipcsShmUioHandler\nuio_id[instance].info.irqcontrol = ipcsShmUioIrqcontrol;;
:err = uio_register_device(&ipc_pdev->dev, &uio_id[instance].info);;
if (uio_register failed?) then (yes)
  :return err;
  stop
endif
:uio_id[instance].state = IPC_SHM_INSTANCE_ENABLED\nreturn 0;;
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
:ret = copy_from_user(&data, user_buffer, sizeof(struct IPCS_UIO_CDEV_DATA_TYPE));;
if (copy failed?) then (yes)
  :return -EFAULT; stop
else (no)
endif
if (instance >= IPC_SHM_MAX_INSTANCES?) then (yes)
  :return -EINVAL; stop
else (no)
endif
:ipc_pdev_priv.uio_id[data.instance].data = data\nerr = ipcsUioInit(data.instance, &data.cfg);;
if (err?) then (yes)
  :return err; stop
else (no)
endif
:return sizeof(data);
stop
""",
    "linux_6_4_25_ipcsShmUioProbe": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  :uio_id[i].irq_num = IPC_IRQ_NONE; irq_num_init[i] = IPC_IRQ_NONE;;
  :i++;
endwhile (no)
:platform_set_drvdata(pdev, uio_id); ipc_pdev = pdev;
:res = platform_get_resource(ipc_pdev, IORESOURCE_MEM, 0);;
:pdev_reg = devm_ioremap_resource(&ipc_pdev->dev, res);;
if (IS_ERR_OR_NULL(pdev_reg)?) then (yes)
  :return -ENOMEM; stop
endif
:err = alloc_chrdev_region(&major, 0, 1, IPC_CDEV_NAME);;
if (err < 0?) then (yes)
  :return err; stop
endif
:cdev_init(&cdev, &ipc_cdev_fops); err = cdev_add(&cdev, major, 1);;
if (err < 0?) then (yes)
  :unregister_chrdev_region(major, 1); return err; stop
endif
:cdev_class = class_create(THIS_MODULE, IPC_CDEV_NAME);;
if (!cdev_class?) then (yes)
  :cdev_del(&cdev); unregister_chrdev_region(major, 1); return -EEXIST; stop
endif
if (!device_create(cdev_class, NULL, major, NULL, IPC_CDEV_NAME)?) then (yes)
  :class_destroy(cdev_class); cdev_del(&cdev); unregister_chrdev_region(major, 1); return -EINVAL; stop
endif
:mutex_init(&mmap_device_mutex);;
:return 0;
stop
""",
    "linux_6_4_26_ipcsShmUioRemove": """
start
:device_destroy(cdev_class, major);;
:class_destroy(cdev_class);;
:cdev_del(&cdev);;
:unregister_chrdev_region(major, 1);;
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
    if (uio_id[i].state == IPC_SHM_INSTANCE_ENABLED?) then (yes)
    :uio_id[i].state = IPC_SHM_INSTANCE_DISABLED;
    if (irq_num_init[i] != IPC_IRQ_NONE?) then (yes)
      :uio_unregister_device(&uio_id[i].info);
    endif
  endif
  :i++;
endwhile (no)
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
:return;
stop
""",
    # --- 6.5 CDEV user proxy ---
    "linux_6_5_1_ipcsOsInit": """
start
if (rx_cb == NULL?) then (yes)
  :return -EINVAL; stop
endif
:priv.id[instance].shm_size = cfg->shm_size; priv.id[instance].rx_cb = rx_cb;;
if (priv.ipc_files_opened == IPC_STATUS_CLEAR?) then (yes)
  :ipc_usr_module_fd = open(IPC_USR_MODULE_PATH, O_RDONLY)\nfinit_module(ipc_usr_module_fd, "", 0);;
  if ((ipc_usr_module_fd == -1) || (finit_module != 0)?) then (yes)
    :return -ENODEV; stop
  endif
  :priv.dev_mem_fd = open(IPC_USR_DEV_MEM_NAME, O_RDWR)\npriv.ipc_usr_fd = open(IPC_USR_CDEV_NAME, O_RDWR);;
  if ((dev_mem_fd == -1) || (ipc_usr_fd == -1)?) then (yes)
    :close(priv.dev_mem_fd)\nclose(priv.ipc_usr_fd)\nclose(ipc_usr_module_fd)\nreturn -ENODEV;;
    stop
  endif
  :priv.ipc_files_opened = IPC_STATUS_SET;
endif
:page_phys_addr = (cfg->local_shm_addr / page_size) * page_size\nlocal_shm_offset = cfg->local_shm_addr - page_phys_addr\nlocal_shm_map = mmap(NULL, local_shm_offset + cfg->shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, dev_mem_fd, page_phys_addr)\nlocal_virt_shm = local_shm_map + local_shm_offset;;
if (local_shm_map == MAP_FAILED?) then (yes)
  :return -ENOMEM; stop
endif
:page_phys_addr = (cfg->remote_shm_addr / page_size) * page_size\nremote_shm_offset = cfg->remote_shm_addr - page_phys_addr\nremote_shm_map = mmap(NULL, remote_shm_offset + cfg->shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, dev_mem_fd, page_phys_addr)\nremote_virt_shm = remote_shm_map + remote_shm_offset;;
if (remote_shm_map == MAP_FAILED?) then (yes)
  :munmap(local_shm_map); return -ENOMEM; stop
endif
if (priv.ipc_soft_created == IPC_STATUS_CLEAR?) then (yes)
  :pthread_attr_init(&irq_thread_attr)\npthread_attr_setschedpolicy(&irq_thread_attr, RX_SOFTIRQ_POLICY)\npthread_attr_setschedparam(&irq_thread_attr, &irq_thread_param)\nerr = pthread_create(&priv.irq_thread_id, &irq_thread_attr, ipcsShmSoftirq, &priv);;
  if (err == -1?) then (yes)
    :munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size)\nreturn err;;
    stop
  endif
  :priv.ipc_soft_created = IPC_STATUS_SET;
endif
:err = ioctl(priv.ipc_usr_fd, IPC_CDEV_CMD_SET_INSTANCE, instance)\nif (!err) err = ioctl(priv.ipc_usr_fd, IPC_CDEV_CMD_INIT_INSTANCE, cfg);;
if (err?) then (yes)
  :munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size)\nreturn err;;
  stop
endif
if (cfg->inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :priv.id[instance].irq_num = IPC_IRQ_NONE;
else (no)
  :priv.id[instance].irq_num = 0;
endif
:priv.id[instance].state = IPC_SHM_INSTANCE_ENABLED; return 0;
stop
""",
    "linux_6_5_2_ipcsOsFree": """
start
:priv.id[instance].state = IPC_SHM_INSTANCE_DISABLED;;
:ipcsHwIrqDisable(instance);;
:munmap(remote_shm_map, remote_shm_offset + shm_size)\nmunmap(local_shm_map, local_shm_offset + shm_size);;
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if (priv.id[i].state == IPC_SHM_INSTANCE_ENABLED?) then (yes)
    :return;
    stop
  endif
  :i++;
endwhile (no)
if (priv.ipc_files_opened == IPC_STATUS_SET?) then (yes)
  :pthread_cancel(priv.irq_thread_id)\npthread_join(priv.irq_thread_id, &res)\npriv.ipc_soft_created = IPC_STATUS_CLEAR;;
  :close(priv.ipc_usr_fd)\nclose(priv.dev_mem_fd);;
  if (delete_module(IPC_ISR_MODULE_NAME, O_NONBLOCK) != 0?) then (yes)
    :shm_err("Can't unload %s module", IPC_ISR_MODULE_NAME);;
  endif
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
:return 0;
stop
""",
    "linux_6_5_10_ipcsHwFree": """
start
:return;
stop
""",
    # --- 6.5 CDEV kernel backend ---
    "linux_6_5_12_ipcsShmHardirq": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if ((instance_id[i].state != IPC_SHM_INSTANCE_DISABLED) && (instance_id[i].irq_num != IPC_IRQ_NONE)?) then (yes)
    :ipcsHwIrqDisable(i);
    :ipcsHwIrqClear(i);
  endif
  :i++;
endwhile (no)
:wait_queue_flag = IPC_CDEV_WAKE_QUEUE; wake_up_interruptible(&wait_queue);
:return IRQ_HANDLED;
stop
""",
    "linux_6_5_13_ipcsOsMapIntc": """
start
:node = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP);;
if (!node?) then (yes)
  :return NULL; stop
endif
:err = of_address_to_resource(node, 0, &res); of_node_put(node);;
if (err?) then (yes)
  :return NULL; stop
endif
:return ioremap(res.start, resource_size(&res));;
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
:err = ipcsHwInit(instance, cfg);
if (err != 0?) then (yes)
  :return err;
  stop
endif
if (inter_core_rx_irq == IPC_IRQ_NONE?) then (yes)
  :irq_num = IPC_IRQ_NONE;
else (no)
  :mscm_node = of_find_compatible_node(NULL, NULL, DT_INTC_NODE_COMP)\nirq_num = of_irq_get(mscm_node, cfg->inter_core_rx_irq);;
  if (mscm missing?) then (yes)
    :return -ENXIO;
    stop
  endif
  :of_node_put(mscm);
endif
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if (irq_num == irq_num_init[i]?) then (yes)
    :ipc_cdev_priv.instance_id[instance].state = IPC_SHM_INSTANCE_ENABLED\nreturn 0;;
    stop
  endif
  :i++;
endwhile (no)
:irq_num_init[instance] = irq_num;
if (irq_num != IPC_IRQ_NONE?) then (yes)
  :err = request_irq(irq_num, ipcsShmHardirq, 0, DRIVER_NAME, &ipc_cdev_priv);;
  if (request_irq failed?) then (yes)
    :return -ENXIO;
    stop
  endif
endif
:ipc_cdev_priv.instance_id[instance].state = IPC_SHM_INSTANCE_ENABLED\nreturn 0;;
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
:err = alloc_chrdev_region(&dev_major_num, 0, 1, DEVICE_NAME);;
if (err != 0?) then (yes)
  :return err;
  stop
endif
:ipc_class = class_create(THIS_MODULE, DEVICE_NAME)\ncdev_init(&ipc_cdev, &ipc_fops)\ncdev_add(&ipc_cdev, dev_major_num, 1);;
:device_create(ipc_class, NULL, dev_major_num, NULL, DEVICE_NAME);;
:dev_is_opened = 0; wait_queue_flag = SLEEP;
:init_waitqueue_head(&wait_queue);
:return 0;
stop
""",
    "linux_6_5_21_ipcsCdevClean": """
start
:i = 0;
while (i < IPC_SHM_MAX_INSTANCES?) is (yes)
  if ((instance_id[i].state != IPC_SHM_INSTANCE_DISABLED) && (instance_id[i].irq_num != IPC_IRQ_NONE)?) then (yes)
    :ipcsHwIrqDisable(i);
    :instance_id[i].state = IPC_SHM_INSTANCE_DISABLED;
    if (irq_num_init[i] != 0?) then (yes)
      :free_irq(instance_id[i].irq_num, &ipc_cdev_priv);
      :irq_num_init[i] = 0;
    endif
  endif
  :i++;
endwhile (no)
:cdev_del(&ipc_cdev);
:device_destroy(ipc_class, dev_major_num);
:class_destroy(ipc_class);
:unregister_chrdev_region(dev_major_num, 1);
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
  :return -EINVAL;
  stop
endif
:ipc_mscm = (struct IPCS_MSCM_REGS_TYPE *)mscm_addr;;
:trust_cores = (local_core->trusted & 0xF) | ((local_core->trusted & 0xF0) << 4);;
:switch(local_core->type)\ncase IPC_CORE_A53: switch(local_core->index) set local_core_idx\ncase IPC_CORE_DEFAULT: local_core_idx = IPC_DEFAULT_LOCAL_CORE\ndefault: return -EINVAL;;
if (invalid local_core?) then (yes)
  :return -EINVAL; stop
endif
if ((!trust_cores) || (trust_cores & ~IPC_MSCM_IRCPCFG_A53_TR) || ((1u << local_core_idx) & ~trust_cores)?) then (yes)
  :return -EINVAL; stop
endif
:switch(remote_core->type)\ncase IPC_CORE_A53/M7: switch(remote_core->index) set remote_core_idx\ncase IPC_CORE_DEFAULT: remote_core_idx = IPC_DEFAULT_REMOTE_CORE\ndefault: return -EINVAL;;
if (invalid remote_core?) then (yes)
  :return -EINVAL; stop
endif
if (((tx_irq != IPC_IRQ_NONE) && (tx_irq == rx_irq)) || (remote_core_idx == readl(&ipc_mscm->CPXNUM)) || (remote_core_idx == local_core_idx)?) then (yes)
  :return -EINVAL; stop
endif
:switch(tx_irq): IPC_IRQ_NONE break; 0->0; 1->1; 2->2; 3->5; 4->6; 5->7; 6->8; 7->9; 8->10; 9->11; 10->12; 11->13\nswitch(rx_irq): IPC_IRQ_NONE break; 0->spi1/msi0; 1->spi2/msi1; 2->spi3/msi2; 3->spi22/msi5; 4->spi23/msi6; 5->spi68/msi7; 6->spi69/msi8; 7->spi164/msi9; 8->spi165/msi10; 9->spi166/msi11; 10->spi167/msi12; 11->spi168/msi13;;
if (invalid irq mapping?) then (yes)
  :return -EINVAL; stop
endif
:mscm_tx_irq = tx_irq; mscm_rx_irq = rx_irq; remote_core = remote_core_idx; local_core = local_core_idx;;
:ipcsHwIrqDisable(instance);;
:ircpcfg_mask = readl(&ipc_mscm->IRCPCFG);;
if (ircpcfg_mask & IPC_MSCM_IRCPCFG_LOCK?) then (yes)
  :return -EACCES; stop
else (no)
  :writel(ircpcfg_mask | trust_cores, &ipc_mscm->IRCPCFG);;
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
