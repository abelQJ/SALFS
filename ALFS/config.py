var_def = '''
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
'''


stage_group = '''
LUSER:         LUSER_BEGIN LUSER_END
SUDO:          SUDO_BEGIN SUDO_END
CHROOT:        SHELL=/tools/bin/bash
CHROOT:        CHROOT_BEGIN CHROOT_END
BOOT:          BOOT_BEGIN BOOT_END
CUSTOM:        CUSTOM_BEGIN CUSTOM_END
'''

make_cmd_tpl_map = {
'cmd_full_path_with_pkg' : '''
__TARGET__:  __DEP__
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@$(call remove_existing_dirs,__PKG_NAME__)
	@$(call unpack,__PKG_NAME__)
	@$(call get_pkg_root_LUSER)
	@echo "export  TEST_LOG=$(TESTLOGDIR)/$@" >> envars && \\
	echo "$(nl_)`date`$(nl_)" >$(TESTLOGDIR)/$@
	@source ~/.bashrc && \\
	$(CMDSDIR)/__TARGET_SHELL__ >> logs/@ 2>&1 && \\
	$(PRT_DU) >>logs/$@
	@$(call remove_build_dirs,__NAME_FORM_TARGET__)
	@$(call housekeeping)
'''
,

'cmd_full_path_no_pkg' : '''
__TARGET__:  __DEP__
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@source ~/.bashrc && \
	$(CMDSDIR)/__TARGET_SHELL__ >> logs/$@ 2>&1 && \
	$(PRT_DU) >>logs/$@
	@$(call housekeeping)
'''
,

'cmd_root_path_no_pkg' : '''
__TARGET__:  __DEP__
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@source envars && \\
	$(crCMDSDIR)/__TARGET_SHELL__ >>logs/$@ 2>&1 && \\
	$(PRT_DU_CR) >>logs/$@
	@$(call housekeeping)

'''
,

'cmd_root_path_with_pkg' : '''
__TARGET__:  __DEP__
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU_CR) >>logs/$@
	@$(call touch_timestamp)
	@$(call remove_existing_dirs2,__PKG_NAME__)
	@$(call unpack2,__PKG_NAME__)
	@$(call get_pkg_root2)
	@echo "export TEST_LOG=$(crTESTLOGDIR)/$@" >> envars && \\
	echo "$(nl_)`date`$(nl_)" >$(crTESTLOGDIR)/$@
	@source envars && \\
	$(crCMDSDIR)/__TARGET_SHELL__ >>logs/$@ 2>&1 && \\
	$(PRT_DU_CR) >>logs/$@
	@$(call remove_build_dirs2,__NAME_FORM_TARGET__)
	@$(call log_new_files,__NAME_FORM_TARGET__)
	@$(call housekeeping)
'''
,

'cmd_sudo_tpl' : '''
__TARGET__:  __DEP__
	@$(call echo_message, Building)
	@export BASHBIN=$(SHELL) && $(SHELL) progress_bar.sh $@ $$PPID &
	@echo "$(nl_)`date`$(nl_)" >logs/$@
	@$(PRT_DU) >>logs/$@
	@export LFS=$(MOUNT_PT) && \\
	lfs-commands/__TARGET_SHELL__ >>logs/$@ 2>&1 && \\
	$(PRT_DU) >>logs/$@
	@$(call housekeeping)
'''
,

'cmd_stage_holder_tpl':'''
__TARGET__:  __DEP__
	@touch $@
'''
}

dep_details = [
    {'target':'LUSER_BEGIN','dep':'022-settingenvironment','pkg':'','tpl':'cmd_stage_holder_tpl'},
    {'target':'034-binutils-pass1','pkg':'binutils-2.27.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'035-gcc-pass1','pkg':'gcc-6.3.0.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'036-linux-headers','pkg':'linux-4.9.9.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'037-glibc','pkg':'glibc-2.25.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'038-gcc-libstdc++','pkg':'gcc-6.3.0.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'039-binutils-pass2','pkg':'binutils-2.27.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'040-gcc-pass2','pkg':'gcc-6.3.0.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'041-tcl','pkg':'tcl-core8.6.6-src.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'042-expect','pkg':'expect5.45.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'043-dejagnu','pkg':'dejagnu-1.6.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'044-check','pkg':'check-0.11.0.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'045-ncurses','pkg':'ncurses-6.0.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'046-bash','pkg':'bash-4.4.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'047-bison','pkg':'bison-3.0.4.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'048-bzip2','pkg':'bzip2-1.0.6.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'049-coreutils','pkg':'coreutils-8.26.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'050-diffutils','pkg':'diffutils-3.5.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'051-file','pkg':'file-5.30.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'052-findutils','pkg':'findutils-4.6.0.tar.gz','tpl':'cmd_full_path_with_pkg'},
    {'target':'053-gawk','pkg':'gawk-4.1.4.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'054-gettext','pkg':'gettext-0.19.8.1.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'055-grep','pkg':'grep-3.0.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'056-gzip','pkg':'gzip-1.8.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'057-m4','pkg':'m4-1.4.18.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'058-make','pkg':'make-4.2.1.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'059-patch','pkg':'patch-2.7.5.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'060-perl','pkg':'perl-5.24.1.tar.bz2','tpl':'cmd_full_path_with_pkg'},
    {'target':'061-sed','pkg':'sed-4.4.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'062-tar','pkg':'tar-1.29.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'063-texinfo','pkg':'texinfo-6.3.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'064-util-linux','pkg':'util-linux-2.29.1.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'065-xz','pkg':'xz-5.2.3.tar.xz','tpl':'cmd_full_path_with_pkg'},
    {'target':'066-stripping','pkg':'','tpl':'cmd_full_path_no_pkg'},
    {'target':'LUSER_END','pkg':'','tpl':'cmd_stage_holder_tpl'},


    {'target':'SUDO_BEGIN','pkg':'','tpl':'cmd_stage_holder_tpl'},
    {'target':'067-changingowner','pkg':'','tpl':'cmd_sudo_tpl'},
    {'target':'069-kernfs','pkg':'','tpl':'cmd_sudo_tpl'},
    {'target':'SUDO_END','pkg':'','tpl':'cmd_stage_holder_tpl'},


    {'target':'CHROOT_BEGIN','pkg':'','tpl':'cmd_stage_holder_tpl'},
    {'target':'072-creatingdirs','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'073-createfiles','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'074-linux-headers','pkg':'linux-4.9.9.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'075-man-pages','pkg':'man-pages-4.09.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'076-glibc','pkg':'glibc-2.25.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'077-adjusting','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'078-zlib','pkg':'zlib-1.2.11.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'079-file','pkg':'file-5.30.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'080-binutils','pkg':'binutils-2.27.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'081-gmp','pkg':'gmp-6.1.2.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'082-mpfr','pkg':'mpfr-3.1.5.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'083-mpc','pkg':'mpc-1.0.3.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'084-gcc','pkg':'gcc-6.3.0.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'085-bzip2','pkg':'bzip2-1.0.6.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'086-pkg-config','pkg':'pkg-config-0.29.1.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'087-ncurses','pkg':'ncurses-6.0.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'088-attr','pkg':'attr-2.4.47.src.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'089-acl','pkg':'acl-2.2.52.src.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'090-libcap','pkg':'libcap-2.25.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'091-sed','pkg':'sed-4.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'092-shadow','pkg':'shadow-4.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'093-psmisc','pkg':'psmisc-22.21.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'094-iana-etc','pkg':'iana-etc-2.30.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'095-m4','pkg':'m4-1.4.18.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'096-bison','pkg':'bison-3.0.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'097-flex','pkg':'flex-2.6.3.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'098-grep','pkg':'grep-3.0.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'099-readline','pkg':'readline-7.0.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'100-bash','pkg':'bash-4.4.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'101-bc','pkg':'bc-1.06.95.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'102-libtool','pkg':'libtool-2.4.6.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'103-gdbm','pkg':'gdbm-1.12.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'104-gperf','pkg':'gperf-3.0.4.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'105-expat','pkg':'expat-2.2.0.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'106-inetutils','pkg':'inetutils-1.9.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'107-perl','pkg':'perl-5.24.1.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'108-xml-parser','pkg':'XML-Parser-2.44.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'109-intltool','pkg':'intltool-0.51.0.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'110-autoconf','pkg':'autoconf-2.69.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'111-automake','pkg':'automake-1.15.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'112-xz','pkg':'xz-5.2.3.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'113-kmod','pkg':'kmod-23.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'114-gettext','pkg':'gettext-0.19.8.1.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'115-procps-ng','pkg':'procps-ng-3.3.12.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'116-e2fsprogs','pkg':'e2fsprogs-1.43.4.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'117-coreutils','pkg':'coreutils-8.26.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'118-diffutils','pkg':'diffutils-3.5.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'119-gawk','pkg':'gawk-4.1.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'120-findutils','pkg':'findutils-4.6.0.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'121-groff','pkg':'groff-1.22.3.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'122-grub','pkg':'grub-2.02~beta3.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'123-less','pkg':'less-481.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'124-gzip','pkg':'gzip-1.8.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'125-iproute2','pkg':'iproute2-4.9.0.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'126-kbd','pkg':'kbd-2.0.4.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'127-libpipeline','pkg':'libpipeline-1.4.1.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'128-make','pkg':'make-4.2.1.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'129-patch','pkg':'patch-2.7.5.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'130-sysklogd','pkg':'sysklogd-1.5.1.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'131-sysvinit','pkg':'sysvinit-2.88dsf.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'132-eudev','pkg':'eudev-3.2.1.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'133-util-linux','pkg':'util-linux-2.29.1.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'134-man-db','pkg':'man-db-2.7.6.1.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'135-tar','pkg':'tar-1.29.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'136-texinfo','pkg':'texinfo-6.3.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'137-vim','pkg':'vim-8.0.069.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'140-revisedchroot','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'CHROOT_END','pkg':'','tpl':'cmd_stage_holder_tpl'},


    {'target':'BOOT_BEGIN','pkg':'','tpl':'cmd_stage_holder_tpl'},
    {'target':'142-bootscripts','pkg':'lfs-bootscripts-20150222.tar.bz2','tpl':'cmd_root_path_with_pkg'},
    {'target':'144-symlinks','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'145-network','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'146-usage','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'147-profile','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'148-inputrc','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'149-etcshells','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'151-fstab','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'152-kernel','pkg':'linux-4.9.9.tar.xz','tpl':'cmd_root_path_with_pkg'},
    {'target':'153-grub','pkg':'','tpl':'cmd_root_path_no_pkg'},
    {'target':'BOOT_END','pkg':'','tpl':'cmd_stage_holder_tpl'},



    {'target':'CUSTOM_BEGIN','pkg':'','tpl':'cmd_stage_holder_tpl'},
    {'target':'201-openssl','pkg':'openssl-1.0.2k.tar','tpl':'cmd_root_path_with_pkg'},
    {'target':'202-openssh','pkg':'openssh-7.4p1.tar','tpl':'cmd_root_path_with_pkg'},
    {'target':'203-CAC','pkg':'CAC.tar.gz','tpl':'cmd_root_path_with_pkg'},
    {'target':'204-curl','pkg':'curl-7.52.1.tar.lzma','tpl':'cmd_root_path_with_pkg'},
    {'target':'CUSTOM_END','pkg':'','tpl':'cmd_stage_holder_tpl'}
]




