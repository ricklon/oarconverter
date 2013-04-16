from pythonmagickwand.image import Image
i = Image('./assets/064fa8ad-4b88-452f-a110-68f1250be0c3_texture.jp2')
i.format = 'PNG'
i.flip()
i.save('flip.png')
