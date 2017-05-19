# Author: Harold Clark
# Copyright Harold Clark 2017
#

class controller(object):
    def __init__(self, ip, name='Not Defined', port=8888):
        self.ip = ip
        self.name = name
        self.port = port
        self.validComandList = []