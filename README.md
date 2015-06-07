# nptel-dl
A small command-line program to download lecture videos from nptel.ac.in 

==================================================================
##Installation

####From Source
* Clone the repo or download the zip
* Make sure you have pip installed
* `cd` to the folder
* `pip -install -r "requirements.txt"`

##Usage
* On the terminal or Command Prompt Type
  `python nptel-dl.py "url" "directory"`
* Example : `python nptel-dl.py 'http://nptel.ac.in/courses/108103007/' 'D:\Tutorials'`
  
###Dependencies
* BeautifulSoup - For HTML parsing
* Requests - for retrieving HTML
