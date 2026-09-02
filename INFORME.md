Redactar un breve informe en donde se detallen los aspectos más importantes de la solución provista, como ser el protocolo de comunicación implementado y los mecanismos para sincronizar la ejecución concurrente.

Hasta ej 5 (es protocolo texto):

El protocolo consiste en una primer comunicación del cliente al servidor informando el id de la agencia correspondiente en 1 byte, para que posteriormente el server pueda mandarle al cliente solo los ganadores correspondientes a esta agencia.
Posteriormente se entra en un loop en el cliente, donde se envia un mensaje por cada linea del archivo INPUT_FILE. Este mensaje consta de 2 partes: un "header" de 4 bytes que indica la longitud de la linea a leer a continuación, y luego el propio mensaje. El servidor sabe que debe leeer 4 bytes y en base a lo recibido leer N mas, pudiendo mediante ciclos garantizarse la llegada del mensaje completo y evitando asi short read/write.
El server recibe las apuestas de distintos clientes y la clase lottery se encarga de filtrar a los ganadores. Es el protocolo el que, en base a los resultados de lottery, parsea las apuestas ganadoras para su posterior envio a los clientes.
El envio de los ganadores sigue la misma idea: hay 4 bytes que indican el largo de la linea que representa una apuesta ganadora, seguido por las bbytes correspondientes a la apuesta. Esto permite al cliente poder determinar la longitud del mensaje correspondiente a una apuesta que debe persistir en OUTPUT_FILE

La idea es dessacoplar en capas. Tanto cliente como servidor se comunican con el protocolo, y el protocolo es quien habla con safe_socket haciendo las validaciones propias para garantizar la correcta comunicacion. El socket realiza el envio/recepción de bytes, garantizando que no hay short write/read medainte ciclos.

Ej: 6

Se agrego una "capa" superior al protocolo. Simplemente se modificaron las funciones existentes para que no se lean 2 campos linea a linea.
El cliente enviara primero 4 bytes con la cantidad de elementos del chunk (ej: N. definido en el BATCH_SIZE), entonces se realiza un ciclo donde se leeran N lineas, y se generara un unico mensaje con los 4 bytes de tamaño del chunk y posteriormente linea a linea como se hacia antes. Esto hace que en vez de enviarse 2N + 1 mensajes se envie uno solo mucho mas grande, y aun asi el server pueda trabajar la información.
El server lee esos primeros 4 bytes para saber cuantas apuestas le llegan, y luego en un ciclo lee las N lineas como se venia haciendo hasta el ejercicio anterior. Esto permite crear N bets por mensaje en el servidor.

Falta manejar los errores correctamente, cerrar FD, y ver si es necesario pasar el protocolo a binario.