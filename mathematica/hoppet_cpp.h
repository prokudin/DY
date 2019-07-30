/* Alexei Prokudin 31/01/2009        */

#ifndef __HOPPET_H__
#define __HOPPET_H__



#ifndef __HOPPET_V1__
#include "hoppet_v1.h"
#include "/Applications/Mathematica.app/Contents/Frameworks/wstp.framework/Versions/4.36/Headers/wstp.h"
#endif

// the initial condition WILL BE USED IN PDF FITTING
void  pdf_init(const double & x,
                   const double & Q,
                   double * pdf);

void set_hoppet( void );

void reset_hoppet( void );

double AlphaS(double mu);

#endif //ifndef __HOPPET_H__
