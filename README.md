# Onfleet Python Wrapper

![Build](https://img.shields.io/travis/onfleet/pyonfleet.svg?style=popout-square)
[![License](https://img.shields.io/github/license/onfleet/pyonfleet.svg?style=popout-square)](https://github.com/onfleet/pyonfleet/blob/master/LICENSE)
[![Latest version](https://img.shields.io/pypi/v/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)
![Top language](https://img.shields.io/github/languages/top/onfleet/pyonfleet.svg?style=popout-square)
[![Downloads](https://img.shields.io/pypi/dm/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)

> *Read this document in another language*:  
> [正體中文](https://github.com/onfleet/pyonfleet/blob/master/README.zh-tw.md)  
> [Español](https://github.com/onfleet/pyonfleet/blob/master/README.es.md)  

Visit our blog post on the [API wrapper project](https://onfleet.com/blog/api-wrappers-explained/) to learn more about our initiatives.  
If you have any questions, please reach us by submitting an issue [here](https://github.com/onfleet/pyonfleet/issues) or contact support@onfleet.com.

## Table of contents
* [Table of contents](#table-of-contents)
* [Synopsis](#synopsis)
* [Installation](#installation)
* [Usage](#usage)
    - [Throttling](#throttling)
    - [Responses](#responses)
    - [Supported CRUD operations](#supported-crud-operations)
        * [GET Requests](#get-requests)
            - [Examples of `get()`](#examples-of-get)
            - [Examples of `get(param)`](#examples-of-getparam)
            - [Examples of `getByLocation`](#examples-of-getbylocation)
        * [POST Requests](#post-requests)
            - [Examples of `create()`](#examples-of-create)
        * [PUT Requests](#put-requests)
            - [Examples of `update()`](#examples-of-update)
            - [Examples of `insertTask()`](#examples-of-inserttask)
        * [DELETE Requests](#delete-requests)
            - [Examples of `deleteOne()`](#examples-of-deleteone)

## Synopsis
The Onfleet Python library provides convenient access to the Onfleet API. 

## Installation
```
pip install pyonfleet
```

## Usage
Before using the API wrapper, you will need to obtain an API key from one of your organization's admins.

Creation and integration of API keys are performed through the [Onfleet dashboard](https://onfleet.com/dashboard#/manage).

To authenticate, you will also need to create a file named `.auth.json` under your working directory –this is where you will store your API credentials.

The format of `.auth.json` is shown below:
```json
{
    "API_KEY": "<your_api_key>"
}
```

You can also opt in to not store your API key here and pass it as param to `Onfleet`:
```python
from onfleet import Onfleet

# Option 1 - Recommended
onfleet_api = Onfleet()  # Using the .auth.json file

# Option 2
onfleet_api = Onfleet(api_key="<your_api_key>")  # Without the .auth.json file
```

Once the `Onfleet` object is created, you will get access to all the API endpoints as documented in the [Onfleet API documentation](https://docs.onfleet.com/).

### Throttling
Rate limiting is enforced by the API with a threshold of 20 requests per second across all your organization's API keys. Learn more about it [here](https://docs.onfleet.com/reference#throttling).

### Responses
Responses of this library are instances of [Response](https://2.python-requests.org//en/master/api/#requests.Response) from the `requests` library.

### Supported CRUD operations 
Here are the operations available for each entity:

| Entity | GET | POST | PUT | DELETE |
| :-: | :-: | :-: | :-: | :-: |
| [Admins/Administrators](https://docs.onfleet.com/reference#administrators) | get() | create(body), matchMetadata(body) | update(id, body) | deleteOne(id) |
| [Containers](https://docs.onfleet.com/reference#containers) | get(workers=id), get(teams=id), get(organizations=id) | x | update(id, body) | x |
| [Destinations](https://docs.onfleet.com/reference#destinations) | get(id) | create(body), matchMetadata(body) | x | x |
| [Hubs](https://docs.onfleet.com/reference#hubs) | get() | create(body) | update(id, body) | x |
| [Organization](https://docs.onfleet.com/reference#organizations) | get(), get(id) | x | insertTask(id, body) | x |
| [Recipients](https://docs.onfleet.com/reference#recipients) | get(id), get(name), get(phone) | create(body), matchMetadata(body) | update(id, body) | x |
| [Tasks](https://docs.onfleet.com/reference#tasks) | get(queryParams), get(id), get(shortId) | create(body), clone(id), forceComplete(id), batch(body), autoAssign(body), matchMetadata(body) | update(id, body) | deleteOne(id) |
| [Teams](https://docs.onfleet.com/reference#teams) | get(), get(id), getWorkerEta(id, queryParams) | create(body), autoDispatch(id, body) | update(id, body), insertTask(id, body) | deleteOne(id) |
| [Webhooks](https://docs.onfleet.com/reference#webhooks) | get() | create(body) | x | deleteOne(id) |
| [Workers](https://docs.onfleet.com/reference#workers) | get(), get(queryParams), get(id), getByLocation(queryParams), getSchedule(id) | create(body), setSchedule(id, body), matchMetadata(body) | update(id, body), insertTask(id, body) | deleteOne(id) |

#### GET Requests
To get all the documents within an endpoint:
```python
get()
```

##### Examples of `get()`
```python
onfleet_api.workers.get()
onfleet_api.workers.get(queryParams="")
```

Optionally you can use `queryParams` for some certain endpoints.  
Refer back to [API documentation](https://docs.onfleet.com/) for endpoints that support query parameters.
```python
# Option 1
onfleet_api.workers.get(queryParams="phones=<phone_number>")

# Option 2
onfleet_api.workers.get(queryParams={"phones": "<phone_number>"})
```

To get one of the document within an endpoint, specify the param that you wish to search by:
```python
get(param="<value>")
```

##### Examples of `get(param)`
```python
onfleet_api.workers.get(id="<24_digit_ID>")
onfleet_api.workers.get(id="<24_digit_ID>", queryParams={"analytics": "true"})

onfleet_api.tasks.get(shortId="<shortId>")

onfleet_api.recipients.get(phone="<phone_number>")
onfleet_api.recipients.get(name="<name>")

onfleet_api.containers.get(workers="<worker_ID>")
onfleet_api.containers.get(teams="<team_ID>")
onfleet_api.containers.get(organizations="<organization_ID>")
```

To get a driver by location, use the `getByLocation` function:
```python
getByLocation(queryParams="<location_params>")
```

##### Examples of `getByLocation`
```python
location_params = {
    "longitude": "-122.4",
    "latitude": "37.7601983",
    "radius": "6000",
}

onfleet_api.workers.getByLocation(queryParams=location_params)
```

#### POST Requests
To create a document within an endpoint:
```python
create(body="<data>")
```

##### Examples of `create()`
```python
data = {
    "name": "John Driver",
    "phone": "+16173428853",
    "teams": ["<team_ID>", "<team_ID> (optional)", "..."],
    "vehicle": {
        "type": "CAR",
        "description": "Tesla Model S",
        "licensePlate": "FKNS9A",
        "color": "purple",
    },
}

onfleet_api.workers.create(body=data)
```

Extended POST requests include `clone`, `forceComplete`, `batchCreate`, `autoAssign` on the *Tasks* endpoint; `setSchedule` on the *Workers* endpoint; `autoDispatch` on the *Teams* endpoint; and `matchMetadata` on all supported entities. For instance:

```python
onfleet_api.tasks.clone(id="<24_digit_ID>")
onfleet_api.tasks.forceComplete(id="<24_digit_ID>", body="<data>")
onfleet_api.tasks.batchCreate(body="<data>")
onfleet_api.tasks.autoAssign(body="<data>")

onfleet_api.workers.setSchedule(id="<24_digit_ID>", body="<data>")

onfleet_api.teams.autoDispatch(id="<24_digit_ID>", body="<data>")

onfleet_api.<entity_name_pluralized>.matchMetadata(body="<data>")
```

For more details, check our documentation on [`clone`](https://docs.onfleet.com/reference#clone-task), [`forceComplete`](https://docs.onfleet.com/reference#complete-task), [`batchCreate`](https://docs.onfleet.com/reference#create-tasks-in-batch), [`autoAssign`](https://docs.onfleet.com/reference#automatically-assign-list-of-tasks), [`setSchedule`](https://docs.onfleet.com/reference#set-workers-schedule), [`matchMetadata`](https://docs.onfleet.com/reference#querying-by-metadata), and [`autoDispatch`](https://docs.onfleet.com/reference#team-auto-dispatch).


#### PUT Requests
To update a document within an endpoint:
```python
update(id="<24_digit_ID>", body="<data>")
```

##### Examples of `update()`
```python
new_data = {
    "name": "Jack Driver",
}

onfleet_api.workers.update(id="<24_digit_ID>", body=new_data)
```

##### Examples of `insertTask()`
```python
onfleet_api.workers.insertTask(id="<24_digit_ID>", body="<data>")
```

#### DELETE Requests
To delete a document within an endpoint:
```python
deleteOne(id="<24_digit_ID>")
```

##### Examples of `deleteOne()`
```python
onfleet_api.workers.deleteOne(id="<24_digit_ID>")
```

*Go to [top](#onfleet-python-wrapper)*.