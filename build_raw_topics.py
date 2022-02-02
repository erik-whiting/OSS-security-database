from db.database import Query

q = Query()
db_raw_topics = q.get('repositories', 'topics')

split_topics = []

for db_raw_topic in db_raw_topics:
  for raw_topic in db_raw_topic:
    split_topics.append(f'{raw_topic}')

longest_topic_name = ''
longest_topic_name_length = 0

for topic in split_topics:
  if len(topic) > longest_topic_name_length:
    longest_topic_name = topic
    longest_topic_name_length = len(topic)

print(f'\nLongest topic name: {longest_topic_name}')
print(f'\nLongest topic name length: {longest_topic_name_length}') # 387

# Some topics are arrays, some are lists of
# words seperated by commas. We already split
# out the arrays, now we have to split out the
# topics that are comma seperated strings.
# Some of the topics are more like descriptions
# and have commas but they're there for grammar
# purposes. We have to seperate those out.

import re
def possible_comma_topics(string):
  instances = re.findall(r',(?! )', string)
  return len(instances)

comma_splittable_topics = []
len_before = len(split_topics)
print(f'split_topics length before finding comma splittable topics: {len_before}')
for topic in split_topics:
  if possible_comma_topics(topic) >= 2:
    comma_splittable_topics.append(topic)
    split_topics.remove(topic)

len_after = len(split_topics)
print(f'split_topics length after finding comma splittable topics: {len_after}')
print(f'Number of splittable topics found: {len(comma_splittable_topics)}')

total = len_after + len(comma_splittable_topics)
print(f'{total} <-- This number should be {len_before}')

len_before = len(split_topics)
print(f'split_topics length before splitting comma topics: {len_before}')
comma_split_topics = []
for topics in comma_splittable_topics:
  for topic in topics.split(','):
    comma_split_topics.append(topic)
    split_topics.append(topic)

number_of_topics_split = len(comma_split_topics)
len_after = len(split_topics)
expected_total = len_before + number_of_topics_split
print(f'Number of topics split: {number_of_topics_split}')
print(f'{expected_total} <-- This number should be {number_of_topics_split + len_before}')

print('\nNow starting to build topic records in database')
print(f'Upserting {len(split_topics)} records, this will probably take a while')

def upsert_topic(topic_name):
  topic_name = topic_name.replace('\'', '\'\'')
  record = q.get('topics', 'name', topic_name)
  if len(record) == 0:
    q.insert('topics', ['name', 'occurences'], [f"'{topic_name}'", 1])
  else:
    q.update(
      'topics',
      'occurences',
      record[0][-1] + 1,
      'name',
      f"'{topic_name}'"
    )

send_alert = len(split_topics) / 20
alert_number = 0
alerts = 0
for topic in split_topics:
  alert_number += 1
  upsert_topic(topic)
  if alert_number >= send_alert:
    alerts += 1
    print(f'[Alert #{alerts}] {alert_number * alerts} records have been inserted')
    print(f'[Alert #{alerts}] {(len(split_topics) - (send_alert * alerts))} to go\n')
    alert_number = 0
