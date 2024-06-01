package server

import (
	"fmt"
	"net/http"
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

		// 处理响应头，防止重复的CORS头被添加
		proxy.ModifyResponse = func(response *http.Response) error {
			response.Header.Del("Access-Control-Allow-Origin")
			return nil
		}

		proxy.ServeHTTP(c.Writer, c.Request)
	}
}


var routerMapper = map[string]string{
	"user":  "http://127.0.0.1:9001",
	"neo4j": "http://127.0.0.1:9002",
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

	api := r.Group("/api")
	api.Use(gin.Recovery())
	api.Use(gin.Logger())

	neo4j := api.Group("/neo4j")
	{
		neo4j.Any("/accident/*any", createReverseProxy(routerMapper["neo4j"]))
		neo4j.Any("/accident", createReverseProxy(routerMapper["neo4j"]))
		neo4j.Any("/danger/*any", createReverseProxy(routerMapper["neo4j"]))
		neo4j.Any("/danger", createReverseProxy(routerMapper["neo4j"]))
		neo4j.Any("", createReverseProxy(routerMapper["neo4j"]))
	}

	user := api.Group("/user")
	{
		user.Any("/*any", createReverseProxy(routerMapper["user"]))
		user.Any("", createReverseProxy(routerMapper["user"]))
	}

	return r
}
