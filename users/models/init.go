package models

import (
	"log"

	"github.com/glebarez/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

func sqliteDB(dsn string, config *gorm.Config) (*gorm.DB, error) {
	db, err := gorm.Open(sqlite.Open(dsn+"?_pragma=foreign_keys(1)"), config)
	if err != nil {
		return nil, err
	}
	sqlDB, err := db.DB()
	sqlDB.SetMaxOpenConns(1)
	if err != nil {
		return nil, err
	}
	return db, nil
}

func migrate() {
	DB.AutoMigrate(&User{})
}

func InitDB() {
	var db *gorm.DB
	var err error
	db, err = sqliteDB("user.db", &gorm.Config{})

	if err != nil {
		log.Panicf("无法连接数据库，%s", err)
	}

	DB = db
	migrate()
	createData()
}

func createData() {
	CreateUser("xyh", "xyh", 20, "男", "12345678901", "xyh")
	CreateUser("hx", "hx", 20, "男", "1234501", "hx")
}
