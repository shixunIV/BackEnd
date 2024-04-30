package main

import (
	"log"
	"users/config"
	"users/models"
	"users/server"
)

func Init() {
	//读取配置
	config.Init()
	models.InitDB()
}

func main() {
	Init()
	api := server.InitRouter()

	err := api.Run(":9001")
	if err != nil {
		log.Panicln(err)
	}
}
