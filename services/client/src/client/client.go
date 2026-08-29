package client

import (
	"net"
	"time"
	"os"
	"bufio"

	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/logger"
	"github.com/7574-sistemas-distribuidos/tp-nivelador/src/safe_socket"
)

const CONNECTION_ATTEMPTS_MAX = 3
const CONNECTION_ATTEMPS_DELAY_MS = 200

const ECHO_CLIENT_BUFFER_SIZE = 512
const ECHO_CLIENT_MESSAGE_AMOUNT = 3
const ECHO_CLIENT_MESSAGE_DELAY_MS = 1000

type ClientConfig struct {
	ServerHost string
	ServerPort string
	AgencyId   string
	InputFile  string
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

	defer file.Close() // El archivo lo cierro ya porque me queda la info en file

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		
		line := scanner.Text() // Lee de a 1 linea

		// Ver si despues se requiere trabajar la linea para que no quede texto
		//De momento solo me copio lo que estaba en el esquleto para mandar las lineas 1 a 1
		//readder := csv.NewReader(file)

		if err := safe_socket.SendAll(client.conn, []byte(line)); err != nil {
			logger.Error("send-message", logger.Fail)
			return err
		}

		responseBuffer, err := safe_socket.RecvAll(client.conn, ECHO_CLIENT_BUFFER_SIZE)
		if err != nil {
			logger.Error("recv-response", logger.Fail)
			return err
		}

		if string(responseBuffer) != line {
			logger.Error("check-response", logger.Fail)
			return err
		}

	}

	return nil
}



func (client *Client) Run() error {
	const mainAction = "test-echo-server"
	defer client.conn.Close()

	/* for messageId := range ECHO_CLIENT_MESSAGE_AMOUNT {
		messageArgs := []any{"agency-id", client.config.AgencyId, "message-id", messageId}
		logger.Info(mainAction, logger.InProgress, messageArgs...)

		clientMessage := client.config.AgencyId

		if err := safe_socket.SendAll(client.conn, []byte(clientMessage)); err != nil {
			logger.Error("send-message", logger.Fail, messageArgs...)
			return err
		}

		responseBuffer, err := safe_socket.RecvAll(client.conn, ECHO_CLIENT_BUFFER_SIZE)
		if err != nil {
			logger.Error("recv-response", logger.Fail, messageArgs...)
			return err
		}

		if string(responseBuffer) != clientMessage {
			logger.Error("check-response", logger.Fail, messageArgs...)
			return err
		}

		time.Sleep(ECHO_CLIENT_MESSAGE_DELAY_MS * time.Millisecond)
	} */
	if err := client.readInputFile(); err != nil {
		logger.Error("read-input-file", logger.Fail)
		return err
	}
	logger.Info(mainAction, logger.Success, "agency-id", client.config.AgencyId)

	return nil
}
