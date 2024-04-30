package server

import (
	"users/server/middlewares"
	"users/server/service"

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
		user := api.Group("user")
		{
			// POST api/user/login | 登录
			user.POST("login", service.HandlerBind(&service.Login{}))
			// POST api/user/register | 注册
			user.POST("register", service.HandlerBind(&service.Register{}))
			// PUT api/user/changePassword | 修改个人信息
			user.PUT("changePassword", service.HandlerBind(&service.UpdatePassword{}))

			// POST api/user/changeAvatar | 修改头像
			auth := user.Group("")
			auth.Use(middlewares.TokenAuthorization())
			{
				// PUT api/user/changeAvatar | 修改头像
				auth.PUT("changeAvatar", service.HandlerBind(&service.ChangeAvatar{}))
				// GET api/user 	| 获取个人信息
				auth.GET("", service.HandlerNoBind(&service.GetUser{}))
				// PUT api/user/update | 修改个人信息
				auth.PUT("update", service.HandlerBind(&service.UpdateUser{}))
			}
		}
	}
	return r
}
