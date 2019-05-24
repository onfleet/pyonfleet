# Onfleet Python Wrapper

![Travis (.org)](https://img.shields.io/travis/onfleet/pyonfleet.svg?style=popout-square)
[![GitHub](https://img.shields.io/github/license/onfleet/pyonfleet.svg?style=popout-square)](https://github.com/onfleet/pyonfleet/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)
![GitHub top language](https://img.shields.io/github/languages/top/onfleet/pyonfleet.svg?style=popout-square)
[![Downloads](https://pepy.tech/badge/pyonfleet)](https://pepy.tech/project/pyonfleet)

*Read this document in another language: [English](https://github.com/onfleet/pyonfleet/blob/master/README.md), [正體中文](https://github.com/onfleet/pyonfleet/blob/master/README.zh-tw.md)*

If you have any questions, please reach out to Onfleet by submitting an issue [here](https://github.com/onfleet/pyonfleet/issues) or contact support@onfleet.com

## Table of Contents
- [Onfleet Python Wrapper](#onfleet-python-wrapper)
  * [Table of Contents](#table-of-contents)
  * [Synopsis](#synopsis)
  * [Installation](#installation)
  * [Usage](#usage)
    + [Throttling](#throttling)
    + [Responses](#responses)
    + [Supported CRUD Operations](#supported-crud-operations)
      - [GET Requests](#get-requests)
        * [Examples of get()](#examples-of-get--)
        * [Examples of get(param)](#examples-of-get-param-)
        * [Examples of getByLocation:](#examples-of-getbylocation-)
      - [POST Requests](#post-requests)
        * [Examples of create()](#examples-of-create--)
      - [PUT Requests](#put-requests)
        * [Examples of update()](#examples-of-update--)
        * [Examples of updateSchedule()](#examples-of-updateschedule--)
        * [Examples of insertTask()](#examples-of-inserttask--)
      - [DELETE Requests](#delete-requests)
        * [Examples of deleteOne()](#examples-of-deleteone--)

## Synopsis

The Onfleet Python library provides convenient access to the Onfleet API. 

## Installation

```
pip install pyonfleet
```
## Usage
Before using the API wrapper, you will need to obtain an API key from your organization admin. Creation and integration of API keys are performed through the [Onfleet dashboard](https://onfleet.com/dashboard#/manage).

To authenticate, you will also need to create a file named `.auth.json` under your working directory, this is where you will store your API credentials.

The format of `.auth.json` is shown below:
```json
{
    "API_KEY": "<your_api_key>", 
}
```
You can also opt in to not store your API key here and use it on the fly instead.

Once the Onfleet object is created, you will get access to all the API endpoints as documented in the [Onfleet API documentation](http://docs.onfleet.com/). Here are some usage case:
```python
from onfleet import Onfleet

api = Onfleet() # if .auth.json was provided
api = Onfleet(api_key="<your_api_key>") # if no .auth.json was provided
```

### Throttling
Rate limiting is enforced by the API with a threshold of 20 requests per second across all your organization's API keys, learn more about it [here](http://docs.onfleet.com/docs/throttling). 

### Responses
The `pyonfleet` API wrapper returns the body of a [Response object](https://2.python-requests.org//en/master/api/#requests.Response).

### Supported CRUD Operations 
The base URL for the Onfleet API is `https://onfleet.com/api/v2`, here are the supported CRUD operations for each endpoint:

| `<endpoint>` | GET | POST | PUT | DELETE |
|:------------:|:---------------------------------------------------------------:|:----------------------------------------------------------------------:|:------------------------------------:|:-------------:|
| [Admins](http://docs.onfleet.com/docs/administrators) | get() | create(body) | update(id, body) | deleteOne(id) |
| [Containers](http://docs.onfleet.com/docs/containers) | get(workers=id), get(teams=id), get(organizations=id) | x | update(id, body) | x |
| [Destinations](http://docs.onfleet.com/docs/destinations) | get(id) | create(body) | x | x |
| [Hubs](http://docs.onfleet.com/docs/hubs) | get() | x | x | x |
| [Organization](http://docs.onfleet.com/docs/organizations) | get(), get(id) | x | insertTask(id, body) | x |
| [Recipients](http://docs.onfleet.com/docs/recipients)  | get(id), get(name), get(phone) | create(body) | update(id, body) | x |
| [Tasks](http://docs.onfleet.com/docs/tasks) | get(queryParams), get(id), get(shortId) | create(body), clone(id), forceComplete(id), batch(body), autoAssign(body) | update(id, body) | deleteOne(id) |
| [Teams](http://docs.onfleet.com/docs/teams) | get(), get(id) | create(body) | update(id, body), insertTask(id, body) | deleteOne(id) |
| [Webhooks](http://docs.onfleet.com/docs/webhooks) | get() | create(body) | x | deleteOne(id) |
| [Workers](http://docs.onfleet.com/docs/workers) | get(), get(queryParams), get(id), getByLocation(queryParams), getSchedule(id) | create(body), setSchedule(id, body) | update(id, body), insertTask(id, body) | deleteOne(id) |

#### GET Requests
To get all the documents within an endpoint:
```python
get()
```
##### Examples of get()
```python
api.workers.get()
api.workers.get(queryParams="")
```
Option to use query parameters for some certain endpoints, refer back to API documents for endpoints that support query parameters:
```python
api.workers.get(queryParams="phones=<phone_number>")

or

api.workers.get(queryParams={"phones":"<phone_number>"})
```

To get one of the document within an endpoint, specify the param that you wish to search by:
```python
get(param=<some_param>)
```

##### Examples of get(param) 
```python
api.workers.get(id="<24_digit_id>")
api.workers.get(id="<24_digit_id>", queryParams={"analytics": "true"})
api.tasks.get(shortId="<shortId>")
api.recipients.get(phone="<phone_number>")
api.recipients.get(name="<recipient_name>")

api.containers.get(workers="<worker_id>")
api.containers.get(teams="<team_id>")
api.containers.get(organizations="<org_id>")
```
To get a driver by location, use the `getByLocation` function:
```python
getByLocation(queryParams=<some_param>)
```

##### Examples of getByLocation:
```python
params = {"longitude":"-122.4","latitude":"37.7601983","radius":"6000"}
api.workers.getByLocation(queryParams=params)
```

#### POST Requests
To create a document within an endpoint:
```python
create(body="<body_object>")
```
##### Examples of create()
```python
driver = {
  "name": "A Swartz Test",
  "phone": "+16173428853",
  "teams": ["<a_team_id>", "<a_team_id> (optional)..."],
  "vehicle": {
    "type": "CAR",
    "description": "Tesla Model S",
    "licensePlate": "FKNS9A",
    "color": "purple",
  }
}

api.workers.create(body=driver)
```
Extended POST requests include `clone`, `forceComplete`, `batchCreate`, `autoAssign` on the tasks endpoint, and `setSchedule` on the workers endpoint:

```python
api.tasks.clone(id="<24_digit_id>")
api.tasks.forceComplete(id="<24_digit_id>", body="<completion_details>")
api.tasks.batchCreate(body="<task_object_get>")
api.tasks.autoAssign(body="<auto_assign_object>")

api.workers.setSchedule(id="<24_digit_id>", body="<schedule_object>")
```
For more details, check our documentation on [clone](http://docs.onfleet.com/docs/tasks#clone-task), [forceComplete](http://docs.onfleet.com/docs/tasks#complete-task), [batchCreate](http://docs.onfleet.com/docs/tasks#create-tasks-in-batch), [autoAssign](http://docs.onfleet.com/docs/tasks#automatically-assign-get-of-tasks), and [setSchedule](http://docs.onfleet.com/docs/workers#set-workers-schedule).

#### PUT Requests
To update a document within an endpoint:
```python
update(id="<24_digit_id>", body="<body_object>")
```
##### Examples of update()
```python
updateBody = {
    "name": "New Driver Name",
}
api.workers.update(id="<24_digit_id>", body=updateBody)
```
##### Examples of updateSchedule()
```python
api.workers.updateSchedule(id="<24_digit_id>", body=newSchedule)
```
For more details, check our documentation on [updateSchedule](http://docs.onfleet.com/docs/workers#update-workers-schedule)

##### Examples of insertTask()
```python
api.workers.insertTask(id="kAQ*G5hnqlOq4jVvwtGNuacl", body="<body_object>")
```

#### DELETE Requests
To delete a document within an endpoint:
```python
deleteOne(id="<24_digit_id>")
```
##### Examples of deleteOne()
```python
api.workers.deleteOne(id="<24_digit_id>")
```
