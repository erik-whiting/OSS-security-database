import csv

from db.database import Query

analysis_id = 17
log_location = f'analysis_{analysis_id}_error_log.csv'
error_data = []

with open(log_location, newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    error_data.append(row)

error_data.pop(0)

error_messages = []
for datum in error_data:
  error_messages.append(datum[1])

missed_repos = []
for msg in error_messages:
  missed_repos.append(
    msg.split(' Insertion of ')[1].split(' vulnerabilities failed')[0]
  )

repos = list(dict.fromkeys(missed_repos))

sql_friendly_repos = []
for repo in repos:
  sql_friendly_repos.append(f"'{repo}'")

sql = f'SELECT id FROM repositories WHERE name IN ('
index = 0
for repo in sql_friendly_repos:
  index += 1
  sql += repo
  if index != len(sql_friendly_repos):
    sql += ','
sql += ')'

q = Query()
repo_data = q.query(sql)

print(repo_data)