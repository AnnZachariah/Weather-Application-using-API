from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, save_weather, get_all_weather, get_weather_by_id, update_weather, delete_weather
import requests
from datetime import datetime, timedelta
import csv
from flask import Response
from io import StringIO

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize the database
init_db()

# API keys
YOUTUBE_API_KEY = "AIzaSyAIHYBJUk0jD0b3rGxE4HPSVaT-BQjDW28"

# Route: Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # Fetch current weather data from OpenWeatherMap API
            api_key = "9d5b0a6867d26523a901f646d0baabf2"
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            current_response = requests.get(current_url).json()

            if current_response.get("cod") == 200:
                # Calculate local time based on timezone offset
                timezone_offset = current_response["timezone"]  # Offset in seconds
                utc_time = datetime.utcnow()
                local_time = utc_time + timedelta(seconds=timezone_offset)
                local_time_str = local_time.strftime("%A, %Y-%m-%d %H:%M:%S")

                weather_data = {
                    "city": city,
                    "temperature": current_response["main"]["temp"],
                    "condition": current_response["weather"][0]["description"],
                    "local_time": local_time_str,
                    "lat": current_response["coord"]["lat"],  # Latitude
                    "lon": current_response["coord"]["lon"],  # Longitude
                }

                # Fetch 5-day forecast data from OpenWeatherMap API
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
                forecast_response = requests.get(forecast_url).json()

                if forecast_response.get("cod") == "200":
                    forecast_data = []
                    daily_forecast = {}

                    # Group the forecast data by date (day)
                    for entry in forecast_response["list"]:
                        forecast_date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
                        date_str = forecast_date.strftime("%Y-%m-%d")  # Format date (e.g., 2025-01-21)

                        if date_str not in daily_forecast:
                            daily_forecast[date_str] = {
                                "date": forecast_date.strftime("%A, %Y-%m-%d"),  # Day of the week and date
                                "temperature": entry["main"]["temp"],
                                "condition": entry["weather"][0]["description"],
                            }

                    # Collect the first 5 days of forecast data
                    for idx, (date, data) in enumerate(daily_forecast.items()):
                        if idx < 5:
                            forecast_data.append(data)

                # Fetch YouTube videos related to the city
                youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={city}&key={YOUTUBE_API_KEY}"
                youtube_response = requests.get(youtube_url).json()
                youtube_videos = []
                for item in youtube_response.get("items", []):
                    youtube_videos.append({
                        "title": item["snippet"]["title"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "description": item["snippet"]["description"]
                    })

                return render_template(
                    "index.html",
                    weather=weather_data,
                    forecast=forecast_data,
                    youtube_videos=youtube_videos,
                )
            else:
                flash("City not found!", "error")
    return render_template("index.html")

@app.route("/export_csv")
def export_csv():
    weather_data = get_all_weather()

    # Create a CSV string
    output = StringIO()
    csv_writer = csv.writer(output)
    
    # Write the header
    csv_writer.writerow(["ID", "City", "Temperature", "Condition", "Timestamp"])

    # Write the data
    for row in weather_data:
        csv_writer.writerow(row)

    # Get the CSV data from the StringIO buffer
    output.seek(0)
    csv_data = output.getvalue()

    # Send the CSV file as a response
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=saved_weather_data.csv"}
    )

# Route: View Saved Weather Data
@app.route("/view")
def view_data():
    weather_data = get_all_weather()
    return render_template("view.html", weather_data=weather_data)

# Route: Edit Weather Data
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "POST":
        city = request.form.get("city")
        temperature = request.form.get("temperature")
        condition = request.form.get("condition")
        update_weather(id, city, temperature, condition)
        flash("Weather data updated successfully!", "success")
        return redirect(url_for("view_data"))
    weather = get_weather_by_id(id)
    return render_template("edit.html", weather=weather)

# Route: Delete Weather Data
@app.route("/delete/<int:id>")
def delete_data(id):
    delete_weather(id)
    flash("Weather data deleted successfully!", "success")
    return redirect(url_for("view_data"))

# Route: Save Weather Data
@app.route("/save", methods=["POST"])
def save_data():
    city = request.form.get("city")
    temperature = request.form.get("temperature")
    condition = request.form.get("condition")
    save_weather(city, temperature, condition)
    flash("Weather data saved successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
