import os
import pyonr
from bcrypt import checkpw as _checkpw
from bcrypt import hashpw as _hashpw
from bcrypt import gensalt as _gensalt
from getpass import getpass as _getpass

from .filesHandler import find_ndb_files
from .errors import *
from . import UTypes

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

def _getAlgo(documents, _filter):
   return [d for d in documents if sum(1 for k, v in d.items() if _filter.get(k)==v) >= len(_filter)]

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
   def __init__(self, host=None, password=None):
      if not host:
         self.__host = find_ndb_files('.')
         if isinstance(self.__host, list):
            raise InvalidHostError(host)
      else:
         self.__host = host

      
      self.__read = pyonr.Read(self.__host)
      self.__schema = {
         '__docs': []
      }

      if self.__read.readfile == None:
         self.__read.write(pyonr.dumps(self.__schema))
      if self.__read.readfile.get('__password'):
         if not password:
            password = ''
         if isinstance(password, str) and not _checkpw(password.encode('utf-8'), self.__read.readfile['__password']):
            raise WrongPasswordError()
         elif isinstance(password, bytes) and not _checkpw(password, self.__read.readfile['__password']):
            raise WrongPasswordError()
      
   # file data
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

   # data setters, getters
   
   def get(self, _filter:dict={}):
      docs = self.__read.readfile['__docs']
      return _getAlgo(docs, _filter)
   
   def getOne(self, _filter:dict={}):
      _r = self.__read
      _docs = _r.readfile['__docs']
      if _filter == {}:
         if len(_docs) == 0:
            return None
         return _docs[0]

      f = self.get(_filter)
      if len(f) == 0:
         return None
      return self.get(_filter)[0]

   def appendOne(self, document:dict):
      if not isinstance(document, dict):
         raise TypeError('Unexpected document type')

      _r = self.__read
      _doc = _r.readfile
      
      _doc['__docs'].append(document)
      self.__read.write(_doc)

   def appendMany(self, documents:list):
      if not isinstance(documents, list):
         raise TypeError(f'Unexpected type: "{type(documents)}"')
      if not checkTypes(documents, dict):
         raise TypeError('Every element in "documents" must be a dict')

      _r = self.__read
      _fd = _r.readfile
      _doc = _fd['__docs']

      for document in documents:
         _doc.append(document)

      _r.write(_fd)

   def removeOne(self, _filter:dict):
      _r = self.__read
      _fd = _r.readfile
      _doc = _fd['__docs']
      full_doc = self.getOne(_filter)

      if not full_doc:
         return None

      _doc.remove(full_doc)
      _r.write(_fd)

   def removeMany(self, _filter):
      _r = self.__read
      _fd = _r.readfile
      _doc = _fd['__docs']
      all_docs = self.get(_filter)

      if not all_docs:
         return None

      for doc in all_docs:
         _doc.remove(doc)

      _r.write(_fd)

   def updateOne(self, _filter:dict, update:dict, type:str):
      if type == UTypes.SET: # "SET" an item in a document
         if len(update) != 1:
            raise InvalidDictError(update)
         _fullDoc = self.getOne(_filter)
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']

         i = _docs.index(_fullDoc)
         _docs[i].update(update)

         _r.write(_fd)
         return None

      if type == UTypes.UNSET: # "UNSET" an item from a document
         _fullDoc = self.getOne(_filter)
         _r = self.__read
         _fd = _r.readfile
         _docs = _fd['__docs']

         i = _docs.index(_fullDoc)
         if isinstance(update, str):
            del _docs[i][update]
            _r.write(_fd)
         elif isinstance(update, dict):
            if len(update) != 1:
               raise InvalidDictError(update)
            del _docs[i][list(update.keys())[0]]
            _r.write(_fd)

         return None

      raise TypeError(f'"{type}": Invalid type, expecting "notdb.SET" or "notdb.UNSET"')

   def updateMany(self, _filter:dict, update:dict):
      pass

   def getOneAndremove(self, _filter:dict):
      f = self.get(_filter)
      self.removeOne(_filter)

      return f

class NotDBCloudClient:
   '''

   
   '''
   def __init__(self, host, password=None):
      pass
   