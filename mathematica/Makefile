# This makefile can be used to build all or some of the sample
# programs. To build all of them, use the command
# 'make all'. To build one, say addtwo, use the command
# 'make addtwo'.

WSLINKDIR = /Applications/Mathematica.app/Contents/SystemFiles/Links/WSTP/DeveloperKit
SYS = MacOSX-x86-64
CADDSDIR = $(WSLINKDIR)/$(SYS)/CompilerAdditions

INCDIR = $(CADDSDIR)
LIBDIR = $(CADDSDIR)

WSPREP = $(CADDSDIR)/wsprep
WSCC = $(CADDSDIR)/wscc

EXTRA_LIBS = -lc++ -framework Foundation

WSTP_LIB = -lWSTPi4


#CPP = $(WSCC)
CPP = g++
FF = gfortran

OPT = -c -O3 -arch x86_64 -m64 -Wall -I./ -I/usr/local/include/ -I${INCDIR}

# Hoppet implements DGLAP
#HOPPETLIB =  -L./hoppet-1.1.5/src  -lhoppet_v1

HOPPETLIB =  -L/usr/local/lib/   -lhoppet_v1

# In order for gfortran to work I need to include this
FLIBS =  -L/usr/local/gfortran/lib/ -lgfortran

# All libraries:
LIB =  $(FLIBS) $(HOPPETLIB) -L${LIBDIR} ${WSTP_LIB} ${EXTRA_LIBS}

#hoppet
#hoppet_cpp.exe: hoppet_cpp.o
#	$(CPP)  -o hoppet_cpp.exe hoppet_cpp.o \
#	$(LIB)
hoppet_cpp.exe:
		$(WSCC) -o hoppet_cpp.exe hoppet.tm hoppet_cpp.o $(LIB)

#this is the MAIN file almost all definitions are here!
hoppet_cpp.o:	hoppet_cpp.cpp hoppet_cpp.h
		$(CPP) $(OPT) $(CFLAGS) -o $@ hoppet_cpp.cpp
		@echo "..................done hoppet_cpp"


#hoppet_cpp: hoppet_cpp.o
#		    ${CC} -I${INCDIR} hoppet_cpp.o -L${LIBDIR} ${WSTP_LIB} ${EXTRA_LIBS} -o $@

clean:
	rm *.exe
	rm *.o
