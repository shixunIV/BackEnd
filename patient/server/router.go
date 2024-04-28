package server

import (
	"patient/server/service"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func InitRouter() *gin.Engine {
	r := gin.New()

	//一些基础配置
	config := cors.DefaultConfig()
	config.ExposeHeaders = []string{"Authorization"}
	config.AllowCredentials = true
	config.AllowAllOrigins = true
	config.AllowHeaders = []string{"Origin", "Content-Length", "Content-Type", "Authorization"}
	r.Use(cors.New(config))
	api := r.Group("api")
	api.Use(gin.Recovery())
	api.Use(gin.Logger())
	{
		patient := api.Group("patient")
		{
			// POST api/patient/login | 登录
			patient.POST("login", service.HandlerBind(&service.Login{}))
			// POST api/patient/register | 注册
			patient.POST("register", service.HandlerBind(&service.Register{}))
		}
	}
	return r
}
