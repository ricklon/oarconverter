#
# Dump XMl file structure
#
#


from lxml import etree
import base64
import binascii

#file = "./faraway/objects/Primitive_235-137-085__38cce89c-5d1c-4eeb-a279-6eeb307ae28f.xml"
file = "./faraway/objects/Primitive_196-088-056__6b2e2415-eca2-450f-a7d5-7fbdd78253d4.xml"
tree = etree.parse(file)
root = tree.getroot()
print root.tag

print(etree.tostring(root, pretty_print=True))
uuids = root.findall(".//UUID/Guid")
for uuid in uuids:
    print "UUID: ", uuid.text

shapes = root.findall(".//Shapes")
for shape in shapes:
    print etree.tostring(shape, pretty_print=True)

textureEntries = root.findall(".//TextureEntry")
for tEntry in textureEntries:
    #print etree.tostring(guid, pretty_print=True)
    print "org: ",tEntry.text,
    #print "decode: ",base64.b64encode(tEntry.text)
    print "hex: ",binascii.hexlify(base64.b64decode(tEntry.text))





