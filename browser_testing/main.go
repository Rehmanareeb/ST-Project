package main

import (
	"log"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
)

func main() {
	// Launch a new browser instance (non-headless mode to see operations)
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

	// Test Weather for Default City (London)
	log.Println("Testing weather for default city: London")
	page = browser.MustPage("http://127.0.0.1:8000/weather")
	page.MustElement(`form[action="/weather"] input[type="submit"]`).MustClick()
	time.Sleep(2 * time.Second) // Wait for the page to reload

	weatherResult := page.MustElement("div").MustText()
	if !contains(weatherResult, "London") {
		log.Fatalf("Weather test failed for default city: %s", weatherResult)
	}
	log.Println("Weather test passed for default city: London")

	// Test Weather for Specific City (New York)
	log.Println("Testing weather for specific city: New York")
	page.MustElement(`input[name="city"]`).MustInput("New York")
	page.MustElement(`form[action="/weather"] input[type="submit"]`).MustClick()
	time.Sleep(2 * time.Second) // Wait for the page to reload

	weatherResultNY := page.MustElement("div").MustText()
	if !contains(weatherResultNY, "New York") {
		log.Fatalf("Weather test failed for New York: %s", weatherResultNY)
	}
	log.Println("Weather test passed for specific city: New York")

	// Test Weather for Invalid City
	log.Println("Testing weather for invalid city: InvalidCity")
	page.MustElement(`input[name="city"]`).MustInput("InvalidCity")
	page.MustElement(`form[action="/weather"] input[type="submit"]`).MustClick()
	time.Sleep(2 * time.Second) // Wait for the page to reload

	weatherResultInvalid := page.MustElement("div").MustText()
	if !contains(weatherResultInvalid, "Weather API Error") {
		log.Fatalf("Weather test failed for invalid city: %s", weatherResultInvalid)
	}
	log.Println("Weather test passed for invalid city: InvalidCity")
}

// Helper function to check if a string contains a substring
func contains(str, substr string) bool {
	return len(str) >= len(substr) && str[:len(substr)] == substr
}
