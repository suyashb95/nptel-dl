import os,sys
import requests,socket
from contextlib import closing
import re,os
from time import sleep

class StreamThread(threading.Thread):
	
	def __init__(self,filename,link,connectionHandler):
		threading.Thread.__init__(self)
		self.filename = filename
		self.link = link
		self.connectionHandler = connectionHandler
		
	def run(self):
		self.getFile(self.filename,self.link)
					
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
			with closing(self.connectionHandler(link,True,15)) as response:
				print "Response: "+ str(response.status_code)		
				file_size = float(response.headers['content-length'])	
				if(os.path.isfile(new_filename)):
					if os.path.getsize(new_filename) >= long(file_size):
						print new_filename + " already exists, skipping."
						return new_filename
					else:
						print "Incomplete download, restarting."
				print "File Size: " + '%.2f' % (file_size/(1000**2)) + ' MB'
				print "Saving as: " + new_filename
				done = 0
				try:
					with open(new_filename,'wb') as file:
						for chunk in response.iter_content(chunk_size=1024):
							if chunk:
								file.write(chunk)
								file.flush()
								done += len(chunk)
								self.progressBar(done,file_size)				
					if os.path.getsize(new_filename) < long(file_size):
						print "\nConnection error. Restarting in 15 seconds."
						sleep(15)
						self.getFile(filename,link)
					print "\nDownload complete."
				except (socket.error,
						requests.exceptions.ConnectionError):
					self.getFile(filename,link)
				except KeyboardInterrupt:
					print "\nExiting."
					sys.exit(0)
		else:
			return 