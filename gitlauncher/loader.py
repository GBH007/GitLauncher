# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import os
from urllib.request import urlopen
import zipfile

class Loader:
	def __init__(self,repository_template='https://github.com/GBH007/{0}/archive/{1}.zip',load_dir='/home/gbh007/Dropbox/projects/ProjectGitLauncher',default_tmp_file='tmp.zip'):
		self.repository_template=repository_template
		self.load_dir=load_dir
		self.default_tmp_file=default_tmp_file
	def _fullTmpPath(self):
		return os.path.join(self.load_dir,self.default_tmp_file)
	def load(self,repo_name,branch_name):
		data=urlopen(self.repository_template.format(repo_name,branch_name)).read()
		f=open(self._fullTmpPath(),'wb')
		f.write(data)
		f.close()
	def decompress(self,alternative_name=None):
		zf=zipfile.ZipFile(self._fullTmpPath(),'r')
		zf.extractall(path=self.load_dir)
		if alternative_name:
			dn=zf.namelist()[0][:-1]
			os.rename(os.path.join(self.load_dir,dn),os.path.join(self.load_dir,alternative_name))
		zf.close()
	def clear(self):
		os.remove(self._fullTmpPath())

def main():
	l=Loader()
	l.decompress('opa')
	l.clear()
	#~ l.load('GMat','b89f98467a45c0b3dbfc1d8222df743968fce6a6')
	#~ l.load('GMat','master')

if __name__=='__main__':
	main()
