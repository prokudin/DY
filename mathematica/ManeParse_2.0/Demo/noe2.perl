# ============================================================
# ============================================================
#   (Sample PERL script)        sample.perl    
#  
#   To run, enter: 
#                  perl sample.perl
#
#   This script prompts the user for a filename.
#   It performs the substitutions: 
#      s/e/ 10^ /g;
#      s/E/ 10^ /g;
#   which globally replaces "e" and "E" with " 10^ "
#   and then writes the changed file 
#   to an output file (currently t.t)
#   
#   If you ever have to do some non-interactive changes,
#   or want to do file I/O in Perl, this will save you 
#   a few hours. It also has some debugging features. 
#   
# ============================================================

#!/usr/bin/perl

# ====== This allows you to choose the input file 
#print "INPUT file name? \n";
#$name = <STDIN>;
#$name = "bug3.txt";
#print "INPUT file name is:",$name;
#open(IN,$name) || die " error in input file";
$fileIn = @ARGV[0];
open(IN,$fileIn) || die " error in input file";

# ====== This allows you to choose the output file 
#print "OUTPUT file name? \n";
#$name = <STDIN>;
#print "OUTPUT file name is:",$name;
#open(OUT,">$name") || die " error in output file";


# ====== This hardwires the output file a "t.t"
#open(OUT,">t.t") || die " error in output file";

# ====== This hardwires the output file a given in the command line
$fileOut = @ARGV[1];
open(OUT,">$fileOut") || die " error in output file";

# ====== Initialization
$n=1;
$line=0;
$debug=0;  # Debug flag: 0= no printout; ne 0: printout
print " \n";

# ====== Start the main loop: 
while(<IN>) {
#while(<>) {

   $n=$n+1;
   $line=$line+1;
   $diff=0;


# ====== This is the core: make subs and printout
#   s/e/ 10^ /g;
#   s/E/ 10^ /g;
#   s/-/E-/g;
#   s/EE/E/g;
   my $before=$_;
   s/(\d)(-|\+)(\d)/$1E$2$3/g;
   my $after=$_;
   if($before ne $after){$diff=1};
#   s/EE/E/g;

   print  OUT $_; #  THIS PRINTS TO OUTPUT FILE: 

# ====== end of  core:  

# ====== PRINT STUFF GOES HERE: 
   if(($debug ne 0) or ($diff ne 0 )){
           print " \n";
	   print "\# $line ====================================== \n";
	   if($diff ne 0){ print " ********** DIFFERENT \n";};
           print "     ",$before;
           print "     "," -------------------------------------- \n";
           print "     ",$after;
	   $diff=0;
   }  #==== END OF DEBUG LOOP

} # ====== End the main loop: 

    print "\#$line ====================================== \n";

# ====== Cleanup
close(IN);
close(OUT);

print "All Done!\n";
# ============================================================
# ============================================================
