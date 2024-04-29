package server

import (
	"fmt"
	"net/http/httputil"
	"net/url"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func createReverseProxy(target string) gin.HandlerFunc {
	targetUrl, _ := url.Parse(target)
	proxy := httputil.NewSingleHostReverseProxy(targetUrl)
	return func(c *gin.Context) {
		fmt.Printf("Forwarding request: %s\n", c.Request.URL)
		proxy.ServeHTTP(c.Writer, c.Request)
	}
}

var routerMapper = map[string]string{
	"patient": "http://127.0.0.1:9001",
	"neo4j":   "http://127.0.0.1:9002",
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
		neo4j := api.Group("neo4j")
		{
			neo4j.Any("", createReverseProxy(routerMapper["neo4j"]))
		}
		patient := api.Group("patient")
		{
			patient.Any("", createReverseProxy(routerMapper["patient"]))
		}
	}
	return r
}
