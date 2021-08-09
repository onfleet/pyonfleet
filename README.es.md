# Onfleet Python Wrapper

![Build](https://img.shields.io/travis/onfleet/pyonfleet.svg?style=popout-square)
[![Licencia](https://img.shields.io/github/license/onfleet/pyonfleet.svg?style=popout-square)](https://github.com/onfleet/pyonfleet/blob/master/LICENSE)
[![PyPI - Versión](https://img.shields.io/pypi/v/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)
![GitHub - Lenguaje principal](https://img.shields.io/github/languages/top/onfleet/pyonfleet.svg?style=popout-square)
[![PyPI - Descargas](https://img.shields.io/pypi/dm/pyonfleet.svg?style=popout-square)](https://pypi.org/project/pyonfleet/)

> *Este documento esta disponible en otros idiomas*:  
> [English](https://github.com/onfleet/pyonfleet/blob/master/README.md)  
> [正體中文](https://github.com/onfleet/pyonfleet/blob/master/README.zh-tw.md)  

Los invitamos a visitar nuestra publicación sobre el [proyecto de librerías para la API](https://onfleet.com/blog/api-wrappers-explained/) para conocer más sobre nuestras iniciativas.  
En caso de preguntas, pueden contactarnos a través de un issue [aquí](https://github.com/onfleet/pyonfleet/issues) o escribirnos a support@onfleet.com.

## Tabla de contenidos
* [Tabla de contenidos](#tabla-de-contenidos)
* [Sinopsis](#sinopsis)
* [Instalación](#instalación)
* [Uso](#uso)
* [Límites](#límites)
* [Respuestas](#respuestas)
* [Operaciones CRUD soportadas](#operaciones-crud-soportadas)
    - [Peticiones GET](#peticiones-get)
        * [Ejemplos de `get()`](#ejemplos-de-get)
        * [Ejemplos de `get(parametro)`](#ejemplos-de-getparametro)
        * [Ejemplos de `getByLocation`](#ejemplos-de-getbylocation)
    - [Peticiones POST](#peticiones-post)
        * [Ejemplos de `create()`](#ejemplos-de-create)
    - [Peticiones PUT](#peticiones-put)
        * [Ejemplos de `update()`](#ejemplos-de-update)
        * [Ejemplos de `updateSchedule()`](#ejemplos-de-updateschedule)
        * [Ejemplos de `insertTask()`](#ejemplos-de-inserttask)
    - [Peticiones DELETE](#peticiones-delete)
        * [Ejemplos de `deleteOne()`](#ejemplos-de-deleteone)

## Sinopsis
La librería en Python de Onfleet nos permite un acceso fácil y cómodo a la API de Onfleet.

## Instalación
```
pip install pyonfleet
```

## Uso
Antes de usar la librería, es indispensable obtener una llave para la API a través de alguno de los administradores de la organización a la que pertenecemos.

La creación e integración de llaves se realiza a través del [panel principal de Onfleet](https://onfleet.com/dashboard#/manage).

Para autenticarse en la API es necesario también crear un archivo `.auth.json` dentro del directorio de trabajo.  
En este archivo es donde se almacenarán las credenciales de la API.

El formato del archivo `.auth.json` es el siguiente:
```json
{
    "API_KEY": "<your_api_key>"
}
```

También tenemos la opción de no crear dicho archivo y, en cambio, proporcionar la llave cuando creamos una instancia de `Onfleet`:
```python
from onfleet import Onfleet

# Opción 1 - Recomendada
api = Onfleet()  # Utilizando el archivo .auth.json

# Opción 2
api = Onfleet(api_key="<your_api_key>")  # Sin el archivo .auth.json
```

Una vez que el objeto `Onfleet` object es creado, obtendremos acceso a todos los recursos de la API referenciados en la [documentación de la API de Onfleet](https://docs.onfleet.com/).

### Límites
La API impone un límite de 20 peticiones por segundo entre todas las peticiones de todas las llaves de la organización. Más detalles [aquí](https://docs.onfleet.com/reference#throttling).

### Respuestas
Las respuestas de esta librería son instancias de [Response](https://2.python-requests.org//en/master/api/#requests.Response) de la librería `requests`.

### Operaciones CRUD soportadas
Estas son las operaciones disponibles para cada endpoint:

| Recurso | GET | POST | PUT | DELETE |
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

#### Peticiones GET
Para obtener todos los elementos disponibles en un recurso:
```python
get()
```

##### Ejemplos de `get()`
```python
api.workers.get()
api.workers.get(queryParams="")
```

Opcionalmente, podemos utilizar `queryParams` en los recursos que lo soportan.  
En la [documentación de la API](https://docs.onfleet.com/) se describe qué recursos lo permiten.
```python
# Opción 1
api.workers.get(queryParams="phones=<phone_number>")

# Opción 2
api.workers.get(queryParams={"phones": "<phone_number>"})
```

Para obtener un elemento dentro de un recurso, éste se puede localizar mediante un parámetro específico:
```python
get(param="<value>")
```

##### Ejemplos de `get(parametro)`
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

Para obtener un driver según su ubicación, podemos utilizar la función `getByLocation`:
```python
getByLocation(queryParams="<location_params>")
```

##### Ejemplos de `getByLocation`:
```python
location_params = {
    "longitude": "-122.4",
    "latitude": "37.7601983",
    "radius": "6000",
}

api.workers.getByLocation(queryParams=location_params)
```

#### Peticiones POST
Para crear un elemento de un recurso:
```python
create(body="<data>")
```

##### Ejemplos de `create()`
```python
data = {
    "name": "John Driver",
    "phone": "+16173428853",
    "teams": ["<team_ID>", "<team_ID> (opcional)", ...],
    "vehicle": {
        "type": "CAR",
        "description": "Tesla Model S",
        "licensePlate": "FKNS9A",
        "color": "purple",
    },
}

api.workers.create(body=data)
```

Otras peticiones POST incluyen `clone`, `forceComplete`, `batchCreate`, `autoAssign` en el recurso *Tasks*; `setSchedule` en el recurso *Workers*; `autoDispatch` en el recurso *Teams*; y `matchMetadata` en todos los recursos que lo soportan. Por ejemplo:

```python
api.tasks.clone(id="<24_digit_ID>")
api.tasks.forceComplete(id="<24_digit_ID>", body="<data>")
api.tasks.batchCreate(body="<data>")
api.tasks.autoAssign(body="<data>")

api.workers.setSchedule(id="<24_digit_ID>", body="<data>")

api.teams.autoDispatch(id="<24_digit_ID>", body="<data>")

api.<entity>.matchMetadata(body="<data>")
```

Para más información, podemos consultar la documentación sobre [`clone`](https://docs.onfleet.com/reference#clone-task), [`forceComplete`](https://docs.onfleet.com/reference#complete-task), [`batchCreate`](https://docs.onfleet.com/reference#create-tasks-in-batch), [`autoAssign`](https://docs.onfleet.com/reference#automatically-assign-list-of-tasks), [`setSchedule`](https://docs.onfleet.com/reference#set-workers-schedule) y [`matchMetadata`](https://docs.onfleet.com/reference#querying-by-metadata).


#### Peticiones PUT
Para modificar un elemento de un recurso:
```python
update(id="<24_digit_ID>", body="<data>")
```

##### Ejemplos de `update()`
```python
new_data = {
    "name": "Jack Driver",
}

api.workers.update(id="<24_digit_ID>", body=new_data)
```

##### Ejemplos de `updateSchedule()`
```python
api.workers.updateSchedule(id="<24_digit_ID>", body="<data>")
```
Para más información, podemos consultar la documentación sobre [`updateSchedule`](https://docs.onfleet.com/reference#update-workers-schedule).

##### Ejemplos de `insertTask()`
```python
api.workers.insertTask(id="<24_digit_ID>", body="<data>")
```

#### Peticiones DELETE
Para eliminar un elemento de un recurso:
```python
deleteOne(id="<24_digit_ID>")
```

##### Ejemplos de `deleteOne()`
```python
api.workers.deleteOne(id="<24_digit_ID>")
```

*Ir al [inicio](#onfleet-python-wrapper)*.