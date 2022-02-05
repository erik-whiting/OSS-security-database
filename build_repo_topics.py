import re
from collections.abc import Iterable

from db.database import Query

q = Query()
rows = q.get('repositories', columns=['id', 'topics'])

repo_topic_dict = {}
for r in rows:
  repo_topic_dict[r[0]] = r[1].split(',')

# clean up
del(rows)


# The following does not need to run every
# time the database is built. I'm keeping
# it here so others can see how I came up
# with the length for this field in the
# database
#
# Find longest topic string
# longest_topic = ''
# longest_topic_length = 0
# for key in repo_topic_dict:
#   for topic in repo_topic_dict[key]:
#     if len(topic) > longest_topic_length:
#       longest_topic_length = len(topic)
#       longest_topic = topic

# print(f'Longest topic is {longest_topic}, its length is {longest_topic_length}')
# Longest length is 35

for key in repo_topic_dict:
  for topic in repo_topic_dict[key]:
    q.insert(
      'repo_topics',
      ['repository_id', 'topic'],
      [key, f"'{topic}'"]
    )
