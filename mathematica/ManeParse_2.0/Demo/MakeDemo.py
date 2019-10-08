#!/usr/bin/env python
"""
This script builds up the demo directories with the relevant PDFs sets.
Send comments, bugs and questions to flyonnet@smu.edu, egodat@smu.edu,
dbclark@smu.edu, or olness@smu.edu
F. 07/15
Created class structure with __main__ to create an executable.
DBC 3 Feb 2016

"""

##############################
# Import the different modules
##############################

#system and file manipulation
import os,sys
#file listing
import glob
#debugger in python
#import pudb
#subprocess
import subprocess as sp
#split command line arguments
import shlex
#split with regular expression
import re

# Fix Python 2.x.
if sys.version_info[0] >= 3:
    try: raw_input = input
    except NameError: pass;


    ######################### 
    # Begin class definitions
    #########################

class MakeDemo(object):
       
 
    def __init__(self):
        ###################################
        # PDFsets needed for the demo files
        ###################################
        self.neededPSets = {
         'CT10': {'Nbsets': 53, 'info': True, 'TobeDownloaded': False,'TobeLinked': False},
         'MSTW2008lo68cl': {'Nbsets': 41, 'info': True, 'TobeDownloaded': False, 'TobeLinked': False},
         'NNPDF30_nlo_as_0118': {'Nbsets': 101, 'info': True, 'TobeDownloaded': False, 'TobeLinked': False},
#        'NNPDF21_lo_as_0119_100': {'Nbsets': 101, 'info': True, 'TobeDownloaded': False, 'TobeLinked': False},
         'ct10.pds': {'Nbsets': 53, 'info': False, 'TobeDownloaded': False,'PDS': True, 'path': '','rootname': 'ct10', 'TobeLinked': False},
         'ctq66m.pds': {'Nbsets': 45, 'info': False, 'TobeDownloaded': False,'PDS': True, 'path': '','rootname': 'ctq66', 'TobeLinked': False},
        }


    #########################
    #Some auxiliary functions
    #########################
    def check_a_pdfset_is_complete(self,key,value,pdata,pds=False):
        #returns True or False according to wether it is a complete PDF set
        #getting the list of files
        if pds : 
            files = glob.glob(pdata+'/'+value['rootname']+'*.pds')
        else :
            files = glob.glob(pdata+key+'/*')
        if files == []:
            return False
        files = [re.split("{}|_|\.".format(pdata+key+'/'),elt)for elt in files]
        files = [elt[-1] if elt[-1] == 'info' else elt[-2] for elt in files]
        try:
            files = [int(elt) if elt != 'info' else elt for elt in files]
        except:
            return False
        #checking that info is in there
        if value['info'] :
            if 'info' in files:
                files.remove('info')
                if sorted(files) == range(value['Nbsets']):
                    return True
                else :
                    return False
            else :
                print("\tError missing `{}.info` file.".format(key))
                return False
        #Else let's check that the files contain all the sets
        elif sorted(files) == range(value['Nbsets']):
                return True
        else :
            return False


    def get_a_pdfset_from_lhapdf(self,key):
        #calls wget to download the corresponding pdfset
        server = "http://www.hepforge.org/archive/lhapdf/pdfsets/6.1"
        p = sp.Popen(shlex.split("wget {}/{}.tar.gz".format(server,key)),stderr =sys.stdout.fileno())
        p.communicate()
        return 


    def get_a_pdsset(self,key):
        #calls wget to download the corresponding pdfset
        server_ctq66,server_ctq10 = "http://hep.pa.msu.edu/cteq/public/6.6/pds/ctq66m.pds.zip","http://hep.pa.msu.edu/cteq/public/ct10_2010/pds/ct10.pds.zip"
        server = server_ctq10 if key =='ct10.pds' else server_ctq66
        p = sp.Popen(shlex.split("wget {}".format(server)),stderr =sys.stdout.fileno())
        p.communicate()
        return 


    def set_up_paths(self):
        #set up the different paths for the demo to work
        listoffiles = [
            'PDF_Sets',
            'PDF_Sets/LHA',
            'PDF_Sets/PDS',
            'PDF_Sets/PDS/ctq66m.pds',
            'PDF_Sets/PDS/ct10.pds',
                ]
        for ll in listoffiles:
            try :
                if not(os.path.isdir(ll)):
                    os.mkdir(ll)
            except OSError :
                print("Error creating {} directory. Check permissions. The demo won't run properly.".format(ll))


    def extract_file_into(self,ffile,into,verbose=False,zip=False):
        #extract the tar.gz into the into directory
        print("Extracting the PDF set {} into {}:".format(ffile,into))
        if not(zip):
            os.popen("tar -xzvf {}.tar.gz -C {}".format(ffile,into))
            print("cleaning up the archive {}.tar.gz".format(ffile))
            os.popen("rm {}.tar.gz".format(ffile))
        else :
            os.popen("unzip {}.zip -d {}".format(ffile.lower(),into))
            print("cleaning up the archive {}.zip".format(ffile))
            todelete = glob.glob(into+"/*w*.pds")
            os.popen("rm {}.zip".format(ffile))
            for ff in todelete : 
                os.popen("rm {}".format(ff))


    def construct_sym_link(self,key,target):
        #Creates a sym link of key into targeT
        print("Creating sym link of {} into {}".format(key,target))
        if not(os.path.isdir(target)):
            os.mkdir(target)
        os.popen("ln -s {}/* {}".format(key,target))


    def run_perl_on_dir(self,key,target,perl):
        #Runs the perl script to fix the Fortran error in CT10 pds files
        print("Fixing bug in {}".format(key))
        if (os.path.isdir(target)):
            files = glob.glob(os.path.abspath(target)+'/*')
            if (os.path.isfile(perl)):
                for elt in files:
                    out = elt+".m"
                    os.popen("perl {} {} {}".format(os.path.abspath(perl),elt,out))
                    os.popen("mv {}.m {}".format(elt, elt))


    ########################
    #End Auxiliary functions
    ########################
    def makeit(self):
        #function to do everything. this facilitates use of __main__ below.
        #DBC 3 Feb 2016
        print("Building the directory structure for the demo...")
        #Checking that lhapdf-config is available
        LHAPDFINSTALLED=False
        try  : 
            p = sp.Popen(shlex.split("lhapdf-config --datadir"),stderr=sp.PIPE,stdout=sp.PIPE)
            pdata,perr = p.communicate()
            if not(perr == '') : 
                print("LHAPDF is not installed or could not be found. Make sure the lhapdf-config is in your `$PATH` variable. Downloading the data set needed for the demo directly...")
            #removing the extra line
            pdata = pdata.replace('\n','/')
            p = sp.Popen(shlex.split("lhapdf-config --version"),stderr=sp.PIPE,stdout=sp.PIPE)
            pversion,perr = p.communicate()
            if not(perr == '') : 
                print("Error while running `lhapdf-config --version` please check that it is available.")
            else :
                #check version is greater than 5
                if (len(pversion) != 0 and int(pversion[0]) > 5) :
                    LHAPDFINSTALLED = True
                else :
                    print("LHAPDF files 6 or greater can be read, downloading the files needed for the demo...")
        except OSError :
            #catching the error
            print("LHAPDF is not installed or could not be found. Make sure the lhapdf-config is in your `$PATH` variable. Downloading the data set needed for the demo directly...")
        #PDS file directory
        understood,setuppaths = False,True
        if setuppaths :
            #set up the path some checks will need to be done
            self.set_up_paths()
            #Let's check before asking for the path that ctq66m and ct10 are not where they are supposed to be
        if not(os.path.isdir('PDF_Sets/PDS/ctq66m.pds') and len(glob.glob('PDF_Sets/PDS/ctq66m.pds/ctq66*.pds')) == self.neededPSets['ctq66m.pds']['Nbsets']):
            understood = False
            while not(understood) : 
                cmdline = raw_input("--> PDS files `ctq66m.pds` is required for the demo to run . Provide if existing the path of this directory otherwise press enter.   ")
                if cmdline == '':
                    understood = True
                elif os.path.isdir(cmdline):
                    self.neededPSets['ctq66m.pds']['path'] = cmdline
                    self.neededPSets['ctq66m.pds']['TobeLinked'] = True
                    understood = True
                elif not(os.path.isdir(cmdline)):
                    print("This directory does not exist, please check: `{}`".format(cmdline))
                else :
                    print("Unknown option. Leave blank if you don't have these files installed.")
        else :
            self.neededPSets['ctq66m.pds']['TobeLinked'] = False
            self.neededPSets['ctq66m.pds']['path']='PDF_Sets/PDS/ctq66m.pds'
        if not(os.path.isdir('PDF_Sets/PDS/ct10.pds') and len(glob.glob('PDF_Sets/PDS/ct10.pds/ct10*.pds')) == self.neededPSets['ct10.pds']['Nbsets']):
            understood = False
            while not(understood) : 
                cmdline = raw_input("--> PDS files `ct10.pds` is required for the demo to run . Provide if existing the path of this directory otherwise press enter.   ")
                if cmdline == '':
                    understood = True
                elif os.path.isdir(cmdline):
                    self.neededPSets['ct10.pds']['path'] = cmdline
                    self.neededPSets['ct10.pds']['TobeLinked'] = True
                    understood = True
                elif not(os.path.isdir(cmdline)):
                    print("This directory does not exist, please check: `{}`".format(cmdline))
                else :
                    print("Unknown option. Leave blank if you don't have these files installed.")
        else :
            self.neededPSets['ct10.pds']['TobeLinked'] = False
            self.neededPSets['ct10.pds']['path']='PDF_Sets/PDS/ct10.pds'
        #1. If lhpadf is installed get the list of the sets and diff it with our list 
        #2. If it is not installed then ask permission and download them 
        for key,val in self.neededPSets.items():
            if not('PDS' in val) : 
                if LHAPDFINSTALLED:
                    if not(self.check_a_pdfset_is_complete(key,val,pdata)) :
                        print("Set {} could not be found in LHAPDF checking in the Demo directory...".format(key))
                        if not(self.check_a_pdfset_is_complete(key,val,'PDF_Sets/LHA/')) :
                            self.neededPSets[key]['TobeDownloaded'] = True
                            print("{} NOT found in `PDF_Sets/LHA/`, downloading it.".format(key))
                        else :
                            print("{} found in `PDF_Sets/LHA/`.".format(key))
                            self.neededPSets[key]['TobeLinked'] = False
                    else :
                        self.neededPSets[key]['TobeLinked'] = True
                else :
                    if not(self.check_a_pdfset_is_complete(key,val,'PDF_Sets/LHA/')) :
                        self.neededPSets[key]['TobeDownloaded'] = True
                    else :
                        self.neededPSets[key]['TobeLinked'] = False
            else :
                if val['path'] != '':
                    if not(self.check_a_pdfset_is_complete(key,val,val['path'],pds=True)):
                        self.neededPSets[key]['TobeDownloaded'] = True
                else :
                    self.neededPSets[key]['TobeDownloaded'] = True
        tobedownloaded = [key for key,val in self.neededPSets.items() if val['TobeDownloaded']]
        if not(tobedownloaded == []):
            print("List of the PDF sets that need to be downloaded:\n\t{}".format("\n\t".join(tobedownloaded)))
        else :
            print("All the pdf files are present.")
        if not(tobedownloaded == []) :
            understood = False
            while not(understood) :
                #ask the permission to download the files
                cmdline = raw_input("--> Do you want to download the PDFsets needed for the demo to run?[Y/N]")
                if cmdline == 'N' or cmdline == 'No' or cmdline == 'NO' or cmdline == 'no':
                    understood = True
                    exit("\tThese PDF sets are required to run the demo, exiting.")
                elif cmdline =='Y' or cmdline == 'y' or cmdline == 'Yes' or cmdline == 'YES' or cmdline == '':
                    understood = True
                    for key in tobedownloaded:
                        if 'PDS' in self.neededPSets[key] :
                            self.get_a_pdsset(key)
                            self.extract_file_into(key,'PDF_Sets/PDS/{}'.format(key),verbose=False,zip=True)
                        else :
                            self.get_a_pdfset_from_lhapdf(key)
                            self.extract_file_into(key,'PDF_Sets/LHA',verbose=False,zip=False)
                else :
                    print("I did not understand! Please answer Y/N!")
        #Creating the links for the sets that already exists or if LHAPDF is installed the PDFsets directory
        tobelinkedLHA = [key for key,value in self.neededPSets.items() 
                if value['TobeLinked'] and not('PDS' in value)]
        tobelinkedPDS = [key for key,value in self.neededPSets.items()
                if value['TobeLinked'] and 'PDS' in value]
        tobelinked = tobelinkedLHA + tobelinkedPDS
        if tobelinked != [] : 
            print("Linking already existing PDF sets: \n\t{}".format('\n\t'.join(tobelinked)))
        else : 
            print("Nothing to be linked.")
        for key in tobelinkedLHA :
            self.construct_sym_link(pdata+key,os.path.abspath('PDF_Sets/LHA/'+key))
        for key in tobelinkedPDS : 
            self.construct_sym_link(os.path.abspath(self.neededPSets[key]['path']), os.path.abspath('PDF_Sets/PDS/'+key))
        #Run perl on CT10
        self.run_perl_on_dir('ct10.pds','PDF_Sets/PDS/ct10.pds','./noe2.perl')
        print("The Demo is ready to be run!")
        return

    def clean(self):
        """
        cleans up the subdirectory structure
        """
        # check if the subdirectory PDF_Sets has been created
        check = len(glob.glob('PDF_Sets')) == 1
        if check:
            try:
                os.popen("rm -rf PDF_Sets").readlines()
            except:
                pass
    
if __name__== "__main__":
    MD = MakeDemo()
    #pudb.set_trace()
    if len(sys.argv) == 2 and sys.argv[-1] == '--clean':
        MD.clean()
    else:
        MD.makeit()

