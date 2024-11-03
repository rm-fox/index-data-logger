from datetime import datetime
current_dateTime = datetime.now()
current_time_nanos = int(current_dateTime.timestamp() * 1_000_000_000)
print(current_time_nanos)