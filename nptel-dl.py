from downloader import downloader
import sys,argparse,os

parser = argparse.ArgumentParser()
parser.add_argument('--url',default = None, type = str, help = 'The URL to download videos from.')
parser.add_argument('--dir',default = os.getcwd(), type = str, help = 'The directory to save videos in. Default value is the current working directory.')
parser.add_argument('--mp4',action = 'store_true',help = 'Flag to download in MP4 format.')
parser.add_argument('--3gp',action = 'store_true',help = 'Flag to download in 3GP format.')
parser.add_argument('--mp3',action = 'store_true',help = 'Flag to download in MP3 audio only.')
parser.add_argument('--exclude',nargs = '+',type = int, help = 'Enter track numbers to exclude.')
parser.add_argument('--include',nargs = '+',type = int, help = 'Enter track numbers to include.')
parser.add_argument('--limit',default = None,type = int,help = 'Maximum number of tracks to download.')
parser.add_argument('--range',nargs = 2,type = int, help = 'Enter range of tracks to download.')

if __name__ == '__main__':
	args = parser.parse_args()
	if args.exclude is not None:
		args.exclude = set(args.exclude)
	if args.include is not None:
		args.include = set(args.include)
	if args.url == None:
		print ("No URL entered.")
		sys.exit(0)
	downloader = downloader.Downloader(args = args)
	try:
		downloader.Download()
	except KeyboardInterrupt:
		print ("\nExiting.")
		sys.exit(0)
