import notdb
from matplotlib import pyplot as plt

db = notdb.NotDBClient()

while True:
   try:
      cmd = input('> ').strip().lower()

      if cmd == 'save':
         fp = input('filepath> ').strip()

         db.files.appendFile(fp, name=input('name> ').strip() or None)

      if cmd == 'show':
         name = input('name> ').strip()

         f = db.files.getFile({'name': name}, 'image')

         plt.imshow(f)
         plt.show()
         
      if cmd == 'clear':
         db.files.removeFiles({})

   except KeyboardInterrupt:
      exit()
   except Exception as e:
      print(f'ERR: {e}')