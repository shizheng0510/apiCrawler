#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pygal
import re
import json
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS
# 执行API调用并存储响应
url = "https://api.github.com/search/repositories?q=language:python&sort=stars&stars:>100&per_page=100&page=1"
r = requests.get(url)
print("Status code:", r.status_code)
# 将API响应存储在一个变量中
response_dict = r.json()
print("Total repositories:", response_dict['total_count'])
# 探索有关仓库的信息
repo_dicts = response_dict['items']
print("Repositories returned:%d\n\n" % len(repo_dicts))
# 将信息打印在文件中
f = open("repo.txt", "w")
i = 1
for repo_dict in repo_dicts:
    if repo_dict['name'] == 'requests':
        pass
    else:
        print('\nNO.', i, file=f)
        i = i+1
        print('Repo_id:', repo_dict['id'], file=f)
        print('Repo_name:', repo_dict['name'], file=f)
        print('Owner:', repo_dict['owner']['login'], file=f)
        print('Owner_id:', repo_dict['owner']['id'], file=f)
        print('Owner_type:', repo_dict['owner']['type'], file=f)
        print('created_at:', repo_dict['created_at'], file=f)
        print('updated_at:', repo_dict['updated_at'], file=f)
		print('size:', repo_dict['size'], file=f)
		print('stargazers_count:', repo_dict['stargazers_count'], file=f)
		print('language:', repo_dict['language'], file=f)
		print('has_issues:', repo_dict['has_issues'], file=f)
		print('has_projects:', repo_dict['has_projects'], file=f)
		print('has_downloads:', repo_dict['has_downloads'], file=f)
		print('has_wiki:', repo_dict['has_wiki'], file=f)
		print('has_pages:', repo_dict['has_pages'], file=f)
		print('forks_count:', repo_dict['forks_count'], file=f)
		print('open_issues_count:', repo_dict['open_issues_count'], file=f)
		f.flush()
f.close()