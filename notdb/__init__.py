r'''

NotDB is an open source document-oriented database that uses PYON-like documents

Developed by Nawaf Alqari in 2022

[Documentation](https://github.com/nawafalqari/NotDB)

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

from .ndb import NotDBClient, NotDBCloudClient, UTypes, create_db, get_password, schema
from .errors import *

__version__ = '1.2.2'
__all__ = ['InvalidDictError', 'InvalidHostError', 'NotDBClient', 'NotDBCloudClient', 'Files', 'UTypes', 'WrongPasswordError',
            'checkTypes', '__version__']