import tkinter as tk
import items as itemPresets

BG_DARK = '#aaa'
BG_LIGHT = '#ccc'

class BudgetSpread(tk.Frame):

	class SpreadSection(tk.Frame):

		class SpreadItem(tk.Frame):
			def __init__(self, master, item, editCallback):
				tk.Frame.__init__(self, master, bg=BG_DARK)
				self.item = item
				self.entryVar = tk.StringVar()
				self.entryVar.set(item.bal)
				self.entryVar.trace_add('write', editCallback)
				tk.Label(self, text=self.item.label, justify=tk.LEFT, anchor='e', bg=BG_DARK).pack(side='left')
				tk.Entry(self, textvariable=self.entryVar, justify=tk.RIGHT, bg=BG_DARK).pack(side='right')

			def updateBal(self):
				try:
					self.item.bal = float(self.entryVar.get())
				except (ValueError):
					print('error update value')

		class SpreadLabel(tk.Frame):
			def __init__(self, master, label):
				tk.Frame.__init__(self, master, bg=BG_LIGHT)
				self.totalVar = tk.DoubleVar()

				tk.Label(self, textvariable=self.totalVar, anchor='e', bg=BG_LIGHT).pack(side='right')
				tk.Label(self, text='$', width=0, anchor='e', bg=BG_LIGHT).pack(side='right', expand=True, fill='both')
				tk.Label(self, text='{}:'.format(label), anchor='e', bg=BG_LIGHT).pack(side='right', expand=True, fill='x')

			def updateVar(self, total):
				self.totalVar.set(total)

		def __init__(self, master, items, editCallback, labeled=False, label=''):
			tk.Frame.__init__(self, master, bg=BG_LIGHT)
			self.labeled = labeled
			self.wid = []

			self.items = []
			for i in items:
				self.items.append(self.SpreadItem(master, i, editCallback))
				self.wid.append(self.items[-1])

			if self.labeled:
				self.wid.append(self.SpreadLabel(master, label))

		def refresh(self):
			for i in self.items:
				i.updateBal()

			if self.labeled:
				self.wid[-1].updateVar(sum([x.item.bal for x in self.items]))

	def __init__(self, master, items, totalVar):
		tk.Frame.__init__(self, master)

		self.bind_class('Entry', '<Down>', self.nextWidget)
		self.bind_class('Entry', '<Up>', self.prevWidget)
		
		self.sectionLabels = []
		self.spreadRows = []
		self.totalVar = totalVar

		self.sections = []
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Income)], self.edit))
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Checking)], self.edit))
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Savings)], self.edit))
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Credit)], self.edit, labeled=True, label='Credit'))
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Goal)], self.edit, labeled=True, label='Goals'))
		self.sections.append(self.SpreadSection(self, [x for x in items if isinstance(x,itemPresets.Expense)], self.edit, labeled=True, label='Expenses'))

		rowCounter = 0
		for i in self.sections:
			for j in i.wid:
				j.grid(column=0, row=rowCounter, sticky='we')
				rowCounter += 1
		
		self.grid_columnconfigure(0, weight=1)

		self.setbg(self, BG_DARK)
		self.refresh()

	def getItems(self):
		items = []
		for s in self.sections:
			for i in s.items:
				items.append(i.item)
		return items

	def generateRow(self, i):
		sI = self.SpreadItem(self, i)
		sI.entryVar.trace_add('write', self.edit)
		return sI

	def generateSectionLabel(self, items, label):

		f = tk.Frame(self)
		tk.Label(f, text=str(sum(i.bal for i in items)), anchor='e').pack(side='right')
		tk.Label(f, text="$", width=0, anchor='e').pack(side='right', expand=True, fill='both')
		tk.Label(f, text='{}:'.format(label), anchor='e').pack(side='right', expand=True, fill='x')
		self.setbg(f, BG_LIGHT)
		return f

	def generateSection(self, items):
		wid = []
		for i in items:
			wid.append(self.generateRow(i))
		return wid

	def generateLabeledSection(self, label, items):
		wid = []
		for i in items:
			wid.append(self.generateRow(i))
		wid.append(self.generateSectionLabel(items, label))
		return wid

	def setbg(self, parent, color):
		parent.configure(bg=color)
		for w in parent.winfo_children():
			w.configure(bg=color)

	def prevWidget(self, event):
		event.widget.tk_focusPrev().focus()
		event.widget.icursor(10)
		return 'break'

	def nextWidget(self, event):
		event.widget.tk_focusNext().focus()
		event.widget.icursor(10)
		return 'break'

	def setbg(self, parent, c):
		for w in parent.winfo_children():
			w.configure(bg=c)

	def edit(self, var, idx, mode):
		self.refresh()

	def refresh(self):
		for i in self.sections:
			i.refresh()
		self.totalVar.set(self.getTotal())

	def getTotal(self):
		spreadItems = []
		for i in [x for x in self.sections]:
			for j in i.items:
				spreadItems.append(j)

		tot = 0
		for i in [x for x in spreadItems if isinstance(x.item, itemPresets.Income)]:
			try:
				tot += i.item.bal# if i.get() != '' else 0
			except ValueError:
				tot += 0
		for i in [x for x in spreadItems if isinstance(x.item, itemPresets.Checking)]:
			try:
				tot+= i.item.bal# if i.get() != '' else 0
			except ValueError:
				tot += 0
		for i in [x for x in spreadItems if isinstance(x.item, itemPresets._Deduction)]:
			try:
				tot -= i.item.bal# if i.get() != '' else 0
			except ValueError:
				tot += 0
		return format(tot, '.2f')