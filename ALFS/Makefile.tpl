

SHELL = /bin/bash

__VAR_DEF_TPL__

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


__STAGE_GROUP_TPL__



__DEP_DETAILS_TPL__