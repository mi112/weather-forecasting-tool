# Use case: Python command line tool that accepts city name as input and returns the current weather for that city
# Usage: python weather.py <city_name>
# Example: python weather.py "New York"
# Output: Current weather in New York, US is 10.0 degrees Celsius with clear sky

# Importing the libraries required for API call, JSON parsing, reading environment variables (for API key) and command line arguments
import requests, json, os, sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Class that accepts city name as input and returns the current weather for that city
class Weather:
    
    #constructor that accepts city name as input, defines the API key and the API URL
    def __init__(self, city_name):
        
        self.city_name = city_name
        
        #check if API key is defined as environment variable
        if os.environ.get("OPENWEATHERMAP_API_KEY") is None:
            print("Please set the OPENWEATHERMAP_API_KEY environment variable")
            sys.exit(1)
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.api_url = "http://api.openweathermap.org/data/2.5/weather?q=" + self.city_name + "&appid=" + self.api_key + "&units=metric"
    
    #function that calls the API and returns the current weather 
    def get_weather(self):
       
        #call the API and display the weather data
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            weather_data = json.loads(response.text)

            #print the weather data for entered city
            print("Current weather in " + self.city_name + ", " + weather_data['sys']['country'] + " is " + str(weather_data['main']['temp']) + " degrees Celsius with " + weather_data['weather'][0]['description'])

        #handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("Error connecting to API")
            print("Please make sure the city name and provided secret OPENWEATHERMAP_API_KEY is correct and try again.")
            sys.exit(1)
        
        #handle connection errors
        except requests.exceptions.ConnectionError as e:
            print("Error connecting to API")
            sys.exit(1)
        
        #handle json parsing errors
        except json.decoder.JSONDecodeError as e:
            print("Error parsing JSON response")
            sys.exit(1)
        
        #handle other exceptions
        except Exception as e:
            print("Error")
            print(e)
            sys.exit(1)



#main function that accepts city name as command line argument and calls the Weather class
if __name__ == "__main__":
    
    #check if city name is passed as command line argument
    if len(sys.argv) >= 2:
        city_name = ' '.join(sys.argv[1:])

        #call the Weather class
        weather = Weather(city_name)
        weather.get_weather()
    else:
        print("Please enter a city name")
        print("Usage Example: python weather.py <city>")
        sys.exit(1)
