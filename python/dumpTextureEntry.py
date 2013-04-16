#
# dumpTextureEntry.py
# Dump the OAR TextureEntry into it's basic components by base64 decoding, and partsing the fiels.
# The definition from http://lib.openmetaverse.org/wiki/TextureEntry is being followed.
#
# Read 16 check 17, Read 16 more , check +1
# When first 00 found read color data check for 00 after color data end
# easy_install bitstring
#>>> h = BitArray('0x12')
#>>> print h.bin
#00010010
# May need to create a TextureEntry object

import base64
import uuid
import binascii
from bitstring import BitStream, BitArray


def main():
	verbose = False 
	position = 15 
	position_prev = 0
	ii = 0
	
	
	
	
	#TextureEntry = "pExBz705TAef/CtY54dqiADasdoAAAAAgD8AAACAPwAAAAAAAAAAAABBAAAAAA=="
	TextureEntry = "1pchHlsBRdmyre5mcisH3Qaoc5ahnZRLzJh7/NZ8cYMSAAAAAH8AAACgQACamRk/AAAAAIv8AAAAAAAAAAAA"
	decodedTextureEntry = base64.b64decode(TextureEntry)
	print binascii.hexlify(decodedTextureEntry)
	if verbose:
	    nn = 0
	    print "len: ",len(binascii.hexlify(decodedTextureEntry))
	    nn+= 16
	    print len(decodedTextureEntry[(nn-16):nn]),":",
	    print binascii.hexlify(decodedTextureEntry[0:nn]),
	    #nn += 1
	    print binascii.hexlify(decodedTextureEntry[nn])
	    print (nn-16),"-", nn, " ",(nn)
	    nn += 17
	    print len(decodedTextureEntry[(nn-16):nn]), ":",
	    print binascii.hexlify(decodedTextureEntry[(nn-16):nn]),
	    #nn+= 1
	    print binascii.hexlify(decodedTextureEntry[nn])
	    print  (nn-16),"-", nn, " ",nn
	    nn += 17
	    print len(decodedTextureEntry[(nn-16):nn]), ":",
	    print binascii.hexlify(decodedTextureEntry[(nn-16):(nn)]),
	    #nn += 1
	    print binascii.hexlify(decodedTextureEntry[(nn)])
	    print  (nn-16),"-", nn, " ",nn
	    nn += 17
	    print len(decodedTextureEntry[(nn-16):nn]), ":",
	    print binascii.hexlify(decodedTextureEntry[nn-16:nn]),
	    #nn += 1
	    print binascii.hexlify(decodedTextureEntry[nn]) 
	    print  (nn-16),"-", nn, " ",nn
	    print "Done"
	
	ii = 16
	while ii < range(len(binascii.hexlify(decodedTextureEntry))): 
	    print len(decodedTextureEntry[(ii-16):ii]), ":",
	    print binascii.hexlify(decodedTextureEntry[(ii-16):(ii)]),
	    print  (ii-16),"-", ii, " ",ii

	    parseFacebits(binascii.hexlify(decodedTextureEntry[ii]))

	    if decodedTextureEntry[ii] == '\x00':
	        print "00: ",ii,
	        ii += 1
	        print "RR: ",binascii.hexlify(decodedTextureEntry[ii]),
	        ii += 1
	        print "GG: ",binascii.hexlify(decodedTextureEntry[ii]),
	        ii += 1
	        print "BB: ",binascii.hexlify(decodedTextureEntry[ii]),
	        ii += 1
	        print "AA: ",binascii.hexlify(decodedTextureEntry[ii])
	        break
	    ii += 17




def parseFacebits(faceBitfield):
    faces = []
    bfield = BitArray(bytes=faceBitfield)
    print "Facebit: ", bfield.bin
    for ii in range(0,16):
        print "0x0001 << %d = 0c%04X" % (bfield[ii], 0x1 << bfield[ii])


if __name__=="__main__":
        main()


#print uuid.

#TextureID = decodedTextureEntry[range(0,15)]
#data  = TextureID.join(TextureID)
#print data
#FaceBitfield


