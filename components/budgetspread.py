import tkinter as tk
import items as itemPresets

BG_DARK = '#aaa'
BG_LIGHT = '#ccc'

class BudgetSpread(tk.Frame):
	def __init__(self, master, items, totalVar):
		tk.Frame.__init__(self, master)

		self.bind_class('Entry', '<Down>', self.nextWidget)
		self.bind_class('Entry', '<Up>', self.prevWidget)
		
		self.entryVar = []
		self.spreadItems = []
		self.totalVar = totalVar

		#income
		self.spreadItems += self.generateSection([x for x in items if isinstance(x,itemPresets.Income)], True)
		#checking
		self.spreadItems += self.generateSection([x for x in items if isinstance(x,itemPresets.Checking)], True)
		#savings
		self.spreadItems += self.generateSection([x for x in items if isinstance(x,itemPresets.Savings)], True)

		self.spreadItems += self.generateLabeledSection('Credit', [x for x in items if isinstance(x,itemPresets.Credit)], True)

		self.spreadItems += self.generateLabeledSection('Goals', [x for x in items if isinstance(x,itemPresets.Goal)], True)

		self.spreadItems += self.generateLabeledSection('Expenses', [x for x in items if isinstance(x,itemPresets.Expense)], True)

		for i in range(len(self.spreadItems)):
			# self.spreadItems[i].configure(anchor='w')
			# self.spreadItems[i].pack(expand=True, fill='x')

			self.spreadItems[i].grid(column=0, row=i, sticky='we')
			self.grid_columnconfigure(0, weight=1)
		# #credit accounts
		# 
		# #goals
		# self.generateLabeledSection('Goals', [x for x in items if isinstance(x,itemPresets.Goal)], True).grid(column=1, sticky='nwse')
		# #expenses
		# self.generateLabeledSection('Expenses', [x for x in items if isinstance(x,itemPresets.Expense)], True).grid(column=1, sticky='nwse')
		self.setbg(self, BG_DARK)
		self.refresh()

	def generateRow(self, i, include):
		f = tk.Frame(self, bg=BG_DARK)
		self.entryVar.append({'v': tk.StringVar(), 'include':include})
		self.entryVar[-1]['v'].set(i.bal)
		self.entryVar[-1]['v'].trace_add('write', self.edit)
		tk.Label(f, text=i.label, justify=tk.LEFT, anchor='e').pack(side='left')
		tk.Entry(f, textvariable=self.entryVar[-1]['v'], justify=tk.RIGHT).pack(side='right')
		self.setbg(f, BG_DARK)
		return f

	def generateSectionLabel(self, items, label):
		f = tk.Frame(self)
		tk.Label(f, text=str(sum(i.bal for i in items)), anchor='e').pack(side='right')
		tk.Label(f, text="$", width=0, anchor='e').pack(side='right', expand=True, fill='both')
		tk.Label(f, text='{}:'.format(label), anchor='e').pack(side='right', expand=True, fill='x')
		self.setbg(f, BG_LIGHT)
		return f

	def generateSection(self, items, include):
		wid = []
		for i in items:
			wid.append(self.generateRow(i, include))
		return wid

	def generateLabeledSection(self, label, items, include):
		wid = []
		for i in items:
			wid.append(self.generateRow(i, include))
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
		self.totalVar.set(self.getTotal())

	def getTotal(self):
		tot = 0
		for i in self.entryVar:
			try:
				tot+= float(i['v'].get())# if i.get() != '' else 0
			except ValueError:
				tot += 0
		return tot