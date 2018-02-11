from azure.monitor import MonitorClient
from azure.mgmt.monitor import MonitorMgmtClient
from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials
import datetime
from pytz import timezone
# Replace this with your subscription id
subscription_id = '265ca25b-9b97-4278-ac4c-51840de247f2'

# See above for details on creating different types of AAD credentials

CLIENT="a6d8c3c6-74bc-48a9-876f-a4955e1301bd"
KEY="redhat@123"
TENANT_ID="96e8e3d4-23c8-4d78-a8f5-87a0ef72c949"

credentials = ServicePrincipalCredentials(
         client_id = CLIENT,
         secret = KEY,
         tenant = TENANT_ID
     )

client = MonitorClient(
    credentials,
    subscription_id
)

monitor_mgmt_client = MonitorMgmtClient(
    credentials,
    subscription_id
)

start_date = datetime.datetime.now() + datetime.timedelta(-30)
filter = " and ".join([
    "eventTimestamp ge {}".format(start_date),
    "resourceGroupName eq 'SainathTest'"
])

select = ",".join([
    "eventName",
    "operationName",
    "resourceId",
    "eventTimestamp",
    "status"
])

activity_logs = client.activity_logs.list(
    filter=filter,
    select=select
)
r=[]
dr=[]
for log in activity_logs:
    # assert isinstance(log, azure.monitor.models.EventData)
    if 'delete' not in log.operation_name.localized_value and log.status.localized_value!='Failed':
      r.append((log.resource_id.split('/')[-2],log.resource_id.split('/')[-1],log.event_timestamp))
    elif 'delete' in log.operation_name.localized_value and log.status.localized_value!='Failed':
      dr.append((log.resource_id.split('/')[-2],log.resource_id.split('/')[-1],log.event_timestamp))  
    print(" ".join([
        log.event_name.localized_value,
        log.operation_name.localized_value,
        log.resource_id,
        str(log.event_timestamp),str(log.status)
    ]))

c=[]
for d in dr:
   for i in r:
     if i[1]==d[1] and i[0]==d[0]:
       print('Match found')
       if i[2]<d[2]:
         c.append(i)
         break

c=list(set(c))
final=r[:]
for d in c:
  for i in r:
    if i[1]==d[1] or i[0]==d[0]:
      try:
        final.remove(i)
      except:
        print "not found"

for i in final:
  date=start_date.replace(tzinfo=timezone('UTC'))
  xdate=i[2].replace(tzinfo=timezone('UTC'))
  if xdate<=date:
    print i[1].split('/')[-1]+" is 30 days old"
