import sys
import random

# number is in decimal
def genRandData(number_):
	number = ''.join(number_)
	counter = int(number, 10)
	strResult = []
	
	while ( counter > 0 ):
		counter -= 1		
		angka = random.randint(0,0xFF)
		sys.stdout.write(str(hex(angka)).replace('0x','').upper())
	return
	

if __name__ == '__main__':
	number = 0x00;
	
	if len(sys.argv) < 2:
		number = raw_input('Enter number data to generate> ')
	else:
		number = sys.argv[1:]
		
	genRandData(number)
	
	