# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

from urllib.request import urlopen
import json

class RepoInfo:
	def __init__(self,repo_name,repo_owner,repo_template='https://api.github.com/repos/{owner}/{repo}'):
		self.repo_name=repo_name
		self.repo_owner=repo_owner
		self.repo_template=repo_template
	def getCommits(self):
		data=urlopen(self.repo_template.format(repo=self.repo_name,owner=self.repo_owner)+'/commits').read()
		data_hesh=json.loads(data.decode())
		commits={i['sha']:i['commit']['message'] for i in data_hesh}
		return commits
	def getCommit(self,sha):
		data=urlopen(self.repo_template.format(repo=self.repo_name,owner=self.repo_owner)+'/commits/'+str(sha)).read()
		data_hesh=json.loads(data.decode())
		commit=(data_hesh['sha'],data_hesh['commit']['message'])
		return commit
	def getTags(self):
		data=urlopen(self.repo_template.format(repo=self.repo_name,owner=self.repo_owner)+'/tags').read()
		data_hesh=json.loads(data.decode())
		commits={i['name']:self.getCommit(i['commit']['sha'])[1] for i in data_hesh}
		return commits

def main():
	r=RepoInfo('test','GBHt')
	print(r.getCommits())
	print(r.getTags())

if __name__=='__main__':
	main()
