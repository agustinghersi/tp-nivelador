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

// Envio un chunk de lineas al servidor
// Manda 4 bytes indicando tamaño de chunk
//Luego, por cada linea, manda 4 bytes de longitud de mensaje y el propio mensaje
func SendAll(socket io.Writer, chunk []string) error {
	elements := len(chunk)
	BytesToSend := []byte{}
	// Agrego el numero de elementos del chunk. Por protocolo son 4 bytes
	BytesToSend = append(BytesToSend, fmt.Sprintf("%04d", elements)...) 
	// El for prepara las N lineas del chunk a enviar
	for i := range elements {
		message := []byte(chunk[i])
		size := len(message)
		BytesToSendMessage := []byte(fmt.Sprintf("%04d", size)) // Tamaño de la linea en 4 bytes
		// Agrego los 2 campos de protocolo por linea leida
		BytesToSend = append(BytesToSend, BytesToSendMessage...)
		BytesToSend = append(BytesToSend, message...)
	}

	// Envio todo el chunk de una
	if err := safe_socket.SendAll(socket, BytesToSend); err != nil {
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