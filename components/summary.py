import tkinter as tk
from components.budgetspread import BudgetSpread

class Summary(tk.Frame):
	def __init__(self, master, items, callback):
		tk.Frame.__init__(self, master)
		self.master = master
		self.callback = callback

		self.leftoverVal = tk.DoubleVar()

		self.genLabel().pack()
		self.spread = self.genSpread(items)
		self.spread.pack(expand=True, fill='x')

		self.genLeftover().pack(expand=True, fill='x')

		self.leftoverVal.trace_add('write', self.leftoverUpdate)

		#self.updateLeftover()

	def leftoverUpdate(self, var, arg, mode):
		self.callback(self.spread.getItems())

	def genLabel(self):
		return tk.Label(self, text='Summary')

	def genSpread(self, items):
		return BudgetSpread(self, items, self.leftoverVal)

	def genLeftover(self):
		lo = tk.Frame(self)
		tk.Label(lo, textvariable=self.leftoverVal, justify=tk.RIGHT).pack(side='right')
		tk.Label(lo, text="$", justify=tk.RIGHT, width=0, anchor='e', bd=-4).pack(side='right')
		tk.Label(lo, text='Leftover:').pack(side='left')
		return lo
