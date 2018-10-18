# salesforce-python

salesforce-python is an API wrapper for Salesforce written in Python

## Installing
```
pip install salesforce-python
```

## Usage
```
from salesforce.client import Client

client = Client('CLIENT_KEY', 'CLIENT_SECRET', 'https://na50.salesforce.com/', 'v41.0') # Host must have trailing slash
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

### Webhooks
In order to create a webhook in Salesforce we need to create an APEX Class, Remote Site and Apex Trigger.

Create the APEX Class
```
In this example we are going to read the apex_class.txt file in the files folder included in this repository:

with open(os.path.join('/path/to/apex_class.txt'), 'r') as file:
    body = file.read()

response = client.create_apex_class('WebhookClass', body)
```

Create the Remote Site
```
URL is a string with the domain of your site:

url = 'https://mywebsite.com/'
response = client.create_remote_site('RemoteSiteSetting', url)
```

Create the APEX Trigger
```
To create the Trigger, we are going to read the apex_trigger.txt file and replace some values.

with open(os.path.join('/path/to/apex_trigger.txt'), 'r') as file:
    body = file.read()

sobject = 'User'
event = 'after insert'
url = 'https://mywebsite.com/notification_url/' #This is the domain url + your webhook path

body = body.replace('{sobject}', sobject)
body = body.replace('{events}', event)
body = body.replace('{url}', "'" + url + "'")

response = client.create_apex_trigger('WebhookTrigger', body, sobject)
```

That's all, you should receive notifications every time you create a new user in your Salesforce dashboard.

## Requirements
- requests

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.
#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/salesforce-python/issues).
#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/salesforce-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
