package middlewares

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func IPAuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		clientIP := c.ClientIP()
		if clientIP != "127.0.0.1:8888" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			c.Abort()
			return
		}
		c.Next()
	}
}
