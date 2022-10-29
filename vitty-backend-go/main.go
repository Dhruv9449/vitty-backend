package main

import (
	"net/http"
	"regexp"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/ping", ping)
	router.POST("/uploadtext/", getTimetable)
	router.Run("localhost:8080") // listen and serve on
}

type TimetableResponse struct {
	ParsedData string `json:"Parsed_Data"`
	Slot       string `json:"Slot"`
	CourseName string `json:"Course_Name"`
	CourseType string `json:"Course_type"`
	Venue      string `json:"Venue"`
}

func ping(c *gin.Context) {
	c.String(200, "pong")
}

func getTimetable(c *gin.Context) {
	data := c.Request.FormValue("request")

	re := regexp.MustCompile(`[A-Z]{1,3}[0-9]{1,2}[\D]{1}[A-Z]{3,4}[0-9]{3,4}[A-Z]{0,1}[\D]{1}[A-Z]{2,3}[\D]{1}[A-Z]{2,6}[0-9]{2,4}[A-Za-z]{0,1}[\D]{1}[A-Z]{2,4}[0-9]{0,3}`)
	slots := re.FindAllString(data, -1)
	var timetable []TimetableResponse
	for _, slot := range slots {
		var obj TimetableResponse

		obj.ParsedData = slot
		obj.Slot = regexp.MustCompile(`[A-Z]{1,3}[0-9]{1,2}\b`).FindAllString(slot, -1)[0]
		obj.CourseName = regexp.MustCompile(`[A-Z]{1,3}[0-9]{1,2}\b`).FindAllString(slot, -1)[0]
		course_type := regexp.MustCompile(`[A-Z]{1,3}[0-9]{1,2}\b`).FindAllString(slot, -1)[0]

		var c_type string
		if course_type == "ELA" || course_type == "LO" {
			c_type = "Lab"
		} else {
			c_type = "Theory"
		}
		obj.CourseType = c_type
		obj.Venue = regexp.MustCompile(`[A-Z]{2,6}[0-9]{2,4}[A-Za-z]{0,1}\b`).FindAllString(slot, -1)[1]
		timetable = append(timetable, obj)
	}

	c.IndentedJSON(http.StatusOK, timetable)
}
