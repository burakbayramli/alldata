import sys, os

if sys.argv[1] == 'zip':
    os.system("zip /opt/Downloads/dotbkps/alldata.zip -r /opt/Downloads/alldata/.git/")
