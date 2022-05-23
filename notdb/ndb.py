import os
from bcrypt import (hashpw as _hashpw, checkpw as _checkpw, gensalt as _gensalt)
import pyonr
from getpass import getpass as _getpass
from requests import request as _req

from .filesHandler import find_ndb_files
from .errors import *
from .popHandler import popDN
from . import UTypes
from .Files import Files
from .algo import _getAlgo

schema = {
   '__docs': []
}

def checkTypes(l:list, type):
   '''
   Checks if every element in a list is the same `type`

   ```python
   >>> l = [1, 2, 3, 'str']
   >>> checkTypes(l, int)
   False
   ```
   '''
   return not list(filter(lambda e:not isinstance(e, type), l))

def get_password():   
   password = _hashpw(_getpass('Password: ').encode('utf-8'), _gensalt())
   return password

def create_db(filename:str, _password=None):
   schema = {
      '__docs': []
   }

   if not filename.endswith('.ndb'):
      filename += '.ndb'

   with open(filename, 'w') as file:
         if not _password:
            file.write(pyonr.dumps(schema))
         else:
            try:
               password = get_password()
               schema['__password'] = password
            except KeyboardInterrupt:
               pass
            file.write(pyonr.dumps(schema))

class NotDBClient:
   '''
   NotDB Databases client

   >>> NotDBClient('test.ndb', password=password)
   
   Full documentation:
   - [NotDB](https://github.com/nawafalqari/NotDB#readme)
   - [NotDB Cloud](https://github.com/nawafalqari/NotDB_Cloud#readme)
   '''
   def __init__(
      self,
      host:str=None,
      password:str=None):
      '''
      NotDB Databases client

      >>> NotDBClient('test.ndb', password=password)
      
      Full documentation:
      - [NotDB](https://github.com/nawafalqari/NotDB#readme)
      - [NotDB Cloud](https://github.com/nawafalqari/NotDB_Cloud#readme)

      `Parameters:`

      `host`: (optional) database filename/url/ip address,
      if `None` was given it will scan the directory for one ndb file
      if there was multiple databases it will raise `InvalidHostError`

      `password`: (optional for unsecured DBs) database's password,
      must be `str` or `bytes`\n
      raise `WrongPasswordError` if the password was wrong
      '''
      if not host:
         self.__host = find_ndb_files('.')
         self.__hostType = 'local'
         if isinstance(self.__host, list):
            raise InvalidHostError(host)
      elif host.startswith(('https://', 'http://')):
         if not host.endswith('.ndb'):
            raise InvalidHostError(host, 'Invalid host, host example: https://example.com/dbname.ndb')
         _req('CONNECT', host)
         self.__host = host
         self.__hostType = 'cloud'
      else:
         self.__host = host
         self.__hostType = 'local'

      self.__schema = {
         '__docs': []
      }
      if self.__hostType == 'local':
         self.__read = pyonr.Read(self.__host)

         if self.__read.readfile == None:
            self.__read.write(pyonr.dumps(self.__schema))
         if self.__read.readfile.get('__password'):
            if not password:
               password = ''
            if isinstance(password, str) and not _checkpw(password.encode('utf-8'), self.__read.readfile['__password']):
               raise WrongPasswordError()
            elif isinstance(password, bytes) and not _checkpw(password, self.__read.readfile['__password']):
               raise WrongPasswordError()

      elif self.__hostType == 'cloud':
         # self.__dbdata = pyonr.loads(_req('BRING', self.__host).content.decode('utf-8'))

         if self.__CDBData == None:
            self.__CWrite(pyonr.dumps(self.__schema))
            self.__CDBData = self.__CRead()
         if self.__CDBData.get('__password'):
            if not password:
               password = ''
            if isinstance(password, str) and not _checkpw(password.encode('utf-8'), self.__CDBData.get('__password')):
               raise WrongPasswordError()
            elif isinstance(password, bytes) and not _checkpw(password, self.__CDBData('__password')):
               raise WrongPasswordError()
      
   # database getters
   @property
   def host(self):
      h = self.__host
      if os.path.isfile(h):
         return os.path.abspath(h)      

      return self.__host
   
   @property
   def documents(self):
      fdata = self.__read.readfile
      schema = self.__schema

      if not fdata:
         self.__read.write(schema)
         fdata = self.__read.readfile

      elif isinstance(fdata, dict) and not fdata.get('__docs'):
         
         if fdata.get('__password'):
            schema['__password'] = fdata['__password']
         self.__read.write(schema)
         fdata = self.__read.readfile

      return len(fdata['__docs'])

   @property
   def hostType(self):
      return self.__hostType

   # Files class
   @property
   def files(self) -> Files:
      return Files(self, self.__read, self.__CRead, self.__CWrite)

   # cloud dbs functions
   def __CRead(self):
      return pyonr.loads(_req('BRING', self.__host).content.decode('utf-8'))

   def __CWrite(self, update:dict):
      req = _req('UPDATE', self.__host, data={
         'update': f'{update}'
      }).content.decode('utf-8')

      if req.startswith('Error'):
         raise ServerError(req)

   @property
   def __CDBData(self):
      return self.__CRead()

   # data setters, getters
   
   def get(self, _filter:dict={}):
      '''
      get a list of documents that match `_filter`

      >>> db.get({'online': True})
      [{'name': 'Nawaf', 'online': True}, {'name': 'Khayal', 'online': True}]
      '''
      docs = self.__read.readfile['__docs'] if self.__hostType == 'local' else self.__CDBData['__docs']
      return _getAlgo(docs, _filter)
   
   def getOne(self, _filter:dict={}):
      '''
      get the first document that match `_filter`

      >>> db.get({'online': True})
      {'name': 'Nawaf', 'online': True}
      '''
      # local
      if self.__hostType == 'local':
         _r = self.__read
         _docs = _r.readfile['__docs']
         if _filter == {}:
            if len(_docs) == 0:
               return None
            return _docs[0]

         f = self.get(_filter)
         if len(f) == 0:
            return None
         return f[0]
      
      # Cloud server
      _docs = self.__CDBData['__docs']
      if _filter == {}:
         if len(_docs) == 0:
            return None
         return _docs[0]
      
      f =  self.get(_filter)
      if len(f) == 0:
         return None
      return f[0]
      

   def appendOne(self, document:dict):
      '''
      Append one document to the end of db

      >>> db.appendOne({'name': 'Nawaf'})
      True

      return True on success
      '''
      if not isinstance(document, dict):
         raise TypeError('Unexpected document type')

      if self.__hostType == 'local': # local db
         _r = self.__read
         _dbd = _r.readfile # db data
         
         _dbd['__docs'].append(document)
         _r.write(_dbd)

         return True
      # server db
      _dbd = self.__CRead() # db data

      _dbd['__docs'].append(document)
      self.__CWrite(_dbd)

      return True

   def appendMany(self, documents:list):
      '''
      Append multiple documents to db

      >>> numbers_from_one_to_ten = list(range(1, 11))
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      >>> db.appendMany(number_from_one_to_ten)
      True

      return True on success
      '''
      if not isinstance(documents, list):
         raise TypeError(f'Unexpected type: "{type(documents)}"')
      if not checkTypes(documents, dict):
         raise TypeError('Every element in "documents" must be a dict')

      if self.__hostType == 'local': # local db
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']

         for document in documents:
            _docs.append(document)

         _r.write(_fd)

         return True

      # server db
      _fd = self.__CRead()
      _docs = _fd['__docs']

      for document in documents:
         _docs.append(document)

      self.__CWrite(_fd)

      return True

   def removeOne(self, _filter:dict):
      '''
      Remove the first document that match `_filter`

      >>> db.removeOne({'name': 'Nawaf'})
      True

      return True on success
      '''

      if self.__hostType == 'local': # local db
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']
         full_doc = self.getOne(_filter)

         if not full_doc:
            return None

         _docs.remove(full_doc)
         _r.write(_fd)

         return True
      
      # Cloud db
      _fd = self.__CRead()
      _docs = _fd['__docs']
      full_doc = self.getOne(_filter)

      if not full_doc:
         return None
      
      _docs.remove(full_doc)
      self.__CWRITE(full_doc)

      return True

   def removeMany(self, _filter):
      '''
      Remove multiple documents from db

      >>> db.removeMany('online': True)
      True

      return True on success
      '''

      if self.__hostType == 'local': # local db
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']
         all_docs = self.get(_filter)

         if not all_docs:
            return None

         for document in all_docs:
            _docs.remove(document)

         _r.write(_fd)
         
         return True
      
      _fd = self.__CRead()
      _docs = _fd['__docs']
      all_docs = self.get(_filter)

      if not all_docs:
         return None

      for document in all_docs:
         _docs.remove(document)

      self.__CWrite(_fd)
      return True

   def updateOne(self, _filter:dict, update:dict, type:str):
      '''
      Update the first element that matches `_filter`

      >>> db.updateOne(
            {'name': 'Nawaf'}, # <---- filter
            {'online': True},  # <---- update (new key),
            notdb.UTypes.SET   # <---- Update type (SET, UNSET, ...)
         )
      True

      return True on success
      '''
      _fullDoc = self.getOne(_filter)
      _r = None
      _fd = None
      _docs = None
      if self.hostType == 'local':
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']
      if self.hostType == 'cloud':
         _fd = self.__CRead()
         _docs = _fd['__docs']

      if type == UTypes.SET: # "SET" an item in a document
         if len(update) != 1:
            raise InvalidDictError(update)

         i = _docs.index(_fullDoc)
         _docs[i].update(update)

         if self.hostType == 'local':
            _r.write(_fd)
         if self.hostType == 'cloud':
            self.__CWrite(_fd)
         return True

      if type == UTypes.UNSET: # "UNSET" an item from a document
         i = _docs.index(_fullDoc)
         if isinstance(update, str):
            del _docs[i][update]
            
            if self.hostType == 'local':
               _r.write(_fd)
            if self.hostType == 'cloud':
               self.__CWrite(_fd)
         elif isinstance(update, dict):
            if len(update) != 1:
               raise InvalidDictError(update)
            del _docs[i][list(update.keys())[0]]

            if self.hostType == 'local':
               _r.write(_fd)
            if self.hostType == 'cloud':
               self.__CWrite(_fd)

         return True

      raise TypeError(f'"{type}": Invalid type, check dir(notdb.UTypes)')

   def updateOnePOP(self, _filter:dict, element:str, element_index:int=-1):
      '''
      Remove and return a list item at index
      (This update type is only for pop)

      >>> db.updateOnePOP(
      {'name': 'Nawaf'},         <-- filter
      'skills.programmingLangs', <-- path to array (dot notation)
      0)                         <-- index (default last)
      '''

      _fullDoc = self.getOne(_filter)
      _r = None
      _fd = None
      _docs = None
      if self.hostType == 'local':
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']
      if self.hostType == 'cloud':
         _fd = self.__CRead()
         _docs = _fd['__docs']
      i = _docs.index(_fullDoc)
      
      poppedItem = popDN(_docs[i], element, element_index)

      if self.hostType == 'local':
         _r.write(_fd)
      if self.hostType == 'cloud':
         self.__CWrite(_fd)

      return poppedItem

   def __repr__(self):
      return f'{self.__class__.__name__}(host="{self.host}")'

class NotDBCloudClient(NotDBClient):
   '''
   NotDB Databases On Cloud

   >>> NotDBCloudClient('https://example.com/t.ndb', password=password)
   
   Full documentation:
   - [NotDB](https://github.com/nawafalqari/NotDB#readme)
   - [NotDB Cloud](https://github.com/nawafalqari/NotDB_Cloud#readme)
   '''
   pass