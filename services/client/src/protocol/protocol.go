package protocol

import (
	"fmt"
	"io"

	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/safe_socket"
)

// Aca defino la primer comunicación del protocolo.
// Envio el largo de la linea en 4 bytes para que el server sepa leerla dinamicamente
// Sigue el flujo con lo ya hecho en SendAll
func SendSize(socket io.Writer, size int) error {
	BytesToSend := []byte(fmt.Sprintf("%04d", size)) // Tamaño de la linea en 4 bytes

	// Envio el tamaño de la linea
	return safe_socket.SendAll(socket, BytesToSend)
}