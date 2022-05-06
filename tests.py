from notdb import NotDBClient

db = NotDBClient('http://192.168.1.111:5000/t.ndb')

print(db.get())
print(db.get({'online': True}))
print(db.getOne({'online': True}))