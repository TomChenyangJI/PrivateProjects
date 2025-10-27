from datetime import datetime


ts = 1752653517

print(datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M"))