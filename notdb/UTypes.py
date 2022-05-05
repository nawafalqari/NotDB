'''
Update Types

>>> db = NotDBClient('test.ndb')
>>> db.updateOne({'test': True}, {
   'test': False
}, UTypes.SET)
'''

SET = 1000
UNSET = 1001