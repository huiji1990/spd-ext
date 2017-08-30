# coding:utf-8
import json
from SpdClient import SpdClient

class RelationBuilder(object):
    def __init__(self, client, data_load_method="spd"):
        self.client = client
        # the way loading data(spd, file, json)
        self.method = data_load_method

    def get_field(self, ci, filed):
        data = json.dumps(ci)
        data = json.loads(data)
        return data[filed]

    def post_format(self, source, target, type):
        relation_post = {"source": self.get_field(source, "_id"),
                         "type": type,
                         "target": self.get_field(target, "_id"),
                         "index": 0,
                         "sysGroups": [self.get_field(source, "_id"), self.get_field(target, "_id")]}
        return relation_post

    def link(self, source, target, relation_con_func):
        def json_json(source, target):
            if relation_con_func(source, target):
                post = self.post_format(source, target, relation_con_func(source, target))
                # client.post_relations(post)
                print post

        def tree_tree(source, target):
            for s in list(source):
                for t in list(target):
                    if relation_con_func(s, t):
                        post = self.post_format(s, t, relation_con_func(s, t))
                        # client.post_relations(post)
                        print post
        if self.method == "json":
            return json_json(source, target)
        elif self.method == "spd":
            source = self.client.get_ci_subtype(source)
            target = self.client.get_ci_subtype(target)
            return tree_tree(source, target)
        elif self.method == "file":
            with open(source) as f:
                source = json.load(f)
            with open(target) as f:
                target = json.load(f)
            return tree_tree(source, target)

    def create_conn_by_fieldname_func(self, sfield, tfield, type):
        def conn_by_fieldname(source, target):
            result = None
            if self.get_field(source, sfield) == self.get_field(target, tfield):
                result = type
            return result
        return conn_by_fieldname

if __name__ == '__main__':
    client = SpdClient("http://127.0.0.1:8000", "tpuser", "tpuser123")
    builder = RelationBuilder(client, "file")
    builder.link("linuxci", "domainci", builder.create_conn_by_fieldname_func("ip", "adminAddress", "has"))
