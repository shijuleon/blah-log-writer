import random
import datetime
import pytz
import argparse
from faker import Faker

log_formats = {
  "nginx_log_format_combined": "{remote_addr} - {remote_user} [{time_local}] \"{request}\" {status} {body_bytes_sent} \"{http_referer}\" \"{http_user_agent}\""
}

def replace(template, values): # Expensive. Lazy evaluate f-strings
  for k, v in values.items():
    key = f"{{{k}}}"
    if template.find(key) >= 0:
      template = template.replace(key, v) # Mutates passed argument
    else:
      raise ValueError

  return template

def generate(log_format, n):
  fake = Faker()
  for i in range(0, n):
    yield replace(log_formats[log_format], {
      "remote_addr": fake.ipv4_public(),
      "remote_user": "-",
      "time_local": (datetime.timedelta(seconds=i) + datetime.datetime.now(pytz.UTC)).strftime("%d/%b/%Y:%H:%M:%S %z"),
      "request": f"{['GET', 'POST', 'PUT', 'DELETE'][random.randint(0, 3)]} /{fake.uri_path()} HTTP/2",
      "status": str([200, 304, 404, 403, 500][random.randint(0, 4)]),
      "body_bytes_sent": str(random.randint(0, 2000)),
      "http_referer": "-",
      "http_user_agent": [fake.chrome(), fake.firefox(), fake.safari()][random.randint(0, 2)]
      })

def main():
  parser = argparse.ArgumentParser(description='Logs go brrr')
  parser.add_argument('n', type=str, help='Number of lines')
  args = parser.parse_args()

  n = int(args.n)
  for line in generate(log_format='nginx_log_format_combined', n=n): print(line)
  
if __name__ == '__main__':
  main()
