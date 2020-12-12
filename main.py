import tkinter as tk
from profile import Profile
from items import *
import ui
import pickle

SAVE_LOC = './profiles/'
PROFILE_EXT = '.bbp' 

class BudgetBuddy:
	def __init__(self, gui):
		self.gui = gui
		self.gui.title("BudgetBuddy")
		self.p = self.loadProfile('user')
		self.summ = ui.Summary(self.gui, 'Summary', self.p.items, self.addItem)
		self.summ.pack(expand='true', fill='x')

		self.saveProfile(self.p)

	def addItem(self):
		print(self.summ.e_newLabel.get() + ': ' + self.summ.e_newBal.get())

	def saveProfile(self, profile):
		pickle.dump(profile, open(SAVE_LOC + profile.username + PROFILE_EXT, 'wb'))

	def loadProfile(self, username):
		return pickle.load(open(SAVE_LOC + username + PROFILE_EXT, 'rb'))
		

def main():
	root = tk.Tk()
	bb = BudgetBuddy(root)
	root.mainloop()

main()