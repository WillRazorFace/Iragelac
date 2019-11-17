#!/usr/bin/python3

# Developed by WillRazorFace
# Contact - willrazorface90s@gmail.com
# Coding - utf-8

# Usage - python3.x iragelac.py -u [URL] -w [WORDLIST] -o [OUTPUT] -i [INTERVAL (MUST BE INTEGER)] --headers [PARAM1]: [VALUE1] [PARAM2]: [VALUE2] ...

from argparse import ArgumentParser
from termcolor import colored
from bs4 import BeautifulSoup
from requests import get
from re import findall
from datetime import datetime
from socket import gethostbyname
from io import StringIO
from os.path import isfile
from time import sleep

def emailfinder(html:str):
	fndemail = []
	emails = findall(r'[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]@[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]', 
					 html)
	if emails:
		for email in emails:
			if email in fndemail:
				continue
			print('	', colored('[+]', 'green'), email)
			fndemail.append(email)
		return fndemail
	else:
		print('	', colored('[-]', 'red'), 'No email found', colored('[-]', 'red'))


def linkfinder(html:str):
	fndlink = []
	links = findall('(?<=href=["\'])https?://.+?(?=["\'])', html)
	if links:
		for link in links:
			if link in fndlink:
				continue
			print('	', colored('[+]', 'green'), link)
			fndlink.append(link)
		return fndlink
	else:
		print('	', colored('[-]', 'red'), 'No link found', colored('[-]', 'red'))


def whois(urlink:str):
	wi = ''
	whoreq = get('https://www.whois.com/whois/{}'.format(urlink))
	if whoreq.status_code == 200:
		wi = ''
		wip = ''
		wiret = ''
		bs = BeautifulSoup(whoreq.text, 'html.parser')
		data = bs.find_all('pre', {'class':'df-raw'})
		for info in data:
			wi = wi + info.get_text()
		for line in StringIO(wi):
			if '%' not in line and ':' in line:
				wip = wip + colored('[+]','green') + line
				wiret = wiret + line
		wip = '	 '+wip.replace('\n', '\n	 ')
		wiret = '	'+wiret.replace('\n', '\n	')
		print(wip)
		return wiret
	else:
		print('	', colored('[-]', 'red'), 'No information found on WhoIS',colored('[-]', 'red'))


def crawler(wordlist:str, urlink:str, time: int):
	if isfile(wordlist) is True:
		with open(wordlist) as f:
			urls = f.readlines()
		urlok = 0
		urlforb = 0
		fndurls = []
		for url in urls:
			crawled = urlink+'/'+url.strip('\n')
			try:
				vrfy = get(crawled)
				sleep(time)
			except:
				continue
			if vrfy.status_code == 200:
				print('	', colored('[+]', 'green'), crawled)
				urlok += 1
				fndurls.append(crawled)
			elif vrfy.status_code == 403:
				print('	', colored('[!]', 'yellow'), crawled)
				urlforb += 1
				fndurls.append(crawled)
		if urlok or urlforb:
			print('\n')
			print('	CRAWLED', colored(urlok+urlforb, 'blue'), 'URL')
			print('	',colored(urlok, 'green'), 'OK CODE')
			print('	',colored(urlforb, 'yellow'), 'FORBIDDEN CODE','\n')
			return fndurls
		else:
			print('	', colored('[-]', 'red'), 'No URL crawled', colored('[-]', 'red'), '\n')
	else:
		print('	', colored('[-]','red'), 'The path entered for a wordlist is invalid. Check it out.',colored('[-]','red'))


iragelac = """ ___ ____      _    ____ _____ _        _    ____ 
|_ _|  _ \    / \  / ___| ____| |      / \  / ___|
 | || |_) |  / _ \| |  _|  _| | |     / _ \| |    
 | ||  _ <  / ___ \ |_| | |___| |___ / ___ \ |___ 
|___|_| \_\/_/   \_\____|_____|_____/_/   \_\____|
"""

ap = ArgumentParser(description="Iragelac Script")
ap.add_argument('-u', '--url', help='URL to the site', required=True)
ap.add_argument('-o', '--output', help='Output file')
ap.add_argument('-w', '--wordlist', help='Path to cralwing wordlist')
ap.add_argument('--headers', help='Headers for the request', nargs='*')
ap.add_argument('-i', '--interval',
                help='Interval between requests (available if there is a word list to crawling) default - 0',
                type=int, default=0)
args = vars(ap.parse_args())

url = args['url']
output = args['output']
wordlist = args['wordlist']
headlist = args['headers']
interval = args['interval']
headers = []
if headlist:
    for i in headlist:
        headers.append(i.replace(':', ''))
    headers = {headers[i]: headers[i+1] for i in range(0, len(headers), 2)}

try:
	req = get(url, headers=headers)
except requests.exceptions.Timeout:
	print('\n', colored('[-]', 'red'), 'Timeout', colored('[-]','red'), '\n')
	exit(1)
except requests.exceptions.ConnectionError:
	print('\n', colored('[-]','red'), 'Connection to site failed', colored('[-]','red'), '\n')
	exit(1)
except requests.exceptions.MissingSchema:
	print('\n', colored('[-]', 'red'), 'Unrecognized URL schema. Specify "http://" or "https://"', colored('[-]','red'), '\n')
	exit(1)

ip = gethostbyname(url.strip('https://'))
localtime = datetime.now().strftime('%H:%M:%S')
server = req.headers['Server']

print(iragelac)

print('\n', colored('Host:', 'blue'), url, 
			colored('Host IP:', 'blue'), ip, 
			colored('Local Time:', 'blue'), localtime, 
			colored('Host Server:','blue'), server, 
			'\n')

print(colored('___________________________________________________________', 'red', 'on_red'))
print(colored('ᴇᴍᴀɪʟ ғɪɴᴅᴇʀ                                               ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
emails = emailfinder(req.text)

print('\n')
print(colored('___________________________________________________________', 'red', 'on_red'))
print(colored('ʟɪɴᴋ ғɪɴᴅᴇʀ                                                ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
links = linkfinder(req.text)

print('\n')
print(colored('___________________________________________________________', 'red','on_red'))
print(colored('ᴡʜᴏɪs                                                      ', 'white', 'on_red'))
print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
who = whois(url)

if wordlist:
	print(colored('___________________________________________________________', 'red','on_red'))
	print(colored('ᴜʀʟ ᴄʀᴀᴡʟᴇʀ                                                ', 'white', 'on_red'))
	print(colored('___________________________________________________________', 'red', 'on_red'), '\n')
	urls = crawler(wordlist, url, interval)

if output:
	date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
	try:
		with open(output, 'w') as f:
			f.write(iragelac+'\n')
			f.write('Date: '+date+
					' Host: '+url+
					' Host IP: '+ip+
					' Host Server: '+server+
					'\n\n')
			f.write('ᴇᴍᴀɪʟ ғɪɴᴅᴇʀ\n')
			if emails:
				for email in emails:
					f.write('	'+email)
					f.write('\n')
			else:
				f.write('	No email found\n')
			f.write('\nʟɪɴᴋ ғɪɴᴅᴇʀ\n')
			if links:
				for link in links:
					f.write('	'+link)
					f.write('\n')
			else:
				f.write('	No link found\n')
			if who:
				f.write('\nᴡʜᴏɪs\n')
				f.write(who.strip('[+]'))
			else:
				f.write('	No information found on WhoIS')
			if urls:
				f.write('\nᴜʀʟ ᴄʀᴀᴡʟᴇʀ\n')
				for url in urls:
					f.write('	'+url)
					f.write('\n')
	except FileNotFoundError:
		print(colored('[-]', 'red'), 
					'The path you entered is not valid for writing a file.', 
			  colored('[-]', 'red'))

localtime = datetime.now().strftime('%H:%M:%S')
print(colored('Closing at','blue'), localtime, '\n')
