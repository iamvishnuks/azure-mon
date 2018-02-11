from azure.monitor import MonitorClient
from azure.mgmt.monitor import MonitorMgmtClient
from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials
import datetime
from pytz import timezone


def find_expired(r,dr):
  c=[]
  for d in dr:
   for i in r:
     if i[1]==d[1] and i[0]==d[0]:
       print('Match found')
       if i[2]<d[2]:
         c.append(i)
  c=list(set(c))
  return c 
         

def remove_expired(c,r):
  final=r[:]
  for d in c:
    for i in r:
      if i[1]==d[1] or i[0]==d[0]:
        if i[2]<d[2]:
          try:
            final.remove(i)
          except:
            pass
   return final

def check_age(final):
  for i in final:
    date=start_date.replace(tzinfo=timezone('UTC'))
    xdate=i[2].replace(tzinfo=timezone('UTC'))
    if xdate>=date:
      print i[1].split('/')[-1]+" is "+days+" days old"


if __name__=='__main__':
  subscription_id = raw_input("Please provide your subscription id : ")
  CLIENT=raw_input("Enter your client id : ")
  KEY=raw_input("Enter the secret key : ")
  TENANT_ID=raw_input("Enter the tenant id : ")
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
  days=raw_input("Enter the threshhold age of resources : ")
  start_date = datetime.datetime.now() + datetime.timedelta(-(int(days)))
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
  c=find_expired(r,dr)
  final=remove_expired(c,r)
  check_age(final)
  
  
