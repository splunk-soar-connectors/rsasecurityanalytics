[comment]: # "Auto-generated SOAR connector documentation"
# RSA Security Analytics

Publisher: Splunk  
Connector Version: 2\.0\.3  
Product Vendor: RSA  
Product Name: RSA Security Analytics  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This App supports ingestion and investigative actions on RSA Security Analytics

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a RSA Security Analytics asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**url** |  required  | string | URL
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
**username** |  required  | string | Username
**password** |  required  | password | Password
**poll\_now\_ingestion\_span** |  required  | numeric | Poll last n days for 'Poll Now'
**first\_scheduled\_ingestion\_span** |  required  | numeric | Poll last n days for first scheduled polling
**max\_incidents** |  required  | numeric | Maximum number of incidents to ingest for scheduled polling
**incident\_manager** |  required  | string | Name of Incident Manager

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the credentials provided for connectivity  
[on poll](#action-on-poll) - Ingest incidents from RSA Security Analytics  
[restart service](#action-restart-service) - DEPRECATED  
[list incidents](#action-list-incidents) - List incidents within a time frame  
[list alerts](#action-list-alerts) - List alerts for an incident  
[list events](#action-list-events) - List events for an alert  
[list devices](#action-list-devices) - List devices connected to RSA Security Analytics  

## action: 'test connectivity'
Validate the credentials provided for connectivity

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Ingest incidents from RSA Security Analytics

Type: **ingest**  
Read only: **True**

Basic configuration parameters for this action are available in asset configuration\.<br><br>The app ingests incidents in ascending order by create time\. Therefore, each polling interval, if <b>max\_incidents</b> is set to <b>n</b>, the app will return the next <b>n</b> created incidents\.<br><br>The <b>poll\_now\_ingestion\_span</b> parameter dictates how far back, in days, the app will search to ingest incidents when running a poll now\.<br><br>The <b>first\_scheduled\_ingestion\_span</b> parameter decides how far back, in days, the app will search to ingest incidents during the first polling interval\. The app will ingest incidents starting with the beginning of this span\.<br><br>The <b>incident\_manager</b> parameter is required for ingestion\.<br><br>During ingestion, a container is created for each incident\. In each container, an artifact is created for each alert and each event associated with the incident\.<br><br>For each container, the source ID will be set to the incident ID\. All data retrieved from RSA Security Analytics will be saved in the data section of the container\.<br><br>For each artifact created for an alert, the source ID will be set to the alert ID\. These artifacts will contain the following CEF fields \(as well as others\)\:<ul><li>incidentId</li><li>alertId</li><li>name</li><li>numEvents</li><li>events</li><li>partOfIncident</li><li>risk\_score</li><li>severity</li></ul><br>For each artifact created for an event, the source ID will be set to the session ID that the event resulted from\. These artifacts will contain the following CEF fields \(as well as others\)\:<ul><li>sessionId</li><li>type</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start\_time** |  optional  | Parameter ignored in this app | numeric | 
**end\_time** |  optional  | Parameter ignored in this app | numeric | 
**container\_id** |  optional  | Parameter ignored in this app | string | 
**container\_count** |  optional  | Maximum number of incidents to ingest during poll now | numeric | 
**artifact\_count** |  optional  | Parameter ignored in this app | numeric | 

#### Action Output
No Output  

## action: 'restart service'
DEPRECATED

Type: **generic**  
Read only: **False**

Please use the NetWitness Logs and Packets 'restart device' action instead\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device** |  required  | Device ID/Name | string |  `rsa sa device` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.device | string |  `rsa sa device` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list incidents'
List incidents within a time frame

Type: **investigate**  
Read only: **True**

If <b>start\_time</b> is not specified, the app will use the epoch\.<br><br>If <b>end\_time</b> is not specified, the app will use the current time\.<br><br>The app searches in descending order by create time\. Therefore if <b>limit</b> is set to <b>n</b>, the app will return the <b>n</b> most recently created incidents\. If the <b>limit</b> parameter is left unspecified, it will default to 100\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start\_time** |  optional  | Start time in format YYYY\-MM\-DD HH\:MM\:SS \(UTC\) | string | 
**end\_time** |  optional  | End time in format YYYY\-MM\-DD HH\:MM\:SS \(UTC\) | string | 
**limit** |  optional  | Maximum number of incidents to list | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.\*\.id | string |  `rsa incident id` 
action\_result\.data\.\*\.\*\.name | string | 
action\_result\.data\.\*\.\*\.status | string | 
action\_result\.data\.\*\.\*\.created | numeric | 
action\_result\.data\.\*\.\*\.sources | string | 
action\_result\.data\.\*\.\*\.summary | string | 
action\_result\.data\.\*\.\*\.assignee\.id | string | 
action\_result\.data\.\*\.\*\.assignee\.name | string | 
action\_result\.data\.\*\.\*\.assignee\.login | string | 
action\_result\.data\.\*\.\*\.assignee\.emailAddress | string |  `email` 
action\_result\.data\.\*\.\*\.priority | string | 
action\_result\.data\.\*\.\*\.createdBy | string | 
action\_result\.data\.\*\.\*\.riskScore | numeric | 
action\_result\.data\.\*\.\*\.alertCount | numeric | 
action\_result\.data\.\*\.\*\.lastUpdated | numeric | 
action\_result\.data\.\*\.\*\.firstAlertTime | numeric | 
action\_result\.data\.\*\.\*\.breachExportStatus | string | 
action\_result\.data\.\*\.\*\.hasRemediationTasks | boolean | 
action\_result\.data\.\*\.\*\.averageAlertRiskScore | numeric | 
action\_result\.data\.\*\.\*\.lastUpdatedByUserName | string | 
action\_result\.data\.\*\.\*\.openRemediationTaskCount | numeric | 
action\_result\.data\.\*\.\*\.totalRemediationTaskCount | numeric | 
action\_result\.data\.\*\.\*\.notes\.\*\.id | string | 
action\_result\.data\.\*\.\*\.notes\.\*\.notes | string | 
action\_result\.data\.\*\.\*\.notes\.\*\.author | string | 
action\_result\.data\.\*\.\*\.notes\.\*\.created | numeric | 
action\_result\.data\.\*\.\*\.notes\.\*\.milestone | string | 
action\_result\.data\.\*\.\*\.notes\.\*\.lastUpdated | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
action\_result\.summary\.num\_incidents | string | 
action\_result\.parameter\.start\_time | string | 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.limit | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list alerts'
List alerts for an incident

Type: **investigate**  
Read only: **True**

The app searches in descending order by create time\. Therefore if <b>limit</b> is set to <b>n</b>, the app will return the <b>n</b> most recently created alerts\. If the <b>limit</b> parameter is left unspecified, it will default to 100\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  optional  | Incident ID | string |  `rsa incident id` 
**limit** |  optional  | Maximum number of alerts to list | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.\*\.id | string |  `rsa alert id` 
action\_result\.data\.\*\.\*\.name | string | 
action\_result\.data\.\*\.\*\.type | string | 
action\_result\.data\.\*\.\*\.source | string | 
action\_result\.data\.\*\.\*\.severity | numeric | 
action\_result\.data\.\*\.\*\.numEvents | numeric | 
action\_result\.data\.\*\.\*\.timestamp | numeric | 
action\_result\.data\.\*\.\*\.incidentId | string |  `rsa incident id` 
action\_result\.data\.\*\.\*\.risk\_score | numeric | 
action\_result\.data\.\*\.\*\.groupby\_type | string | 
action\_result\.data\.\*\.\*\.host\_summary | string | 
action\_result\.data\.\*\.\*\.signature\_id | string | 
action\_result\.data\.\*\.\*\.user\_summary | string | 
action\_result\.data\.\*\.\*\.related\_links\.\*\.url | string | 
action\_result\.data\.\*\.\*\.related\_links\.\*\.type | string | 
action\_result\.data\.\*\.\*\.groupby\_domain | string |  `domain` 
action\_result\.data\.\*\.\*\.partOfIncident | boolean | 
action\_result\.data\.\*\.\*\.groupby\_filename | string | 
action\_result\.data\.\*\.\*\.groupby\_data\_hash | string | 
action\_result\.data\.\*\.\*\.groupby\_source\_ip | string |  `ip` 
action\_result\.data\.\*\.\*\.destination\_country | string | 
action\_result\.data\.\*\.\*\.groupby\_detector\_ip | string |  `ip` 
action\_result\.data\.\*\.\*\.groupby\_destination\_ip | string |  `ip` 
action\_result\.data\.\*\.\*\.groupby\_source\_country | string | 
action\_result\.data\.\*\.\*\.groupby\_source\_username | string | 
action\_result\.data\.\*\.\*\.groupby\_destination\_port | string |  `port` 
action\_result\.data\.\*\.\*\.groupby\_destination\_country | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.num\_alerts | numeric | 
action\_result\.parameter\.id | string |  `rsa incident id` 
action\_result\.parameter\.limit | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list events'
List events for an alert

Type: **investigate**  
Read only: **True**

The app searches in descending order by create time\. Therefore if <b>limit</b> is set to <b>n</b>, the app will return the <b>n</b> most recently created alerts\. If the <b>limit</b> parameter is left unspecified, it will default to 100\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Alert ID | string |  `rsa alert id` 
**limit** |  optional  | Maximum number of events to list | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.\*\.id | string |  `netwitness session ids` 
action\_result\.data\.\*\.\*\.to | string | 
action\_result\.data\.\*\.\*\.data\.\*\.hash | string | 
action\_result\.data\.\*\.\*\.data\.\*\.size | numeric | 
action\_result\.data\.\*\.\*\.data\.\*\.filename | string | 
action\_result\.data\.\*\.\*\.file | string | 
action\_result\.data\.\*\.\*\.from | string | 
action\_result\.data\.\*\.\*\.size | numeric | 
action\_result\.data\.\*\.\*\.type | string | 
action\_result\.data\.\*\.\*\.user | string | 
action\_result\.data\.\*\.\*\.domain | string |  `domain` 
action\_result\.data\.\*\.\*\.source\.user\.username | string | 
action\_result\.data\.\*\.\*\.source\.user\.ad\_domain | string |  `domain` 
action\_result\.data\.\*\.\*\.source\.user\.ad\_username | string | 
action\_result\.data\.\*\.\*\.source\.user\.email\_address | string | 
action\_result\.data\.\*\.\*\.source\.device\.port | numeric |  `port` 
action\_result\.data\.\*\.\*\.source\.device\.facility | string | 
action\_result\.data\.\*\.\*\.source\.device\.asset\_type | string | 
action\_result\.data\.\*\.\*\.source\.device\.ip\_address | string |  `ip` 
action\_result\.data\.\*\.\*\.source\.device\.criticality | string | 
action\_result\.data\.\*\.\*\.source\.device\.geolocation\.city | string | 
action\_result\.data\.\*\.\*\.source\.device\.geolocation\.domain | string |  `domain` 
action\_result\.data\.\*\.\*\.source\.device\.geolocation\.country | string | 
action\_result\.data\.\*\.\*\.source\.device\.geolocation\.organization | string | 
action\_result\.data\.\*\.\*\.source\.device\.mac\_address | string |  `mac address` 
action\_result\.data\.\*\.\*\.source\.device\.netbios\_name | string | 
action\_result\.data\.\*\.\*\.source\.device\.business\_unit | string | 
action\_result\.data\.\*\.\*\.source\.device\.compliance\_rating | string | 
action\_result\.data\.\*\.\*\.detector\.ip\_address | string | 
action\_result\.data\.\*\.\*\.detector\.device\_class | string | 
action\_result\.data\.\*\.\*\.detector\.product\_name | string | 
action\_result\.data\.\*\.\*\.timestamp | string | 
action\_result\.data\.\*\.\*\.enrichment | string | 
action\_result\.data\.\*\.\*\.description | string | 
action\_result\.data\.\*\.\*\.destination\.user\.username | string | 
action\_result\.data\.\*\.\*\.destination\.user\.ad\_domain | string |  `domain` 
action\_result\.data\.\*\.\*\.destination\.user\.ad\_username | string | 
action\_result\.data\.\*\.\*\.destination\.user\.email\_address | string | 
action\_result\.data\.\*\.\*\.destination\.device\.port | numeric |  `port` 
action\_result\.data\.\*\.\*\.destination\.device\.facility | string | 
action\_result\.data\.\*\.\*\.destination\.device\.asset\_type | string | 
action\_result\.data\.\*\.\*\.destination\.device\.ip\_address | string |  `ip` 
action\_result\.data\.\*\.\*\.destination\.device\.criticality | string | 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.city | string | 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.domain | string |  `domain` 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.country | string | 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.latitude | numeric | 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.longitude | numeric | 
action\_result\.data\.\*\.\*\.destination\.device\.geolocation\.organization | string | 
action\_result\.data\.\*\.\*\.destination\.device\.mac\_address | string |  `mac address` 
action\_result\.data\.\*\.\*\.destination\.device\.netbios\_name | string | 
action\_result\.data\.\*\.\*\.destination\.device\.business\_unit | string | 
action\_result\.data\.\*\.\*\.destination\.device\.compliance\_rating | string | 
action\_result\.data\.\*\.\*\.detected\_by | string | 
action\_result\.data\.\*\.\*\.related\_links\.\*\.url | string | 
action\_result\.data\.\*\.\*\.related\_links\.\*\.type | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.num\_events | numeric | 
action\_result\.parameter\.id | string |  `rsa alert id` 
action\_result\.parameter\.limit | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list devices'
List devices connected to RSA Security Analytics

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.\*\.id | numeric |  `rsa sa device` 
action\_result\.data\.\*\.\*\.host | string |  `ip` 
action\_result\.data\.\*\.\*\.port | numeric |  `port` 
action\_result\.data\.\*\.\*\.baseType | string | 
action\_result\.data\.\*\.\*\.licensed | boolean | 
action\_result\.data\.\*\.\*\.username | string | 
action\_result\.data\.\*\.\*\.enableSSL | boolean | 
action\_result\.data\.\*\.\*\.validated | string | 
action\_result\.data\.\*\.\*\.deviceType | string | 
action\_result\.data\.\*\.\*\.displayName | string |  `rsa sa device` 
action\_result\.data\.\*\.\*\.displayType | string | 
action\_result\.data\.\*\.\*\.deviceFamily | string | 
action\_result\.data\.\*\.\*\.deviceVersion | string | 
action\_result\.data\.\*\.\*\.systemUpdateStatusDesc | string | 
action\_result\.data\.\*\.\*\.systemUpdatesStatusFeedback | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.num\_devices | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 