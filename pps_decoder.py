##########################################################
#	pps_decoder.py 
#		Author 	: Bondhan Novandy
#		Date	: 16-18 May 2011
#
#		License	: Creative Commons Attribution-ShareAlike 3.0 Unported License.
#				  http://creativecommons.org/licenses/by-sa/3.0/
#		Publish	: http://bondhan.web.id (For education purpose only)
#		Version	: v0.1
#		Purpose	: Decode PPS bytes sequnece 
#
#		Fixes	: 18 May 2011, Initial release
#				  
#
##########################################################

import sys
import re
import atr_decoder

# Constants
PPS_ERR_MSG = {}
PPS_ERR_MSG[0x500] = 'PPS is invalid, the length is not even!'
PPS_ERR_MSG[0x501] = 'PPS is invalid. Unknown chars found!'
PPS_ERR_MSG[0x502] = 'TS is unknown'
PPS_ERR_MSG[0x503] = 'Incomplete PPS'

def decode_pps(pps):
	
	PPS1 = -1
	PPS2 = -1
	PPS3 = -1
	
	lRet = 0
	pps_seq = ''.join(pps)		# Join the list again as full string

	#############################
	# Cek if PPS is valid
	#############################
	print '____________________PPS____________________'
	print 'PPS	= '+pps_seq.upper()
	
	# if contains besides alphabet or numbers
	pattern = '[^a-zA-Z0-9]'
	
	# Cek if the length is even
	if (len(pps_seq) % 2) != 0:
		return PPS_ERR_MSG[0x500]
	elif len(re.findall(pattern, pps_seq)) != 0:
		return PPS_ERR_MSG[0x501]
	
	# PPSS
	byte = 0
	MSB = (pps_seq[byte:(byte+1)]).upper()
	LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	
	print
	print 'PPSS	= '+MSB+LSB	
	
	#PPS0
	byte += 2
	if byte+2 > len(pps_seq):
		return PPS_ERR_MSG[0x503]	
	
	MSB = (pps_seq[byte:(byte+1)]).upper()
	LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	
	print 'PPS0	= '+MSB+LSB
	
	LSB_PPS0_INT = int(LSB, 16)
	MSB_PPS0_INT = int(MSB, 16)
	
	print '		-> T= ' + str(LSB_PPS0_INT) + ' protocol'
	
	if (MSB_PPS0_INT & 0b0001) !=0:
		PPS1 = 0
		print '		-> PPS1 exists'
	if (MSB_PPS0_INT & 0b0010) !=0:
		PPS2 = 0
		print '		-> PPS2 exists'
	if (MSB_PPS0_INT & 0b0100) !=0:
		PPS3 = 0
		print '		-> PPS3 exists'
	if (MSB_PPS0_INT & 0b1000) !=0:
		print '		-> Wrong PPS0. Last bit must be zero (check!)'		
	
	#PPS1
	byte += 2
	if byte+2 > len(pps_seq):
		return PPS_ERR_MSG[0x503]	
	
	if PPS1 > -1:
		MSB = (pps_seq[byte:(byte+1)]).upper()
		LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	
		print 'PPS1	= '+MSB+LSB
		
		PPS_FI = MSB
		PPS_DI = LSB
		
		PPS_ETU = atr_decoder.calcEtu(PPS_FI, PPS_DI)
		
		print '		-> New ETU = ' + str(PPS_ETU)
	
	#PPS2 (Reserved)
	if PPS2 > -1:
		byte += 2
		MSB = (pps_seq[byte:(byte+1)]).upper()
		LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	
		print 'PPS2		= '+MSB+LSB	

	#PPS3 (Reserved)
	if PPS3 > -1:
		byte += 2
		MSB = (pps_seq[byte:(byte+1)]).upper()
		LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	
		print 'PPS3		= '+MSB+LSB	
		
	#TCK
	byte += 2
	if byte+2 > len(pps_seq):
		return PPS_ERR_MSG[0x503]
		
	MSB = (pps_seq[byte:(byte+1)]).upper()
	LSB = (pps_seq[(byte+1):(byte+2)]).upper()
	BOTH = MSB+LSB
		
	print 'TCK	= '+BOTH

	xored = 0
	for i in range (0, len(pps_seq)-2, 2):
		var = (pps_seq[i]+pps_seq[i+1])
		xored ^= int(var, 16)
		#print var + '->' + str(xored)
			
	print '		-> Calculated TCK: (Dec) '+str(xored)+' or '+str(hex(xored).replace('0x','').upper())
		
	if xored == int(BOTH,16):
		print '		-> PPS Sequence is valid!'
	else:
		print '		-> PPS Sequence is invalid!'
			
	
	
	return lRet
	
## Main function
if __name__ == '__main__':
	pps = []

	if len(sys.argv) < 2:
		pps = raw_input('Enter the PPS sequence> ')
		pps = pps.split()
	else:
		pps = sys.argv[1:]

	# Let's decode it
	lRet = decode_pps(pps)
	
	if ( lRet != 0 ):
		print	
		print 'Error Message: '
		print lRet
	