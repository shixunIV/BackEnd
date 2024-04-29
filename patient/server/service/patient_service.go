package service

import (
	"errors"
	"log"
	"patient/config"
	"patient/models"
	"patient/utils"

	"github.com/gin-gonic/gin"
)

type Login struct {
	ID       string `form:"id"`
	Password string `form:"password"`
}

func (s *Login) Handle(c *gin.Context) (any, error) {
	patient, err := models.GetPatientByID(s.ID)
	if err != nil {
		return nil, errors.New("用户不存在")
	}
	if !utils.ComparePasswords(patient.Password, s.Password, config.CFG.Salt) {
		return nil, errors.New("密码错误")
	}
	//得到token
	token, err := utils.CreateToken(patient.ID)
	if err != nil {
		return nil, err
	}
	return []map[string]interface{}{
		{
			"token": token,
		},
	}, nil
}

type Register struct {
	ID       string `form:"id"`
	Name     string `form:"name"`
	Age      int    `form:"age"`
	Phone    string `form:"phone"`
	Password string `form:"password"`
	Gender   string `form:"gender"`
}

func (s *Register) Handle(c *gin.Context) (any, error) {
	password, err := utils.HashPassword(s.Password, config.CFG.Salt)
	if err != nil {
		return nil, err
	}
	if err := models.CreatePatient(s.ID, s.Name, s.Age, s.Gender, s.Phone, password); err != nil {
		return nil, err
	}
	return nil, nil
}

type ChangeAvatar struct {
	Avatar string `form:"avatar"`
}

func (s *ChangeAvatar) Handle(c *gin.Context) (any, error) {
	id, _ := c.Get("id")
	if err := models.UpdateAvatar(id.(string), s.Avatar); err != nil {
		return nil, err
	}
	return nil, nil
}

type GetPatient struct {
}

func (s *GetPatient) Handle(c *gin.Context) (any, error) {
	id, _ := c.Get("id")
	log.Print(id)
	patient, err := models.GetPatientByID(id.(string))
	if err != nil {
		return nil, err
	}
	return patient, nil
}

type UpdatePassword struct {
	Id          string `form:"id"`
	OldPassword string `form:"old_password"`
	NewPassword string `form:"new_password"`
}

func (s *UpdatePassword) Handle(c *gin.Context) (any, error) {
	err := models.ChangePassword(s.Id, s.NewPassword, s.OldPassword)
	return nil, err
}

type UpdatePatient struct {
	Name   string `form:"name"`
	Age    int    `form:"age"`
	Gender string `from:"gender"`
	Phone  string `form:"phone"`
}

func (s *UpdatePatient) Handle(c *gin.Context) (any, error) {
	id, _ := c.Get("id")
	return nil, models.UpdatePatient(id.(string), s.Name, s.Age, s.Gender, s.Phone)
}
