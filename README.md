# SCM Latam Challenge - Backend 


## 1. Instalación

Para descargar la aplicación del repo, se debe escribir el siguiente comando:

```
$ git clone https://github.com/FragmentosTemporales/scm-latam-challenge-backend
```

### Variables de entorno

Al interior de la carpeta /Sripts debes crear un documento env.env el cual debe contener las siguiente variables, puedes guiarte con el documento example.env :

```
FLASK_ENV=dev

JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_EXPIRES_HOURS=
JWT_ACCESS_TOKEN_EXPIRES_DAYS=
SECRET_KEY=

POSTGRES_USER=postgres
POSTGRES_PASSWORD=654321
POSTGRES_DB=example
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

En este repositorio en particular, incluyo valores de variables que *DEBEN* coincidir con el docker-compose.yml

### Instalación de Docker Compose

Para instalar la aplicación debes ejecutar el siguiente código, es necesario que las variables de entorno estén definidas para este punto:

```
$ docker compose build
```

## 2. Ejecución

Para ejecutar la aplicación debes ingresar el siguiente comando:

```
$ docker compose up
```

## 3.- ¿Qué podemos ejecutar?

En el archivo *manage.py* podrás encontrar comandos por consola. Una vez hayas iniciado la aplicación deberás vincularla a la base de datos:

```
$ docker compose run --rm scripts sh -c "python manage.py db init"
```

Luego deberás migrar:

```
$ docker compose run --rm scripts sh -c "python manage.py db migrate"
```

Para finalmente upgradear:

```
$ docker compose run --rm scripts sh -c "python manage.py db upgrade"
```

<hr/>

En estos momentos debes tener tu base de datos enlazada a tu aplicación, si es que quieres probar esto puedes ejecutar el siguiente comando:

```
$ docker compose run --rm scripts sh -c "python manage.py create-user --email example@mail.com --password 123456 --w_real 14"
```

En caso de estar funcionando todo correctamente debería retornar un mensaje tipo:

*"Usuario guardado correctamente"*

También puedes probar la función para crear el usuario a través del endpoint:

```
http://localhost:4000/register
```

Enviando un objeto JSON como el siguiente:

```
{
	"email": "example@mail.com",
	"password": "123456",
	"w_real": 14
}
```

<hr/>

A estas alturas ya estás en condiciones de insertar la información básica a la base de datos, para esto podrías usar los endpoints. Afortunadamente, para modos de prueba existe una función ejecutable desde consola:

```
$ docker compose run --rm scripts sh -c "python manage.py instalar"
```

Esto generará la data necesaria para poder ejecutar nuestra aplicación, hablamos de los horarios (Shifts) y demanda de trabajadores (Forecast).

### ¿Quieres probar?

Una vez creado el usuario y cargada la data básica podemos probar nuestra función ejecutando el siguiente comando:

```
$ docker compose run --rm scripts sh -c "python manage.py prueba"
```

Por consola te debería aparecer información sobre los objetos que se guardan en tu base de datos.


### ¿Y los testeos?

Si ya llegaste a este punto, podemos hablar de testeos.
Esta aplicación tiene desarrollados testeos para ciertos modelos, los cuales puedes ejecutar a través de la consola con el siguiente comando:

```
$ docker compose run --rm scripts sh -c "python manage.py test"
```

*IMPORTANTE*

No sólo podrás ejecutar los testeos, esta función también incluye flake8, un corrector de sintáxis diseñado para python, podrás ejecutarlo con el siguiente código:

```
$ docker compose run --rm scripts sh -c "python manage.py test && flake8"
```

<hr/>

### Terminando

En el archivo manage.py también encontrarás una función para eliminar la data almacenada en tu base de datos, esto eliminará todos los datos asociados al primer usuario creado (considéralo si quieres crear más de un usuario).


```
$ docker compose run --rm scripts sh -c "python manage.py eliminar"
```

## 4.- Bibliografía

A continuación te dejo el link con la documentación de Flask, específicamente la versión utilizada en este repositorio.

```
https://flask.palletsprojects.com/en/2.3.x/
```

También te dejo el repositorio (Jupyter Notebook) utilizado para crear esta aplicación:

```
https://github.com/crcordova/Disponibilidad_Algoritmo
```