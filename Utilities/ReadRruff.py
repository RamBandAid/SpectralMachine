#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
*********************************************
*
* ReadRRuFF
* Convert RRuFFspectra to ASCII
* File must be in RRuFF
* version: 20170309j
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************
'''
print(__doc__)


import numpy as np
import sys, os.path, getopt, glob, csv

def main():
	if(len(sys.argv)<2):
		print(' Usage: \n  python readrruff.py <RRuFF filename>\n')
		return

	try:
		with open(sys.argv[1], 'r') as f:
			M = np.loadtxt(f, skiprows = 9, delimiter = ',', unpack=False)
		print(str(' ' + sys.argv[1]) + '\n File OK, converting to ASCII... \n')
	except:
		print('\033[1m ' + str(sys.argv[1]) + ' file not found \n' + '\033[0m')
		return

	newFile = os.path.splitext(sys.argv[1])[0] + '_b.txt'

	with open(newFile, 'ab') as f:
		np.savetxt(f, M, delimiter='\t', fmt='%10.6f')

	print(' Done!\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
