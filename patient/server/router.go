package server

import (
	"patient/server/middlewares"
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
	api.Use(middlewares.IPAuthMiddleware())
	{
		patient := api.Group("patient")
		{
			// POST api/patient/login | 登录
			patient.POST("login", service.HandlerBind(&service.Login{}))
			// POST api/patient/register | 注册
			patient.POST("register", service.HandlerBind(&service.Register{}))
			// PUT api/patient/changePassword | 修改个人信息
			patient.PUT("changePassword", service.HandlerBind(&service.UpdatePassword{}))

			// POST api/patient/changeAvatar | 修改头像
			auth := patient.Group("")
			auth.Use(middlewares.TokenAuthorization())
			{
				// PUT api/patient/changeAvatar | 修改头像
				auth.PUT("changeAvatar", service.HandlerBind(&service.ChangeAvatar{}))
				// GET api/patient 	| 获取个人信息
				auth.GET("", service.HandlerNoBind(&service.GetPatient{}))
				// PUT api/patient/update | 修改个人信息
				auth.PUT("update", service.HandlerBind(&service.UpdatePatient{}))
			}
		}
	}
	return r
}
