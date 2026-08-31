package safe_socket

import "io"
import "fmt"

//TODO: Complete with a short-read/short-write tolerant implementation

// Aca defino la primer comunicación del protocolo.
// Envio el largo de la linea en 4 bytes para que el server sepa leerla dinamicamente
// Sigue el flujo con lo ya hecho en SendAll
func SendSize(socket io.Writer, size int) error {
	BytesToSend := []byte(fmt.Sprintf("%04d", size)) // Tamaño de la linea en 4 bytes

	// Envio el tamaño de la linea
	return SendAll(socket, BytesToSend)
}

func SendAll(socket io.Writer, bytes []byte) error {
	cantBytes := len(bytes) //Cantidad de bytes a escribir
	cantBytesWrited := 0 // contador de bytes escritos
	
	for cantBytesWrited < cantBytes {
		//Mando los bytes que faltan por escribir de esta linea
		bytesWrited, err := socket.Write(bytes[cantBytesWrited:])
		if err != nil {
			return err
		}
		cantBytesWrited += bytesWrited // Actualizo lo ya escrito
	}

	return nil
}

func RecvAll(socket io.Reader, size int) ([]byte, error) {
	buff := make([]byte, size)
	cantBytes := size // Cantidad de bytes a leer
	cantBytesReaded := 0 // Contador de bytes leidos

	for cantBytesReaded < cantBytes {
		n, err := socket.Read(buff[cantBytesReaded:])
		if err != nil {
			return nil, err // Ver este caso despues
		}

		cantBytesReaded += n // Actualizo lo ya leido
	}
	return buff[:cantBytesReaded], nil
}
