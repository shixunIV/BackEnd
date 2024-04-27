package main

import (
	"gateway/server"
	"log"
)

func main() {
	// Start the gateway server
	api := server.InitRouter()

	err := api.Run(":9000")
	if err != nil {
		log.Panicln(err)
	}
}
