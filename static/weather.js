document.getElementById("search-btn").addEventListener("click", getWeather);

function getWeather() {
    let city = document.getElementById("city").value;

    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=9d5b0a6867d26523a901f646d0baabf2`)
        .then(response => response.json())
        .then(data => {
            if (!data.weather) {
                alert("Could not retrieve weather data.");
                return;
            }

            let condition = data.weather[0].main;
            let description = data.weather[0].description;
            let temp = Math.round(data.main.temp - 273.15);
            let wind = data.wind.speed;
            let humidity = data.main.humidity;
            let pressure = data.main.pressure;

            document.getElementById("temp").textContent = `${temp}°`;
            document.getElementById("condition").textContent = `${condition} | FEELS LIKE ${temp}°`;
            document.getElementById("wind").textContent = wind;
            document.getElementById("humidity").textContent = humidity;
            document.getElementById("description").textContent = description;
            document.getElementById("pressure").textContent = pressure;

            // Fetch forecast data
            fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=9d5b0a6867d26523a901f646d0baabf2`)
                .then(response => response.json())
                .then(forecastData => {
                    let forecast = forecastData.list.slice(0, 5);
                    for (let i = 0; i < 5; i++) {
                        let day = forecast[i];
                        let date = new Date(day.dt * 1000).toLocaleDateString();
                        let tempForecast = Math.round(day.main.temp - 273.15);
                        let conditionForecast = day.weather[0].description;

                        document.getElementById(`forecast-date${i + 1}`).textContent = `Day ${i + 1}: ${date}`;
                        document.getElementById(`forecast-temp${i + 1}`).textContent = `${tempForecast}°`;
                        document.getElementById(`forecast-cond${i + 1}`).textContent = conditionForecast;
                    }
                });
        })
        .catch(err => {
            alert("Error retrieving data: " + err);
        });
}

// Function to update clock
setInterval(() => {
    let currentTime = new Date().toLocaleTimeString();
    document.getElementById("clock").textContent = currentTime;
}, 1000);
