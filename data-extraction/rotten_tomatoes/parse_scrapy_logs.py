import re
import csv
from urllib.parse import unquote

status_code = 403
regex = rf"DEBUG: Crawled \({status_code}\) <GET https://www.rottentomatoes.com/m/(.*)>"

with open("raw-data/movies_names.csv", "r") as m_file:
  reader = csv.reader(m_file, delimiter=',', quotechar='"')
  m_names = []
  m_ids = []

  next(reader)
  for mid, _, name in reader:
    m_names.append(name)
    m_ids.append(mid)

with open("logs.txt", "r") as logs:
  for line in logs:
    url = re.search(regex, line)

    if url is not None:
      name = url.group(1)

      mid = m_ids[m_names.index(unquote(name))]

      print(str(mid) + "," + name)

