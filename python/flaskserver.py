import os
import tarfile
from lxml import etree
import base64
import binascii
from pprint import pprint as pp
from optparse import OptionParser
import json


from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER']= 'oars'


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
	file = request.files['oar']
	if file:
	    filename = secure_filename(file.filename)
	    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    outpath = os.path.basename(file.filename)
	    untar(os.path.join(app.config['UPLOAD_FOLDER'], filename), outpath, False)
	    object_dir='./'+outpath+'/objects'
	    parsedJson = walk_objects(object_dir, False)
	    print parsedJson
	    return parsedJson

def walk_objects(object_dir,verbose):
    jsonData = '['
    for root, dirs, files in os.walk(object_dir):
        for name in files:
            filename = os.path.join(root, name)
            jsonData +=json.dumps(parseXMLFile(filename, verbose))+','
    jsonData = jsonData[:-1] +']'
    return jsonData
	    
def parseXMLFile(file, verbose):
	tree = etree.parse(file)
	root = tree.getroot()
	uuids = root.findall(".//UUID/Guid")
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
	return data

def getDict(tag):
	items = {}
	for elem in tag:
		items[elem.tag] = elem.text.strip()
	return items

def parse_textureEntry(textureEntry):
        #convert from base64 to base16
	bitmask = "11111111"
        decodedTextureEntry = binascii.hexlify(base64.b64decode(textureEntry))
	data = {}
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
	
if __name__ == '__main__':
    app.run(port=3004,host='0.0.0.0', debug=True)
