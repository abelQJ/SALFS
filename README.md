# SALFS
一个简化版本的自动化[LFS](http://www.linuxfromscratch.org/lfs/)编译框架,软件包对应lfs-8.0

该框架部分代码来自[ALFS](http://www.linuxfromscratch.org/alfs/)项目

# 使用方法：
1. 首先自行格式化磁盘、分区并挂载
   ```
   sudo fdisk /dev/sdb
   sudo mkfs.ext4 /dev/sdb1
   sudo mount /dev/sdb1 /mnt/lfs
   ```
2. 将ALFS目录和source目录拷贝至/mnt/lfs下,source目录从[SALFS-Sources](https://github.com/abelQJ/SALFS-Sources)下载
3. 修改/mnt/lfs目录为任意用户可读写
   ```
   sudo chmod a+rwx /mnt/lfs
   ```
4. 进入目录/mnt/lfs/ALFS执行命令
   ```
   python gen_makefile.py
   make
   ```
   大约经过10个小时即可完成编译
   
# 其他说明

a. 内核定制需要自行运行make menuconfig将配置生成的config文件保存在source目录下，文件名为kernel_config

b. 需要安装grub到mbr，在整个编译完成后自行执行grub-install /dev/sdb

c. 如果目标磁盘不是/dev/sdb，需要修改如下文件：153-grub,/etc/fstab将其中磁盘设置做相应修改

  

   

   
