import argparse
import os
from . import create_db

def read(rel_path):
   import codecs
   here = os.path.abspath(os.path.dirname(__file__))
   with codecs.open(os.path.join(here, rel_path), 'r') as fp:
      return fp.read()

def get_version(rel_path):
   for line in read(rel_path).splitlines():
      if line.startswith('__version__'):
         delim = '"' if '"' in line else "'"
         return line.split(delim)[1]
   else:
      raise RuntimeError("Unable to find version string.")

v = get_version('__init__.py')

def main():
   pass

if __name__ == '__main__' or __name__ == 'notdb.__main__':
   parser = argparse.ArgumentParser('NotDB', 'notdb [filename]', f'NotDB command line tool v{v}',)

   parser.add_argument('filename', nargs=1, type=str, help='Create a database with the given filename', metavar='filename')
   parser.add_argument('-p', '--password', action='store_true', help='Secure the database with a password')
   parser.add_argument('-v', '--version', action='version', version=f'notdb {v}', help='Show the notdb version')

   args = parser.parse_args()

   if len(args.filename) != 0:
      filename = args.filename[0]
      ispassword = args.password

      if os.path.isfile(filename) or os.path.isfile(f'{filename}.ndb'):
         parser.error(f'{filename}: already exists')
      else:
         if not filename.endswith('.ndb'):
            filename += '.ndb'

         create_db(filename, ispassword)