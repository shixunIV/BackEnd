package server

import (
	"net/http/httputil"
	"net/url"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func createReverseProxy(target string) gin.HandlerFunc {
	targetUrl, _ := url.Parse(target)
	proxy := httputil.NewSingleHostReverseProxy(targetUrl)
	return func(c *gin.Context) {
		proxy.ServeHTTP(c.Writer, c.Request)
	}
}

var routerMapper = map[string]string{
	"patient": "http://127.0.0.1:9001",
}

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
			patient.POST("/*", createReverseProxy(routerMapper["patient"]))
			patient.GET("/*", createReverseProxy(routerMapper["patient"]))
			patient.PUT("/*", createReverseProxy(routerMapper["patient"]))
			patient.DELETE("/*", createReverseProxy(routerMapper["patient"]))
		}
	}
	return r
}
