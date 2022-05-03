r'''

NotDB is an open source document-oriented database that uses PYON-like documents

Developed by Nawaf Alqari in 2022

Example:
First you need to make your database
you can make it manually by just creating a `.ndb` file

or by using the command line tool:
$ notdb [filename]
if you want to secure your db with a password you can use the `--password` or `-p` flag
$ notdb [filename] --password

>>> import notdb
>>> db = notdb.NotDBClient('dbName.ndb')
>>> db.get({}) # will return every document in the db

'''

from .notdb import *

__version__ = '1.0.0'