import sqlite3

DB_NAME = "weather_data.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature TEXT NOT NULL,
            condition TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Save weather data
def save_weather(city, temperature, condition):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather (city, temperature, condition) VALUES (?, ?, ?)",
                   (city, temperature, condition))
    conn.commit()
    conn.close()

# Get all weather data
def get_all_weather():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Get weather data by ID
def get_weather_by_id(weather_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather WHERE id = ?", (weather_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# Update weather data
def update_weather(weather_id, city, temperature, condition):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE weather SET city = ?, temperature = ?, condition = ? WHERE id = ?",
                   (city, temperature, condition, weather_id))
    conn.commit()
    conn.close()

# Delete weather data
def delete_weather(weather_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather WHERE id = ?", (weather_id,))
    conn.commit()
    conn.close()
