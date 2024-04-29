package models

import (
	"encoding/base64"
	"errors"
	"io"
	"log"
	"os"
	"patient/config"
	"patient/utils"
)

type Patient struct {
	ID       string `json:"id" gorm:"primaryKey"`
	Name     string `json:"name" gorm:"unique"`
	Age      int    `json:"age"`
	Gender   string `json:"gender"`
	Phone    string `json:"phone" gorm:"unique"`
	Password string `json:"-"`
	Avatar   string `json:"avatar" gorm:"default:'https://cdn.jsdelivr.net/gh/linyows/images/2021/09/01/202109011634.jpg'"`
}

func CreatePatient(id string, name string, age int, gender string, phone string, password string) error {
	if gender != "男" && gender != "女" {
		return errors.New("性别只能为男或女")
	}
	if _, err := GetPatientByID(id); err == nil {
		return errors.New("ID已存在")
	}
	if _, err := GetPatientByPhone(phone); err == nil {
		return errors.New("手机号已存在")
	}
	password, err := utils.HashPassword(
		password,
		config.CFG.Salt,
	)
	if err != nil {
		return err
	}
	patient := Patient{
		ID:       id,
		Name:     name,
		Age:      age,
		Gender:   gender,
		Phone:    phone,
		Password: password,
		Avatar:   getDefaultAvatar(),
	}
	return DB.Create(&patient).Error
}

func GetPatientByID(id string) (*Patient, error) {
	var patient Patient
	err := DB.Where("id = ?", id).First(&patient).Error
	return &patient, err
}

func GetPatientByPhone(phone string) (*Patient, error) {
	var patient Patient
	err := DB.Where("phone = ?", phone).First(&patient).Error
	return &patient, err
}

func UpdatePatient(id string, name string, age int, gender string, phone string, password string) error {
	var patient Patient
	if DB.First(&patient, id).Error != nil {
		return errors.New("患者不存在")
	}
	patient.Name = name
	patient.Age = age
	patient.Gender = gender
	patient.Phone = phone
	patient.Password = password
	return DB.Save(&patient).Error
}

func UpdateAvatar(id string, avatar string) error {
	var patient Patient
	if DB.First(&patient, id).Error != nil {
		return errors.New("患者不存在")
	}
	patient.Avatar = avatar
	return DB.Save(&patient).Error
}

func GetAvatar(id string) (string, error) {
	var patient Patient
	if DB.First(&patient, id).Error != nil {
		return "", errors.New("患者不存在")
	}
	return patient.Avatar, nil
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
