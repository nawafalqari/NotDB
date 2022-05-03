import notdb

db = notdb.NotDBClient("test.ndb")

while True:
	cmd = input('> ').strip()

	if cmd == 'setSalary':
		employee = input('employee name: ')
		salary = int(input('salary: '))
		
		emp_obj = db.getOne({
			'name': employee
		})

		if not emp_obj:
			print('Invalid employee.')
		else:
			db.updateOne(emp_obj,
						{
							'salary': salary # type=int
						}, notdb.SET)

	elif cmd == 'setAdmin':
		employee = input('employee: ').strip()

		emp_obj = db.getOne({
			'name': employee
		})

		if not emp_obj:
			print('Invalid emplyee.')
		else:
			db.updateOne(emp_obj, {
				'isAdmin': True
			}, notdb.SET)

	elif cmd == 'unsetAdmin':
		employee = input('employee: ').strip()

		emp_obj =  db.getOne({
			'name': employee
		})

		if not emp_obj:
			print('Invalid employee')
		elif not emp_obj.get('isAdmin'):
			print('employee is not even admin')
		else:
			db.updateOne(emp_obj, 'isAdmin', notdb.UNSET)
	
	else:
		db.appendOne({
			'name': cmd
		})