#!/bin/bash
#
# Config file to export all the variables needed for this utility to work
#
# Produces env:
#		MW_HOME 		: The MiddleWare home		
#		JAVA_HOME 		: The JDK Home
#		ORACLE_COMMON 	: The FMW Oracle Common 
# 
###############################################################################

MW_HOME=/opt/oracle/middleware/12.2/fmw
export  MW_HOME

JAVA_HOME=/opt/oracle/middleware/12.2/jdk
export JAVA_HOME

ORACLE_COMMON=$MW_HOME/oracle_common
export ORACLE_COMMON