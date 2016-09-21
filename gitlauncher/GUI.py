# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import tkinter
import tkinter.scrolledtext
import git_info_loader as gil

class VersionSelecterFrame(tkinter.Toplevel):
	def __init__(self,repo_name,repo_owner,callback,parent=None):
		tkinter.Toplevel.__init__(self,parent)
		
		self.gil=gil.RepoInfo(repo_name,repo_owner)
		self.ver_list={}
		self.callback=callback
		
		fr1=tkinter.Frame(self)
		fr2=tkinter.Frame(self)
		sb=tkinter.Scrollbar(fr1)
		self.vl=tkinter.Listbox(fr1,yscrollcommand=sb.set)
		self.vl.bind('<Button-1>',lambda *x:self.after(500,self.verUpdate))
		sb.config(command=self.vl.yview)
		self.vl.pack(side=tkinter.LEFT,fill=tkinter.Y)
		sb.pack(side=tkinter.LEFT,fill=tkinter.Y)
		self.desc=tkinter.scrolledtext.ScrolledText(fr1,width=30,height=10)
		self.desc.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
		
		
		self.vs=tkinter.IntVar(value=0)
		self._vs_old=0
		bts=[tkinter.Radiobutton(fr2,text=e,variable=self.vs,value=i) for i,e in enumerate(['master','tags','commits'])]
		for b in bts:
			b.pack(side=tkinter.LEFT)
			b.bind('<Button-1>',lambda *x:self.after(500,self.typeUpdate))
		tkinter.Button(fr2,text='select',command=self.ok).pack(side=tkinter.LEFT,fill=tkinter.X)
		tkinter.Button(fr2,text='cancel',command=self.cnl).pack(side=tkinter.LEFT,fill=tkinter.X)
		fr1.pack(side=tkinter.TOP)
		self.status_label=tkinter.Label(self,text='')
		self.status_label.pack(side=tkinter.LEFT)
		fr2.pack(side=tkinter.RIGHT)
	def ok(self):
		try:
			self.callback(self.vl.get(tkinter.ACTIVE),self.ver_list[self.vl.get(tkinter.ACTIVE)])
		except KeyError:
			self.callback(None,None)
		self.destroy()
	def cnl(self):
		self.callback(None,None)
		self.destroy()
	def loadVerToList(self):
		self.vl.delete(0,tkinter.END)
		self.vl.insert(0,*self.ver_list.keys())
		self.vl.update()
	def loadDesc(self,desc):
		self.desc.delete('1.0',tkinter.END)
		self.desc.insert('1.0',desc)
		self.update()
	def typeUpdate(self):
		ct=self.vs.get()
		if ct!=self._vs_old:
			self.status_label.config(text='loading')
			self.status_label.update()
			self._vs_old=ct
			if ct==1:
				self.ver_list=self.gil.getTags()
			elif ct==2:
				self.ver_list=self.gil.getCommits()
			self.loadVerToList()
			self.status_label.config(text='')
			self.status_label.update()
	def verUpdate(self):
		self.loadDesc(self.ver_list[self.vl.get(tkinter.ACTIVE)])

def main():
	f=VersionSelecterFrame('test','GBH007',print)
	tkinter.mainloop()

if __name__=='__main__':
	main()
