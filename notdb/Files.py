import os
import io
from random import sample
from mimetypes import guess_type
from datetime import datetime

from .algo import _getAlgo
from .errors import *

def generateCode(length:int=8):
   '''
   Generate a random code
   '''
   upperCase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   lowerCase = 'abcdefghijklmnopqrstuvwxyz'
   digits    = '0123456789'

   _all = list(upperCase + lowerCase + digits)

   return ''.join(sample(_all, length))

def generateTime() -> list:
   d = datetime.now()
   data = [d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond]

   return data

class Files:
   '''
   Handle files inside NotDB databases
   '''
   def __init__(
      self,
      cls,
      read,
      CRead,
      CWrite,
      encoding:str='utf-8'):
      '''
      Handle files inside NotDB databases

      `Parameters:`

      `cls`: main `NotDBClient` instance
      '''
      self.cls = cls
      self.read = read
      self.__CRead = CRead
      self.__CWrite = CWrite
      self.encoding = encoding

   def appendFile(self, fp:str, filename:str=None, name:str=None):
      '''
      
      Append file to db
      
      >>> db.files.appendFile('logo.png', filename='logo.png', name='logo') 

      `Parameters:`

      `fp`: filepath to file

      `filename`: filename will be stored with the file document (not required if name was given)
      >>> db.files.getFile({'filename': 'logo.png'})

      `name`: name can be used to get the file (not required if filename was given)
      >>> db.files.getFile({'name': 'logo'})

      `note`: if name was not given, a generated code will take it place (The opposite is true)
      
      also both of them can be given

      '''
      if not filename and not name: # if filename and name wasn't given
         raise TypeError('both filename and name are not specified')
      if not isinstance(fp, str) or (not isinstance(filename, str) and filename != None) or (not isinstance(name, str) and name != None): # if one of the params is not "str"
         raise TypeError('Every parameter in `appendFile` must be `str`')
      if not os.path.isfile(fp): # if the file doesn't exist
         raise FileNotFoundError(f'{fp} is not a file or not found')

      # Storing file data inside document
      document = {}
      
      extension = os.path.splitext(fp)[-1]
      if not name:
         document['name'] = generateCode()
      else:
         document['name'] = name

      if not filename:
         document['filename'] = f'{generateCode()}{extension}' # filename.ext "extension variable has a dot at the begining"
      else:
         document['filename'] = filename
      with open(fp, 'rb') as f:
         document['data'] = f.read()

      document['type'] = extension

      fileMimeType = guess_type(fp)
      if fileMimeType:
         document['mimetype'] = fileMimeType[0]
      else:
         document['mimetype'] = None

      document['size'] = os.path.getsize(fp)
      document['uploadDate'] = generateTime()

      if self.cls.hostType == 'local': # local db
         _r = self.read
         _dbd = _r.readfile # db data

         if not _dbd.get('__files'): # if __files doesn't exists in the db
            self.__make_files_section() # add __files
            _dbd = _r.readfile # db data

         _dbd['__files'].append(document)
         _r.write(_dbd)

         return True

      # server db
      _dbd = self.__CRead() # db data

      if not _dbd.get('__files'): # if __files doesn't exists in the db
         self.__make_files_section_server() # add __files

      _dbd = self.__CRead() # db data
      _dbd['__files'].append(document)
      self.__CWrite(_dbd)

      return True
      
      
   # def appendFileBinary(self, binary:bytes):
   #    pass

   def removeFile(self, _filter:dict):
      '''
      Remove a file from db

      removing using `name`:
      >>> db.files.removeFile({'name': 'Logo'}) # "name" is A name was given when appending the file

      removing using `filename`:
      >>> db.files.removeFile({'filename': 'logo.png'}) # must add extension

      Note: if a name or filename was not given when appending, A random generated code will take it place

      `Parameters:`

      `_filter`: filter is used to get the file information

      if `_filter={}` it will remove every file
      >>> db.files.removeFile({
         'name': 'Logo',
         'filename': 'logo.png'
      }) # one of them must be specified

      '''
      if not isinstance(_filter, dict):
         raise TypeError('`_filter` must be a dict')

      if not self.read.readfile.get('__files'):
         if self.cls.hostType == 'local':
            self.__make_files_section()
         if self.cls.hostType == 'cloud':
            self.__make_files_section_server()

      if self.cls.hostType == 'local': # local db
         _r = self.read
         _fd = _r.readfile
         _files = _fd['__files']
         fullFileDoc = self.getFile(_filter)

         if not fullFileDoc:
            return None
         
         _files.remove(fullFileDoc)
         _r.write(_fd)

         return True

      # Cloud db
      _fd = self.__CRead()
      _files = _fd['__files']
      fullFileDoc = self.getFile(_filter)

      if not fullFileDoc:
         return None

      _files.remove(fullFileDoc)
      self.__CWrite(fullFileDoc)

      return True

   def removeFiles(self, _filter:dict):
      if self.cls.hostType == 'local':
         _r = self.read
         _fd = _r.readfile
         _files = _fd['__files']
         all_files = self.getFiles(_filter)

         if not all_files:
            return None

         for file in all_files:
            _files.remove(file)

         _r.write(_fd)
      
         return True

      _fd = self.__CRead()
      _files = _fd['__files']
      all_files = self.getFiles(_filter)

      if not all_files:
         return None

      for file in all_files:
         _files.remove(file)

      self.__CWrite(_fd)
      return True

   def getFiles(self, _filter:dict={}, returnType:str='dict'):
      '''
      
      Get files that match the `_filter`

      >>> db.files.getFiles({'name': 'logo'})
      [{...}, {...}] # list of files that match {'name': 'logo'}

      `Parameters:`
      
      `_filter`: used to filter matches (don't use `getFiles` if you are expecting one result)

      `returnType`: used to specifiy the return type
      
      Types:

         `dict`: will return the entire filedata (default)
         >>> db.files.getFiles({'name': 'logo'}, 'dict') # since 'dict' is the default value you don't have to type it
         [{
            'name': ..., 'filename': ..., 'data': ..., 'type': ...,
            'mimetype': ..., 'size': ..., 'uploadDate':  [...]
         },
         [exact same as above, as long as it matches the filter]]

         `open`, `io`: will return the files as if you used `open()` on them
         >>> db.files.getFiles({'filename': 'logo.png'}, 'open')
         [<_io.BytesIO object at 0x0000017E621B1220>,
         <_io.BytesIO object at 0x0000017E621B1220>]

         `image`, `imread`: will return `matplotlib.pyplot.imread(file)` (you must install matplotlib)
         >>> from matplotlib import pyplot as plt
         >>> img = db.files.getFiles({'filename': 'logo.png'}, 'image')[0] # select the first image that matches the filter
         >>> plt.imshow(img)
         >>> plt.show()

      '''
      if not isinstance(_filter, dict):
         raise TypeError('`_filter` must be a dict')
      
      if not self.read.readfile.get('__files'):
         if self.cls.hostType == 'local':
            self.__make_files_section()
         if self.cls.hostType == 'cloud':
            self.__make_files_section_server()

      docs = self.read.readfile['__files'] if self.cls.hostType == 'local' else self.__CRead()['__files']
      returnType = returnType.strip().lower()

      files = _getAlgo(docs, _filter)

      if returnType == 'dict':
         return files

      if returnType == 'open' or returnType == 'io':
         filesBin = map(lambda e:e['data'], files)
         filesBytesIO = list(map(io.BytesIO, filesBin))

         return filesBytesIO 
      if returnType == 'image' or returnType == 'imread':
         try:
            from matplotlib.pyplot import imread
         except ModuleNotFoundError:
            raise ImportError('matplotlib is not installed (to use matplotlib.pyplot.imread) install it first')

         filesBin = map(lambda e:e['data'], files)
         filesBytesIO = list(map(io.BytesIO, filesBin))

         return list(map(imread, filesBytesIO))
      
      raise ValueError('Invalid returnType, check documentation for types')

   def getFile(self, _filter:dict={}, returnType:str='dict'):
      '''
      
      Get the first file that match `_filter`

      >>> db.files.getFile({'name': 'logo'})
      {...} # document of file data

      `Parameters:`

      `_filter`: used to filter matches

      `returnType`: used to specifiy the return type

      Types:

         `dict`: will return the entire filedata (default)
         >>> db.files.getFile({'name': 'logo'}, 'dict') # since 'dict' is the default value you don't have to type it
         {
            'name': ..., 'filename': ..., 'data': ..., 'type': ...,
            'mimetype': ..., 'size': ..., 'uploadDate':  [...]
         }

         `open`, `io`: will return the file as if you used `open()` on it
         >>> db.files.getFile({'filename': 'logo.png'}, 'open')
         <_io.BytesIO object at 0x0000017E621B1220>

         `image`, `imread`: will return `matplotlib.pyplot.imread(file) # matplotlib must be installed
         >>> from matplotlib import pyplot as plt
         >>> img = db.files.getFiles({'filename': 'logo.png'}, 'image')
         >>> plt.imshow(img)
         >>> plt.show()

      '''
      if not self.read.readfile.get('__files'):
         if self.cls.hostType == 'local':
            self.__make_files_section()
         if self.cls.hostType == 'cloud':
            self.__make_files_section_server()

      if self.cls.hostType == 'local': #local db
         _r = self.read
         _files = _r.readfile['__files']
         if _filter == {}:
            if len(_files) == 0:
               return None
            return _files[0]
         
         f = self.getFiles(_filter, returnType)
         if len(f) == 0:
            return None
         return f[0]

      # Cloud server
      _files = self.__CRead()['__files']
      if _filter == {}:
         if len(_files) == 0:
            return None
         return _files[0]

      f = self.getFiles(_filter, returnType)
      if len(f) == 0:
         return None
      return f[0]

   def __make_files_section(self):
      _r = self.read
      _dbd = _r.readfile

      _dbd['__files'] = []
      _r.write(_dbd)

   def __make_files_section_server(self):
      _r = self.read
      _dbd = _r.readfile

      _dbd['__files'] = []
      self.__CWrite(_dbd)