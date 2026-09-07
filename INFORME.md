Redactar un breve informe en donde se detallen los aspectos más importantes de la solución provista, como ser el protocolo de comunicación implementado y los mecanismos para sincronizar la ejecución concurrente.

Lo primero a destacar es la interacción dentro del sistema. El cliente se comunica con el servidor, pero agregue capas para desacoplar. Tanto cliente como servidor no se comunican con los sockets, arme un protocolo que funciona como capa intermedia entre ambos para permitir mayor abstracción. La idea es que cliente/server hable con el protocolo y este, de alguna forma, le devuelva un mensaje con los datos en un formato deseado.
Ademas, en el servidor arme una clase monitor. La idea es que el monitor sea unico, y todos los threads que se generan por cada cliente lo utilicen.

El protocolo implementado esta basado en lo aprendido en la materia Taller de Programación y el protocolo TLV. La idea es enviar la longitud del mensaje (apuesta) en un tamaño fijo conocido por el protocolo (4 bytes). Se lee en el receptor el lenght, y luego puede leerse el Value de forma dinamica, pues distintos mensajes tienen distinta longitud.
El short write/read se soluciona con esta información. Los primeros 4 bytes indiccan cuantos leer, pudiendose  realizar varios write/read en caso de no haberse obtenido todos al primer intento. Esta es responsabilidad del safe_socket, de forma que el protocolo solo le dicce cuanto leer y sabe que el mensaje obtenido tendra esa longitud.
Con esto, el ejercicio 5 esta completado (enviar de a una apuesta). En la parte de batch se reutiliza lo hecho y se agrega un campo nuevo al comienzo del mensaje. La idea es, de nuevo, un campo fijo (4 bytes) que indica la cantidad de mensajes (apuestas) a enviar. Esto permite leer el valor N en 4 bytes, generar un ciclo de N iteraciones, y recuperar los N mensajes como se venia haciendo 1 por 1.
Es el propio protocolo el que arma un listado de mensajes con el formato esperado para que el cliente simplemente los agregue en el OUTPUT_FILE.
Por ultimo, al cominezar la comunicación entre cliente y servidor, debe enviarse un unico byte indicando la agencia, de forma que el servidor sepa que ganadores enviarle luego.

En cuanto a la concurrencia, se genera un thread por cada cliente que se conecta, y cada uno utiliza un unico monitor que gestiona el uso de lottery (recurso compartido).
De esta forma, el servidor recibe clientes que comparten el uso del monitor, y la comunicación de cada thread se realiza utilizando el monitor y el protocolo. Internamente, el monitor se comunica con lottery y el protocolo con el socket, pudiendo asi desacoplar el sistema.
Ademas, al comunicarse con todos los clientes, el monitor se encarga de verificar que se cumpla con el quorum minimo de agencias antes de empezar a enviar ganadores (notifica a las priemras con notifyAll).

Por ultimo, para gestionar el SIGTERM es distinta la implementación del cliente que en el servidor. En el servidor se cierra el socket y se llama a shutdown del monitor. Como el monitor es 1 y lo utilizan todos los threads, el shutdown cambia un flag que permite hacer un notifyAll a cada thread, haciendo que terminen, salgan del while del run del server y, por ultimo, los threads hagan join.
En el caso del cliente, hay un canal esperando la llegada de la SIGTERM. Esta go routine cierra el socket y permite detectar, ante un error, si se ocasiono por una SIGTERM. En este caso, el run de client termina sin error.

Algunas posibles mejoras no implementadas serian un mejor manejo de errores y el cierre de sockets en estos casos. Ademas, el envio de ACKs ayudaria a gestionar posibles fallas, y no depender exclusivamente del short write/read arreglado.
