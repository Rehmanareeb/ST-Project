package endpoints

import (
	"log"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
)

func TestForms() {
	browser := rod.New().ControlURL(launcher.New().Leakless(false).Headless(false).MustLaunch()).MustConnect()
	defer browser.MustClose()

	// Open the FastAPI application
	page := browser.MustPage("http://127.0.0.1:8000/twoforms")

	// Test Form 1: Add 2
	page.MustElement(`input[name="number"]`).MustInput("15")
	page.MustElement(`form[action="/form1"] input[type="submit"]`).MustClick()
	time.Sleep(2 * time.Second) // Wait for the page to reload

	// Verify the result for Form 1
	form1Result := page.MustElement("h2").MustText()
	if form1Result != "Your number is 15 and the result is 17." {
		log.Fatalf("Form 1 test failed: %s", form1Result)
	}
	log.Println("Form 1 test passed with input 15!")

	// Additional Test: Form 1 with input 0
	page.MustElement(`input[name="number"]`).MustInput("0")
	page.MustElement(`form[action="/form1"] input[type="submit"]`).MustClick()
	time.Sleep(2 * time.Second) // Wait for the page to reload

	form1ResultZero := page.MustElement("h2").MustText()
	if form1ResultZero != "Your number is 0 and the result is 2." {
		log.Fatalf("Form 1 test failed with input 0: %s", form1ResultZero)
	}
	log.Println("Form 1 test passed with input 0!")
}
