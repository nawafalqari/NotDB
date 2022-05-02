import os

def find_ndb_files(path):
   p = path
   if path == '.':
      p = os.getcwd()
   files = [f for f in os.listdir(p) if f.endswith('.ndb')]

   if len(files) == 1:
      return files[0]
   else:
      return files