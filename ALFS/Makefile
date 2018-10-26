

SHELL = /bin/bash


SRC            = /sources
MOUNT_PT       = /mnt/lfs
PKG_LST        = unpacked
LUSER          = lfs
LGROUP         = lfs
LHOME          = /home
SCRIPT_ROOT    = ALFS

BASEDIR        = $(MOUNT_PT)
SRCSDIR        = $(BASEDIR)/sources
CMDSDIR        = $(BASEDIR)/$(SCRIPT_ROOT)/lfs-commands
LOGDIR         = $(BASEDIR)/$(SCRIPT_ROOT)/logs
TESTLOGDIR     = $(BASEDIR)/$(SCRIPT_ROOT)/test-logs

crCMDSDIR      = /$(SCRIPT_ROOT)/lfs-commands
crLOGDIR       = /$(SCRIPT_ROOT)/logs
crTESTLOGDIR   = /$(SCRIPT_ROOT)/test-logs
crFILELOGDIR   = /$(SCRIPT_ROOT)/installed-files


SU_LUSER       = sudo -u $(LUSER) -i sh -c
LUSER_HOME     = $(LHOME)/$(LUSER)
PRT_DU         = echo -e "\nKB: `du -skx --exclude=$(SCRIPT_ROOT) --exclude=lost+found $(MOUNT_PT) `\n"
PRT_DU_CR      = echo -e "\nKB: `du -skx --exclude=$(SCRIPT_ROOT) --exclude=lost+found --exclude /var/lib / `\n"



export PATH := ${PATH}:/usr/sbin

include makefile-functions

CHROOT1= /usr/sbin/chroot $(MOUNT_PT) /tools/bin/env -i HOME=/root TERM="$$TERM" PS1='\u:\w\$$ ' PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin /tools/bin/bash --login +h

CHROOT2= /usr/sbin/chroot $(MOUNT_PT) /usr/bin/env -i HOME=/root TERM="$$TERM" PS1='\u:\w\$$ ' PATH=/bin:/usr/bin:/sbin:/usr/sbin /bin/bash --login


all:	ck_UID mk_SETUP mk_LUSER mk_SUDO mk_CHROOT mk_BOOT mk_CUSTOM
	@sudo make do_housekeeping
	@echo 8.0 > lfs-release && \
	sudo mv lfs-release $(MOUNT_PT)/etc && \
	sudo chown root:root $(MOUNT_PT)/etc/lfs-release
	@/bin/echo -e -n \
	DISTRIB_ID=\"Linux From Scratch\"\\n\
	DISTRIB_RELEASE=\"8.0\"\\n\
	DISTRIB_CODENAME=\"abel-alfs\"\\n\
	DISTRIB_DESCRIPTION=\"Linux From Scratch\"\\n\
	> lsb-release && \
	sudo mv lsb-release $(MOUNT_PT)/etc && \
	sudo chown root:root $(MOUNT_PT)/etc/lsb-release
	@$(call echo_finished,8.0)

ck_UID:
	@if [ `id -u` = "0" ]; then \
	  echo "--------------------------------------------------"; \
	  echo "You cannot run this makefile from the root account"; \
	  echo "--------------------------------------------------"; \
	  exit 1; \
	fi

mk_SETUP:
	@$(call echo_SU_request)
	@sudo make BREAKPOINT=$(BREAKPOINT) SETUP
	@touch $@

mk_LUSER: mk_SETUP
	@$(call echo_SULUSER_request)
	@( $(SU_LUSER) "make -C $(MOUNT_PT)/$(SCRIPT_ROOT) BREAKPOINT=$(BREAKPOINT) LUSER" )
	@sudo make restore-luser-env
	@touch $@

mk_SUDO: mk_LUSER
	@sudo make BREAKPOINT=$(BREAKPOINT) SUDO
	@touch $@

mk_CHROOT: mk_SUDO
	@$(call echo_CHROOT_request)
	@( sudo $(CHROOT1) -c "cd $(SCRIPT_ROOT) && make BREAKPOINT=$(BREAKPOINT) CHROOT")
	@touch $@

mk_BOOT: mk_CHROOT
	@$(call echo_CHROOT_request)
	@( sudo $(CHROOT2) -c "cd $(SCRIPT_ROOT) && make BREAKPOINT=$(BREAKPOINT) BOOT")
	@touch $@

mk_CUSTOM: mk_BOOT
	@$(call echo_CHROOT_request)
	@( sudo $(CHROOT2) -c "cd $(SCRIPT_ROOT) && make BREAKPOINT=$(BREAKPOINT) CUSTOM")
	@touch $@	

devices: 
	sudo mount -v --bind /dev $(MOUNT_PT)/dev
	sudo mount -vt devpts devpts $(MOUNT_PT)/dev/pts
	sudo mount -vt proc proc $(MOUNT_PT)/proc
	sudo mount -vt sysfs sysfs $(MOUNT_PT)/sys
	sudo mount -vt tmpfs tmpfs $(MOUNT_PT)/run
	if [ -h $(MOUNT_PT)/dev/shm ]; then \
	  sudo mkdir -p $(MOUNT_PT)/$$(readlink $(MOUNT_PT)/dev/shm); \
	fi
	@touch $@

teardown:
	sudo umount -v $(MOUNT_PT)/sys
	sudo umount -v $(MOUNT_PT)/proc
	sudo umount -v $(MOUNT_PT)/dev/pts
	if mountpoint -q $(MOUNT_PT)/run; then \
	  sudo umount -v $(MOUNT_PT)/run; \
	elif [ -h $(MOUNT_PT)/dev/shm ]; then \
	  link=$$(readlink $(MOUNT_PT)/dev/shm); \
	  sudo umount -v $(MOUNT_PT)/$$link; \
	  unset link; \
	else \
	  sudo umount -v $(MOUNT_PT)/dev/shm; \
	fi
	sudo umount -v $(MOUNT_PT)/dev

chroot: devices
	sudo $(CHROOT2)
	$(MAKE) teardown


restore-luser-env:
	@$(call echo_message, Building)
	@if [ -f $(LUSER_HOME)/.bashrc.XXX ]; then \
		mv -f $(LUSER_HOME)/.bashrc.XXX $(LUSER_HOME)/.bashrc; \
	fi;
	@if [ -f $(LUSER_HOME)/.bash_profile.XXX ]; then \
		mv $(LUSER_HOME)/.bash_profile.XXX $(LUSER_HOME)/.bash_profile; \
	fi;
	@chown $(LUSER):$(LGROUP) $(LUSER_HOME)/.bash*
	@$(call housekeeping)

do_housekeeping:
	@-umount $(MOUNT_PT)/sys
	@-umount $(MOUNT_PT)/proc
	@-if mountpoint -q $(MOUNT_PT)/run; then \
	  umount $(MOUNT_PT)/run; \
	elif [ -h $(MOUNT_PT)/dev/shm ]; then \
	  link=$$(readlink $(MOUNT_PT)/dev/shm); \
	  umount $(MOUNT_PT)/$$link; \
	  unset link; \
	else \
	  umount $(MOUNT_PT)/dev/shm; \
	fi
	@-umount $(MOUNT_PT)/dev/pts
	@-umount $(MOUNT_PT)/dev
	@-rm /tools
	@-if [ ! -f luser-exist ]; then \
		userdel $(LUSER); \
		rm -rf $(LUSER_HOME); \
	fi;


020-creatingtoolsdir:
	@$(call echo_message, Building)
	@mkdir $(MOUNT_PT)/tools && \
	rm -f /tools && \
	ln -s $(MOUNT_PT)/tools /
	@$(call housekeeping)

021-addinguser:  020-creatingtoolsdir
	@$(call echo_message, Building)
	@-if [ ! -d $(LUSER_HOME) ]; then \
		groupadd $(LGROUP); \
		useradd -s /bin/bash -g $(LGROUP) -m -k /dev/null $(LUSER); \
	else \
		touch luser-exist; \
	fi;
	@chown $(LUSER) $(MOUNT_PT)/tools && \
	chmod -R a+wt $(MOUNT_PT)/$(SCRIPT_ROOT) && \
	chmod a+wt $(SRCSDIR)
	@$(call housekeeping)

022-settingenvironment:  021-addinguser
	@$(call echo_message, Building)
	@if [ -f $(LUSER_HOME)/.bashrc -a ! -f $(LUSER_HOME)/.bashrc.XXX ]; then \
		mv $(LUSER_HOME)/.bashrc $(LUSER_HOME)/.bashrc.XXX; \
	fi;
	@if [ -f $(LUSER_HOME)/.bash_profile  -a ! -f $(LUSER_HOME)/.bash_profile.XXX ]; then \
		mv $(LUSER_HOME)/.bash_profile $(LUSER_HOME)/.bash_profile.XXX; \
	fi;
	@echo "set +h" > $(LUSER_HOME)/.bashrc && \
	echo "umask 022" >> $(LUSER_HOME)/.bashrc && \
	echo "LFS=$(MOUNT_PT)" >> $(LUSER_HOME)/.bashrc && \
	echo "LC_ALL=POSIX" >> $(LUSER_HOME)/.bashrc && \
	echo "LFS_TGT=x86_64-lfs-linux-gnu" >> $(LUSER_HOME)/.bashrc && \
	echo "PATH=/tools/bin:/bin:/usr/bin" >> $(LUSER_HOME)/.bashrc && \
	echo "export LFS LC_ALL LFS_TGT PATH" >> $(LUSER_HOME)/.bashrc && \
	echo "source /mnt/lfs/$(SCRIPT_ROOT)/envars" >> $(LUSER_HOME)/.bashrc && \
	chown $(LUSER):$(LGROUP) $(LUSER_HOME)/.bashrc && \
	touch envars && \
	chown $(LUSER) envars
	@$(call housekeeping)




SETUP:         020-creatingtoolsdir 021-addinguser 022-settingenvironment



LUSER:         LUSER_BEGIN LUSER_END
SUDO:          SUDO_BEGIN SUDO_END
CHROOT:        SHELL=/tools/bin/bash
CHROOT:        CHROOT_BEGIN CHROOT_END
BOOT:          BOOT_BEGIN BOOT_END
CUSTOM:        CUSTOM_BEGIN CUSTOM_END






LUSER_BEGIN:  022-settingenvironment
	@touch $@


034-binutils-pass1:  LUSER_BEGIN
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,binutils-2.27.tar.bz2)
	@$(call unpack,binutils-2.27.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/034-binutils-pass1 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,034-binutils-pass1)
	@$(call housekeeping)


035-gcc-pass1:  034-binutils-pass1
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gcc-6.3.0.tar.bz2)
	@$(call unpack,gcc-6.3.0.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/035-gcc-pass1 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,035-gcc-pass1)
	@$(call housekeeping)


036-linux-headers:  035-gcc-pass1
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,linux-4.9.9.tar.xz)
	@$(call unpack,linux-4.9.9.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/036-linux-headers >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,036-linux-headers)
	@$(call housekeeping)


037-glibc:  036-linux-headers
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,glibc-2.25.tar.xz)
	@$(call unpack,glibc-2.25.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/037-glibc >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,037-glibc)
	@$(call housekeeping)


038-gcc-libstdc++:  037-glibc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gcc-6.3.0.tar.bz2)
	@$(call unpack,gcc-6.3.0.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/038-gcc-libstdc++ >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,038-gcc-libstdc++)
	@$(call housekeeping)


039-binutils-pass2:  038-gcc-libstdc++
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,binutils-2.27.tar.bz2)
	@$(call unpack,binutils-2.27.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/039-binutils-pass2 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,039-binutils-pass2)
	@$(call housekeeping)


040-gcc-pass2:  039-binutils-pass2
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gcc-6.3.0.tar.bz2)
	@$(call unpack,gcc-6.3.0.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/040-gcc-pass2 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,040-gcc-pass2)
	@$(call housekeeping)


041-tcl:  040-gcc-pass2
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,tcl-core8.6.6-src.tar.gz)
	@$(call unpack,tcl-core8.6.6-src.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/041-tcl >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,041-tcl)
	@$(call housekeeping)


042-expect:  041-tcl
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,expect5.45.tar.gz)
	@$(call unpack,expect5.45.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/042-expect >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,042-expect)
	@$(call housekeeping)


043-dejagnu:  042-expect
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,dejagnu-1.6.tar.gz)
	@$(call unpack,dejagnu-1.6.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/043-dejagnu >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,043-dejagnu)
	@$(call housekeeping)


044-check:  043-dejagnu
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,check-0.11.0.tar.gz)
	@$(call unpack,check-0.11.0.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/044-check >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,044-check)
	@$(call housekeeping)


045-ncurses:  044-check
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,ncurses-6.0.tar.gz)
	@$(call unpack,ncurses-6.0.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/045-ncurses >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,045-ncurses)
	@$(call housekeeping)


046-bash:  045-ncurses
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,bash-4.4.tar.gz)
	@$(call unpack,bash-4.4.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/046-bash >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,046-bash)
	@$(call housekeeping)


047-bison:  046-bash
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,bison-3.0.4.tar.xz)
	@$(call unpack,bison-3.0.4.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/047-bison >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,047-bison)
	@$(call housekeeping)


048-bzip2:  047-bison
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,bzip2-1.0.6.tar.gz)
	@$(call unpack,bzip2-1.0.6.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/048-bzip2 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,048-bzip2)
	@$(call housekeeping)


049-coreutils:  048-bzip2
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,coreutils-8.26.tar.xz)
	@$(call unpack,coreutils-8.26.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/049-coreutils >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,049-coreutils)
	@$(call housekeeping)


050-diffutils:  049-coreutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,diffutils-3.5.tar.xz)
	@$(call unpack,diffutils-3.5.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/050-diffutils >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,050-diffutils)
	@$(call housekeeping)


051-file:  050-diffutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,file-5.30.tar.gz)
	@$(call unpack,file-5.30.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/051-file >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,051-file)
	@$(call housekeeping)


052-findutils:  051-file
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,findutils-4.6.0.tar.gz)
	@$(call unpack,findutils-4.6.0.tar.gz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/052-findutils >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,052-findutils)
	@$(call housekeeping)


053-gawk:  052-findutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gawk-4.1.4.tar.xz)
	@$(call unpack,gawk-4.1.4.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/053-gawk >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,053-gawk)
	@$(call housekeeping)


054-gettext:  053-gawk
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gettext-0.19.8.1.tar.xz)
	@$(call unpack,gettext-0.19.8.1.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/054-gettext >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,054-gettext)
	@$(call housekeeping)


055-grep:  054-gettext
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,grep-3.0.tar.xz)
	@$(call unpack,grep-3.0.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/055-grep >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,055-grep)
	@$(call housekeeping)


056-gzip:  055-grep
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,gzip-1.8.tar.xz)
	@$(call unpack,gzip-1.8.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/056-gzip >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,056-gzip)
	@$(call housekeeping)


057-m4:  056-gzip
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,m4-1.4.18.tar.xz)
	@$(call unpack,m4-1.4.18.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/057-m4 >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,057-m4)
	@$(call housekeeping)


058-make:  057-m4
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,make-4.2.1.tar.bz2)
	@$(call unpack,make-4.2.1.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/058-make >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,058-make)
	@$(call housekeeping)


059-patch:  058-make
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,patch-2.7.5.tar.xz)
	@$(call unpack,patch-2.7.5.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/059-patch >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,059-patch)
	@$(call housekeeping)


060-perl:  059-patch
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,perl-5.24.1.tar.bz2)
	@$(call unpack,perl-5.24.1.tar.bz2)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/060-perl >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,060-perl)
	@$(call housekeeping)


061-sed:  060-perl
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,sed-4.4.tar.xz)
	@$(call unpack,sed-4.4.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/061-sed >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,061-sed)
	@$(call housekeeping)


062-tar:  061-sed
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,tar-1.29.tar.xz)
	@$(call unpack,tar-1.29.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/062-tar >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,062-tar)
	@$(call housekeeping)


063-texinfo:  062-tar
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,texinfo-6.3.tar.xz)
	@$(call unpack,texinfo-6.3.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/063-texinfo >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,063-texinfo)
	@$(call housekeeping)


064-util-linux:  063-texinfo
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,util-linux-2.29.1.tar.xz)
	@$(call unpack,util-linux-2.29.1.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/064-util-linux >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,064-util-linux)
	@$(call housekeeping)


065-xz:  064-util-linux
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,xz-5.2.3.tar.xz)
	@$(call unpack,xz-5.2.3.tar.xz)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/tmp_tools/065-xz >> logs/@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,065-xz)
	@$(call housekeeping)


066-stripping:  065-xz
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@source ~/.bashrc && 	$(CMDSDIR)/tmp_tools/066-stripping >> logs/$@ 2>&1 && 	$(PRT_DU) >>logs/$@
	@$(call housekeeping)


LUSER_END:  066-stripping
	@touch $@


SUDO_BEGIN:  LUSER_END
	@touch $@


067-changingowner:  SUDO_BEGIN
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@export LFS=$(MOUNT_PT) && \
	lfs-commands/prepare/067-changingowner >>logs/$@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call housekeeping)


069-kernfs:  067-changingowner
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@export LFS=$(MOUNT_PT) && \
	lfs-commands/prepare/069-kernfs >>logs/$@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call housekeeping)


DEVICES:  069-kernfs
	@make devices
	@touch $@


SUDO_END:  DEVICES
	@touch $@


CHROOT_BEGIN:  SUDO_END
	@touch $@


072-creatingdirs:  CHROOT_BEGIN
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/072-creatingdirs >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



073-createfiles:  072-creatingdirs
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/073-createfiles >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



074-linux-headers:  073-createfiles
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,linux-4.9.9.tar.xz)
	@$(call unpack2,linux-4.9.9.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/074-linux-headers >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,074-linux-headers)
	@$(call log_new_files,074-linux-headers)
	@$(call housekeeping)


075-man-pages:  074-linux-headers
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,man-pages-4.09.tar.xz)
	@$(call unpack2,man-pages-4.09.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/075-man-pages >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,075-man-pages)
	@$(call log_new_files,075-man-pages)
	@$(call housekeeping)


076-glibc:  075-man-pages
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,glibc-2.25.tar.xz)
	@$(call unpack2,glibc-2.25.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/076-glibc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,076-glibc)
	@$(call log_new_files,076-glibc)
	@$(call housekeeping)


077-adjusting:  076-glibc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/077-adjusting >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



078-zlib:  077-adjusting
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,zlib-1.2.11.tar.xz)
	@$(call unpack2,zlib-1.2.11.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/078-zlib >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,078-zlib)
	@$(call log_new_files,078-zlib)
	@$(call housekeeping)


079-file:  078-zlib
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,file-5.30.tar.gz)
	@$(call unpack2,file-5.30.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/079-file >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,079-file)
	@$(call log_new_files,079-file)
	@$(call housekeeping)


080-binutils:  079-file
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,binutils-2.27.tar.bz2)
	@$(call unpack2,binutils-2.27.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/080-binutils >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,080-binutils)
	@$(call log_new_files,080-binutils)
	@$(call housekeeping)


081-gmp:  080-binutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gmp-6.1.2.tar.xz)
	@$(call unpack2,gmp-6.1.2.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/081-gmp >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,081-gmp)
	@$(call log_new_files,081-gmp)
	@$(call housekeeping)


082-mpfr:  081-gmp
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,mpfr-3.1.5.tar.xz)
	@$(call unpack2,mpfr-3.1.5.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/082-mpfr >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,082-mpfr)
	@$(call log_new_files,082-mpfr)
	@$(call housekeeping)


083-mpc:  082-mpfr
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,mpc-1.0.3.tar.gz)
	@$(call unpack2,mpc-1.0.3.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/083-mpc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,083-mpc)
	@$(call log_new_files,083-mpc)
	@$(call housekeeping)


084-gcc:  083-mpc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gcc-6.3.0.tar.bz2)
	@$(call unpack2,gcc-6.3.0.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/084-gcc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,084-gcc)
	@$(call log_new_files,084-gcc)
	@$(call housekeeping)


085-bzip2:  084-gcc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,bzip2-1.0.6.tar.gz)
	@$(call unpack2,bzip2-1.0.6.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/085-bzip2 >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,085-bzip2)
	@$(call log_new_files,085-bzip2)
	@$(call housekeeping)


086-pkg-config:  085-bzip2
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,pkg-config-0.29.1.tar.gz)
	@$(call unpack2,pkg-config-0.29.1.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/086-pkg-config >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,086-pkg-config)
	@$(call log_new_files,086-pkg-config)
	@$(call housekeeping)


087-ncurses:  086-pkg-config
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,ncurses-6.0.tar.gz)
	@$(call unpack2,ncurses-6.0.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/087-ncurses >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,087-ncurses)
	@$(call log_new_files,087-ncurses)
	@$(call housekeeping)


088-attr:  087-ncurses
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,attr-2.4.47.src.tar.gz)
	@$(call unpack2,attr-2.4.47.src.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/088-attr >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,088-attr)
	@$(call log_new_files,088-attr)
	@$(call housekeeping)


089-acl:  088-attr
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,acl-2.2.52.src.tar.gz)
	@$(call unpack2,acl-2.2.52.src.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/089-acl >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,089-acl)
	@$(call log_new_files,089-acl)
	@$(call housekeeping)


090-libcap:  089-acl
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,libcap-2.25.tar.xz)
	@$(call unpack2,libcap-2.25.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/090-libcap >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,090-libcap)
	@$(call log_new_files,090-libcap)
	@$(call housekeeping)


091-sed:  090-libcap
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,sed-4.4.tar.xz)
	@$(call unpack2,sed-4.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/091-sed >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,091-sed)
	@$(call log_new_files,091-sed)
	@$(call housekeeping)


092-shadow:  091-sed
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,shadow-4.4.tar.xz)
	@$(call unpack2,shadow-4.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/092-shadow >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,092-shadow)
	@$(call log_new_files,092-shadow)
	@$(call housekeeping)


093-psmisc:  092-shadow
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,psmisc-22.21.tar.gz)
	@$(call unpack2,psmisc-22.21.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/093-psmisc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,093-psmisc)
	@$(call log_new_files,093-psmisc)
	@$(call housekeeping)


094-iana-etc:  093-psmisc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,iana-etc-2.30.tar.bz2)
	@$(call unpack2,iana-etc-2.30.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/094-iana-etc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,094-iana-etc)
	@$(call log_new_files,094-iana-etc)
	@$(call housekeeping)


095-m4:  094-iana-etc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,m4-1.4.18.tar.xz)
	@$(call unpack2,m4-1.4.18.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/095-m4 >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,095-m4)
	@$(call log_new_files,095-m4)
	@$(call housekeeping)


096-bison:  095-m4
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,bison-3.0.4.tar.xz)
	@$(call unpack2,bison-3.0.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/096-bison >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,096-bison)
	@$(call log_new_files,096-bison)
	@$(call housekeeping)


097-flex:  096-bison
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,flex-2.6.3.tar.gz)
	@$(call unpack2,flex-2.6.3.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/097-flex >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,097-flex)
	@$(call log_new_files,097-flex)
	@$(call housekeeping)


098-grep:  097-flex
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,grep-3.0.tar.xz)
	@$(call unpack2,grep-3.0.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/098-grep >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,098-grep)
	@$(call log_new_files,098-grep)
	@$(call housekeeping)


099-readline:  098-grep
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,readline-7.0.tar.gz)
	@$(call unpack2,readline-7.0.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/099-readline >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,099-readline)
	@$(call log_new_files,099-readline)
	@$(call housekeeping)


100-bash:  099-readline
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,bash-4.4.tar.gz)
	@$(call unpack2,bash-4.4.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/100-bash >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,100-bash)
	@$(call log_new_files,100-bash)
	@$(call housekeeping)


101-bc:  100-bash
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,bc-1.06.95.tar.bz2)
	@$(call unpack2,bc-1.06.95.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/101-bc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,101-bc)
	@$(call log_new_files,101-bc)
	@$(call housekeeping)


102-libtool:  101-bc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,libtool-2.4.6.tar.xz)
	@$(call unpack2,libtool-2.4.6.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/102-libtool >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,102-libtool)
	@$(call log_new_files,102-libtool)
	@$(call housekeeping)


103-gdbm:  102-libtool
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gdbm-1.12.tar.gz)
	@$(call unpack2,gdbm-1.12.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/103-gdbm >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,103-gdbm)
	@$(call log_new_files,103-gdbm)
	@$(call housekeeping)


104-gperf:  103-gdbm
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gperf-3.0.4.tar.gz)
	@$(call unpack2,gperf-3.0.4.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/104-gperf >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,104-gperf)
	@$(call log_new_files,104-gperf)
	@$(call housekeeping)


105-expat:  104-gperf
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,expat-2.2.0.tar.bz2)
	@$(call unpack2,expat-2.2.0.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/105-expat >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,105-expat)
	@$(call log_new_files,105-expat)
	@$(call housekeeping)


106-inetutils:  105-expat
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,inetutils-1.9.4.tar.xz)
	@$(call unpack2,inetutils-1.9.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/106-inetutils >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,106-inetutils)
	@$(call log_new_files,106-inetutils)
	@$(call housekeeping)


107-perl:  106-inetutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,perl-5.24.1.tar.bz2)
	@$(call unpack2,perl-5.24.1.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/107-perl >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,107-perl)
	@$(call log_new_files,107-perl)
	@$(call housekeeping)


108-xml-parser:  107-perl
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,XML-Parser-2.44.tar.gz)
	@$(call unpack2,XML-Parser-2.44.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/108-xml-parser >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,108-xml-parser)
	@$(call log_new_files,108-xml-parser)
	@$(call housekeeping)


109-intltool:  108-xml-parser
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,intltool-0.51.0.tar.gz)
	@$(call unpack2,intltool-0.51.0.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/109-intltool >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,109-intltool)
	@$(call log_new_files,109-intltool)
	@$(call housekeeping)


110-autoconf:  109-intltool
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,autoconf-2.69.tar.xz)
	@$(call unpack2,autoconf-2.69.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/110-autoconf >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,110-autoconf)
	@$(call log_new_files,110-autoconf)
	@$(call housekeeping)


111-automake:  110-autoconf
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,automake-1.15.tar.xz)
	@$(call unpack2,automake-1.15.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/111-automake >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,111-automake)
	@$(call log_new_files,111-automake)
	@$(call housekeeping)


112-xz:  111-automake
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,xz-5.2.3.tar.xz)
	@$(call unpack2,xz-5.2.3.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/112-xz >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,112-xz)
	@$(call log_new_files,112-xz)
	@$(call housekeeping)


113-kmod:  112-xz
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,kmod-23.tar.xz)
	@$(call unpack2,kmod-23.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/113-kmod >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,113-kmod)
	@$(call log_new_files,113-kmod)
	@$(call housekeeping)


114-gettext:  113-kmod
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gettext-0.19.8.1.tar.xz)
	@$(call unpack2,gettext-0.19.8.1.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/114-gettext >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,114-gettext)
	@$(call log_new_files,114-gettext)
	@$(call housekeeping)


115-procps-ng:  114-gettext
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,procps-ng-3.3.12.tar.xz)
	@$(call unpack2,procps-ng-3.3.12.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/115-procps-ng >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,115-procps-ng)
	@$(call log_new_files,115-procps-ng)
	@$(call housekeeping)


116-e2fsprogs:  115-procps-ng
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,e2fsprogs-1.43.4.tar.gz)
	@$(call unpack2,e2fsprogs-1.43.4.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/116-e2fsprogs >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,116-e2fsprogs)
	@$(call log_new_files,116-e2fsprogs)
	@$(call housekeeping)


117-coreutils:  116-e2fsprogs
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,coreutils-8.26.tar.xz)
	@$(call unpack2,coreutils-8.26.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/117-coreutils >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,117-coreutils)
	@$(call log_new_files,117-coreutils)
	@$(call housekeeping)


118-diffutils:  117-coreutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,diffutils-3.5.tar.xz)
	@$(call unpack2,diffutils-3.5.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/118-diffutils >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,118-diffutils)
	@$(call log_new_files,118-diffutils)
	@$(call housekeeping)


119-gawk:  118-diffutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gawk-4.1.4.tar.xz)
	@$(call unpack2,gawk-4.1.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/119-gawk >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,119-gawk)
	@$(call log_new_files,119-gawk)
	@$(call housekeeping)


120-findutils:  119-gawk
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,findutils-4.6.0.tar.gz)
	@$(call unpack2,findutils-4.6.0.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/120-findutils >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,120-findutils)
	@$(call log_new_files,120-findutils)
	@$(call housekeeping)


121-groff:  120-findutils
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,groff-1.22.3.tar.gz)
	@$(call unpack2,groff-1.22.3.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/121-groff >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,121-groff)
	@$(call log_new_files,121-groff)
	@$(call housekeeping)


122-grub:  121-groff
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,grub-2.02~beta3.tar.xz)
	@$(call unpack2,grub-2.02~beta3.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/122-grub >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,122-grub)
	@$(call log_new_files,122-grub)
	@$(call housekeeping)


123-less:  122-grub
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,less-481.tar.gz)
	@$(call unpack2,less-481.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/123-less >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,123-less)
	@$(call log_new_files,123-less)
	@$(call housekeeping)


124-gzip:  123-less
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,gzip-1.8.tar.xz)
	@$(call unpack2,gzip-1.8.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/124-gzip >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,124-gzip)
	@$(call log_new_files,124-gzip)
	@$(call housekeeping)


125-iproute2:  124-gzip
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,iproute2-4.9.0.tar.xz)
	@$(call unpack2,iproute2-4.9.0.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/125-iproute2 >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,125-iproute2)
	@$(call log_new_files,125-iproute2)
	@$(call housekeeping)


126-kbd:  125-iproute2
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,kbd-2.0.4.tar.xz)
	@$(call unpack2,kbd-2.0.4.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/126-kbd >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,126-kbd)
	@$(call log_new_files,126-kbd)
	@$(call housekeeping)


127-libpipeline:  126-kbd
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,libpipeline-1.4.1.tar.gz)
	@$(call unpack2,libpipeline-1.4.1.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/127-libpipeline >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,127-libpipeline)
	@$(call log_new_files,127-libpipeline)
	@$(call housekeeping)


128-make:  127-libpipeline
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,make-4.2.1.tar.bz2)
	@$(call unpack2,make-4.2.1.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/128-make >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,128-make)
	@$(call log_new_files,128-make)
	@$(call housekeeping)


129-patch:  128-make
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,patch-2.7.5.tar.xz)
	@$(call unpack2,patch-2.7.5.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/129-patch >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,129-patch)
	@$(call log_new_files,129-patch)
	@$(call housekeeping)


130-sysklogd:  129-patch
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,sysklogd-1.5.1.tar.gz)
	@$(call unpack2,sysklogd-1.5.1.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/130-sysklogd >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,130-sysklogd)
	@$(call log_new_files,130-sysklogd)
	@$(call housekeeping)


131-sysvinit:  130-sysklogd
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,sysvinit-2.88dsf.tar.bz2)
	@$(call unpack2,sysvinit-2.88dsf.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/131-sysvinit >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,131-sysvinit)
	@$(call log_new_files,131-sysvinit)
	@$(call housekeeping)


132-eudev:  131-sysvinit
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,eudev-3.2.1.tar.gz)
	@$(call unpack2,eudev-3.2.1.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/132-eudev >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,132-eudev)
	@$(call log_new_files,132-eudev)
	@$(call housekeeping)


133-util-linux:  132-eudev
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,util-linux-2.29.1.tar.xz)
	@$(call unpack2,util-linux-2.29.1.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/133-util-linux >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,133-util-linux)
	@$(call log_new_files,133-util-linux)
	@$(call housekeeping)


134-man-db:  133-util-linux
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,man-db-2.7.6.1.tar.xz)
	@$(call unpack2,man-db-2.7.6.1.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/134-man-db >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,134-man-db)
	@$(call log_new_files,134-man-db)
	@$(call housekeeping)


135-tar:  134-man-db
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,tar-1.29.tar.xz)
	@$(call unpack2,tar-1.29.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/135-tar >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,135-tar)
	@$(call log_new_files,135-tar)
	@$(call housekeeping)


136-texinfo:  135-tar
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,texinfo-6.3.tar.xz)
	@$(call unpack2,texinfo-6.3.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/136-texinfo >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,136-texinfo)
	@$(call log_new_files,136-texinfo)
	@$(call housekeeping)


137-vim:  136-texinfo
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,vim-8.0.069.tar.bz2)
	@$(call unpack2,vim-8.0.069.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/137-vim >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,137-vim)
	@$(call log_new_files,137-vim)
	@$(call housekeeping)


140-revisedchroot:  137-vim
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/base_tools/140-revisedchroot >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



CHROOT_END:  140-revisedchroot
	@touch $@


BOOT_BEGIN:  CHROOT_END
	@touch $@


142-bootscripts:  BOOT_BEGIN
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,lfs-bootscripts-20150222.tar.bz2)
	@$(call unpack2,lfs-bootscripts-20150222.tar.bz2)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/boot/142-bootscripts >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,142-bootscripts)
	@$(call log_new_files,142-bootscripts)
	@$(call housekeeping)


144-symlinks:  142-bootscripts
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/144-symlinks >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



145-network:  144-symlinks
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/145-network >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



146-usage:  145-network
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/146-usage >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



147-profile:  146-usage
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/147-profile >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



148-inputrc:  147-profile
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/148-inputrc >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



149-etcshells:  148-inputrc
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/149-etcshells >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



151-fstab:  149-etcshells
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/151-fstab >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



152-kernel:  151-fstab
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,linux-4.9.9.tar.xz)
	@$(call unpack2,linux-4.9.9.tar.xz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/boot/152-kernel >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,152-kernel)
	@$(call log_new_files,152-kernel)
	@$(call housekeeping)


153-grub:  152-kernel
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \
	$(crCMDSDIR)/boot/153-grub >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)



BOOT_END:  153-grub
	@touch $@


CUSTOM_BEGIN:  BOOT_END
	@touch $@


201-openssl:  CUSTOM_BEGIN
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,openssl-1.0.2k.tar)
	@$(call unpack2,openssl-1.0.2k.tar)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/user/201-openssl >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,201-openssl)
	@$(call log_new_files,201-openssl)
	@$(call housekeeping)


202-openssh:  201-openssl
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,openssh-7.4p1.tar)
	@$(call unpack2,openssh-7.4p1.tar)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/user/202-openssh >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,202-openssh)
	@$(call log_new_files,202-openssh)
	@$(call housekeeping)


203-CAC:  202-openssh
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,CAC.tar.gz)
	@$(call unpack2,CAC.tar.gz)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/user/203-CAC >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,203-CAC)
	@$(call log_new_files,203-CAC)
	@$(call housekeeping)


204-curl:  203-CAC
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,curl-7.52.1.tar.lzma)
	@$(call unpack2,curl-7.52.1.tar.lzma)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \
	$(crCMDSDIR)/user/204-curl >>logs/$@ 2>&1 && \
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,204-curl)
	@$(call log_new_files,204-curl)
	@$(call housekeeping)


CUSTOM_END:  204-curl
	@touch $@
