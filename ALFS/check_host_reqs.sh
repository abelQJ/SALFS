# $Id: func_check_version.sh 4026 2018-01-13 09:08:56Z pierre $ 

check_version() {
: <<inline_doc
      Tests for a minimum version level. Compares to version numbers and forces an
        exit if minimum level not met.
      NOTE: This test will fail on versions containing alpha chars. ie. jpeg 6b

    usage:	check_version "2.6.2" "`uname -r`"         "KERNEL"
		check_version "3.0"   "$BASH_VERSION"      "BASH"
		check_version "3.0"   "`gcc -dumpversion`" "GCC"

    input vars: $1=min acceptable version
    		$2=version to check
		$3=app name
    externals:  --
    modifies:   --
    returns:    nothing
    on error:	write text to console and dies
    on success: write text to console and returns
inline_doc

  declare -i major minor revision change
  declare -i ref_major ref_minor ref_revision ref_change
  declare -r spaceSTR="                   "

  shopt -s extglob	#needed for ${x##*(0)} below

  ref_version=$1
  tst_version=$2
  TXT=$3

  # This saves us the save/restore hassle of the system IFS value
  local IFS

  write_error_and_die() {
     echo -e "\n\t\t$TXT is missing or version -->${tst_version}<-- is too old.
		    This script requires ${ref_version} or greater\n"
   # Ask the user instead of bomb, to make happy that packages which version
   # ouput don't follow our expectations
    echo "If you are sure that you have installed a proper version of ${BOLD}$TXT${OFF}"
    echo "but jhalfs has failed to detect it, press 'c' and 'ENTER' keys to continue,"
    echo -n "otherwise press 'ENTER' key to stop jhalfs.  "
    read ANSWER
    if [ x$ANSWER != "xc" ] ; then
      echo "${nl_}Please, install a proper $TXT version.${nl_}"
      exit 1
    else
      minor=$ref_minor
      revision=$ref_revision
    fi
  }

  echo -ne "${TXT}${dotSTR:${#TXT}} ${L_arrow}${BOLD}${tst_version}${OFF}${R_arrow}"

#  echo -ne "$TXT:\t${L_arrow}${BOLD}${tst_version}${OFF}${R_arrow}"
  IFS=".-(pab"   # Split up w.x.y.z as well as w.x.y-rc  (catch release candidates)
  set -- $ref_version # set positional parameters to minimum ver values
  ref_major=$1; ref_minor=$2; ref_revision=$3
  #
  set -- $tst_version # Set positional parameters to test version values
  # Values beginning with zero are taken as octal, so that for example
  # 2.07.08 gives an error because 08 cannot be octal. The ## stuff supresses
  # leading zero's
  major=${1##*(0)}; minor=${2##*(0)}; revision=${3##*(0)}
  #
  # Compare against minimum acceptable version..
  (( major > ref_major )) &&
    echo " ${spaceSTR:${#tst_version}}${GREEN}OK${OFF} (Min version: ${ref_version})" &&
    return
  (( major < ref_major )) && write_error_and_die
    # major=ref_major
  (( minor < ref_minor )) && write_error_and_die
  (( minor > ref_minor )) &&
    echo " ${spaceSTR:${#tst_version}}${GREEN}OK${OFF} (Min version: ${ref_version})" &&
    return
    # minor=ref_minor
  (( revision >= ref_revision )) &&
    echo " ${spaceSTR:${#tst_version}}${GREEN}OK${OFF} (Min version: ${ref_version})" &&
    return

  # oops.. write error msg and die
  write_error_and_die
}
#  local -r PARAM_VALS='${config_param}${dotSTR:${#config_param}} ${L_arrow}${BOLD}${!config_param}${OFF}${R_arrow}'

#----------------------------#
check_prerequisites() {      #
#----------------------------#

  #HOSTREQS=$(find $BOOK -name hostreqs.xml)

  #eval $(xsltproc $COMMON_DIR/hostreqs.xsl $HOSTREQS)
  # Avoid translation of version strings
  local LC_ALL=C
  export LC_ALL

  # LFS/HLFS/CLFS prerequisites
  if [ -n "$MIN_Linux_VER" ]; then
    check_version "$MIN_Linux_VER"     "`uname -r`"          "KERNEL"
  fi
  if [ -n "$MIN_Bash_VER" ]; then
    check_version "$MIN_Bash_VER"      "$BASH_VERSION"       "BASH"
  fi
  if [ ! -z $MIN_GCC_VER ]; then
    check_version "$MIN_GCC_VER"     "`gcc -dumpversion`"  "GCC"
    check_version "$MIN_GCC_VER"     "`g++ -dumpversion`"  "G++"
  elif [ ! -z $MIN_Gcc_VER ]; then
    check_version "$MIN_Gcc_VER"     "`gcc -dumpversion`"  "GCC"
  fi
  if [ -n "$MIN_Glibc_VER" ]; then
    check_version "$MIN_Glibc_VER"     "$(ldd --version  | head -n1 | awk '{print $NF}')"   "GLIBC"
  fi
  if [ -n "$MIN_Binutils_VER" ]; then
    check_version "$MIN_Binutils_VER"  "$(ld --version  | head -n1 | awk '{print $NF}')"    "BINUTILS"
  fi
  if [ -n "$MIN_Tar_VER" ]; then
    check_version "$MIN_Tar_VER"       "$(tar --version | head -n1 | cut -d" " -f4)"        "TAR"
  fi
  if [ -n "$MIN_Bzip2_VER" ]; then
  bzip2Ver="$(bzip2 --version 2>&1 < /dev/null | head -n1 | cut -d" " -f8)"
    check_version "$MIN_Bzip2_VER"     "${bzip2Ver%%,*}"     "BZIP2"
  fi
  if [ -n "$MIN_Bison_VER" ]; then
    check_version "$MIN_Bison_VER"     "$(bison --version | head -n1 | cut -d" " -f4)"      "BISON"
  fi
  if [ -n "$MIN_Coreutils_VER" ]; then
    check_version "$MIN_Coreutils_VER" "$(chown --version | head -n1 | cut -d" " -f4)"      "COREUTILS"
  fi
  if [ -n "$MIN_Diffutils_VER" ]; then
    check_version "$MIN_Diffutils_VER" "$(diff --version  | head -n1 | cut -d" " -f4)"      "DIFF"
  fi
  if [ -n "$MIN_Findutils_VER" ]; then
    check_version "$MIN_Findutils_VER" "$(find --version  | head -n1 | cut -d" " -f4)"      "FIND"
  fi
  if [ -n "$MIN_Gawk_VER" ]; then
    check_version "$MIN_Gawk_VER"      "$(gawk --version  | head -n1 | awk -F'[ ,]+' '{print $3}')" "GAWK"
  fi
  if [ -n "$MIN_Grep_VER" ]; then
    check_version "$MIN_Grep_VER"      "$(grep --version  | head -n1 | awk '{print $NF}')"  "GREP"
  fi
  if [ -n "$MIN_Gzip_VER" ]; then
    check_version "$MIN_Gzip_VER"      "$(gzip --version 2>&1 | head -n1 | cut -d" " -f2)"  "GZIP"
  fi
  if [ -n "$MIN_M4_VER" ]; then
    check_version "$MIN_M4_VER"        "$(m4 --version 2>&1 | head -n1 | awk '{print $NF}')" "M4"
  fi
  if [ -n "$MIN_Make_VER" ]; then
    check_version "$MIN_Make_VER"      "$(make --version  | head -n1 | cut -d " " -f3 | cut -c1-4)" "MAKE"
  fi
  if [ -n "$MIN_Patch_VER" ]; then
    check_version "$MIN_Patch_VER"     "$(patch --version | head -n1 | sed 's/.*patch //')" "PATCH"
  fi
  if [ -n "$MIN_Perl_VER" ]; then
    check_version "$MIN_Perl_VER"      "$(perl -V:version | cut -f2 -d\')"                  "PERL"
  fi
  if [ -n "$MIN_Sed_VER" ]; then
    check_version "$MIN_Sed_VER"       "$(sed --version   | head -n1 | cut -d" " -f4)"      "SED"
  fi
  if [ -n "$MIN_Texinfo_VER" ]; then
    check_version "$MIN_Texinfo_VER"   "$(makeinfo --version | head -n1 | awk '{ print$NF }')" "TEXINFO"
  fi
  if [ -n "$MIN_Xz_VER" ]; then
    check_version "$MIN_Xz_VER"        "$(xz --version | head -n1 | cut -d" " -f4)"         "XZ"
  fi
}

# define the host requirement
MIN_Linux_VER=3.0
MIN_Bash_VER=3.2
MIN_GCC_VER=4.7
MIN_Glibc_VER=2.11
MIN_Binutils_VER=2.17
MIN_Tar_VER=1.22
MIN_Bzip2_VER=1.0.4
MIN_Bison_VER=2.3
MIN_Coreutils_VER=6.9
MIN_Diffutils_VER=2.8.1
MIN_Findutils_VER=4.2.31
MIN_Gawk_VER=4.0.1
MIN_Grep_VER=2.5.1
MIN_Gzip_VER=1.3.12
MIN_M4_VER=1.4.10
MIN_Make_VER=3.81
MIN_Patch_VER=2.5.4
MIN_Perl_VER=5.8.8
MIN_Sed_VER=4.1.5
MIN_Texinfo_VER=4.7
MIN_Xz_VER=5.0.0

#do the check
check_prerequisites