from datetime import datetime

def unix_to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp)


if __name__ == '__main__':
  test = unix_to_datetime(1762614940.61236)
  print(type(unix_to_datetime(1762614940.61236)))
  s2 = test.strftime("%d/%m/%Y %H:%M:%S")
  print(s2.split(" "))
  print(type(s2))