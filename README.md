# salesforce-python

salesforce-python is an API wrapper for Sales written in Python

## Installing
```
pip install git+git://github.com/GearPlug/salesforce-python.git
```

## Usage
```
from salesforce.client import Client

client = Client('CLIENT_KEY', 'CLIENT_SECRET', 'https://na50.salesforce.com/', 'v41.0')
```

Get authorization url
```
url = client.authorization_url('REDIRECT_URI')
```

Exchange the code for a token
```
token = client.exchange_code('REDIRECT_URI', 'CODE')
```

Set the token
```
client.set_access_token('TOKEN')
```

Refresh the token
```
new_token = client.refresh_token()
```

Get user information
```
user = client.get_user_info()
```

Get API versions
```
user = client.get_versions()
```

Get all resources by the version specified in the client instantiation.
```
versions = client.get_versions()
```

Get all objects described
```
metadata = client.get_describe_global()
```

Get an object
```
object = client.get_sobject('Lead)
```

Create an object
```
data = {'LastName': 'Doe', 'IsConverted': 'False', 'Status': 'Open - Not Contacted', 'IsUnreadByOwner': 'False', 'Company': 'NA', 'FirstName': 'John'}
response = client.create_sobject('Lead', data)
```

Get an object described
```
metadata = client.get_sobject_describe('Lead')
```

## Requirements
- requests
