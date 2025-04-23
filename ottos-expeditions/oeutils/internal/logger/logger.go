package logger

import (
	"log"
)

var Logger = log.New(log.Writer(), "[oeutils] ", log.LstdFlags|log.Lshortfile)
