Redactar un breve informe en donde se detallen los aspectos más importantes de la solución provista, como ser el protocolo de comunicación implementado y los mecanismos para sincronizar la ejecución concurrente.

El protocolo inicialmente conciste en el envio de 4 bytes fijos de cliente a servidor, indicando el tamaño de mensaje enviado para que el socket tenga la cantidad de bytes que se van a recibir.
Con esto se evita el hardcodeo inicial, y puede validarse que se reciba todo el mensaje.
Hasta este momento, no es necesario todavia la implementación de esto desde el servidor al cliente.
Mas alla de short write/read, es todo lo que se agrega al protocolo por el momento.

Hice que pueda usarse recv_size. Esto no deberia pasar mas adelante y utilizarse internamente.
Tambien falta manejar los errores