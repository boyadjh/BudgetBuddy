class Profile:
	def __init__(self, username='user', items=[]):
		self.items = items
		self.username = username
		
	def __str__(self):
		s = ''
		for i in self.items:
			s += str(i)
		return s
