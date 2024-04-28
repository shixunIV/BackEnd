package utils_test

import (
	"log"
	"patient/utils"
	"testing"
)

func TestHashPassword(t *testing.T) {
	password := "xyh666"

	hashedPassword, err := utils.HashPassword(password, "6666")
	if err != nil {
		t.Errorf("Error hashing password: %v", err)
	}
	log.Print(hashedPassword)
}

func TestComparePasswords(t *testing.T) {
	password := "xyh666"
	salt := "6666"

	hashedPassword, err := utils.HashPassword(password, salt)
	if err != nil {
		t.Errorf("Error hashing password: %v", err)
	}

	if !utils.ComparePasswords(hashedPassword, password, salt) {
		t.Errorf("Passwords do not match")
	}
}
