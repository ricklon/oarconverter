from pythonmagickwand.image import Image
i = Image('foo.jpg')
i.format = 'PNG'
i.flip()
i.save('flip.png')
