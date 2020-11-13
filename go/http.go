package http

import (
	"fmt"
	"net"
	"net/http"
	"github.com/sirupsen/logrus"
)

type LoggerServer struct {
	handler http.Handler
}

func NewLoggerServer(handler http.Handler) *LoggerServer {
	return &LoggerServer{handler: handler}
}

func (loggerServer *LoggerServer) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	logrus.Infof("%s %s", request.Method, request.RequestURI)
	loggerServer.handler.ServeHTTP(writer, request)
}

func GetFreePort() (int, error) {
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		return 0, err
	}

	l, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return 0, err
	}
	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port, nil
}


func StartSimpleServer() {
	var wait chan error

	port, _ := GetFreePort()
	addr := fmt.Sprintf("localhost:%d", port)

	go func() {
		wait <- http.ListenAndServe(addr, NewLoggerServer(http.FileServer(http.Dir("."))))
	}()

	logrus.Infof("server started at %s", addr)

	<-wait
}
