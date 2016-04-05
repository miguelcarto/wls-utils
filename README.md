# wls-utils

Set of utilities to perform specific actions on an existing middleware installation
The project contains 2 main folders
- config : Where the environment variables are set
- wlst : Where the wlst main scripts exist

Inside the wlst folder it will exist a lib folder where we should add costum python modules.

## Fix Datasources

This script transforms the existing generic datasources into multi datasources. 
This action is needed when you create your datasources loading the default definitions from
the STB (when we create our domains based on that info).

We transform the existing generic datasource into a multi datasource with the same jndi name.

From:
- mds-owsm (generic)
	 
To: 
- mds-owsm (multi)
 - mds-owsm-rac1 (generic)
 - mds-owsm-rac2 (generic)

To execute this action you should define a properties file that must contain 
- DS_RAC_NODES : A coma separated string that contains all the database rac nodes
- DS_TARGET : The cluster/server name that we must validate to select the datasources to modify, 
cause we are not interested in modifying the datasources that are only deployed to the admin server
- MW_TARGET : The Admin server url that we should use to connect and do the action