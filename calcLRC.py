import sys;
import re;

# Constants
LRC_ERR_MSG = {}
LRC_ERR_MSG[0x500] = 'Byte sequence is invalid, the length is not even!'
LRC_ERR_MSG[0x501] = 'Byte sequence is invalid. Unknown chars found!'
LRC_ERR_MSG[0x502] = 'TS is unknown'
LRC_ERR_MSG[0x503] = 'Incomplete Byte sequence'


def calcLRC(rawByte):
	Byte = ''.join(rawByte)

	#############################
	# Cek if BYTE sequence is valid
	#############################
	print '____________________LRC____________________'
	print 'BYTE	= '+Byte.upper()+' (length = '+str(len(Byte)/2)+' Dec or 0x'+ str(hex(len(Byte)/2)).replace('0x','').upper() +' )'
	
	# if contains besides alphabet or numbers
	pattern = '[^a-fA-F0-9]'
	
	# Cek if the length is even
	if (len(Byte) % 2) != 0:
		return LRC_ERR_MSG[0x500]
	elif len(re.findall(pattern, Byte)) != 0:
		return LRC_ERR_MSG[0x501]

	index = 0;
	tmpStr = ''
	intEDC = 0
	for i in range (index, len(Byte), 2):

		tmpStr += Byte[i]
		tmpStr += Byte[i+1]
		intEDC ^= int(str(tmpStr), 16)
		
		# clear the temp variable
		tmpStr = ''

	print
	print 'LRC	= 0x'+str(hex(intEDC)).replace('0x','').upper()
		
	return
	
if __name__ == '__main__':
	if len(sys.argv) < 2:
		rawByte = raw_input('Enter the BYTEs sequence> ')
		rawByte = rawByte.split()
	else:
		rawByte = sys.argv[1:]

	# Let's calculate the LRC
	lRet = calcLRC(rawByte)
	
	if ( lRet != 0 ):
		print	
		print 'Error Message: '
		print lRet
	