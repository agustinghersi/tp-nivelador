package client

import (
	"net"
	"time"
	"os"
	"bufio"
	"os/signal"
	"syscall"

	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/logger"
	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/protocol"
)

const CONNECTION_ATTEMPTS_MAX = 3
const CONNECTION_ATTEMPS_DELAY_MS = 200

type ClientConfig struct {
	ServerHost string
	ServerPort string
	AgencyId   string
	InputFile  string
	OutputFile string
	BatchSize  int
}

type Client struct {
	conn   net.Conn
	config ClientConfig
}

func NewClient(config ClientConfig) (*Client, error) {
	conn, err := connectToServer(config.ServerHost, config.ServerPort)
	if err != nil {
		logger.Warn("connect-to-server", logger.Fail)
		return nil, err
	}

	client := &Client{conn: conn, config: config}
	return client, nil
}

func connectToServer(host, port string) (net.Conn, error) {
	const action = "connect-to-server"
	var err error
	var conn net.Conn

	logger.Info(action, logger.InProgress)
	for i := range CONNECTION_ATTEMPTS_MAX {
		conn, err = net.Dial("tcp", host+":"+port)
		if err != nil {
			logger.Warn(action, logger.Fail, "attempt", i)
			time.Sleep(CONNECTION_ATTEMPS_DELAY_MS * time.Millisecond)
			continue
		}

		logger.Info(action, logger.Success)
		break
	}

	return conn, err
}

func (client *Client) readInputFile() error {
	// Abro el archivo definido como INPUT_FILE en docker-compose.yaml
	file, err := os.Open(client.config.InputFile)
	if err != nil {
		logger.Error("open-input-file", logger.Fail, "input-file", client.config.InputFile)
		return err
	}

	defer file.Close() // El archivo se cierra al final de a funcion

	// Aca empiezo con lectura y escritura
	scanner := bufio.NewScanner(file)

	// Mando una sola vez la agencia para que sepa con que cliente esta trabajando
	if err := protocol.SendAgency(client.conn, client.config.AgencyId); err != nil {
		logger.Error("send-agency", logger.Fail)
		return err
	}

	for {
		chunk := []string{}
		// El for lee la cantidad de lineas definidas en el chunk
		for i := 0; i < client.config.BatchSize; i++ {
			if !scanner.Scan() {
				break // Aca no hay mas lineas
			}
			line := scanner.Text() // Lee de a 1 linea
			chunk = append(chunk, line)
		}

		if len(chunk) == 0 {
			break // No hay nada que mandarle al server
		}

		if err := protocol.SendAll(client.conn, chunk); err != nil {
			logger.Error("send-message", logger.Fail)
			return err
		}

	}

	// Cierro la escritura del socket luego de mandar todos los mensajes
	if tcpConn, ok := client.conn.(*net.TCPConn); ok {
		tcpConn.CloseWrite()
	}

	return nil
}

func (client *Client) recvWinners() error {
	// Creo o trunco el output
	outPutFile, err := os.Create(client.config.OutputFile)
	if err != nil {
		logger.Error("open-output-file", logger.Fail, "output-file", client.config.OutputFile)
		return err
	}

	defer outPutFile.Close()

	// Recibo todos los ganadores
	winners, err := protocol.RecvWinners(client.conn)
	if err != nil {
		logger.Error("recv-response", logger.Fail)
		return err
	}

	//Aca escribo el output
	_, err = outPutFile.WriteString(string(winners))
	if err != nil {
		logger.Error("write-output-file", logger.Fail, "output-file", client.config.OutputFile)
		return err
	}

	return nil
}



func (client *Client) Run() error {
	const mainAction = "test-echo-server"
	defer client.conn.Close()

	// Por lo que investigue, necesito un canal que reciba la syscall ya l recibirla
	// se ejecuta la goroutine que cierra el socket
	sigchanel := make(chan os.Signal, 1)
	signal.Notify(sigchanel, syscall.SIGTERM)
	stopchannel := make(chan bool, 1) // Canal para detectar cuando devolver nil por el SIGTERM
	go func() {
		<-sigchanel
		client.conn.Close()
		stopchannel <- true
	}()

	if err := client.readInputFile(); err != nil {
		select {
		case <-stopchannel:
			return nil // Para que main devuelva 0 y no 1 por error
		default:
			logger.Error("read-input-file", logger.Fail)
			return err
		}
	}
	logger.Info(mainAction, logger.Success, "agency-id", client.config.AgencyId)
	
	// Luego de mandar todo recibo los ganadores
	if err := client.recvWinners(); err != nil {
		select {
		case <-stopchannel:
			return nil // Para que main devuelva 0 y no 1 por error
		default:
			logger.Error("recv-winners", logger.Fail)
			return err
		}
	}

	return nil
}
