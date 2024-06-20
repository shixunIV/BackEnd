package models

import (
	"encoding/base64"
	"errors"
	"io"
	"log"
	"os"
	"users/utils"
)

type User struct {
	ID       string `json:"id" gorm:"primaryKey"`
	Name     string `json:"name" gorm:"unique"`
	Age      int    `json:"age"`
	Gender   string `json:"gender"`
	Phone    string `json:"phone" gorm:"unique"`
	Password string `json:"-"`
	Avatar   string `json:"avatar"`
}

func CreateUser(id string, name string, age int, gender string, phone string, password string) error {
	if gender != "男" && gender != "女" {
		return errors.New("性别只能为男或女")
	}
	if _, err := GetUserByID(id); err == nil {
		return errors.New("ID已存在")
	}
	if _, err := GetUserByPhone(phone); err == nil {
		return errors.New("手机号已存在")
	}
	password, err := utils.HashPassword(password)
	if err != nil {
		return err
	}
	user := User{
		ID:       id,
		Name:     name,
		Age:      age,
		Gender:   gender,
		Phone:    phone,
		Password: password,
		Avatar:   getDefaultAvatar(),
	}
	return DB.Create(&user).Error
}

func GetUserByID(id string) (*User, error) {
	var user User
	err := DB.Where("id = ?", id).First(&user).Error
	return &user, err
}

func GetUserByPhone(phone string) (*User, error) {
	var user User
	err := DB.Where("phone = ?", phone).First(&user).Error
	return &user, err
}

func UpdateUser(id string, name string, age int, gender string, phone string) error {
	var user User
	if DB.Where("id = ?", id).First(&user).Error != nil {
		return errors.New("患者不存在")
	}
	user.Name = name
	user.Age = age
	user.Gender = gender
	user.Phone = phone
	return DB.Save(&user).Error
}

func UpdateAvatar(id string, avatar string) error {
	var user User
	if DB.Where("id = ?", id).First(&user).Error != nil {
		return errors.New("患者不存在")
	}
	user.Avatar = avatar
	return DB.Save(&user).Error
}

func GetAvatar(id string) (string, error) {
	var user User
	if DB.Where("id = ?", id).First(&user).Error != nil {
		return "", errors.New("患者不存在")
	}
	return user.Avatar, nil
}

func getDefaultAvatar() string {
	// 打开图片文件
	file, err := os.Open("./assets/avatar.png")
	if err != nil {
		log.Fatalf("打开图片失败: %v", err)
	}
	defer file.Close()
	imgData := make([]byte, 0)
	buf := make([]byte, 1024)
	for {
		n, err := file.Read(buf)
		if err != nil && err != io.EOF {
			log.Fatalf("读取图片失败: %v", err)
		}
		if n == 0 {
			break
		}
		imgData = append(imgData, buf[:n]...)
	}
	imgBase64Str := base64.StdEncoding.EncodeToString(imgData)
	return imgBase64Str
}

func ChangePassword(id string, newPassword string, oldPassword string) error {
	var user User
	if DB.Where("id = ?", id).First(&user).Error != nil {
		return errors.New("用户不存在")
	}
	if !utils.ComparePasswords(user.Password, oldPassword) {
		return errors.New("密码错误")
	}
	password, err := utils.HashPassword(newPassword)
	if err != nil {
		return err
	}
	user.Password = password
	return DB.Save(&user).Error
}
