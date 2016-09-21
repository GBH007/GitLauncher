# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import tkinter
import tkinter.scrolledtext
import gitlauncher.git_info_loader as gil
import gitlauncher.loader as loader
import json
import os
import subprocess

class VersionSelecterFrame(tkinter.Toplevel):
	def __init__(self,repo_name,repo_owner,callback,parent=None):
		tkinter.Toplevel.__init__(self,parent)
		self.title('version selecter')
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
		if self.vs.get():
			try:
				self.callback(self.vl.get(tkinter.ACTIVE),self.ver_list[self.vl.get(tkinter.ACTIVE)])
			except KeyError:
				self.callback(None,None)
		else:
			self.callback('master','last version')
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

class GUISettingMenu(tkinter.Toplevel):
	def __init__(self,settings,parent=None):
		tkinter.Toplevel.__init__(self,parent)
		self.title('setting')
		self.settings=settings
		
		tkinter.Label(self,text='launch_command').pack(fill=tkinter.X)
		self.lc=tkinter.StringVar(value=settings.get('launch_command','{path}/run.sh'))
		tkinter.Entry(self,textvariable=self.lc).pack(fill=tkinter.X)
		tkinter.Label(self,text='repo_owner').pack(fill=tkinter.X)
		self.ro=tkinter.StringVar(value=settings.get('repo_owner','GBH007'))
		tkinter.Entry(self,textvariable=self.ro).pack(fill=tkinter.X)
		tkinter.Label(self,text='repo').pack(fill=tkinter.X)
		self.rp=tkinter.StringVar(value=settings.get('repo','test'))
		tkinter.Entry(self,textvariable=self.rp).pack(fill=tkinter.X)
		
		tkinter.Button(self,text='ok',command=self.ok).pack(fill=tkinter.X,side=tkinter.LEFT,expand=tkinter.YES)
		tkinter.Button(self,text='cancel',command=self.cnl).pack(fill=tkinter.X,side=tkinter.RIGHT,expand=tkinter.YES)
	def ok(self):
		self.settings['launch_command']=self.lc.get()
		self.settings['repo_owner']=self.ro.get()
		self.settings['repo']=self.rp.get()
		self.destroy()
	def cnl(self):
		self.destroy()
		
class MainWindow(tkinter.Tk):
	def __init__(self,load_dir='/home/gbh007/Dropbox/projects/ProjectGitLauncher'):
		tkinter.Tk.__init__(self)
		try:
			self.settings=json.load(open('cfg.cfg'))
		except (FileNotFoundError,json.decoder.JSONDecodeError):
			self.settings={
				'repo':'tfgl',
				'repo_owner':'GBH007',
				'launch_command':'sh {path}/run.sh',
				'last_branch':'master',
				'last_desc':'123123',
			}
		self.load_dir=load_dir
		fr1=tkinter.Frame(self)
		self.vl=tkinter.Label(fr1,text='')
		self.vl.pack(fill=tkinter.X,side=tkinter.TOP)
		tkinter.Button(fr1,text='version select',command=self.versionSelect).pack(fill=tkinter.X,side=tkinter.TOP)
		tkinter.Button(fr1,text='settings',command=self.setSetting).pack(fill=tkinter.X,side=tkinter.TOP)
		self.lob=tkinter.Button(fr1,text='load',command=self.load)
		self.lob.pack(fill=tkinter.X,side=tkinter.TOP)
		self.lab=tkinter.Button(fr1,text='launch',command=self.launch)
		self.lab.pack(fill=tkinter.X,side=tkinter.TOP)
		tkinter.Button(fr1,text='exit',command=self.destructor).pack(fill=tkinter.X,side=tkinter.TOP)
		
		self.desc=tkinter.scrolledtext.ScrolledText(self,width=30,height=10)
		self.desc.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
		fr1.pack(side=tkinter.RIGHT)
		self.loadDesc(self.settings['last_branch'],self.settings['last_desc'])
		
	def callback(self,branch,desc):
		if branch:
			self.settings['last_branch']=branch
			self.settings['last_desc']=desc
			self.loadDesc(branch,desc)
	def load(self):
		#~ fd=os.path.join(self.load_dir,'{0}-{1}'.format(self.settings['repo'],self.settings['last_branch']))
		#~ if os.path.exists(fd):
			#~ os.remove(fd)
		lr=loader.Loader(
			load_dir=self.load_dir,
			repo_owner=self.settings['repo_owner']
		)
		lr.load(self.settings['repo'],self.settings['last_branch'])
		lr.decompress(self.settings['repo']+'-'+self.settings['last_branch'])
		lr.clear()
		self.reloadButton()
	def launch(self):
		fd=os.path.join(self.load_dir,'{0}-{1}'.format(self.settings['repo'],self.settings['last_branch']))
		if os.path.exists(fd):
			self.withdraw()
			self.update()
			#~ subprocess.call(self.settings['launch_command'].format(path=fd))
			os.system(self.settings['launch_command'].format(path=fd))
			self.deiconify()
			self.update()
		else:
			self.load()
			self.reloadButton()
			self.after(500,self.launch)
	def versionSelect(self):
		VersionSelecterFrame(self.settings['repo'],self.settings['repo_owner'],self.callback,self)
	def setSetting(self):
		#~ self.withdraw()
		#~ self.update()
		GUISettingMenu(self.settings,self)
		#~ self.deiconify()
		#~ self.update()
	def loadDesc(self,ver,desc):
		self.desc.delete('1.0',tkinter.END)
		self.desc.insert('1.0',desc)
		self.vl.config(text='version:\n{0}'.format(ver))
		self.reloadButton()
	def reloadButton(self):
		if os.path.exists(os.path.join(self.load_dir,'{0}-{1}'.format(self.settings['repo'],self.settings['last_branch']))):
			self.lob.config(text='reload')
			self.lab.config(text='launch')
		else:
			self.lob.config(text='load')
			self.lab.config(text='load&launch')
		self.update()
	def destructor(self):
		json.dump(self.settings,open('cfg.cfg','w'))
		self.destroy()

def main():
	#~ f=VersionSelecterFrame('test','GBH007',print)
	#~ GUISettingMenu({})
	#~ tkinter.mainloop()
	root=MainWindow()
	root.mainloop()

if __name__=='__main__':
	main()
