import Beta
import math
import Pair
import numpy as np
import sys


def log2(nb) :
    return math.log(nb,2)


def logBase(base, nb) :
    return math.log(nb) / math.log(base)


def getLogGeometric(param, value) :
    if (value < 0) :
        return -sys.float_info.max # means infinity


    if (param == 1) :
        if (value == 0) :
            return 0

        else :
            return -sys.float_info.max



    return value*math.log(1-param)+math.log(param)


def getGeometric(param, value) :
    if (value < 0) :
        return 0

    temp1=math.pow(1 - param, value) * param

    return temp1

def getCdfGeometric(param,value) :
    if (value<0) :
        return 0

    temp1=1.-math.pow(1.-param, value+1)

    return temp1


def getLogCdfIntervalGeometric(param,minKIncluded,maxKExcluded) :
    temp=1.- ((1-param) ** (maxKExcluded-minKIncluded))
    return minKIncluded * math.log(1-param) + np.log(temp)


def getCdfIntervalGeometric(param,minKIncluded,maxKExcluded) :
    temp1=getCdfGeometric(param, maxKExcluded-1)
    temp2
    if (minKIncluded==0) :
        temp2=0

    else :
        temp2=getCdfGeometric(param, minKIncluded-1)

    return temp1-temp2



def getLogCdfBinomial(n, k, p,dp) :
    if (k<0 or n<0 or p<0  or p>1) :
        raise RuntimeException("n and k must be positive and p must be between 0 and 1")

    #long startTime = System.nanoTime()

    temp1=Beta.logRegularizedIncompleteBetaFunction(n - k, k + 1, 1 - p)
    #long endTime = System.nanoTime()
    #dp.statistics.timeBinomial+=(endTime-startTime)
    #dp.statistics.nbCallsBetaFunction+=1

    return temp1


def getCdfBinomial(n, k, p) :
    if (k<0 or n<0 or p<0  or p>1) :
        raise RuntimeException("n and k must be positive and p must be between 0 and 1")

    if (k>=n) :
        return 1

    temp1=Beta.regularizedIncompleteBetaFunction(n - k, k + 1, 1 - p)

    return temp1


def getLogCdfIntervalBinomial(n,p, minKIncluded,maxKExcluded,dp) :

    tempD1=Pair.Pair(0., 0.)
    tempD2=Pair.Pair(0., 0.)

    if (maxKExcluded<=minKIncluded) :
        return -sys.float_info.max


    if (maxKExcluded-1>=n) :
        tempD1.first=0.
        tempD1.second=-sys.float_info.max

    else :
        tt=getLogCdfBinomial(n, maxKExcluded-1, p,dp)
        tempD1.first=tt.first
        tempD1.second=tt.second



    if (minKIncluded-1<0) :
        tempD2.first=-sys.float_info.max
        tempD2.second=0.

    else :
        #long startTime = System.nanoTime()
        tt=getLogCdfBinomial(n, minKIncluded-1, p,dp)
        tempD2.first=tt.first
        tempD2.second=tt.second
        #long endTime = System.nanoTime()
        #dp.statistics.timeBinomial+=(endTime-startTime)



    if (((maxKExcluded+1.)/(n+3))>p) :
        # work with 1-F(b) CDF
        temp=tempD2.second
        temp3=0
        if (tempD1.second!=-sys.float_info.max) :
            temp3=math.log(1.-math.exp(tempD1.second-tempD2.second))

        temp=temp+temp3


    else :
        # work with F(b)
        temp=tempD1.first
        temp3=0
        if (tempD2.first!=0) :
            if tempD2.first == -sys.float_info.max and tempD1.first == -sys.float_info.max :
                temp3 = -sys.float_info.max
            else :
                temp3=math.log(1-math.exp(tempD2.first-tempD1.first))


        temp=temp+temp3



    return temp



def getCdfIntervalBinomial(n,p, minKIncluded,maxKExcluded) :
    if (maxKExcluded-1>=n) :
        temp1=1

    else :
        #temp1=Binomial.cdf((int)maxKExcluded-1,(int) n, p)
        temp1=getCdfBinomial(n, maxKExcluded-1, p)


    if (minKIncluded==0) :
        temp2=0

    else :
        #temp2=Binomial.cdf( (int)minKIncluded-1,(int)n, p)
        temp2=getCdfBinomial(n, minKIncluded-1, p)

    return temp1-temp2


def getBinomial(n, k, p) :
    if (k < 0 or n < 0 or k > n) :
        return 0

    temp1=k*math.log(p)+(n-k)*math.log(1.-p)+getLogNChooseK(n, k)

    temp1=math.exp(temp1)
    return temp1


def getLogNChooseK(n, k) :
    if (k > n) :
        raise RuntimeException("calculation not possible")

    if (k < 0 or n < 0) :
        raise RuntimeException("calculation not possible")

    if (k == 0 or k == n) :
        return 0


    if (n <= 10) :
        comb = 1

        for i in range(1,n-k+1) :
            comb /= i

        for i in range(k+1,n+1) :
            comb *= i


        return math.log(comb)

    else :
        logComb=Gamma.logGamma(n+1)-Gamma.logGamma(k+1)-Gamma.logGamma(n-k+1)
        return logComb
