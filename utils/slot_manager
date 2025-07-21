
import sqlite3
from datetime import datetime, timedelta

# Define service durations (in minutes)
SERVICE_DURATIONS = {
    "exterior": 90,
    "full": 150,
    "standard": 90,
    "premium": 150
}

# Define working hours
WEEKDAY_START = 15  # 3:00 PM
WEEKDAY_END = 21    # 9:00 PM
WEEKEND_START = 9
WEEKEND_END = 21

# Split Sheen by postcode prefixes (example logic)
EAST_SHEEN = ['sw148']
WEST_SHEEN = ['sw147']

def get_side_from_postcode(postcode):
    postcode = postcode.replace(" ", "").lower()
    if any(postcode.startswith(prefix) for prefix in EAST_SHEEN):
        return "east"
    elif any(postcode.startswith(prefix) for prefix in WEST_SHEEN):
        return "west"
    return "unknown"

def get_existing_bookings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT date, time FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return set((d, t) for d, t in bookings)

def get_available_slots(postcode, service):
    region = get_side_from_postcode(postcode)
    duration = SERVICE_DURATIONS.get(service, 90)
    today = datetime.now().date()
    all_slots = []
    taken = get_existing_bookings()

    for day_offset in range(0, 30):
        date = today + timedelta(days=day_offset)
        weekday = date.weekday()

        # Region-based filtering
        if region == "east" and weekday in [1, 3, 5]:  # Tue, Thu, Sat
            continue
        if region == "west" and weekday in [0, 2, 4]:  # Mon, Wed, Fri
            continue

        start_hour = WEEKEND_START if weekday >= 5 else WEEKDAY_START
        end_hour = WEEKEND_END if weekday >= 5 else WEEKDAY_END
        current_time = datetime.combine(date, datetime.min.time()).replace(hour=start_hour)

        while current_time.hour + duration // 60 <= end_hour:
            time_str = current_time.strftime("%H:%M")
            date_str = date.isoformat()
            if (date_str, time_str) not in taken:
                all_slots.append({
                    "date": date_str,
                    "time": time_str
                })
            current_time += timedelta(minutes=30)

    return all_slots

def save_booking(data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, phone, postcode, service, date, time) VALUES (?, ?, ?, ?, ?, ?)",
              (data['name'], data['phone'], data['postcode'], data['service'], data['date'], data['time']))
    conn.commit()
    conn.close()
