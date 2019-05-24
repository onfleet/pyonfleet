# Onfleet Python Wrapper

![Travis (.org)](https://img.shields.io/travis/onfleet/pyonfleet.svg?style=popout-square)
[![GitHub](https://img.shields.io/github/license/onfleet/pyonfleet.svg?style=popout-square)](https://github.com/onfleet/pyonfleet/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)
![GitHub top language](https://img.shields.io/github/languages/top/onfleet/pyonfleet.svg?style=popout-square)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)

*其他語言版本: [English](https://github.com/onfleet/pyonfleet/blob/master/README.md),[正體中文](https://github.com/onfleet/pyonfleet/blob/master/README.zh-tw.md)*

如果對於Onfleet應用程式介面或是我們產品有任何的問題，歡迎在此留言或直接聯繫 support@onfleet.com。

## 目錄
- [Onfleet Python Wrapper](#onfleet-python-wrapper)
  * [概要](#概要)
  * [安裝](#安裝)
  * [使用守則](#使用守則)
    + [API速限](#API速限)
    + [請求回應](#請求回應)
    + [支援的CRUD操作](#支援的CRUD操作)
      - [GET 請求](#get-請求)
        * [使用get展示所有資源的範例](#使用get展示所有資源的範例)
        * [使用get展示指定資源的範例](#使用get展示指定資源的範例)
      - [POST 請求](#post-請求)
        * [使用create提交指定資源的範例](#使用create提交指定資源的範例)
      - [PUT 請求](#put-請求)
        * [使用update取代指定資源的範例](#使用update取代指定資源的範例)
        * [使用insertTask取代指定資源的範例](#使用insertTask取代指定資源的範例)
      - [DELETE 請求](#delete-請求)
        * [使用deleteOne刪除指定資源的範例](#使用deleteone刪除指定資源的範例)


## 概要

`python_onfleet` 提供一個快速又便捷的方式，以獲取Onfleet應用程式介面內的資料。

## 安裝

```
pip install pyonfleet
```

## 使用守則
在使用Onfleet應用程式介面之前，請先索取應用程式介面金鑰。創建應用程式介面金鑰的詳情，請洽[Onfleet官方網站]((https://onfleet.com/dashboard#/manage)。

將您的金鑰取代下面的api_key參數即可開始使用：
在開始使用之前，請先在工作資料夾內創建一個檔案，並命名為`.auth.json`，內容存入您的金鑰參數。

`.auth.json`的格式如下:
```json
{
    "API_KEY": "<你的API金鑰>", 
}
```
當Onfleet物件成功被創建，而金鑰又是合法的，您會獲得訪問以下各endpoint資源的函式。欲獲得各endpoint資源的定義，請洽[Onfleet官方應用程式介面文件](http://docs.onfleet.com/)。

假如您不想儲存金鑰至檔案內，您亦可以直接引入API金鑰做為一參數：

```python
from onfleet import Onfleet

api = Onfleet() #有.auth.json檔案的前提
api = Onfleet(api_key="<your_api_key>") #直接引入參數
```
### API速限
原則上API的速限為每秒鐘20次請求，詳情請參考[官方文件](http://docs.onfleet.com/docs/throttling)。

### 請求回應
`pyonfleet`所回應的物件為一[Response物件](https://2.python-requests.org//en/master/api/#requests.Response)的本體。

### 支援的CRUD操作
Onfleet應用程式介面的基本URL為 `https://onfleet.com/api/v2`，下面為各endpoint所支援的函式列表：

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

#### GET 請求
展示所有資源的指令如下：
```python
get()
```
##### 使用get展示所有資源的範例
```python
api.workers.get()
api.workers.get(queryParams="")
```
部分的endpoint有支援queryParam（查詢參數），詳情請參考Onfleet官方文件：
```python
api.workers.get(queryParams="phones=<phone_number>")
```

展示指定資源的指令如下，根據欲展示的資源參數取代`param`則會根據參數做展示：
```python
get(param=<some_param>)
```

##### 使用get展示指定資源的範例
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

#### POST 請求
提交某單一指定資源的指令如下:
```python
create(body="<body_object>")
```
##### 使用create提交指定資源的範例
```python
driver = {
  "name": "A Swartz Test",
  "phone": "617-342-8853",
  "teams": ["W*8bF5jY11Rk05E0bXBHiGg2"],
  "vehicle": {
    "type": "CAR",
    "description": "Tesla Model S",
    "licensePlate": "FKNS9A",
    "color": "purple",
  }
}

api.workers.create(body=driver)
```
其他延伸的POST請求包含了tasks節點上的`clone`, `forceComplete`, `batchCreate`, `autoAssign`，以及workers節點上的`setSchedule`：

```python
api.tasks.clone(id="<24_digit_id>")
api.tasks.forceComplete(id="<24_digit_id>", body="<completion_details>")
api.tasks.batchCreate(body="<task_object_get>")
api.tasks.autoAssign(body="<auto_assign_object>")

api.workers.setSchedule(id="<24_digit_id>", body="<schedule_object>")
```
參考資料：[clone](http://docs.onfleet.com/docs/tasks#clone-task), [forceComplete](http://docs.onfleet.com/docs/tasks#complete-task), [batchCreate](http://docs.onfleet.com/docs/tasks#create-tasks-in-batch), [autoAssign](http://docs.onfleet.com/docs/tasks#automatically-assign-get-of-tasks)以及[setSchedule](http://docs.onfleet.com/docs/workers#set-workers-schedule).

#### PUT 請求
取代（更新）某單一指定資源的指令如下:
```python
update(id="<24_digit_id>", body="<body_object>")
```
##### 使用update取代指定資源的範例
```python
updateBody = {
    "name": "New Driver Name",
}
api.workers.update(id="<24_digit_id>", body=updateBody)
```
其他延伸的PUT請求包含了updateSchedule：
```python
api.workers.updateSchedule(id="<24_digit_id>", body=newSchedule)
```
參考資料：[updateSchedule](http://docs.onfleet.com/docs/workers#update-workers-schedule)

##### 使用insertTask取代指定資源的範例
```python
api.workers.insertTask(id="kAQ*G5hnqlOq4jVvwtGNuacl", body="<body_object>")
```

#### DELETE 請求
刪除某單一指定資源的指令如下:
```python
deleteOne(id="<24_digit_id>")
```
##### 使用deleteOne刪除指定資源的範例
```python
api.workers.deleteOne(id="<24_digit_id>")
```