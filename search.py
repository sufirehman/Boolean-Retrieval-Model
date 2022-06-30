import timeit     #for measuring time in fetching
# Import os Module
import os
from xml.dom.pulldom import CHARACTERS

from b_system import BRsystem
  
# Giving the Folder Path                        #NOTE: Change this path to directory where you have downloaded my assignment
path = "D:\semester 6\i190583 IR Assignment1"   #NOTE: select the assignment folder and copy the whole path

docs=[]
# Change the directory
os.chdir(path)
  
# Reading text File
def read_file(file_path):
        with open(file_path, 'r') as f:
            docs.append(f.read())
  
# iterate through all files
for files in os.listdir():
    # Check whether file is in text format or not
    if files.endswith(".txt"):
        file_path = f"{path}\{files}"
        
        # calling read text file function
        read_file(file_path)

stop_words = ['is', 'a', 'for', 'the', 'of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no','we','do']

def main():
    br = BRsystem(docs, stop_words=stop_words)
    characters = "@.,!#$%^&*();:\n\t\\\"?!{}[]<>"
    while True:
        query = input('Enter the query: ')
        start = timeit.default_timer()         #starts time clock
        result = br.process(query)             #query passed
        end = timeit.default_timer()           #measures end time
        if(result is not None):
            print ('Processing time: {:.1} seconds'.format(end - start))
            print('\nResults found in Docs: ')
            print(result)
        print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Exit')