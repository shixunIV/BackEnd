package config

import (
	"log"
	"math/rand"
	"os"

	"gopkg.in/yaml.v2"
)

var CFG Config

const CONFIG_FILE_PATH = "../config.yml"

type Config struct {
	JWTSigningString string `yaml:"jwt_signing_string"`
	Salt             string `yaml:"salt"`
}

func Init() Config {
	if _, err := os.Stat(CONFIG_FILE_PATH); os.IsNotExist(err) {
		// 文件不存在，创建默认配置
		CFG = Config{
			JWTSigningString: generateRandomString(20),
			Salt:             generateRandomString(20),
		}
		// 将默认配置写入文件
		data, err := yaml.Marshal(&CFG)
		if err != nil {
			log.Fatalf("error: %v", err)
		}
		err = os.WriteFile(CONFIG_FILE_PATH, data, 0644)
		if err != nil {
			log.Fatalf("error: %v", err)
		}
		return CFG
	} else {
		// 文件存在，读取配置
		file, err := os.ReadFile(CONFIG_FILE_PATH)
		if err != nil {
			log.Fatalf("error: %v", err)
		}

		err = yaml.Unmarshal(file, &CFG)
		if err != nil {
			log.Fatalf("error: %v", err)
		}
		return CFG
	}
}

func generateRandomString(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyz" +
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[rand.Intn(len(charset))]
	}
	return string(b)
}
