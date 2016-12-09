from tornado import ioloop
from facebook import GraphAPI

access_token = 'EAACEdEose0cBAIvLN5egpSmBPbxTcbxNiHFstyipxkiw0EoM3n5i8xuE6YgiGpplBlabvRUck4w8sYZCfYmhbTxuKfPwzRdZBQkk2hZBQz2PvVHCtoZCCbg7bv2CLtCddhLoSesTgFl2DZClA4I2qrzFf1PcLZBfWZAzjmvQYZAlVgZDZD'
ioloop = ioloop.IOLoop.instance()
graph = GraphAPI(access_token)

# a simple callback that prints social graph responses
def print_callback(data):
    print data
    ioloop.stop()

#do something with the user's data, like print it's first name
def get_first_name(me):
    print me['name']
    ioloop.stop()

# graph.get_object('/me', callback=print_callback)
result = graph.get_object('/v2.8/me', callback=get_first_name)

ioloop.start()
