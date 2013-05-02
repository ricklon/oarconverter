def getCube(shape):
	vertexObject = {}
	vertexObject['Vertices'] = []
	vertexObject['Vertices'].append(getVector3(float(shape['Scale']['X'])/2, float(shape['Scale']['Y'])/2, float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(float(shape['Scale']['X'])/2, float(shape['Scale']['Y'])/2, -float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(float(shape['Scale']['X'])/2, -float(shape['Scale']['Y'])/2, float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(float(shape['Scale']['X'])/2, -float(shape['Scale']['Y'])/2, -float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(-float(shape['Scale']['X'])/2, float(shape['Scale']['Y'])/2, float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(-float(shape['Scale']['X'])/2, float(shape['Scale']['Y'])/2, -float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(-float(shape['Scale']['X'])/2, -float(shape['Scale']['Y'])/2, float(shape['Scale']['Y'])/2))
	vertexObject['Vertices'].append(getVector3(-float(shape['Scale']['X'])/2, -float(shape['Scale']['Y'])/2, -float(shape['Scale']['Y'])/2))
	vertexObject['Faces'] = []
	vertexObject['Faces'].append(getFace4(0,1,4,5, shape['TextureEntry'][0])) #top
	vertexObject['Faces'].append(getFace4(0,1,2,3, shape['TextureEntry'][1])) #sides
	vertexObject['Faces'].append(getFace4(4,5,6,7, shape['TextureEntry'][2]))
	vertexObject['Faces'].append(getFace4(0,4,2,6, shape['TextureEntry'][3]))
	vertexObject['Faces'].append(getFace4(1,5,3,7, shape['TextureEntry'][4]))
	vertexObject['Faces'].append(getFace4(2,3,6,7, shape['TextureEntry'][5])) #bottom
	return vertexObject


def getFace3(pointA,pointB,pointC, material):
	face = {}
	face['Vertices']=[]
	face['Vertices'].append(pointA)
	face['Vertices'].append(pointB)
	face['Vertices'].append(pointC)
	face['Texture'] = material
	return face

def getFace4(pointA,pointB,pointC,pointD, material):
	face = {}
	face['Vertices']=[]
	face['Vertices'].append(pointA)
	face['Vertices'].append(pointB)
	face['Vertices'].append(pointC)
	face['Vertices'].append(pointD)
	face['Texture'] = material
	return face

def getVector3(x,y,z):
	vector = {}
	vector["X"] = x
	vector["Y"] = y
	vector["Z"] = z
	return vector

