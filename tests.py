import notdb

db = notdb.NotDBClient('test.ndb')

db.updateOnePOP({'name': 'Nawaf'}, 'skills.langs')
# print(db.get())