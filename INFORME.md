Redactar un breve informe en donde se detallen los aspectos más importantes de la solución provista, como ser el protocolo de comunicación implementado y los mecanismos para sincronizar la ejecución concurrente.

El protocolo inicialmente conciste en el envio en un byte del id de agencia para la persistencia de donde proceden las apuestas. Posteriormente, se envian 4 bytes fijos de cliente a servidor, indicando el tamaño de mensaje enviado para que el socket tenga la cantidad de bytes que se van a recibir. Este mensaje es la linea con tada la información de la apuesta, enviandose una a una.
Con esto se evita el hardcodeo inicial, y puede validarse que se reciba todo el mensaje. Ademas, es el protocolo el encargado de generar el formato requerido de los Bet para ser usados en lottery.

Falta manejar los errores, cerrar FD, enviar de server a cleinte solo los ganadores de esa agencia y evitar el eco, y ver si es necesario pasar el protocolo a binario.