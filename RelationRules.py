# coding:utf-8
from SpdClient import SpdClient
from objectpath import *

client = SpdClient("http://127.0.0.1:8000", "tpuser", "tpuser123")
server_tree = Tree(client.get_cmdbinfo("?subtype=wls.server"))
domain_tree = Tree(client.get_cmdbinfo("?subtype=wls.domain"))
linux_tree = Tree(client.get_cmdbinfo("?subtype=linux"))

# result = domain_tree.execute("$*[@.name is '10.1.17.127_7001_ilogustest_domain1']")
# print linux_tree.execute("$*")

def server_doamin():
    for server in server_tree.execute("$*"):
        try:
            domain_info = domain_tree.execute("$*[@.name is '{}']".format(server["domainName"])).next()
        except:
            domain_info = None
        if domain_info:
            target = domain_info["_id"]
            source = server["_id"]
            post_lws_relation = {"source":source,
                         "type":"In",
                         "target":target,
                         "index":0,
                         "sysGroups":
                             [source, target]}
            client.post_relations(post_lws_relation)
        try:
            linux_info = linux_tree.execute("$*[@.name is '{}']".format(server["hostName"])).next()
        except:
            linux_info = None
        if linux_info:
            linux_target=linux_info["_id"]
            source = server["_id"]
            post_linux_relation = {"source":source,
                         "type":"In",
                         "target":linux_target,
                         "index":0,
                         "sysGrups":
                             [source,linux_target]}
            client.post_relations(post_linux_relation)

def domain_re_linux():
    for domain in domain_tree.execute("$*"):
        ip_list = domain["hostNames"].split(",")
        for ip in ip_list:
            try:
                linux_info = linux_tree.execute("$*[@.ip is '{}']".format(ip)).next()
            except:
                linux_info = None
            if not linux_info:
                try:
                    linux_info = linux_tree.execute("$*[@.name is '{}']".format(ip)).next()
                except:
                    linux_info = None
            if linux_info:
                source = domain["_id"]
                target = linux_info["_id"]
                post_lws_relation = {"source":source,
                             "type":"In",
                             "target":target,
                             "index":0,
                             "sysGroups":
                                 [source,target]}
                client.post_relations(post_lws_relation)
def ip_relation(localip):
    linux_info = linux_tree.execute("$*[@.ip is '{}']".format(localip)).next()
    server_info = server_tree.execute("$*[@.listenAdress is '{}']".format(localip))
    domain_ip = domain_tree.execute("$*[@.adminAddress is '{}']".format(localip))
    for server in server_info:
        # relation server in domain
        try:
            domain_info = domain_tree.execute("$*[@.name is '{}']".format(server["domainName"])).next()
        except:
            domain_info = None
        if domain_info:
            source = server["_id"]
            target = domain_info["_id"]
            post_lws_relation = {"source": source,
                                 "type": "In",
                                 "target": target,
                                 "index": 0,
                                 "sysGroups":
                                     [source, target]}
            client.post_relations(post_lws_relation)
            # relation server in linux
        linux_target = linux_info["_id"]
        post_linux_relation = {"source": source,
                               "type": "In",
                               "target": linux_target,
                               "index": 0,
                               "sysGrups":
                                   [source, linux_target]}
        client.post_relations(post_linux_relation)
        for domain in domain_ip:
            ip_list = domain["hostNames"].split(",")
            for ip in ip_list:
                try:
                    linux_info = linux_tree.execute("$*[@.ip is '{}']".format(ip)).next()
                except:
                    linux_info = None
                if not linux_info:
                    try:
                        linux_info = linux_tree.execute("$*[@.name is '{}']".format(ip)).next()
                    except:
                        linux_info = None
                if linux_info:
                    source = domain["_id"]
                    target = linux_info["_id"]
                    post_lws_relation = {"source": source,
                                         "type": "In",
                                         "target": target,
                                         "index": 0,
                                         "sysGroups":
                                             [source, target]}
                    client.post_relations(post_lws_relation)

if __name__ == "__main__":
    # domain_re_linux()
    # server_doamin()
    ip_relation("10.1.117.100")
    # ip_list = domain.execute("$.hostName").split(",")

