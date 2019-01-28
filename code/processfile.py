import requests
import re
import json

repo_num = 578#爬取的项目编号
start_repo_num = 578#爬取的项目起始编号
end_repo_num = 1000#爬取的项目终结编号
langu="Ruby"
file_num = 1#保存的文件编号
i = 1 #项目个数编号
langu = "Ruby"
handle_list = [404, 403, 401,500] #如果返回这个列表中的状态码，爬虫也不会终止（该程序会让其终止）
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token 1b2e684d82367defd6a257c8bb9f27e0e4be6a4a'
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token 9b81e79d19dab66b129bb93f893b6f26f5a621f5'
}
headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token 8dbebb8c8b0f0d4cb2216634f76edc35e10c4605'
}
headers4 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token a4340f187b9b28de82eac78594951334d006a084'
}
headers5 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token e3e542bebc96d52e447f153d4ccd942fe4dee8e7'
}
headers6 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'application/vnd.github.v3.star+json',
    'Accept-Language': 'en',
    'Authorization': 'token f0f1147d70df77018989579552b83e616a9286c0'
}

f_in = open("full_name_"+langu+".txt","r")             # 返回一个文件对象
record = open("recode_"+langu+".txt","w")

for repo_num in range(start_repo_num, end_repo_num):
    line = f_in.readline()  # 调用文件的 readline()方法
    st = line.replace('\n', '')#获取项目全名
    print("__repo_num", repo_num)
    page_num = 1
    f_out = open("star_inf_" + langu + "_" + str(repo_num) + ".txt", "w")
    while 1:
        url = "https://api.github.com/repos/"+st+"/stargazers?per_page=100&page=" + str(page_num)
        if page_num%3 == 1:
            r = requests.get(url, headers=headers1)
        elif page_num%3 == 2:
            r = requests.get(url, headers=headers2)
        elif page_num%3 == 3:
            r = requests.get(url, headers=headers3)
        elif page_num%3 == 4:
            r = requests.get(url, headers=headers4)
        elif page_num%3 == 5:
            r = requests.get(url, headers=headers5)
        else:
            r = requests.get(url, headers=headers6)
        print("Status code:", r.status_code)
        print("page_num", page_num)
        if r.status_code != 200:
            print(st, " page_num: ", page_num, file=record)
            record.flush()
            break
        if page_num >11:
            print(repo_num, st, " page_num: ", page_num, file=record)
            record.flush()
            break;
        # 将API响应存储在一个变量中
        repo_dicts = r.json()
        # 将信息打印在文件中
        for repo_dict in repo_dicts:
            print("user: ", repo_dict['user']['login'], file=f_out)
            print("starred_at: ", repo_dict['starred_at'], file=f_out)
            f_out.flush()
        page_num = page_num + 1
    f_out.close()
f_in.close()
record.close()