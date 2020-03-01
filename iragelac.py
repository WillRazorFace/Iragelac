#!/usr/bin/python3

# Developed by WillRazorFace
# Contact - willrazorface90s@gmail.com
# Coding - utf-8

# Usage - python3.x iragelac.py -u [URL] -w [WORDLIST] -o [OUTPUT] -i [INTERVAL (MUST BE INTEGER)] --cookies COOKIE1: value1 COOKIE2: value2 ... --headers PARAM1: value1 PARAM2: value2 ...

from argparse import ArgumentParser
from scanner import Iragelac
from termcolor import colored
from socket import gethostbyname
from datetime import datetime

ap = ArgumentParser(description="Iragelac Script")
ap.add_argument('-u', '--url', help='URL to the site', required=True, type=str)
ap.add_argument('-o', '--output', help='Output file', type=str)
ap.add_argument('-w', '--wordlist', help='Path to cralwing wordlist', type=str)
ap.add_argument('--headers', help='Headers File for the request', type=str)
ap.add_argument('-i', '--interval',
                help='Interval between requests (available if there is a word list to crawling) default - 0',
                type=int, default=0)
args = vars(ap.parse_args())

URL = args['url']
OUTPUT = args['output']
WORDLIST = args['wordlist']
HEADERSFILE = args['headers']
INTERVAL = args['interval']

iragelac = Iragelac(URL, OUTPUT, WORDLIST, HEADERSFILE, INTERVAL)
if HEADERSFILE:
    iragelac.headers, iragelac.cookies = iragelac.parse_headers(HEADERSFILE)

iragelac.check_conn()
ip = gethostbyname(URL.strip('https://'))
localtime = datetime.now().strftime('%H:%M:%S')
server = iragelac.req.headers['Server']

print(iragelac.banner)
print('\n', colored('Host:', 'blue'), URL,
            colored('Host IP:', 'blue'), ip,
            colored('Local Time:', 'blue'), localtime,
            colored('Host Server:', 'blue'), server,
      '\n')

print(colored('___________________________________________________________', 'red', 'on_red'))
print(colored('ᴇᴍᴀɪʟ ғɪɴᴅᴇʀ                                               ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
emails = iragelac.find_emails()

print('\n')
print(colored('___________________________________________________________', 'red', 'on_red'))
print(colored('ʟɪɴᴋ ғɪɴᴅᴇʀ                                                ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
links = iragelac.find_links()

print('\n')
print(colored('___________________________________________________________', 'red','on_red'))
print(colored('ᴡʜᴏɪs                                                      ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
who = iragelac.whois_check()

if WORDLIST:
	print(colored('___________________________________________________________', 'red','on_red'))
	print(colored('ᴜʀʟ ᴄʀᴀᴡʟᴇʀ                                                ', 'white', 'on_red'))
	print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
	urls = iragelac.crawler()

if OUTPUT:
	iragelac.save_output()

localtime = datetime.now().strftime('%H:%M:%S')
print(colored('Closing at','blue'), localtime)
