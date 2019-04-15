import sys
import json

def parse_bird_line_insert_values(line):
  bird_json = json.loads(line.rstrip('\n'))
  bird_id = bird_json['id']
  bird_name = bird_json['name']
  return '(' + str(bird_id) + ", '" + bird_name + "')"

with open('data/bird/bird.txt', 'r') as bird_file:
  file_lines = map(lambda l : l.rstrip('\n'), bird_file.readlines())
  value_lines = map(parse_bird_line_insert_values, file_lines)
  bird_insert_query = ('INSERT INTO\n'
           '  bird (id, name)\n'
           'VALUES\n'
           '  ' + ',\n  '.join(value_lines) + ';\n')
  with open('convert/insert-bird.sql', 'wb+') as insert_bird_query_file:
    insert_bird_query_file.write(bird_insert_query.encode(sys.getdefaultencoding()))
