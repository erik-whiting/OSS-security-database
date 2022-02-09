import xml.etree.ElementTree as et

from db.database import Query

file_loc = './db/cwec_v4.6.xml'
tree = et.parse(file_loc)
root = tree.getroot()

weaknesses = root[0]

weakness_xml_keys = ['ID', 'Name', 'Abstraction', 'Structure', 'Status']

# Find longest lengths for db constraints:
ids = []
names = []
abstractions = []
structures = []
statuses = []

for weakness in weaknesses:
  ids.append(weakness.attrib['ID'])
  names.append(weakness.attrib['Name'])
  abstractions.append(weakness.attrib['Abstraction'])
  structures.append(weakness.attrib['Structure'])
  statuses.append(weakness.attrib['Status'])

def get_longest_length(arr, name):
  longest_length = 0
  longest_value = ''
  for item in arr:
    if len(item) > longest_length:
      longest_length = len(item)
      longest_value = item
  print(f'Longest {name}: {longest_value}')
  print(f'Longest lenght: {longest_length}\n')

get_longest_length(ids, 'ID')
get_longest_length(names, 'Name')
get_longest_length(abstractions, 'Abstraction')
get_longest_length(structures, 'Structure')
get_longest_length(statuses, 'Status')

# Longest ID: 1004
# Longest lenght: 4

# Longest Name: Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')
# Longest lenght: 118

# Longest Abstraction: Compound
# Longest lenght: 8

# Longest Structure: Composite
# Longest lenght: 9

# Longest Status: Incomplete
# Longest lenght: 10


columns = ['id', 'name', 'abstraction', 'structure', 'status']
q = Query()

# Need to help unescape apostrophes
def unescape_single_quotes(value):
  return value.replace('\'', '\'\'')

print('Inserting CWEs')

for weakness in weaknesses:
  insert_values = [
    int(weakness.attrib['ID']),
    f"'{unescape_single_quotes(weakness.attrib['Name'])}'",
    f"'{unescape_single_quotes(weakness.attrib['Abstraction'])}'",
    f"'{unescape_single_quotes(weakness.attrib['Structure'])}'",
    f"'{unescape_single_quotes(weakness.attrib['Status'])}'"
  ]
  q.insert(
    'common_weakness_enumerations',
    columns,
    insert_values
  )

print('Finished inserting CWEs')
