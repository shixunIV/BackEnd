package main

import (
	"log"
	"patient/config"
	"patient/models"
	"patient/server"
)

func Init() {
	//读取配置
	config.Init()
	models.InitDB()
}

func main() {
	Init()
	api := server.InitRouter()

	err := api.Run(":9000")
	if err != nil {
		log.Panicln(err)
	}
}
