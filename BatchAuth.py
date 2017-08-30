# coding=utf-8
from SpdClient import SpdClient
import xlrd
import pymongo

client = SpdClient("http://127.0.0.1:8000", "tpuser", "tpuser123")
mongoclient = pymongo.MongoClient("mongodb://shepherd:Eproe123@localhost/shepherd")
db = mongoclient.shepherd

def main():
    xls_data = xlrd.open_workbook('ExportFile.xlsx')
    user_dict = {}
    table = xls_data.sheets()[0]
    for i in range(table.nrows):
        if table.cell(i, 2).value != u'运维负责人' and table.cell(i, 2).value != '':
            try:
                user_dict[table.cell(i, 2).value].append(table.cell(i, 0).value)
            except:
                user_dict[table.cell(i, 2).value] = []
    for key in user_dict:
        sys_list = []
        for sys in user_dict[key]:
            sys_list.append(add_auth_group(sys))
        post_auth = {
            "username": get_username(key),
            "authorizationGroup": sys_list
        }
        print post_auth

def add_auth_group(sysname):
    auth_group = {
        "sysGroup": get_sysid(sysname),
        "operoles": [
            get_operid("admin")
        ]
    }
    return auth_group

def get_sysid(sysname):
    item = db.sysgroups.find({'name': sysname})[0]
    return str(item['_id'])

def get_operid(operrole):
    item = db.operroles.find({'name': operrole})[0]
    return str(item['_id'])

def get_username(displayname):
    if displayname == u"姚雷":
        username = "ian"
    # item = db.users.find({'username': username})[0]
    return username

if __name__ == '__main__':
    main()