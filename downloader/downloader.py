import requests,os,sys,HTMLParser,re
from bs4 import BeautifulSoup
from contextlib import closing
from time import sleep
import socket

class Downloader():
	
	def __init__(self,args = None):
		self.url = args.url
		self.dirname = args.dir
		self.args = args
		self.session = requests.Session()
		self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=2))
		self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=2))
		self.completed = 0
		
	def connectionHandler(self,url,stream = False,timeout = 15):
		try:
			response = self.session.get(url,stream = stream,timeout = timeout)
			assert response.status_code == 200
			return response
		except (requests.exceptions.ConnectionError,
				TypeError,
				socket.error):
			print "Connection error. Retrying in 15 seconds."
			sleep(15)
			self.connectionHandler(url,stream)
		except (AssertionError,
				requests.exceptions.HTTPError):
			print "Connection error or invalid URL."
			return
		except KeyboardInterrupt:
			print "Exiting."
			sys.exit(0)
			
	def getVideos(self,soup):
		items = soup.findAll('a',{'class':'header','href':''})
		print "%d lecture videos found." % (len(items))
		for index,item in enumerate(items):
			url = 'http://nptel.ac.in' + item['onclick'].split('=')[1][1:-1]	
			while(1):
				try:	
					response = self.connectionHandler(url)
					subsoup = BeautifulSoup(response.text, 'html.parser')
					break
				except KeyboardInterrupt:
					sys.exit(0)
			divs = subsoup.findAll('p',{'class':'format-label'})
			links = []
			for div in divs:
				links.append(div.find('a')['href'])			
			if self.args.mp4:
				dl_url = [url for url in links if url.endswith('.mp4')][0]
				format = '.mp4'
			elif self.args.	__getattribute__('3gp'):
				dl_url = [url for url in links if url.endswith('.3gp')][0]
				format = '.3gp' 
			elif self.args.	__getattribute__('mp3'):
				dl_url = [url for url in links if url.endswith('.mp3')][0]
				format = '.mp3' 
			else:
				dl_url = [url for url in links if url.endswith('.flv')][0]
				format = '.flv'
			if self.args.limit is not None:
				if self.completed == self.args.limit:
					return
			if self.args.include is not None:
				if self.completed == len(self.args.include):
					break
				if(index + 1) not in self.args.include:
					if self.args.range:
						if not (self.args.range[0] <= (index + 1) <= self.args.range[1]):
							continue
					else:
						continue
			elif self.args.exclude is not None:
				if (index + 1) in self.args.exclude:
					print "Skipping " + item.text
					continue
			self.getFile(item.text + format ,dl_url)
			self.completed += 1
			
	def progressBar(self,done,file_size):
		percentage = ((done/file_size)*100)
		sys.stdout.flush()
		sys.stdout.write('\r')	
		sys.stdout.write('[' + '#'*int((percentage/5)) + ' '*int((100-percentage)/5) + ']')
		sys.stdout.write(' | %.2f' % percentage + ' %')
				
	def getFile(self,filename,link):
		new_filename = re.sub('[\/:*"?<>|]','_',filename)
		if link is not None:
			print "\nConnecting to stream..."
			try:
				with closing(self.connectionHandler(link,True,5)) as response:
					print "Response: "+ str(response.status_code)		
					file_size = float(response.headers['content-length'])	
					if(os.path.isfile(new_filename)):
						if os.path.getsize(new_filename) >= long(file_size):
							print new_filename + " already exists, skipping."
							return new_filename
						else:
							print "Incomplete download, restarting."
					print "Saving as: " + new_filename
					print "File Size: " + '%.2f' % (file_size/(1000**2)) + ' MB'			
					try:
						done = 0
						with open(new_filename,'wb') as file:
							for chunk in response.iter_content(chunk_size=1024):
								if chunk:
									file.write(chunk)
									file.flush()
									done += len(chunk)
									self.progressBar(done,file_size)
						if os.path.getsize(new_filename) < long(file_size):
							print "\nConnection error. Restarting in 15 seconds.LOL"
							sleep(15)
							self.getFile(filename,link)
						return new_filename
					except KeyboardInterrupt:
						print "\nExiting."
						sys.exit(0)
					except (socket.error,
							requests.exceptions.ConnectionError):
						self.getFile(filename,link)
			except AttributeError:
				self.getFile(filename,link)
			except KeyboardInterrupt:
				os.remove(new_filename)
				print "\nExiting." 
				sys.exit(0)
		else:
			return 

			
	def Download(self):
		if self.url is None:
			print "No URL entered."
			return
		elif 'nptel' not in self.url:
			print "Invalid URL"
			return
		try:
			if self.dirname is not None:
				os.chdir(str(self.dirname))
			print "Connecting ... "
			response = self.connectionHandler(self.url)
		except WindowsError:
			print "Invalid Directory"
			return
		print "Response: " + str(response.status_code)
		soup = BeautifulSoup(response.text, 'html.parser')
		folder = re.sub('[\/:*"?<>|]','_',soup.find('title').text)
		if not os.path.isdir(folder):
			os.mkdir(folder)
		os.chdir(os.getcwd() + '\\' + str(folder))
		self.getVideos(soup)