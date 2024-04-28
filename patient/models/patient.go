package models

import (
	"errors"
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
