#include "../src/hoppet_v1.h"
#include<iostream>
#include<cmath>
#include<cstdio>

using namespace std;


// definition of the initial condition function
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf);


//----------------------------------------------------------------------
int main () {

    
//     ! start the dglap evolution/convolution package 
   double   ymax  = 12.;        //      ! max value of ln 1/x
   double   dy    = 0.1;        //     ! the internal grid spacing (smaller->higher accuarcy)
                                // ! 0.1 should provide at least 10^{-3} accuracy 
   double   Qmin  = 1.;  //   ! smallest Q value in tabulation
   double   Qmax  = 1e+4;       // ! largest Q value in tabulation
   double   dlnlnQ = dy/4.;     // ! tabulation spacing in dlnlnQ (dy/4 recommended)
   int   nloop  = 1;            // ! the number of loops to initialise (max=3!)
   int   order  = -6;           // ! numerical interpolation order (-6 is a good choice)

   int   scheme = 5;            // ! 1=unpol-MSbar, 2=unpol-DIS, 3=Pol-MSbar, 
                                // ! 4=frag, 5=TransMsbar

//      ! call this once at the beginning of your program
   hoppetStartExtended(ymax,dy,Qmin,Qmax,dlnlnQ,nloop,order,
                              scheme);
   cout <<  "Splitting functions initialised!" << endl;

//   double dy    = 0.1;
//   int    nloop = 1;
// 
//   // initialise with NNLO, VFN
//   hoppetStart(dy, nloop);
  // hoppetSetPoleMassVFN(1.414213563, 4.5, 175.0);
  
  // evolve the initial condition
  double asQ0 = 0.35, Q0=sqrt(2.0);
  hoppetEvolve(asQ0, Q0, nloop, 1.0, heralhc_init, Q0);
  // alternatively preprepare an evolution and then use its cached version.x
  //hoppetPreEvolve(asQ0, Q0, nloop, 1.0, Q0);
  //hoppetCachedEvolve(heralhc_init);

  // output the results
  double pdf[13];
  double xvals[9]={1e-5,1e-4,1e-3,1e-2,0.1,0.3,0.5,0.7,0.9};
  double Q = 100;
  printf("           Evaluating PDFs at Q = %8.3f GeV\n",Q);
  printf("    x      u-ubar      d-dbar    2(ubr+dbr)    c+cbar       gluon\n");
  for (int ix = 0; ix < 9; ix++) {
    hoppetEval(xvals[ix], Q, pdf);
    printf("%7.1E %11.4E %11.4E %11.4E %11.4E %11.4E\n",xvals[ix],
           pdf[6+2]-pdf[6-2], 
           pdf[6+1]-pdf[6-1], 
           2*(pdf[6-1]+pdf[6-2]),
           (pdf[6-4]+pdf[6+4]),
           pdf[6+0]);
  }
}


//----------------------------------------------------------------------
// the initial condition, we can include 1/2 (f(x,q0) + g(x,q0)) here as well
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf) {
  double uv, dv;
  double ubar, dbar;
  double N_g=1., N_ls=1.;
  double N_uv=5., N_dv=1.;
  double N_db=N_ls/2;

  uv = N_uv * pow(x,0.8) * pow((1-x),3);
  dv = 0.*N_dv * pow(x,0.8) * pow((1-x),4);
  dbar = 0.*N_db * pow(x,-0.1) * pow(1-x,6);
  ubar = 0.*dbar * (1-x);

  pdf[ 0+6] = 0.*N_g * pow(x,-0.1) * pow(1-x,5);
  pdf[-3+6] = 0.*0.2*(dbar + ubar);
  pdf[ 3+6] = 0.*pdf[-3+6];
  pdf[ 2+6] = uv ;
  pdf[-2+6] = 0.*ubar;
  pdf[ 1+6] = 0.*dv + dbar;
  pdf[-1+6] = 0.*dbar;

  pdf[ 4+6] = 0;
  pdf[ 5+6] = 0;
  pdf[ 6+6] = 0;
  pdf[-4+6] = 0;
  pdf[-5+6] = 0;
  pdf[-6+6] = 0;
}

