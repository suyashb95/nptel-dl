from downloader import downloader
import sys,argparse,os

parser = argparse.ArgumentParser()
parser.add_argument('--url',default = None, type = str, help = 'The URL to download videos from.')
parser.add_argument('--dir',default = os.getcwd(), type = str, help = 'The directory to save videos in. Default value is the current working directory.')
parser.add_argument('--mp4',action = 'store_true',help = 'Flag to download in MP4 format.')
parser.add_argument('--3gp',action = 'store_true',help = 'Flag to download in 3GP format.')

if __name__ == '__main__':
	args = parser.parse_args()
	if args.url == None:
		print "No URL entered."
		sys.exit(0)
	downloader = downloader.Downloader(args = args)
	downloader.Download()