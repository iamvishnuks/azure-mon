from azure.monitor import MonitorClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials
import datetime
from pytz import timezone
import json

def find_expired(r,dr):
  c=[]
  for d in dr:
   for i in r:
     if i[1]==d[1] and i[0]==d[0]:
       #print('Match found')
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
    date=age_date.replace(tzinfo=timezone('UTC'))
    xdate=i[2].replace(tzinfo=timezone('UTC'))
    delta=date-xdate
    if delta.days>day:
      print i[1].split('/')[-1]+" is "+str(delta.days)+" days old"
    #print delta.days, i[1].split('/')[-1]


if __name__=='__main__':
  try:
    with open('config.json','r') as readfile:
      data=json.load(readfile)
    subscription_id=str(data['id'])
    CLIENT=data['client']
    KEY=data['key']
    TENANT_ID=data['tenant']
  except:
    subscription_id = raw_input("Please provide your subscription id : ")
    CLIENT=raw_input("Enter your client id : ")
    KEY=raw_input("Enter the secret key : ")
    TENANT_ID=raw_input("Enter the tenant id : ")
    data={'id':subscription_id,'client':CLIENT,'key':KEY,'tenant':TENANT_ID}
    with open('config.json','w') as outfile:
      json.dump(data,outfile)
  credentials = ServicePrincipalCredentials(
         client_id = CLIENT,
         secret = KEY,
         tenant = TENANT_ID
       )
  client = MonitorClient(
      credentials,
      subscription_id
    )
  monitor_mgmt_client = MonitorManagementClient(
      credentials,
      subscription_id
    )
  days=int(raw_input("Enter the number of days to pull the activity log : "))
  day=int(raw_input("Enter the minimum age for resources : "))
  start_date = datetime.datetime.now() + datetime.timedelta(-(days))
  age_date= datetime.datetime.now()
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
      '''print(" ".join([
          log.event_name.localized_value,
          log.operation_name.localized_value,
          log.resource_id,
          str(log.event_timestamp),str(log.status)
          ]))'''
  c=find_expired(r,dr)
  final=remove_expired(c,r)
  check_age(final)
  
  
