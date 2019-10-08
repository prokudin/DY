#include <iostream>
#include <iomanip>
#include <fstream>
#include <math.h>
#include <stdio.h>
#include "hoppet_cpp.h"


using namespace std;

const double PI     = 3.1415926543; // Pi
const double fourpi = 4.0 * PI ;
const double nf = 5; //2014
const double LamQCD = 0.225; //2014

const double beta_0 = 11.0 - 2.0*nf/3.0;
const double beta_1 = 102. - nf*38.0/3.0;


double AlphaS(double mu){
// Uncomment below for NLO expression

/*
return fourpi/beta_0/log(mu*mu/LamQCD/LamQCD) * ( 1 - beta_1/beta_0/beta_0*log(log(mu*mu/LamQCD/LamQCD))/log(mu*mu/LamQCD/LamQCD));
*/

//return fourpi/beta_0/log(mu*mu/LamQCD/LamQCD); // MAIN

return fourpi/beta_0/log(mu*mu/LamQCD/LamQCD) * ( 1. - beta_1/beta_0/beta_0*log(log(mu*mu/LamQCD/LamQCD))/log(mu*mu/LamQCD/LamQCD)); // PENG 2014

}


//Settings for hoppet:
void set_hoppet( void ){ // this function will set hoppet correctly

int    dummy = 0;


//      ! start the dglap evolution/convolution package
double   ymax  = 12.;        //      ! max value of ln 1/x
double   dy    = 0.1;        //     ! the internal grid spacing (smaller->higher accuarcy)
                               // ! 0.1 should provide at least 10^{-3} accuracy
//   double   Qmin  = sqrt(0.3);  //   ! smallest Q value in tabulation
//   double   Qmin  = 3.2;  //   ! smallest Q value in tabulation
//   double   Qmin  = C1/bmax;  //   ! smallest Q value in tabulation
double   Qmin  = 0.5;  //   ! smallest Q value in tabulation
double   Qmax  = 1.e+5;       // ! largest Q value in tabulation
double   dlnlnQ = dy/4.;     // ! tabulation spacing in dlnlnQ (dy/4 recommended)
int   nloop  = 1;            // ! the number of loops to initialise (max=3!)
int   order  = -6;           // ! numerical interpolation order (-6 is a good choice)

//   ! change the ipdf and scheme to select different pdfs
//   int  ipdf = 1;               // ! 1=f1, 2=f1Tp1, 3=g1, 4=g1T1, 5=h1,
                               // ! 6=h1p1, 7=h1Lp1, 8=h1Tp1, 9=H1p1
int   scheme = 5;            // ! 1=unpol-MSbar, 2=unpol-DIS, 3=Pol-MSbar,
                               // ! 4=frag, 5=TransMsbar, 6=SiversMsbar
//     int   scheme = 1;            // ! 1=unpol-MSbar, 2=unpol-DIS, 3=Pol-MSbar,
                               // ! 4=frag, 5=TransMsbar, 6=SiversMsbar

// NOTE NO DUMMY VARIABLE NEEDED IN HOPPET-1-15!!!! CHECK THIS
//      ! call this once at the beginning of your program
//   hoppetStartExtended(ymax,dy,Qmin,Qmax,dlnlnQ,nloop,order,
//                              scheme,dummy);
// NOTE: new hoppet
  hoppetStartExtended(ymax,dy,Qmin,Qmax,dlnlnQ,nloop,order,
                             scheme);


  cout <<  "Splitting functions initialised!" << endl;

//      ! tell hoppet to use a variable flavour number scheme with
//      ! the following c,b,t quark masses
//      hoppetSetVFN(1.4,4.5,175);

//      ! set the initial scale and the coupling there (in general the PDF
//      ! and coupling may be specified at different scales -- this is not
//      ! done here) and
//      double asQ0 =  0.706862, Q0=sqrt(0.3);
//      double asQ0 =  0.13939, Q0=91.187;
//      double asQ0 = 0.127, Q0=91.1876;

     double Q0 = sqrt(2.4), asQ0 = AlphaS(Q0);
     //cout << "alphas0 " << asQ0 << endl;
     //cout << "alphaMz" << AlphaS(91.1876) << endl;
     //hold(true);

//      ! the ratio xmu = mu_F/mu_R to be used in the evolution.
     double xmu  = 1.0;

//      ! carry out the evolution to create a tabulation, corresponding
//      ! to the initial condition pdf_init(...) given below
//      hoppetEvolve(asQ0,Q0,nloop,xmu,pdf_init,Qmin,dummy);
//NOTE new hoppet for TRANSVERSITY and COLLINS:
     hoppetEvolve(asQ0,Q0,nloop,xmu,pdf_init,Q0); // FENG 2014 COLLINS



//      ! alternatively if you need to repeat the same evolution on very
//      ! many pdf sets, used a cached evolution (set up once, use many times
//      ! and gain a factor 3-4 in speed.
//      !call hoppetPreEvolve(asQ0,Q0,nloop,xmu,Q0)
//      !call hoppetCachedEvolve(evolvePDF)
     cout<< "Evolution done!" << endl;
}

//Settings for hoppet:->reset evolution when parameters are changed
void reset_hoppet( void ){ // this function will set hoppet correctly

     int   nloop  = 1;            // ! the number of loops to initialise (max=3!)

     double Q0 = sqrt(2.4), asQ0 = AlphaS(Q0);
//      ! the ratio xmu = mu_F/mu_R to be used in the evolution.
     double xmu  = 1.0;

//NOTE new hoppet for TRANSVERSITY and COLLINS:
     hoppetEvolve(asQ0,Q0,nloop,xmu,pdf_init,Q0); // FENG 2014 COLLINS
     cout<< "Evolution reset done!" << endl;
}


//----------------------------------------------------------------------
// the initial condition for TMDs
void  pdf_init(const double & x, const double & Q,  double * pdf) {


// MAIN CHOICE FOR 2015
 pdf[-3+6] = 0.; //strange
 pdf[ 3+6] = 0.;//anti_strange
 pdf[ 2+6] = x*(1-x) ;  // x*UP
 pdf[-2+6] = x*(1-x); //x*DOWN
// MAIN CHOICE FOR 2015




// this part is for Collins FF:
 pdf[ 6+6] = 0.;
 pdf[-6+6] = 0.;
 pdf[ 5+6] = 0.;
 pdf[-5+6] = 0.;
 pdf[ 4+6] = 0.;
 pdf[-4+6] = 0.;


 pdf[ 1+6] = 0.; // Collins H(3) up == FAV(z) NB collins = 2 N x^a (1-x)^b  //U->pi+

 pdf[-1+6] = 0.; // Collins H(3) down == UNFAV(z) UBAR --> pi+
 pdf[3+6] = 0.; // Collins H(3) strange == UNFAV1(z) strange --> pi+
//NOTE HOPPET EVOLVES X * DISTRIBUTION(X) !!!!!
 pdf[-3+6] = 0.;
//ATTENTION NOTE NOTE:
//ATTENTION!!!!!!
// HOPPEN DOES NOT EVOLVE pdf[ 6+6], I DO NOT KNOW WHY!!!!!!
//ATTENTION
}



//========================================================= main
int main(int argc, char *argv[])
{

  set_hoppet(); // DON'T FORGET TO SET HOPPET

  return WSMain(argc, argv);
}
