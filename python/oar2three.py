#
# oar2openscad
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
import tarfile

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
		if verbose:
				print "UUID: ", uuid, " TYPE: ", asset_type
		return [uuid, asset_type]

def parse_object_name(file, verbose):
		name = os.path.basename(file).split("_")[0]
		xx = os.path.basename(file).split("-")[0].split("_")[1]
		yy = os.path.basename(file).split("-")[1]
		zz = os.path.basename(file).split("-")[2].split("__")[0]
		uuid = os.path.basename(file).split("__")[1].split(".")[0]
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



if __name__=="__main__":
        main()


