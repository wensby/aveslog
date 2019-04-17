import sys
import json

def parse_sighting_line_insert_values(line):
  sighting_json = json.loads(line.rstrip('\n'))
  sighting_id = sighting_json['id']
  sighting_person_id = sighting_json['person_id']
  sighting_bird_id = sighting_json['bird_id']
  return '(' + str(sighting_id) + ", " + str(sighting_person_id) + ", " + str(sighting_bird_id) + ")"

with open('data/sighting/sighting.txt', 'r') as sighting_file:
  file_lines = map(lambda l : l.rstrip('\n'), sighting_file.readlines())
  value_lines = map(parse_sighting_line_insert_values, file_lines)
  sighting_insert_query = ('INSERT INTO\n'
           '  sighting (id, person_id, bird_id)\n'
           'VALUES\n'
           '  ' + ',\n  '.join(value_lines) + ';\n')
  with open('convert/insert-sighting.sql', 'wb+') as insert_sighting_query_file:
    insert_sighting_query_file.write(sighting_insert_query.encode(sys.getdefaultencoding()))
