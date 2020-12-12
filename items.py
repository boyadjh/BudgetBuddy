class _Item:
	def __init__(self, label, bal):
		self.label = label
		self.bal = bal

	def __str__(self):
		return self.label + ':\t$'+str(self.bal)+'\n'

class Income(_Item):
	def __init__(self, label='Income', bal=0):
		super().__init__(label, bal)

class _Deduction(_Item):
	def __init__(self, label, bal):
		super().__init__(label, bal)

class Expense(_Deduction):
	def __init__(self, label='Generic Expense', bal=0):
		super().__init__(label, bal)

class Goal(_Deduction):
	def __init__(self, label='Goal Item', bal=0):
		super().__init__(label, bal)