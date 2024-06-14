from datetime import datetime
ts = int('1284101485')


# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
print(datetime.fromtimestamp(int("1294113662")).strftime('%Y-%m-%d %H:%M:%S'))