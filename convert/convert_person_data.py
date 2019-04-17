import sys
import json

def parse_person_line_insert_values(line):
  person_json = json.loads(line.rstrip('\n'))
  person_id = person_json['id']
  person_name = person_json['name']
  return '(' + str(person_id) + ", '" + person_name + "')"

with open('data/person/person.txt', 'r') as person_file:
  file_lines = map(lambda l : l.rstrip('\n'), person_file.readlines())
  value_lines = map(parse_person_line_insert_values, file_lines)
  person_insert_query = ('INSERT INTO\n'
           '  person (id, name)\n'
           'VALUES\n'
           '  ' + ',\n  '.join(value_lines) + ';\n')
  with open('convert/insert-person.sql', 'wb+') as insert_person_query_file:
    insert_person_query_file.write(person_insert_query.encode(sys.getdefaultencoding()))
