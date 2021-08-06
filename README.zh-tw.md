# Onfleet Python Wrapper

![Build](https://img.shields.io/travis/onfleet/pyonfleet.svg?style=popout-square)
[![License](https://img.shields.io/github/license/onfleet/pyonfleet.svg?style=popout-square)](https://github.com/onfleet/pyonfleet/blob/master/LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)
![GitHub - Top language](https://img.shields.io/github/languages/top/onfleet/pyonfleet.svg?style=popout-square)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)

> *其他語言版本*:  
> [English](https://github.com/onfleet/pyonfleet/blob/master/README.md)  
> [Español](https://github.com/onfleet/pyonfleet/blob/master/README.es.md)  

欲了解本開源專案的背景，請參閱[我們的部落格](https://onfleet.com/blog/api-wrappers-explained/)，如果對於Onfleet應用程式介面或是我們產品有任何的問題，歡迎[在此留言](https://github.com/onfleet/pyonfleet/issues)或直接聯繫 support@onfleet.com。

## 目錄
* [目錄](#目錄)
* [概要](#概要)
* [安裝](#安裝)
* [使用守則](#使用守則)
* [API速限](#API速限)
* [請求回應](#請求回應)
* [支援的CRUD操作](#支援的CRUD操作)
    - [GET 請求](#get-請求)
        * [使用`get`展示所有資源的範例](#使用get展示所有資源的範例)
        * [使用`get(param)`展示指定資源的範例](#使用get展示指定資源的範例)
    - [POST 請求](#post-請求)
        * [使用`create`提交指定資源的範例](#使用create提交指定資源的範例)
    - [PUT 請求](#put-請求)
        * [使用`update`取代指定資源的範例](#使用update取代指定資源的範例)
        * [使用`insertTask`取代指定資源的範例](#使用insertTask取代指定資源的範例)
    - [DELETE 請求](#delete-請求)
        * [使用`deleteOne`刪除指定資源的範例](#使用deleteone刪除指定資源的範例)


## 概要
`python_onfleet` 提供一個快速又便捷的方式，以獲取Onfleet應用程式介面內的資料。

## 安裝
```
pip install pyonfleet
```

## 使用守則
在使用Onfleet應用程式介面之前，請先索取應用程式介面金鑰。創建應用程式介面金鑰的詳情，請洽[Onfleet官方網站](https://onfleet.com/dashboard#/manage)。

將您的金鑰取代下面的api_key參數即可開始使用：
在開始使用之前，請先在工作資料夾內創建一個檔案，並命名為`.auth.json`，內容存入您的金鑰參數。

`.auth.json`的格式如下:
```json
{
    "API_KEY": "<your_API_key>"
}
```

當Onfleet物件成功被創建，而金鑰又是合法的，您會獲得訪問以下各endpoint資源的函式。欲獲得各endpoint資源的定義，請洽[Onfleet官方應用程式介面文件](http://docs.onfleet.com/)。

假如您不想儲存金鑰至檔案內，您亦可以直接引入API金鑰做為一參數：

```python
from onfleet import Onfleet

api = Onfleet()  # 有.auth.json檔案的前提

api = Onfleet(api_key="<your_api_key>")  # 直接引入參數
```
### API速限
原則上API的速限為每秒鐘20次請求，詳情請參考[官方文件](https://docs.onfleet.com/reference#throttling)。

### 請求回應
`pyonfleet`所回應的物件為一[Response物件](https://2.python-requests.org//en/master/api/#requests.Response)的本體。

### 支援的CRUD操作
下面為各entity所支援的函式列表：

| Entity | GET | POST | PUT | DELETE |
|:------------:|:---------------------------------------------------------------:|:----------------------------------------------------------------------:|:------------------------------------:|:-------------:|
| [Admins/Administrators](https://docs.onfleet.com/reference#administrators) | get() | create(body), matchMetadata(body) | update(id, body) | deleteOne(id) |
| [Containers](https://docs.onfleet.com/reference#containers) | get(workers=id), get(teams=id), get(organizations=id) | x | update(id, body) | x |
| [Destinations](https://docs.onfleet.com/reference#destinations) | get(id) | create(body), matchMetadata(body) | x | x |
| [Hubs](https://docs.onfleet.com/reference#hubs) | get() | create(body) | update(id, body) | x |
| [Organization](https://docs.onfleet.com/reference#organizations) | get(), get(id) | x | insertTask(id, body) | x |
| [Recipients](https://docs.onfleet.com/reference#recipients)  | get(id), get(name), get(phone) | create(body), matchMetadata(body) | update(id, body) | x |
| [Tasks](https://docs.onfleet.com/reference#tasks) | get(queryParams), get(id), get(shortId) | create(body), clone(id), forceComplete(id), batch(body), autoAssign(body), matchMetadata(body) | update(id, body) | deleteOne(id) |
| [Teams](https://docs.onfleet.com/reference#teams) | get(), get(id), getWorkerEta(id, queryParams) | create(body), autoDispatch(id, body) | update(id, body), insertTask(id, body) | deleteOne(id) |
| [Webhooks](https://docs.onfleet.com/reference#webhooks) | get() | create(body) | x | deleteOne(id) |
| [Workers](https://docs.onfleet.com/reference#workers) | get(), get(queryParams), get(id), getByLocation(queryParams), getSchedule(id) | create(body), setSchedule(id, body), matchMetadata(body) | update(id, body), insertTask(id, body) | deleteOne(id) |

#### GET 請求
展示所有資源的指令如下：
```python
get()
```

##### 使用`get`展示所有資源的範例
```python
api.workers.get()
api.workers.get(queryParams="")
```

部分的endpoint有支援`queryParams`（查詢參數），詳情請參考Onfleet官方文件：
```python
# Option 1
api.workers.get(queryParams="phones=<phone_number>")

# Option 2
api.workers.get(queryParams={"phones": "<phone_number>"})
```

展示指定資源的指令如下，根據欲展示的資源參數取代`param`則會根據參數做展示：
```python
get(param=<some_param>)
```

##### 使用`get(param)`展示指定資源的範例
```python
api.workers.get(id="<24_digit_ID>")
api.workers.get(id="<24_digit_ID>", queryParams={"analytics": "true"})

api.tasks.get(shortId="<shortId>")

api.recipients.get(phone="<phone_number>")
api.recipients.get(name="<name>")

api.containers.get(workers="<worker_ID>")
api.containers.get(teams="<team_ID>")
api.containers.get(organizations="<organization_ID>")
```

#### POST 請求
提交某單一指定資源的指令如下:
```python
create(body="<data>")
```

##### 使用`create`提交指定資源的範例
```python
data = {
    "name": "John Driver",
    "phone": "+16173428853",
    "teams": ["<team_ID>", "<team_ID> (optional)", ...],
    "vehicle": {
        "type": "CAR",
        "description": "Tesla Model S",
        "licensePlate": "FKNS9A",
        "color": "purple",
    },
}

api.workers.create(body=data)
```
其他延伸的POST請求包含了*Tasks*節點上的`clone`, `forceComplete`, `batchCreate`, `autoAssign`，*Workers*節點上的`setSchedule`，*Teams*節點上的`autoDispatch`，以及所有支持節點上的`matchMetadata`：

```python
api.tasks.clone(id="<24_digit_ID>")
api.tasks.forceComplete(id="<24_digit_ID>", body="<data>")
api.tasks.batchCreate(body="<data>")
api.tasks.autoAssign(body="<data>")

api.workers.setSchedule(id="<24_digit_ID>", body="<data>")

api.teams.autoDispatch(id="<24_digit_ID>", body="<data>")

api.<entity>.matchMetadata(body="<data>")
```

參考資料：[`clone`](https://docs.onfleet.com/reference#clone-task), [`forceComplete`](https://docs.onfleet.com/reference#complete-task), [`batchCreate`](https://docs.onfleet.com/reference#create-tasks-in-batch), [`autoAssign`](https://docs.onfleet.com/reference#automatically-assign-list-of-tasks), [`setSchedule`](https://docs.onfleet.com/reference#set-workers-schedule), [`matchMetadata`](https://docs.onfleet.com/reference#querying-by-metadata), 以及[`autoDispatch`](https://docs.onfleet.com/reference#team-auto-dispatch)。

#### PUT 請求
取代（更新）某單一指定資源的指令如下:
```python
update(id="<24_digit_ID>", body="<data>")
```

##### 使用`update`取代指定資源的範例
```python
new_data = {
    "name": "Jack Driver",
}

api.workers.update(id="<24_digit_ID>", body=new_data)
```

其他延伸的PUT請求包含了`updateSchedule`：
```python
api.workers.updateSchedule(id="<24_digit_ID>", body="<data>")
```
參考資料：[updateSchedule](https://docs.onfleet.com/reference#update-workers-schedule)

##### 使用`insertTask`取代指定資源的範例
```python
api.workers.insertTask(id="24_digit_ID", body="<data>")
```

#### DELETE 請求
刪除某單一指定資源的指令如下:
```python
deleteOne(id="<24_digit_ID>")
```

##### 使用`deleteOne`刪除指定資源的範例
```python
api.workers.deleteOne(id="<24_digit_ID>")
```

*返回[頂端](#onfleet-python-wrapper)*。