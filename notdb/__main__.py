import argparse
import os
from getpass import getpass
from bcrypt import hashpw, gensalt
import pyonr

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

def get_password():   
   password = hashpw(getpass('Password: ').encode('utf-8'), gensalt())
   return password

def create_db(name, _password=None):
   schema = {
      '__docs': []
   }

   with open(name, 'w') as file:
         if not _password:
            file.write(pyonr.dumps(schema))
         else:
            try:
               password = get_password()
               schema['__password'] = password
            except KeyboardInterrupt:
               pass
            file.write(pyonr.dumps(schema))

def main():
   pass

parser = argparse.ArgumentParser('NotDB', 'notdb [filename]', f'NotDB command line tool v{v}', )

parser.add_argument('filename', nargs=1, type=str, help='Create a database with the given filename', metavar='filename')
parser.add_argument('-p', '--password', action='store_true', help='Secure the database with a password')
parser.add_argument('-v', '--version', action='version', version=f'notdb {v}', help='Show the notdb_viewer version')

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