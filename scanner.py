from argparse import ArgumentParser
from termcolor import colored
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import Timeout, ConnectionError, MissingSchema
from re import findall
from socket import gethostbyname
from io import StringIO
from os.path import isfile
from time import sleep
from datetime import datetime


class Iragelac:
	def __init__(self, url: str, output: str, wordlist: str, headlist: str,
				 interval: int):
		self.url = url
		self.output = output
		self.wordlist = wordlist
		self.interval = interval
		self.headers = {}
		self.cookies = {}
		self.banner = r"""
		 ___________  ___  _____  _____ _       ___  _____
		|_   _| ___ \/ _ \|  __ \|  ___| |     / _ \/  __ \
		  | | | |_/ / /_\ \ |  \/| |__ | |    / /_\ \ /  \/
		  | | |    /|  _  | | __ |  __|| |    |  _  | |
		 _| |_| |\ \| | | | |_\ \| |___| |____| | | | \__/\
		 \___/\_| \_\_| |_/\____/\____/\_____/\_| |_/\____/
		"""

	def check_conn(self) -> None:
		try:
			self.req = get(self.url, headers=self.headers, cookies=self.cookies)
		except Timeout:
			print('\n', colored('[-]', 'red'), 'Timeout', colored('[-]','red'), '\n')
			exit(1)
		except ConnectionError:
			print('\n', colored('[-]','red'), 'Connection to site failed', colored('[-]','red'), '\n')
			exit(1)
		except MissingSchema:
			print('\n', colored('[-]', 'red'),
		  		  'Unrecognized URL schema. Specify "http://" or "https://"', colored('[-]','red'),
		  		  '\n')
			exit(1)

	def find_emails(self) -> list:
		self.fndemails = []
		emails = findall(r'[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]@[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]',
					 	 self.req.text)
		if emails:
			for email in emails:
				if email in self.fndemails:
					continue
				print('	', colored('[+]', 'green'), email)
				self.fndemails.append(email)
			return self.fndemails
		else:
			print('	', colored('[-]', 'red'), 'No email found', colored('[-]', 'red'))

	def find_links(self) -> list:
		self.fndlinks = []
		links = findall('(?<=href=["\'])https?://.+?(?=["\'])', self.req.text)
		if links:
			for link in links:
				if link in self.fndlinks:
					continue
				print('	', colored('[+]', 'green'), link)
				self.fndlinks.append(link)
			return self.fndlinks
		else:
			print('	', colored('[-]', 'red'), 'No link found', colored('[-]', 'red'))

	def whois_check(self) -> str:
		whoreq = get('https://www.whois.com/whois/{}'.format(self.url))
		if whoreq.status_code == 200:
			wi = ''
			wip = ''
			self.wiret = ''
			bs = BeautifulSoup(whoreq.text, 'html.parser')
			data = bs.find_all('pre', {'class':'df-raw'})
			for info in data:
				wi = wi + info.get_text()
			for line in StringIO(wi):
				if '%' not in line and ':' in line:
					wip = wip + colored('[+]','green') + line
					self.wiret = self.wiret + line
			wip = '	 ' + wip.replace('\n', '\n	 ')
			self.wiret = '	' + self.wiret.replace('\n', '\n	')
			print(wip)
			return self.wiret
		else:
			print('	', colored('[-]', 'red'), 'No information found on WhoIS',colored('[-]', 'red'))

	def crawler(self) -> list:
		if isfile(self.wordlist) is True:
			with open(self.wordlist) as f:
				urls = f.readlines()
			urlok = 0
			urlforb = 0
			self.fndurls = []
			for url in urls:
				crawled = self.url + '/' + url.strip('\n')
				try:
					vrfy = get(crawled, headers=self.headers, cookies=self.cookies)
					sleep(time)
				except:
					continue
				if vrfy.status_code == 200:
					print('	', colored('[+]', 'green'), crawled)
					urlok += 1
					self.fndurls.append(crawled)
				elif vrfy.status_code == 403:
					print('	', colored('[!]', 'yellow'), crawled)
					urlforb += 1
					self.fndurls.append(crawled)
			if urlok or urlforb:
				print('\n')
				print('	CRAWLED', colored(urlok + urlforb, 'blue'), 'URL')
				print('	', colored(urlok, 'green'), 'OK CODE')
				print('	', colored(urlforb, 'yellow'), 'FORBIDDEN CODE', '\n')
				return self.fndurls
			else:
				print('	', colored('[-]', 'red'), 'No URL crawled', colored('[-]', 'red'), '\n')
		else:
			print('	', colored('[-]', 'red'),
			  	  'The path entered for a wordlist is invalid. Check it out.',
			  	  colored('[-]', 'red'))

	def save_output(self) -> None:
		date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		ip = gethostbyname(self.url.strip('https://'))
		server = server = self.req.headers['Server']
		try:
			with open(self.output, 'w') as f:
				f.write(self.banner + '\n')
				f.write('Date: ' + date +
						' Host: ' + self.url +
						' Host IP: ' + ip +
						' Host Server: ' + server +
						'\n\n')
				f.write('EMAIL FINDER\n')
				if self.fndemails:
					for email in self.fndemails:
						f.write('	' + email)
						f.write('\n')
				else:
					f.write('	No email found\n')
					f.write('\nLINK FINDER\n')
				if self.fndlinks:
					for link in self.fndlinks:
						f.write('	' + link)
						f.write('\n')
				else:
					f.write('	No link found\n')
				if self.wiret:
					f.write('\nWHOIS\n')
					f.write(self.wiret.strip('[+]'))
				else:
					f.write('	No information found on WhoIS')
				if self.fndurls:
					f.write('\nURL CRAWLER\n')
					for url in self.fndurls:
						f.write('	' + url)
						f.write('\n')
		except FileNotFoundError:
			print(colored('[-]', 'red'),
						  'The path you entered is not valid for writing a file.',
			  	  colored('[-]', 'red'))

	def parse_headers(self, file: str, headers={}, cookies={}) -> tuple:
		with open(file, 'r') as f:
			headerspt = f.read().splitlines()
			if 'GET' or 'POST' in headerspt[0]:
				headerspt.remove(headerspt[0])
			for i in headerspt:
				i = i.split(':')
				i[1] = i[1].replace(' ', '', 1)
				headers[i[0]] = i[1]
			if headers['Cookie'] or headers['cookie']:
				cookiespt = headers['Cookie']
				try:
					del(headers['Cookie'])
				except KeyError:
					del(headers['cookie'])
				cookiespt = cookiespt.split(';')
				for i in cookiespt:
					i = i.split('=')
					if ' ' in i[0]:
						i[0] = i[0].replace(' ', '', 1)
						cookies[i[0]] = i[1]
		return headers, cookies
