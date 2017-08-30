# coding:utf-8
import requests
import json
"""
test api
"""
class SpdClient(object):
    def __init__(self,api_url,username,password):
        self.api_url = api_url
        self.username = username
        self.password = password
        params = {'username': self.username, 'password': self.password}
        data = json.dumps(params)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0","Content-Type": "application/json","Accept": "application/json, text/plain, */*"}
        login_url  = self.api_url+"/auth/signin"
        r = requests.post(login_url,data,headers = headers)
        cookie = r.cookies['connect.sid']
        self.headers = {"Cookie":"connect.sid="+cookie}

    def post_report(self,report):
        post_url = self.api_url+"/api/v1/reports"
        requests.post(post_url,json = report,headers=self.headers)

    def post_results(self,results):
        post_url = self.api_url+"/api/v1/results"
        requests.post(post_url,json = results,headers=self.headers)

    def get_report(self,select_condition):
        get_url = self.api_url+"/api/v1/reports"+select_condition
        report_name = requests.get(get_url,headers=self.headers)
        return report_name.json()

    def get_perfdata(self,select_condition):
        get_url = self.api_url+"/api/v1/perfdata"+select_condition
        perfdata = requests.get(get_url,headers=self.headers)
        return perfdata.json()

    def post_perfdata(self,prefdata):
        post_url = self.api_url+"/api/v1/perfdata"
        requests.post(post_url,json = prefdata,headers=self.headers)

    def get_mondata(self,select_condition):
        get_url = self.api_url+"/mondata/origin"+select_condition
        perfdata = requests.get(get_url)
        return perfdata.json()

    def get_cmdbinfo(self,select=""):
        get_url = self.api_url+"/cfgitems"+select
        perfdata = requests.get(get_url)
        return perfdata.json()
	#return perfdata
    def post_relations(self,data):
        post_url = self.api_url+"/relations"
        requests.post(post_url, json=data, headers=self.headers)

    def post_authorizations(self,data):
        post_url = self.api_url+"/authorizations"
        requests.post(post_url, json=data, headers=self.headers)

    def get_ci_subtype(self, select=""):
        get_url = self.api_url+"/cfgitems?subtype="+select
        perfdata = requests.get(get_url)
        return perfdata.json()
