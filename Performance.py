# coding=UTF-8

## @package Performance
# Performance script is listing all the
# necessary formula for calculate performance of our system
# 
# From: BVES: Effizienzleitfaden für PV-Speichersysteme (Version 2.0.1) part 4.9
#       You can find this file on: https://www.bves.de/technische-dokumente/
#
# requires: numpy
#
# Date created: 2022-08-18
# Author: MarcAndreC16

import numpy

def efficiency(P_A,P_P_B):
    """
    Ratio of the energy extracted by the DUT A to the energy theoretically provided by B 
    Arguments:
        P_A: array (W), power drawn from the device under test A
        P_B: array (W), Power theoretically provided by B
    Returns:
        η : efficiency
    """
    return numpy.trapz(P_A)/numpy.trapz(P_B)

# https://numpy.org/doc/stable/reference/generated/numpy.trapz.html#

def energy(P,tM):
    """
    Arguments:
        P = array (W), power/Leistung
        tM = float (h), Periode
    Returns:
        E: energy (Wh) during periode tM
    """
    return numpy.trapz(P,None,tM/numpy.size(P))

def Capacity(I,tM):
    """
    Arguments:
        I = array (A), 
        tM = float (h), Periode
    Returns:
        C: Capacity (Ah) during periode tM
    """
    return numpy.trapz(I,None,tM/numpy.size(P))



# P1 = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# P2 = [ 10, 9 ,8 ,7 ,6 ,5, 4 ,3 ,2 ,1]
# print(formula_1(P1, P2))
# print(formula_2(P1, P2,1))
# print(energy(P1, 0.5))