#!/bin/bash
#
# The WLST custom tool used to launch the wlst environment or the wlst script.
#
# Requires env:
#		ORACLE_COMMON : The oracle common directory $MW_HOME/oracle_common
#
###############################################################################

SCRIPT_PATH=`dirname $0`
SCRIPT_NAME=`basename $0`
. $SCRIPT_PATH/config/env.sh

# Export WLST_LIB to include further in your wlst scripts
export WLST_LIB=$SCRIPT_PATH/wlst/lib

###############################################################################
#
#
###############################################################################

function help() {
	echo "Usage: $SCRIPT_NAME <properties_file> [wlst_script]"
	
}

###############################################################################
#
#
###############################################################################

if [ $# -lt 1 ]; then
  help
  exit 0
fi

propertiesFile=$1
shift


export WLST_PROPERTIES="-Dweblogic.security.SSL.ignoreHostnameVerification=true \
-Dweblogic.security.TrustKeyStore=DemoTrust"

$ORACLE_COMMON/common/bin/wlst.sh -skipWLSModuleScanning -loadProperties $propertiesFile $@
