##########################################################
#	T1starLogDecoder.py 
#		Author 	: Bondhan Novandy
#		Date	: 16-18 May 2011
#
#		License	: Creative Commons Attribution-ShareAlike 3.0 Unported License.
#				  http://creativecommons.org/licenses/by-sa/3.0/
#		Publish	: http://bondhan.web.id (For education purpose only)
#		Version	: v0.1
#		Purpose	: Will decode a log file of T=1 from Star 3150 (copy clipboard) 
#				  into plain text
#		Files required:
#				  - atr_decoder.py
#				  - t1ApduDecoder.py
#				  - pps_decoder.py
#				  - Python 2.7
#
#		Fixes	: 18 May 2011, Initial release
#				  
#
##########################################################

import sys
import re
import atr_decoder
import pps_decoder
import t1ApduDecoder

def pause():
	raw_input('Please ENTER to continue')

def prepLogFile(fileName):

	SENTINEL = '## '

 	fHandle = 0
	try:
		fHandle = open(filename, 'r')
	except IOError:
		print
		print 'Error Message:'
		print filename+' not found!'
		return	
		
	keywords_counter = {'Card ATR':0, 'Term Bytes':0, 'Card Bytes':0}
	keywords = {'CardATR', 'CardBytes', 'TermBytes'}
	#keywords = {'cardatr', 'termbytes', 'card'}
	pattern = '[^a-fA-F0-9]'
	
	# Let's process it
	buffer = []
	buffz = fHandle.readlines()
	for buff in buffz:
		tmp = buff.strip()
		tmp = tmp.replace(' ','')
		buffer.append(tmp)
		
	ready_save = []
	ready_buffer = ''

	iter_word = iter(buffer)

	loop = True
	isRecording = False
	isFilled = False
	while loop == True:
		try:
			if isFilled == False:
				word = iter_word.next()
				word = word.strip()				
			elif isFilled == True:
				isFilled = False
			
			#print 'word = ' + word
			#print isFilled
			#pause()
			# find non hex
			if len(re.findall(pattern, word)) > 0:
				for key in keywords:
					#print 'word = ' + word +' key = ' + key
					#pause()
					#if word.find(key) > -1:
					if len(re.findall(key, word)) > 0:
						#print 'found key = ' + word
						#pause()
						isRecording = True
						tmp = ''
						tmp = SENTINEL + key + ':\n'
						ready_save.append(tmp)
						#print ' tmp = ' + tmp + ' word = ' + word
						#pause()
						while isRecording == True:
							word = iter_word.next()
							word = word.strip()
							if len(re.findall(pattern, word)) > 0:
								isRecording == False
								ready_buffer += '\n'
								ready_save.append(ready_buffer)
								ready_buffer = ''
								#print 'isRecording found non hex ' + word
								#print 'ready_save = '
								#print ready_save
								isFilled = True
								break # while
							else:
								ready_buffer += word
						
						if isRecording == False:
							break; # for
																	
	
		except StopIteration:		
			loop = False			
			#print ready_save
			#print 'word = ' + word
			ready_save.append(ready_buffer+'\n')
			#print 'End of buffer'
			#pause()
			
	return ready_save

	
## Main function
if __name__ == '__main__':
	lRet = 0
	print '_________________________________________________'
	print 'Star 3150 log decoder for T=1 (by clipboard copy)'
	print 'Using this script for T=0 will result errors!'
	print '_________________________________________________'
	if len(sys.argv) < 2:
		filename = raw_input('Enter filename> ')
	else:
		filename = sys.argv[1:]

	filename = filename[0]
	filtered_text = prepLogFile(filename)
	
	#print filtered_text
	#pause()


	for i in filtered_text:
		i = i.strip()
		#print 'i.strip() = ' + i
		#print 'i[0:2] = ' + i[0:2]
		key = i[0:2]
		#print i
		#pause()		
		#if key == '3B' or key == '3F':
		if len(re.findall('3B', key)) > 0:
			#print 'FOUND ATR '
			lRet = atr_decoder.decode_atr(i)
		elif i[0:2] == 'FF':
			#print 'FOUND PPS'
			lRet = pps_decoder.decode_pps(i)
		elif i[0:2] == '##':
			#print '# FOUND comment'
			print 
			print i
			lRet = 0
		else:
			#print 'FOUND T1 apdu'
			lRet = t1ApduDecoder.decodeT1(i)
	
		if ( lRet != 0 ):
			print	
			print 'Error Message: '
			print lRet
