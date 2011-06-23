##########################################################
#	t1ApduDecoder.py 
#		Author 	: Bondhan Novandy
#		Date	: 15-16 May 2011
#
#		License	: Creative Commons Attribution-ShareAlike 3.0 Unported License.
#				  http://creativecommons.org/licenses/by-sa/3.0/
#		Publish	: http://bondhan.web.id (For education purpose only)
#		Version	: v0.1
#
#		Fixes	: 16 May 2011, Initial release
#				  
#
##########################################################

import sys
import re


# Constants
T1_ERR_MSG = {}
T1_ERR_MSG[0x500] = 'T1 stream bytes are invalid, the length is not even!'
T1_ERR_MSG[0x501] = 'T1 stream bytes are invalid. Unknown chars found!'
T1_ERR_MSG[0x502] = 'Incomplete T1 stream bytes'
T1_ERR_MSG[0x503] = 'T1 stream bytes are more than 32 bytes'
T1_ERR_MSG[0x504] = 'Unknown bytes found after EDC'

def pause():
	raw_input('press Enter to continue..')

# This function will check if the stream bytes are belong
# to I, R or S block and describe the entities for each component
def decodeT1(streamBytes):
	# if contains besides alphabet or numbers
	pattern = '[^a-fA-F0-9]'

	strBytes = ''.join(streamBytes)
	print '_________________T=1__APDU_________________'
	print 'T1	= '+strBytes
	print
	
	lRet = 0
	if (len(strBytes) % 2) != 0:
		return T1_ERR_MSG[0x500]
	elif len(re.findall(pattern, strBytes)) != 0:
		return T1_ERR_MSG[0x501]
	
	# Prologue
	# Consists of NAD | PCB | LEN
	
	# NAD
	byte = 0
	if byte+2 > len(strBytes):
		return T1_ERR_MSG[0x502]
		
	NAD_MSB = (strBytes[byte:(byte+1)]).upper()
	NAD_LSB = (strBytes[(byte+1):(byte+2)]).upper()
	NAD = NAD_MSB+NAD_LSB
	print 'NAD	= '+ NAD
	
	if NAD == '00':
		print '		-> NAD is ignored'
	elif NAD == 'FF':
		print '		-> NAD is invalid'
		
	NAD_MSB_INT = int(NAD_MSB, 16)
	NAD_LSB_INT = int(NAD_LSB, 16)
	
	print '		-> SAD (Source Address) '+ str(NAD_LSB_INT & 0b0111)
	print '		-> DAD (Destination Address) '+ str(NAD_MSB_INT & 0b0111)
	
	# PCB
	byte += 2
	if byte+2 > len(strBytes):
		return T1_ERR_MSG[0x502]
	PCB_MSB = (strBytes[byte:(byte+1)]).upper()
	PCB_LSB = (strBytes[(byte+1):(byte+2)]).upper()
	PCB = PCB_MSB+PCB_LSB
	print 'PCB	= '+ PCB
	
	PCB_INT = int(PCB, 16)
	PCB_MSB_INT = int(PCB_MSB,16)
	PCB_LSB_INT = int(PCB_LSB,16)
	
	if (PCB_MSB_INT & 0b1000) == 0:
		print '		-> I Block Identifier'
		
		if (PCB_MSB_INT & 0b0100) != 0:
			print '		-> N(S) = 1'
		else:
			print '		-> N(S) = 0'
		
		if (PCB_MSB_INT & 0b0010) != 0:
			print '		-> M = 1 (Chaining on progress)'
		else:
			print '		-> M = 0'
			
	elif (PCB_MSB_INT & 0b1100) == 0b1000:
		print '		-> R Block Identifier'
		
		if (PCB_MSB_INT & 0b0001) == 0b0001:
			print '		-> N(R) = 1'
		else:
			print '		-> N(R) = 0'
		
		if PCB_LSB_INT == 0x00:
			print '		-> No Error'
		elif PCB_LSB_INT == 0x01:
			print '		-> EDC or parity error'
		elif PCB_LSB_INT == 0x02:
			print '		-> Other Error'

	elif (PCB_MSB_INT & 0b1100) == 0b1100:
		print '		-> S Block Identifier'
		
		if (PCB_INT & 0xFF) == 0b11000000:
			print '		-> Resync Request (only from terminal)'
		elif (PCB_INT & 0xFF) == 0b11100000:
			print '		-> Resync Response (only from smart card)'
		elif (PCB_INT & 0xFF) == 0b11000001:
			print '		-> Request change to information field size'
		elif (PCB_INT & 0xFF) == 0b11100001:
			print '		-> Response to Request change to information field size'
		elif (PCB_INT & 0xFF) == 0b11000010:
			print '		-> Request Abort'
		elif (PCB_INT & 0xFF) == 0b11100010:
			print '		-> Response to Abort Request'
		elif (PCB_INT & 0xFF) == 0b11000011:
			print '		-> Request waiting time extension (only from smart card)'		
		elif (PCB_INT & 0xFF) == 0b11100011:
			print '		-> Response to waiting time extension (only from terminal)'		
		elif (PCB_INT & 0xFF) == 0b11100100:
			print '		-> Vpp Error Response (only from smart card)'			
			
	# LEN
	byte += 2
	if byte+2 > len(strBytes):
		return T1_ERR_MSG[0x502]
	LEN_MSB = (strBytes[byte:(byte+1)]).upper()
	LEN_LSB = (strBytes[(byte+1):(byte+2)]).upper()
	LEN = LEN_MSB+LEN_LSB
	print 'LEN	= '+ LEN	
	
	intLen = int(''.join(LEN), 16)
	
	print '		-> Inf Length = (Dec) ' + str(intLen)
	# INF
	byte += 2
	if byte+intLen > len(strBytes):
		return T1_ERR_MSG[0x502]
		
	if intLen > 0:
		print 'INF	= '+strBytes[byte:(byte+(intLen*2))]
	else:
		print 'INF	= No INF'
	
	# EDC
	byte += (intLen*2)
	if byte+2 > len(strBytes):
		return T1_ERR_MSG[0x502]
		
	EDC_MSB = (strBytes[byte:(byte+1)]).upper()
	EDC_LSB = (strBytes[(byte+1):(byte+2)]).upper()
	EDC = EDC_MSB+EDC_LSB
	print 'EDC	= '+ EDC
	
	xored = 0
	for i in range (2, len(strBytes)-2, 2):
			
		var = (strBytes[i]+strBytes[i+1])
		xored ^= int(var, 16)
		#print var + '->' + str(xored)
			
	print '		-> Calculated EDC: (Dec) '+str(xored)+' or '+str(hex(xored))
		
	if xored == int(EDC,16):
		print '		-> EDC Sequence is valid!'
	else:
		print '		-> EDC Sequence is invalid!'
	
	byte += 2
	if byte < len(strBytes):
		print 'UNKNOWN = '+ strBytes[byte:len(strBytes)]
		return T1_ERR_MSG[0x504]
	
	return lRet

## Main function
if __name__ == '__main__':
	streamBytes = ''
	if len(sys.argv) < 2:
		streamBytes = raw_input('Enter the T1 stream bytes> ')
		streamBytes = streamBytes.split()
	else:
		streamBytes = sys.argv[1:]

	# Let's decode it
	lRet = decodeT1(streamBytes)
	
	if ( lRet != 0 ):
		print	
		print 'Error Message: '
		print lRet