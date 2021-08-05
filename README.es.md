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
Si tienen preguntas, nos pueden contactar creando un issue [aquí](https://github.com/onfleet/pyonfleet/issues) o escribiendo a support@onfleet.com.

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
Antes de usar la librería, es indispensable obtener una clave para la API a través de alguno de los administradores de la organización a la que pertenecemos.

La creación e integración de las claves para la API se realiza a través del [panel principal de Onfleet](https://onfleet.com/dashboard#/manage).

Para autenticarse en la API es necesario también crear un archivo `.auth.json` dentro del directorio de trabajo.  
En este archivo es donde se almacenarán las credenciales de la API.

El formato del archivo `.auth.json` es el siguiente:
```json
{
    "API_KEY": "<clave_para_la_api>"
}
```

También tenemos la opción de no crear dicho archivo y, en cambio, proporcionar la clave para la API directamente en cada petición:
```python
from onfleet import Onfleet

# Opción 1 - Recomendada
api = Onfleet()  # Utilizando el archivo .auth.json

# Opción 2
api = Onfleet(api_key="<clave_para_la_api>")  # Sin el archivo .auth.json
```

Una vez que el objeto `Onfleet` object es creado, obtendremos acceso a todos los recursos de la API referenciados en la [documentación de la API de Onfleet](https://docs.onfleet.com/).

### Límites
La API impone un límite de 20 peticiones por segundo, sumando las peticiones de todas las claves para la API disponibles en nuestra organización. [Aquí](https://docs.onfleet.com/reference#throttling) se pueden encontrar más detalles al respecto.

### Respuestas
Las respuestas de esta librería corresponden a instancias de [Response](https://2.python-requests.org//en/master/api/#requests.Response) de la librería `requests`.

### Operaciones CRUD soportadas
Estos son las ooperaciones disponibles para cada endpoint:

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
En la [documentación de la API](https://docs.onfleet.com/) están descritos qué recursos lo permiten.
```python
# Opción 1
api.workers.get(queryParams="phones=<phone_number>")

# Opción 2
api.workers.get(queryParams={"phones": "<phone_number>"})
```

Para obtener un elemento en particular dentro de un recurso se puede localizar mediante un parámetro específico, así:
```python
get(parametro="<dato>")
```

##### Ejemplos de `get(parametro)`
```python
api.workers.get(id="<ID_de_24_digitos>")
api.workers.get(id="<ID_de_24_digitos>", queryParams={"analytics": "true"})

api.tasks.get(shortId="<shortID>")

api.recipients.get(phone="<phone_number>")
api.recipients.get(name="<name>")

api.containers.get(workers="<ID_de_un_worker>")
api.containers.get(teams="<ID_de_un_team>")
api.containers.get(organizations="<ID_de_un_organization>")
```

Para obtener un conductor según su ubicación, podemos utilizar la funcion `getByLocation`:
```python
getByLocation(queryParams="<datos_de_ubicacion>")
```

##### Ejemplos de `getByLocation`:
```python
datos_de_ubicacion = {
    "longitude": "-122.4",
    "latitude": "37.7601983",
    "radius": "6000",
}

api.workers.getByLocation(queryParams=datos_de_ubicacion)
```

#### Peticiones POST
Para crear un elemento de un recurso:
```python
create(body="<datos>")
```

##### Ejemplos de `create()`
```python
datos = {
    "name": "Hola Mundo",
    "phone": "+16173428853",
    "teams": ["<ID_de_un_team>", "<otro_ID_de_un_team> (opcional)", ...],
    "vehicle": {
        "type": "CAR",
        "description": "Tesla Model S",
        "licensePlate": "FKNS9A",
        "color": "purple",
    },
}

api.workers.create(body=datos)
```

Otras peticiones POST incluyen `clone`, `forceComplete`, `batchCreate`, `autoAssign` en el recurso *Tasks*; `setSchedule` en el recurso *Workers*; `autoDispatch` en el recurso *Teams*; y `matchMetadata` en todos los recursos que lo soportan. Por ejemplo:

```python
api.tasks.clone(id="<ID_de_24_digitos>")
api.tasks.forceComplete(id="<ID_de_24_digitos>", body="<datos>")
api.tasks.batchCreate(body="<datos>")
api.tasks.autoAssign(body="<datos>")

api.workers.setSchedule(id="<ID_de_24_digitos>", body="<datos>")

api.teams.autoDispatch(id="<ID_de_24_digitos>", body="<datos>")

api.<recurso>.matchMetadata(body="<datos>")
```

Para más información, podemos consultar la documentación sobre [`clone`](https://docs.onfleet.com/reference#clone-task), [`forceComplete`](https://docs.onfleet.com/reference#complete-task), [`batchCreate`](https://docs.onfleet.com/reference#create-tasks-in-batch), [`autoAssign`](https://docs.onfleet.com/reference#automatically-assign-list-of-tasks), [`setSchedule`](https://docs.onfleet.com/reference#set-workers-schedule) y [`matchMetadata`](https://docs.onfleet.com/reference#querying-by-metadata).


#### Peticiones PUT
Para modificar un elemento de un recurso:
```python
update(id="<ID_de_24_digitos>", body="<datos>")
```

##### Ejemplos de `update()`
```python
datos_nuevos = {
    "name": "Nombre Nuevo",
}

api.workers.update(id="<ID_de_24_digitos>", body=datos_nuevos)
```

##### Ejemplos de `updateSchedule()`
```python
api.workers.updateSchedule(id="<ID_de_24_digitos>", body="<datos>")
```
Para más información, podemos consultar la documentación sobre [`updateSchedule`](https://docs.onfleet.com/reference#update-workers-schedule).

##### Ejemplos de `insertTask()`
```python
api.workers.insertTask(id="<ID_de_24_digitos>", body="<datos>")
```

#### Peticiones DELETE
Para eliminar un elemento de un recurso:
```python
deleteOne(id="<ID_de_24_digitos>")
```

##### Ejemplos de `deleteOne()`
```python
api.workers.deleteOne(id="<ID_de_24_digitos>")
```

*Ir al [inicio](#onfleet-python-wrapper)*.