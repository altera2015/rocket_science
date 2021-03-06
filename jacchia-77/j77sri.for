C*********************************************************************C
C*                                                                   *C
C*  j77sri.for                                                       *C
C*                                                                   *C
C*  Written by:  David L. Huestis, Molecular Physics Laboratory      *C
C*                                                                   *C
C*  Copyright (c) 1999,2002  SRI International                       *C
C*  All Rights Reserved                                              *C
C*                                                                   *C
C*  This software is provided on an as is basis; without any         *C
C*  warranty; without the implied warranty of merchantability or     *C
C*  fitness for a particular purpose.                                *C
C*                                                                   *C
C*********************************************************************C
C*
C*      Given an exospheric temperature, this subroutine returns model 
C*      atmospheric altitude profiles of temperature, the number 
C*      densities of N2, O2, O, Ar, He, H, the sum thereof, and the 
C*      molecular weight.
C*
C*      For altitudes of 90 km and above, we use the 1977 model of 
C*      Jacchia [Ja77].  H-atom densities are returned as non-zero 
C*      for altitudes of 150 km and above if the maximum altitude 
C*      requested is 500 km or more.
C*
C*      For altitudes of 85 km and below we use the 1976 U. S. Standard
C*      Atmosphere, as coded by Carmichael [Ca99], which agrees with 
C*      Table III.1 (pp 422-423) of Chamberlain and Hunten [CH87] 
C*	and Table I (pp 50-73) of the "official" U.S. Standard
C*	Atmosphere 1976 [COESA76].
C*
C*      For altitudes from 86 to 89 km we calculate the extent of 
C*      oxygen dissociation and the effective molecular weight by a 
C*      polynomial fit connecting the O-atom mole fraction at 86 km 
C*      from Chamberlain and Hunten Table III.4 (p 425) [CH87] and 
C*      the O-atmom mole fractions at 90, 91, and 92 km from Jacchia 
C*      1977 [Ja77] for an exospheric temperature of 1000 K.  For 
C*      graphical continunity, the same formulas are used to calculate
C*      O-atom densities for altitudes of 85 km and below.
C*
C*  USAGE:
C*              program main
C*              integer maxz    ! INPUT:  highest altitude (km)
C*              parameter (maxz=2500)   ! for example
C*              real Tinf,      ! INPUT:  exospheric temp (K)
C*           *    Z(0:maxz),    ! OUTPUT: altitude (km)
C*           *    T(0:maxz),    ! OUTPUT: temperature (K)
C*           *    CN2(0:maxz),  ! OUTPUT: [N2] (1/cc)
C*           *    CO2(0:maxz),  ! OUTPUT: [O2] (1/cc)
C*           *    CO(0:maxz),   ! OUTPUT: [O] (1/cc)
C*           *    CAr(0:maxz),  ! OUTPUT: [Ar] (1/cc)
C*           *    CHe(0:maxz),  ! OUTPUT: [He] (1/cc)
C*           *    CH(0:maxz),   ! OUTPUT: [H] (1/cc)
C*           *    CM(0:maxz),   ! OUTPUT: [M] (1/cc)
C*           *    WM(0:maxz)    ! OUTPUT: molecular weight (g)
C*              call j77sri(maxz,Tinf,Z,T,CN2,CO2,CO,CAr,CHe,CH,CM,WM)
C*              end
C*
C*  REFERENCES:
C*
C*      Ca99    R. Carmichael, "Fortran (90) coding of Atmosphere,"
C*              (http://www.pdas.com/atmosf90.htm, March 1, 1999).
C*
C*      CH87    J. W. Chamberlain and D. M. Hunten, "Theory of 
C*              Planetary Atmospheres," (Academic Press, NY, 1987).
C*
C*	COESA76	U.S. Committee on Extension to the Standard
C*		Atmosphere, "U.S. Standard Atmospheres 1976"
C*		(USGPO, Washington, DC, 1976).
C*
C*      Ja77    L. G. Jacchia, "Thermospheric Temperature, Density 
C*              and Composition: New Models," SAO Special Report No.
C*              375 (Smithsonian Institution Astrophysical 
C*              Observatory, Cambridge, MA, March 15, 1977).
C*
C*  EDIT HISTORY:
C*
C*	11-27-02  DLH	Repair temperatures 12-47 km (add 0.5 K)
C*
C*      10-10-99  DLH   Original j77sri.for with [O] for z .lt. 90 km
C*
C*      09-xx-99  DLH   Trial versions called j77.for
C*
C**********************************************************************

        subroutine j77sri( maxz, Tinf, 
     *    Z, T, CN2, CO2, CO, CAr, CHe, CH, CM, WM )

        parameter (pi2=1.57079632679)
        parameter (wm0=28.96, wmN2=28.0134, wmO2=31.9988,
     *    wmO=15.9994, wmAr=39.948, wmHe=4.0026, wmH=1.0079)
        parameter (qN2=0.78110, qO2=0.20955, qAr=0.009343,
     *    qHe=0.000005242)
        dimension Z(0:maxz), T(0:maxz), CN2(0:maxz), CO2(0:maxz), 
     *    CO(0:maxz), CAr(0:maxz), CHe(0:maxz), CH(0:maxz), 
     *    CM(0:maxz), WM(0:maxz)
        dimension E5M(0:10), E6P(0:10)

        do 500 iz = 0, maxz
          Z(iz) = iz
          CH(iz) = 0

C  --------------------------------------------------------------------
C
C       For Z .lt. 86, use U.S. Standard Atmosphere 1976 with added [O].
C
C  --------------------------------------------------------------------

          if( iz .le. 85 ) then
            h = Z(iz)*6369.0/(Z(iz)+6369.0)
            if( iz .le. 32 ) then
              if( iz .le. 11 ) then
                hbase = 0.0
                pbase = 1.0
                tbase = 288.15
                tgrad = -6.5
                go to 110
              else if( iz .le. 20 ) then
                hbase = 11
                pbase = 2.233611E-1
                tbase = 216.65
                tgrad = 0
                go to 120
              else
                hbase = 20.0
                pbase = 5.403295E-2
                tbase = 216.65
                tgrad = 1
                go to 110
              end if
            else if( iz .le. 51 ) then
              if( iz .le. 47 ) then
                hbase = 32.0
                pbase = 8.5666784E-3
                tbase = 228.65
                tgrad = 2.8
                go to 110
              else
                hbase = 47
                pbase = 1.0945601E-3
                tbase = 270.65
                tgrad = 0
                go to 120
              end if
            else if( iz .le. 71 ) then
              hbase = 51.0
              pbase = 6.6063531E-4
              tbase = 270.65
              tgrad = -2.8
              go to 110
            else
              hbase = 71.0
              pbase = 3.9046834E-5
              tbase = 214.65
              tgrad = -2.0
              go to 110
            end if

110         continue
            T(iz) = tbase + tgrad*(h-hbase)
            x = (tbase/T(iz))**(34.163195/tgrad)
            go to 130
120         T(iz) = tbase
            x = exp(-34.163195*(h-hbase)/tbase)
130         continue
            CM(iz) = 2.547E19*(288.15/T(iz))*pbase*x
            go to 400

C  --------------------------------------------------------------------
C
C       For 85 .lt. Z .lt. 90, integrate barometric equation with 
C       fudged molecular weight
C
C  --------------------------------------------------------------------

          else if( iz .le. 89 ) then
            T(iz) = 188.0
            y = 10.0**(-3.7469+(iz-85)*(0.226434-(iz-85)*5.945E-3))
            WM(iz) = wm0*(1-y)
            CM(iz) = CM(iz-1)*(T(iz-1)/T(iz))*(WM(iz)/WM(iz-1))
     *          * exp( - 0.5897446*( 
     *            (WM(iz-1)/T(iz-1))*(1+Z(iz-1)/6356.766)**(-2)
     *            + (WM(iz)/T(iz))*(1+Z(iz)/6356.766)**(-2) ))
            go to 400

C  --------------------------------------------------------------------
C
C       For Z .gt. 89, use Jacchia 1977
C
C  --------------------------------------------------------------------

          else
            if( iz .le. 90 ) then
              T(iz) = 188.0
            else if( Tinf .lt. 188.1 ) then
              T(iz) = 188.0
            else
              x = 0.0045 * (Tinf-188.0)
              Tx = 188.0 + 110.5 * alog( x + sqrt(x*x+1.0) )
              Gx = pi2*1.9*(Tx - 188.0)/(125.0-90.0)
              if( iz .le. 125 ) then
                T(iz) = Tx + ((Tx-188.0)/pi2)
     *            * atan( (Gx/(Tx-188.0))*(Z(iz)-125.0)
     *              * (1.0 + 1.7*((Z(iz)-125.0)/(Z(iz)-90.0))**2))
              else
                T(iz) = Tx + ((Tinf-Tx)/pi2)
     *            * atan( (Gx/(Tinf-Tx))*(Z(iz)-125.0)
     *              * (1.0 + 5.5e-5*(Z(iz)-125.0)**2))
              endif
            end if
            if( iz .le. 100 ) then
              x = iz - 90
              E5M(iz-90) = 28.89122 + x*(-2.83071E-2 
     *           + x*(-6.59924E-3 + x*(-3.39574E-4
     *           + x*(+6.19256E-5 + x*(-1.84796E-6) ))))
              if( iz .le. 90 ) then
                E6P(0) = 7.145E13*T(90)
              else
                G0 = (1+Z(iz-1)/6356.766)**(-2)
                G1 = (1+Z(iz)/6356.766)**(-2)
                E6P(iz-90) = E6P(iz-91)*exp( - 0.5897446*( 
     *            G1*E5M(iz-90)/T(iz) + G0*E5M(iz-91)/T(iz-1) ) )
              end if
              x = E5M(iz-90)/wm0
              y = E6P(iz-90)/T(iz)
              CN2(iz) = qN2*y*x
              CO(iz) = 2.0*(1.0 - x)*y
              CO2(iz) = (x*(1.0+qO2)-1.0)*y
              CAr(iz) = qAr*y*x
              CHe(iz) = qHe*y*x
              CH(iz) = 0
            else
              G0 = (1+Z(iz-1)/6356.766)**(-2)
              G1 = (1+Z(iz)/6356.766)**(-2)
              x =  0.5897446*( G1/T(iz) + G0/T(iz-1) )
              y = T(iz-1)/T(iz)
              CN2(iz) = CN2(iz-1)*y*exp(-wmN2*x)
              CO2(iz) = CO2(iz-1)*y*exp(-wmO2*x)
              CO(iz)  =  CO(iz-1)*y*exp(-wmO*x)
              CAr(iz) = CAr(iz-1)*y*exp(-wmAr*x)
              CHe(iz) = CHe(iz-1)*(y**0.62)*exp(-wmHe*x)
              CH(iz) = 0
            end if
            go to 500
          end if
          go to 500

C  --------------------------------------------------------------------
C
C       Calculate O/O2 dissociation for Z .lt. 90 km
C
C  --------------------------------------------------------------------

400       continue
          y = 10.0**(-3.7469+(iz-85)*(0.226434-(iz-85)*5.945E-3))
          x = 1 - y
          WM(iz) = wm0*x
          CN2(iz) = qN2*CM(iz)
          CO(iz) = 2.0*y*CM(iz)
          CO2(iz) = (x*qO2-y)*CM(iz)
          CAr(iz) = qAr*CM(iz)
          CHe(iz) = qHe*CM(iz)
          CH(iz) = 0
500     continue

C  --------------------------------------------------------------------
C
C       Add Jacchia 1977 empirical corrections to [O] and [O2]
C
C  --------------------------------------------------------------------

        do iz = 90, maxz
          CO2(iz) = CO2(iz)
     *          *( 10.0**(-0.07*(1.0+tanh(0.18*(Z(iz)-111.0)))) )
          CO(iz) = CO(iz)
     *          *( 10.0**(-0.24*exp(-0.009*(Z(iz)-97.7)**2)) )
          CM(iz) = CN2(iz)+CO2(iz)+CO(iz)+CAr(iz)+CHe(iz)+CH(iz)
          WM(iz) = ( wmN2*CN2(iz)+wmO2*CO2(iz)+wmO*CO(iz)
     *          +wmAr*CAr(iz)+wmHe*CHe(iz)+wmH*CH(iz) ) / CM(iz)
        end do

C  --------------------------------------------------------------------
C
C       Calculate [H] from Jacchia 1997 formulas if maxz .ge. 500.
C
C  --------------------------------------------------------------------

        if( maxz .ge. 500 ) then
          phid00 = 10.0**( 6.9 + 28.9*Tinf**(-0.25) ) / 2.E20
          phid00 = phid00 * 5.24E2
          H_500 = 10.0**( -0.06 + 28.9*Tinf**(-0.25) )
          do iz=150,maxz
            phid0 = phid00/sqrt(T(iz))
            WM(iz) = wmH*0.5897446*( (1.0+Z(iz)/6356.766)**(-2) )
     *          / T(iz) + phid0
            CM(iz) = CM(iz)*phid0
          end do
          y = WM(150)
          WM(150) = 0
          do iz=151,maxz
            x = WM(iz-1) + (y+WM(iz))
            y = WM(iz)
            WM(iz) = x
          end do
          do iz = 150, maxz
            WM(iz) = exp( WM(iz) ) * ( T(iz)/T(150) )**0.75
            CM(iz) = WM(iz)*CM(iz)
          end do
          y = CM(150)
          CM(150) = 0
          do iz=151,maxz
            x = CM(iz-1) + 0.5*(y+CM(iz))
            y = CM(iz)
            CM(iz) = x
          end do

          do iz = 150, maxz
            CH(iz) = ( WM(500)/WM(iz) ) * (H_500 - (CM(iz)-CM(500)) )
          end do
          
          do iz=150, maxz
            CM(iz) = CN2(iz)+CO2(iz)+CO(iz)+CAr(iz)+CHe(iz)+CH(iz)
            WM(iz) = ( wmN2*CN2(iz)+wmO2*CO2(iz)+wmO*CO(iz)
     *          +wmAr*CAr(iz)+wmHe*CHe(iz)+wmH*CH(iz) ) / CM(iz)
          end do
        end if

        return
        end

