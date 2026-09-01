package protocol

import (
	"fmt"
	"io"
	"strconv"

	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/safe_socket"
)

// Se envia una sola vez la agencia del cliente con el que se comunica
func SendAgency(socket io.Writer, agency string) error {
	return safe_socket.SendAll(socket, []byte(agency))
}

// Envio el largo de la linea en 4 bytes para que el server sepa leerla dinamicamente
// Sigue el flujo con lo ya hecho en SendAll
func SendAll(socket io.Writer, bytes []byte) error {
	size := len(bytes)
	BytesToSend := []byte(fmt.Sprintf("%04d", size)) // Tamaño de la linea en 4 bytes

	// Envio el tamaño de la linea
	if err := safe_socket.SendAll(socket, BytesToSend); err != nil {
		return err
	}

	//Ahora puedo enviar la linea
	if err := safe_socket.SendAll(socket, bytes); err != nil {
		return err
	}

	return nil

}

func RecvWinners(socket io.Reader) ([]byte, error) {
	message := []byte{}
	// Repito hasta que no llegue ningun ganador mas
	for {
		// primero recupero la longitud del mensaje
		lineSize, err := safe_socket.RecvAll(socket, 4)
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		// Ahora recibo el ganador sabiendo longitud. El short read se hace en socket
		size, err := strconv.Atoi(string(lineSize))
		if err != nil {
			return nil, err
		}
		line, err := safe_socket.RecvAll(socket, size)
		if err != nil {
			return nil, err
		}
		message = append(message, line...)
		message = append(message, '\n')
	}

	return message, nil
}