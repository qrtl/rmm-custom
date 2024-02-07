## AUTHENTICATION

- login
- logout

Before you can make use of this module, an access token is required for all requests except for the authentication endpoints.

#### Get Token

These following fields are needed for token generation:

1. `login`: a valid user login name or email.
2. `password`: the related password to the account in [1].
3. `db`: the database the user is trying to connect to.

```python
# Sample request.
import requests

url = "http://localhost:8069/api/auth/token"
headers = {
    "login": "admin",
    "password": "admin",
    "db": "api.ng",
    "content-type": "application/jsonp"
}

response = requests.get(url, headers=headers)
print(response.json())

Get Token Response

{
   "uid": 2,
   "user_context": {
     "lang": "en_US",
     "tz": "Europe/Brussels",
     "uid": 2
   },
   "company_id": 1,
   "company_ids": [
     1
   ],
   "partner_id": 3,
   "access_token": "access_token_bb4545413125847104b02a4e9a4aa8088a90903d",
   "company_name": "YourCompany",
   "currency": "USD",
   "country": "United States",
   "contact_address": "YourCompany\n215 Vine St\n\nScranton PA 18503\nUnited States",
   "customer_rank": 0
}

Delete token [LOGOUT]
To logout means that the token needs to be deleted.

import requests

url = "http://localhost:8069/api/sale.order/36"
headers = {
    "Content-Type": "message/http",
    "access-token": "access_token_bb4545413125847104b02a4e9a4aa8088a90903d"
}

response = requests.delete(url, headers=headers)
print(response.json())

CRUD Operation
To get or fetch existing sale order:

import requests

url = "http://192.168.43.58:8069/api/sale.order"
payload = "{\"limit\": 2, \"fields\": \"['id', 'partner_id', 'name']\", \"domain\":\"[('id', 'in', [10,11,12,13,14])]\", \"offset\":0}"
headers = {
    'access-token': "access_token_79406d541ea0a79a942e19871a9c806236d5638c",
    'content-type': "messsge/http"
}

response = requests.request("GET", url, data=payload, headers=headers)
print(response.text)

There is the possibility of applying some record filters in order to get just the specific record:

limit: This defines the total number of records we are expecting.
offset: Where the query will start from.
fields: This is the list of fields that we want to return, this can be left empty if we want to return all fields.
domain: Domain is like a filter; it is always a list of tuples (field, operator, value).
These payloads apply to all records in Odoo.

We can perform create, update, and delete operations on any records using corresponding HTTP request methods:

GET: For retrieving existing records.
POST: For creating new records.
PATCH: To call an action button on a record.
DELETE: To delete a record.
All the APIs of currently installed modules or any module that may be installed have already catered for dynamically. The API follows this semantic pattern:

/api/{api route}/model/{model name}/{optional id for delete request}

e.g., for sale order, a Get request to /api/sale.order endpoint will return all the sale orders in the system.

Sale Order
GET Request

import requests

url = "http://192.168.43.58:8069/api/sale.order"
payload = "{}"
headers = {
    'content-type': "message/http"
}

response = requests.request("GET", url, data=payload, headers=headers)
print(response.text)
Response

{
   "count": 1,
   "data": [
     {
       "id": 30,
       "name": "SO029",
       ...
     }
   ]
}
The response with all the fields, but the return fields can be specified alongside the request, and also, specific records can be specified by sending along the request Odoo domain as a JSON body.


{"limit": 2, "fields": "['id', 'partner_id', 'name']", "domain":"[('id', 'in', [10,11,12,13,14])]", "offset":0}
The above will only return 2 maximum records, id, partner, and sale order name, that have an ID in the given list [10,11,12,13,14], the offset can be set also.

POST (Create Sale Order)

import requests

url = "http://192.168.43.58:8069/api/sale.order"
payload = "{'partner_id': 10, '__api__order_line':"[(0, 0, {'product_id': 1,'price_unit':4000})]"}
headers = {
    'content-type': "message/http",
    'access-token': "access_token_79406d541ea0a79a942e19871a9c806236d5638c"
}

response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
Note the __api__order_line; this is a shortcut for creating the line item together with the main record, indicating that an order line or line items is being created from an API endpoint. order_line is the One2many field that links sale order and order line together.

This pattern is applicable to other models.

PATCH REQUEST
Patch request is meant for calling an action button on a record, e.g., validating a sale order.

import requests

url = "http://192.168.43.58:8069/api/sale.order/37"
payload = "{\"_method\":\"action_confirm\"}"
headers = {
    'content-type': "message/http",
    'access-token': "access_token_79406d541ea0a79a942e19871a9c806236d5638c"
}

response = requests.request("PATCH", url, data=payload, headers=headers)
print(response.text)

DELETE SALE ORDER

import requests

url = "http://192.168.43.58:8069/api/sale.order/37"
payload = "{}"
headers = {
    'content-type': "message/http",
    'access-token': "access_token_79406d541ea0a79a942e19871a9c806236d5638c"
}

response = requests.request("DELETE", url, data=payload, headers=headers)
print(response.text)

New Documentation
For accessing the new documentation:

http://localhost:8069/api/sale.order?limit=10&domain=id:>:1&fields=name,id,partner_id,origin&order=id asc&offset=10
