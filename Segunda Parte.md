# Parte 2 - Preguntas conceptuales

## ¿Cómo enfrentarías el problema en el caso de que la demanda se encontrara en periodos de 15 minutos (96 datos por día)?

R.- En lugar de almacenar toda la información en instancias diferentes, realizaría un diccionario JSON con la mayor cantidad de información y la almacenaría como una sola instancia. De este modo, la cantidad de consultas a la base de datos sería menor, la información se podría ubicar más fácilmente y posibilita la ejecución del servicio desde diferentes usuarios a la misma base de datos.

## ¿Podrías levantar todo este proceso en un solo microservicio (monolito)? ¿Qué ventajas y desventajas tendría pensado en que el servicio se utiliza en productivo para varios clientes?

R.- El proceso se podría levantar en un solo microservicio, esto debido a que se genera una clase que se amolda a los parámetros recibidos desde el modelo User. Una de las mayores desventajas es la gran acumulación de información en las bases de datos, en este sentido, sería prudente cambiar la estructura en que se almacena la información.   

## ¿Qué proceso implementarías en el caso que se deba ejecutar esta solución 1000 veces? ¿Qué cambios harías a tu implementación?

R.- Añadiría información adicional a la función set_availability(), generando un campo "SESSION", de esta manera, el usuario podría realizar muchas veces una consulta, sobre diferentes áreas en caso de ser necesario. El atributo "SESSION" se utilizaría para diferenciar los turnos. Otra opción sería, como mencioné anteriormente, guardar toda la información realizada en la sessión en un sólo diccionario JSON, de esta manera no sobrecargamos la base de datos con consultas.
