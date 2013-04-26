#
# oar2three
# Read the Open Sim Archive extract it, read through the files, generate three.js json object
# 
# usage:
# oar2three archivename.oar
#
# Consideration OpenSim/Second Life uses jpeg2000, jp2 which is a license encumbered format
# Possible convert assett out of jpeg2000, but to what? What's collada/webgl/unity3d support
#
#PyhonMagick used to process the jpeg2000 files to png.
#


import os
import dictToThree
import tarfile
from lxml import etree
import base64
import binascii
from pprint import pprint as pp
from optparse import OptionParser




def main():
        usage = "usage: %prog [options] arg"
        parser = OptionParser(usage)
        #Actions
        #parser.add_option("-h", "--help", action="help")
        parser.add_option("-o", "--output", dest="output", help="specify an output directory")
        parser.add_option("-v", "--verbose",
                                    action="store_true", dest="verbose", default=True,
                                    help="show debug info [default]")
        parser.add_option("-q", "--quiet",  action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
        (options, args) = parser.parse_args()

        if len(args) != 1:
                parser.error("incorrect number of arguments")
        file = args[0]
        outpath = os.path.basename(file).split(".")[0]
		
        if options.verbose:
		print "file: ", file ,", outdir: ", options.output
        #unpack the oar file, it's really a tar.gz file.
        untar(file, outpath, options.verbose)
        #walk through the asset directory
        asset_dir = './' + outpath + '/assets'
        object_dir = './' + outpath + '/objects'
        if options.verbose:
		print asset_dir
                print object_dir
        walk_assets(asset_dir, options.verbose)
        #walk through objectsA
        walk_objects(object_dir, options.verbose)

      

def walk_assets(asset_dir,verbose):
    for root, dirs, files in os.walk(asset_dir):
        for name in files:
            filename = os.path.join(root, name)
#            print filename
            parse_asset_name(filename, verbose)

def walk_objects(object_dir,verbose):
    for root, dirs, files in os.walk(object_dir):
        for name in files:
            filename = os.path.join(root, name)
            print filename
            parse_object_name(filename, verbose)


def parse_asset_name(file, verbose):
		uuid = os.path.basename(file).split("_")[0]
		asset_type = os.path.basename(file).split("_")[1].split(".")[0]
		if asset_type == "object":
			mapThreeJS(parseXMLFile(file,verbose))
			
		if verbose:
				print "UUID: ", uuid, " TYPE: ", asset_type
		return [uuid, asset_type]

def parse_object_name(file, verbose):
		name = os.path.basename(file).split("_")[0]
		xx = os.path.basename(file).split("-")[0].split("_")[1]
		yy = os.path.basename(file).split("-")[1]
		zz = os.path.basename(file).split("-")[2].split("__")[0]
		uuid = os.path.basename(file).split("__")[1].split(".")[0]
		mapThreeJS(parseXMLFile(file,verbose))
		if verbose:
                    print "Name: ", name, "X: ",xx, " Y: ",yy, " Z: ",zz, " UUID: ", uuid
		return [uuid, name, xx, yy, zz]
		

def untar(file, outpath, verbose):
		tar = tarfile.open(file)
		if tarfile.is_tarfile(file):
				if verbose:
						print "Unpacking Contents"
						#print tar.list(verbose=True)
				tar.extractall(outpath)
				tar.close()
		else:
				parser.error("Not a valid oar file.")
		

def get_password(option, opt_str, value, parser ):
        if parser.values.password is None:
                parser.values.password = getpass.getpass("Enter password: ")

        if parser.values.password is None:
                print "No password given\n"
                parser.print_help()
                exit(-1)
                
        return


def parseXMLFile(file, verbose):
	tree = etree.parse(file)
	root = tree.getroot()
	uuids = root.findall(".//UUID/Guid")
	#shapes = root.findall(".//Shapes")
	#textureEntries = root.findall(".//TextureEntry")
	
	data = {}
	data['TextureEntry'] = parse_textureEntry(root.findtext(".//TextureEntry"))
	GroupPosition = root.find(".//GroupPosition")
	data['GroupPosition'] = getDict(GroupPosition)
	data['OffestPosition'] = getDict(  root.find(".//OffsetPosition"))
	data['RotationOffset'] = getDict(root.find(".//RotationOffset"))
	data['Color'] = getDict(root.find(".//Color"))
	data['Profileshape'] = root.findtext(".//ProfileShape")
	#data['path'] = root.findall(".//path")
	#data['Shape'] = getDict(root.find(".//Shape"))
	data['Scale'] = getDict(root.find(".//Scale"))
	data['ParentID'] = root.find(".//ParentID").text

	if verbose:
		pp(data)
		#print root.tag
		#print(etree.tostring(root, pretty_print=True))
		#for uuid in uuids:
		#    print "UUID: ", uuid.text

		#for shape in shapes:
		#    print etree.tostring(shape, pretty_print=True)

		#for tEntry in textureEntries:
		#    #print etree.tostring(guid, pretty_print=True)
		#    print "org: ",tEntry.text,
		#    #print "decode: ",base64.b64encode(tEntry.text)

		#    print "hex: ",binascii.hexlify(base64.b64decode(tEntry.text))
	return data
		
def getDict(tag):
	items = {}
	for elem in tag:
		items[elem.tag] = elem.text.strip()
	return items


def mapThreeJS(prim):
	pp(prim['Scale'])

#use the base 64 texture entry, and return a dictionary containing the faces and the associated files
def parse_textureEntry(textureEntry):
        #convert from base64 to base16
	bitmask = "11111111"
        decodedTextureEntry = binascii.hexlify(base64.b64decode(textureEntry))
	data = {}
	print("New Texutre Entry")
        print decodedTextureEntry
	ii=32
	while(True):
                #the actual id of the texture entry
                currentTexture = decodedTextureEntry[ii-32:ii]
                ii+=2
		for i in xrange(0,8):
			if(bitmask[i]=='1'):
				data[i]=currentTexture
		bitmask=getBitmask(decodedTextureEntry[ii-2:ii])
		#the bitmask will be all 0's if it is the end of the texture. Next block is stuff like alpha's which we don't care about for now
		if(bitmask=="00000000"):
			break
		ii+=32
                #bitmask that identifies which faces the texture is applied to, the first is the default so it doesn't have a bitmask
	return data

#converts the hex string into the bitmask
def getBitmask(hexstring):
	bitmask=""
	for hexChar in hexstring:
		bitmask+=hexCharToBinString(hexChar)
	return bitmask

#converts one hex character to four binary characters
def hexCharToBinString(hexChar):
	return {
		'0': "0000",
		'1': "0001",
		'2': "0010",
		'3': "0011",
		'4': "0100",
		'5': "0101",
		'6': "0110",
		'7': "0111",
		'8': "1000",
		'9': "1001",
		'a': "1010",
		'b': "1011",
		'c': "1100",
		'd': "1101",
		'e': "1110",
		'f': "1111",
	}[hexChar]

if __name__=="__main__":
        main()


