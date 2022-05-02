import notdb

client = notdb.NotDBClient(password='123')

print(client.getOne({'name': 'Nawaf'}))
print('Before update.')

client.updateOne({
   'name': 'Nawaf'
}, {
   'languages': ['Python', 'JavaScript', 'PYON']
}, notdb.SET)

print('After update.')
print(client.getOne({'name': 'Nawaf'}))