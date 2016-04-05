"""
Updates all existing datasources that are targeted to the cluster specified by DS_TARGET.
It transforms all the generic data sources into Multi Datasources to fullfill the Oracle 
Rac-One specifications.

"""

# dsRacNodes = ['dbs01', 'dbs02', 'dbs03']
# target = 'coh01_coh01_app'
# mwTarget = 't3s://lab01g:10002'

urlFormat = 'jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=DBHOST)(PORT=DBPORT)))(CONNECT_DATA=(SERVICE_NAME=DBSERVICENAME)))'
dsRacNodes = DS_RAC_NODES.split(',')
target = DS_TARGET
mwTarget = MW_TARGET

dsParams = {
   'secondsToTrustAnIdlePoolConnection': 0,
   'testConnectionsOnReserve': 1,
   'xaSetTransactionTimeout': 1}


def copy(origin, target, name):
   """
   Util function to coppy attr between Objects.
   It copies the value only if it's defined in the origin object

   :param origin: The Origin object to copy from
   :param target: The Target object to copy to
   :param name:  The attribute to copy
   """
   if origin.isSet(name[0].upper() + name[1:]):
      setattr(target, name, getattr(origin, name))

def commit_changes():
   """
   Save and activate an edit session
   """
   save()
   activate()

def start_edit():
   """
   Initializes an edit session
   """
   edit()
   startEdit()

def relocate_aware(datasource):
   """
   Updates the generic datasources to be compliant to the Oracle Rac database definition to be relocate aware.

   :param datasource:
   :type datasource:
   """
   ores = datasource.JDBCResource
   oparams = ores.JDBCConnectionPoolParams
   defaultParam = dsParams['secondsToTrustAnIdlePoolConnection']
   setattr(oparams, 'secondsToTrustAnIdlePoolConnection', defaultParam)

   defaultParam = dsParams['testConnectionsOnReserve']
   setattr(oparams, 'testConnectionsOnReserve', defaultParam)

   # Set Transaction specific parameters
   dparams = ores.JDBCDriverParams
   oparams = ores.JDBCXAParams

   dName = dparams.driverName
   if 'XA' in dName:
      defaultParam = dsParams['xaSetTransactionTimeout']
      setattr(oparams, 'xaSetTransactionTimeout', defaultParam)

def create_rac_datasources(genericdatasource):
   """
   Creates all the rac generic datasources according to oracle definitions
   We append the '-rac' string tho the datasource name an jndi values

   :param datasource: The datasource to copy from
   :param count: The datasource count to append to the new ds name
   :return: The newly created datasource
   """
   dscount = 1
   while dscount <= len(dsRacNodes):
      print '| create_rac_datasources -> Creating datasource ' + genericdatasource.name + '-rac' + str(dscount)
      newdatasource = copy_datasource(genericdatasource, dscount)
      relocate_aware(newdatasource)
      dscount+=1

def copy_datasource(datasource, count):
   """
   Copies the given datasource.
   We append the '-rac' string tho the datasource name an jndi values
   :param datasource: The datasource to copy from
   :param count: The datasource count to append to the new ds name
   :return: The newly created datasource
   """
   ods = datasource

   new_name = ods.name + '-rac' + str(count)
   print "| copy_datasource about to copy datasource from '%s' to '%s'" % (ods.name, new_name)

   # create a JDBC System resource
   tds = cmo.createJDBCSystemResource(new_name)
   copy(ods, tds, 'notes')
   copy(ods, tds, 'compatibilityName')
   copy(ods, tds, 'deploymentPrincipalName')

   for target in ods.targets:
      tds.addTarget(target)

   ores = ods.JDBCResource
   tres = tds.JDBCResource
   tres.name = new_name

   # Set Connection Pool specific parameters
   oparams = ores.JDBCConnectionPoolParams
   tparams = tres.JDBCConnectionPoolParams
   copy(oparams, tparams, 'capacityIncrement')
   copy(oparams, tparams, 'connectionCreationRetryFrequencySeconds')
   copy(oparams, tparams, 'connectionHarvestMaxCount')
   copy(oparams, tparams, 'connectionHarvestTriggerCount')
   copy(oparams, tparams, 'connectionLabelingCallback')
   copy(oparams, tparams, 'connectionReserveTimeoutSeconds')
   copy(oparams, tparams, 'credentialMappingEnabled')
   copy(oparams, tparams, 'driverInterceptor')
   copy(oparams, tparams, 'fatalErrorCodes')
   copy(oparams, tparams, 'highestNumWaiters')
   copy(oparams, tparams, 'identityBasedConnectionPoolingEnabled')
   copy(oparams, tparams, 'ignoreInUseConnectionsEnabled')
   copy(oparams, tparams, 'inactiveConnectionTimeoutSeconds')
   copy(oparams, tparams, 'initSql')
   copy(oparams, tparams, 'initialCapacity')
   copy(oparams, tparams, 'JDBCXADebugLevel')
   copy(oparams, tparams, 'loginDelaySeconds')
   copy(oparams, tparams, 'maxCapacity')
   copy(oparams, tparams, 'minCapacity')
   copy(oparams, tparams, 'pinnedToThread')
   copy(oparams, tparams, 'profileHarvestFrequencySeconds')
   copy(oparams, tparams, 'profileType')
   copy(oparams, tparams, 'removeInfectedConnections')
   copy(oparams, tparams, 'secondsToTrustAnIdlePoolConnection')
   copy(oparams, tparams, 'shrinkFrequencySeconds')
   copy(oparams, tparams, 'statementCacheSize')
   copy(oparams, tparams, 'statementCacheType')
   copy(oparams, tparams, 'statementTimeout')
   copy(oparams, tparams, 'testConnectionsOnReserve')
   copy(oparams, tparams, 'testFrequencySeconds')
   copy(oparams, tparams, 'testTableName')
   copy(oparams, tparams, 'wrapTypes')

   # Set Data Source parameters
   oparams = ores.JDBCDataSourceParams
   tparams = tres.JDBCDataSourceParams

   tparams.JNDINames = map(lambda n: n + '-rac' + str(count),oparams.JNDINames)

   copy(oparams, tparams, 'algorithmType')
   copy(oparams, tparams, 'connectionPoolFailoverCallbackHandler')
   copy(oparams, tparams, 'dataSourceList')
   copy(oparams, tparams, 'failoverRequestIfBusy')
   copy(oparams, tparams, 'globalTransactionsProtocol')
   copy(oparams, tparams, 'keepConnAfterGlobalTx')
   copy(oparams, tparams, 'keepConnAfterLocalTx')
   copy(oparams, tparams, 'rowPrefetch')
   copy(oparams, tparams, 'rowPrefetchSize')
   copy(oparams, tparams, 'scope')
   copy(oparams, tparams, 'streamChunkSize')

   # Set Driver parameters
   oparams = ores.JDBCDriverParams
   tparams = tres.JDBCDriverParams

   copy(oparams, tparams, 'url')
   copy(oparams, tparams, 'driverName')
   copy(oparams, tparams, 'passwordEncrypted')
   copy(oparams, tparams, 'usePasswordIndirection')
   copy(oparams, tparams, 'useXaDataSourceInterface')

   # compose URL
   # the original format is jdbc:oracle:thin:@//dbs01:1521/ORCL
   dbURL = dsRacNodes[count-1]
   existingurl = tparams.url
   spliturl = existingurl.split(':')
   dbport = spliturl[4].split('/')[0]
   dbservicename = spliturl[4].split('/')[1]
   dbhost = spliturl[3].split('/')[2]

   newurl = urlFormat.replace('DBHOST',dbhost)
   newurl = newurl.replace('DBPORT',dbport)
   newurl = newurl.replace('DBSERVICENAME',dbservicename)
   tparams.url = newurl

   oprops = oparams.properties
   tprops = tparams.properties
   for oprop in oprops.properties:
      print ' %s, %s' % (oprop.name, oprop.value)
      tprops.createProperty(oprop.name, oprop.value)

      # Set Oracle Driver parameters
   oparams = ores.JDBCOracleParams
   tparams = tres.JDBCOracleParams
   copy(oparams, tparams, 'affinityPolicy')
   copy(oparams, tparams, 'connectionInitializationCallback')
   copy(oparams, tparams, 'fanEnabled')
   copy(oparams, tparams, 'onsNodeList')
   copy(oparams, tparams, 'onsWalletFile')
   copy(oparams, tparams, 'onsWalletPasswordEncrypted')
   copy(oparams, tparams, 'oracleEnableJavaNetFastPath')
   copy(oparams, tparams, 'oracleOptimizeUtf8Conversion')
   copy(oparams, tparams, 'oracleProxySession')
   copy(oparams, tparams, 'useDatabaseCredentials')

   # Set Transaction specific parameters
   oparams = ores.JDBCXAParams
   tparams = tres.JDBCXAParams

   copy(oparams, tparams, 'keepLogicalConnOpenOnRelease')
   copy(oparams, tparams, 'keepXaConnTillTxComplete')
   copy(oparams, tparams, 'needTxCtxOnClose')
   copy(oparams, tparams, 'newXaConnForCommit')
   copy(oparams, tparams, 'recoverOnlyOnce')
   copy(oparams, tparams, 'resourceHealthMonitoring')
   copy(oparams, tparams, 'rollbackLocalTxUponConnClose')
   copy(oparams, tparams, 'xaEndOnlyOnce')
   copy(oparams, tparams, 'xaRetryDurationSeconds')
   copy(oparams, tparams, 'xaRetryIntervalSeconds')
   copy(oparams, tparams, 'xaSetTransactionTimeout')
   copy(oparams, tparams, 'xaTransactionTimeout')

   return tds

def ds_remove_targets(datasource):
   """
   Untarget the given datasource
   :param datasource: The datasource to untarget
   """
   for target in datasource.targets:
      datasource.removeTarget(target)


def ds_destroy(datasource):
   """
   Destroy the given datasource
   :param datasource: The Datasource to destroy
   """
   cd('/JDBCSystemResources/')
   cmo.destroyJDBCSystemResource(datasource)

def create_multidatasource(genericds, targetlist):
   """
   Creates a multidatasource with exactly the same jndi name that the generic ds that we are replacing
   The target list was gattered before the genericds untarget in order to maintain the targets between datasources
   :param genericds: A Generic Datasource MBean
   :param targetlist: A list containing the targets ( Server/Cluster MBeans )
   """
   mdsname = genericds.name +'-mds'
   mutidatasource = cmo.createJDBCSystemResource(mdsname)

   cd('/JDBCSystemResources/'+mdsname)
   for target in targetlist:
      mutidatasource.addTarget(target)

   cd('/JDBCSystemResources/'+mdsname+'/JDBCResource/'+mdsname)
   cmo.setName(mdsname)
   cmo.setDatasourceType('MDS')

   dslist = genericds.name + '-rac1'
   iter = 2
   while iter <= len(dsRacNodes):
      dslist += ',' + genericds.name + '-rac'+iter

   mutidatasource.JDBCResource.JDBCDataSourceParams.dataSourceList = dslist

   cd('/JDBCSystemResources/'+mdsname+'/JDBCResource/'+mdsname+'/JDBCDataSourceParams/'+mdsname)
   set('JNDINames',genericds.JDBCResource.JDBCDataSourceParams.JNDINames)
   cmo.setAlgorithmType('Failover')
   cmo.setFailoverRequestIfBusy(true)


"""
The main script.
The variable targets should be filled with the admin address to connect and apply the actions
"""



try:
   adminUserName = raw_input('WLS Admin username: ')
   console = System.console()
   passwdCharArr = console.readPassword("%s", ["WLS Admin password: "])
   adminPassword = "".join(passwdCharArr)

   connect(adminUserName, adminPassword, mwTarget)
   start_edit()
   try:
      print "About to update %s %d" % (mwTarget, len(sys.argv))
      cd('/JDBCSystemResources')
      datasources = ls('c', 'true')
      for generic in datasources:

         genericds = getMBean(generic)
         print '| -> datasource : %s ' % genericds

         dstargetlist = genericds.targets
         print '| -> datasource target list : %s ' % dstargetlist

         found = [elem for elem in dstargetlist if elem.name == target]
         if len(found) == 0:
            print target + ' not found in '+str(dstargetlist)+', keep going'
            continue

         # copy the ds with the new name
         create_rac_datasources(genericds)

         # untarget existing generic datasource
         ds_remove_targets(genericds)

         # apply changes
         commit_changes()
         start_edit()

         create_multidatasource(genericds, dstargetlist)

         cd('/JDBCSystemResources')
         ds_destroy(genericds)

         # apply changes
         commit_changes()
         start_edit()
         cd('/JDBCSystemResources')
      save()

   except RuntimeError:
      undo('true', 'y')
      cancelEdit('y')
      raise
   activate()
   disconnect()
except RuntimeError:
   dumpStack()
