#!/usr/bin/env python

import socket

def check_server(address,port):
    s=socket.socket()
    try:
        s.connect((address,port))
        return True
    except socket.error,e:
        return False

if __name__=='__main__':
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option("-a","--address",dest="address",default='localhost',help="Address for server",metavar="ADDRESS")
    parser.add_option("-s","--start",dest="start_port",type="int",default=1,help="start port",metavar="SPORT")
    parser.add_option("-e","--end",dest="end_port",type="int",default=1,help="end port",metavar="EPORT")
    (options,args)=parser.parse_args()
    print 'options: %s, args: %s' % (options, args)
    port=options.start_port
    while(port<=options.end_port):
        check = check_server(options.address, port)
        if (check):
            print 'Port  %s is on' % port
        port=port+1
        
        
