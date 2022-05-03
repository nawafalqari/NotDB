import argparse
import os
from getpass import getpass
from bcrypt import hashpw, gensalt
import pyonr

v = '1.0.0b1'

def get_password():   
   password = hashpw(getpass('Password: ').encode('utf-8'), gensalt())
   return password

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
   schema = {
      '__docs': []
   }

   if os.path.isfile(filename) or os.path.isfile(f'{filename}.ndb'):
      parser.error(f'{filename}: already exists')
   else:
      if not filename.endswith('.ndb'):
         filename += '.ndb'

      with open(filename, 'w') as file:
         if not ispassword:
            file.write(pyonr.dumps(schema))
         else:
            try:
               password = get_password()
               schema['__password'] = password
            except KeyboardInterrupt:
               pass
            file.write(pyonr.dumps(schema))