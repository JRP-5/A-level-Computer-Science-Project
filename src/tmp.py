from datetime import datetime
now = datetime.now()  # get the time
time = now.strftime("%H%M.%S%f")
print(time)