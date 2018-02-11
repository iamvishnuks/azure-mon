# azure-mon
A tool for monitoring azure resources in a subscription.

## Installation and Usage
Run `pip install azure-mon` for installation

After installation you have to create a service principle. You can create one service principle by simply running this command
`az ad sp create-for-rbac --name "any name" --password "any password"`

When you succesully create a service principle you will get an appid, key, tenant_id. You need to note it down for configuring our tool. And yes .. you should have your subscription_id also for moving forward.

After getting the required keys and ids type `azure-mon` in terminal, it will ask for subscrition_id, app_id, secret_key and tenant_id. azure-mon will ask this things only for the first run. Later it will get all this values locally as all the values will be stored in the present working directory in a file nameed config.json
