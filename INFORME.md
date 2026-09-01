Redactar un breve informe en donde se detallen los aspectos más importantes de la solución provista, como ser el protocolo de comunicación implementado y los mecanismos para sincronizar la ejecución concurrente.

Hasta ej 5:

El protocolo consiste en una primer comunicación del cliente al servidor informando el id de la agencia correspondiente, para que posteriormente el server pueda mandarle al cliente solo los ganadores correspondientes a esta agencia.
Posteriormente se entra en un loop en el cliente, donde se envia un mensaje por cada linea del archivo INPUT_FILE. Este mensaje consta de 2 partes: un "header" de 4 bytes que indica la longitud de la linea a leer a continuación, y luego el propio mensaje. El servidor sabe que debe leeer 4 bytes y en base a lo recibido leer N mas, pudiendo mediante ciclos garantizarse la llegada del mensaje completo y evitando asi short read/write.
El server recibe las apuestas de distintos clientes y la clase lottery se encarga de filtrar a los ganadores. Es el protocolo el que, en base a los resultados de lottery, parsea las apuestas ganadoras para su posterior envio a los clientes.
El envio de los ganadores sigue la misma idea: hay 4 bytes que indican el largo de la linea que representa una apuesta ganadora, seguido por las bbytes correspondientes a la apuesta. Esto permite al cliente poder determinar la longitud del mensaje correspondiente a una apuesta que debe persistir en OUTPUT_FILE

La idea es dessacoplar en capas. Tanto cliente como servidor se comunican con el protocolo, y el protocolo es quien habla con safe_socket haciendo las validaciones propias para garantizar la correcta comunicacion. El socket realiza el envio/recepción de bytes, garantizando que no hay short write/read medainte ciclos.

Falta manejar los errores, cerrar FD, y ver si es necesario pasar el protocolo a binario.