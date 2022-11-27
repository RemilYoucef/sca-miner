import Pair
import math
import Gamma
import sys


def beta(x, y) :
    return math.exp(Gamma.logGamma(x) + Gamma.logGamma(y) - Gamma.logGamma(x + y))



def regularizedIncompleteBetaFunction(alpha, beta, x) :
    if (x < 0.0 or x > 1.0) :
        raise IllegalArgumentException("Invalid x: " + x)


    ibeta = 0.0
    if (x == 0.0) :
        ibeta = 0.0
    else :
        if (x == 1.0) :
            ibeta = 1.0
        else :
            # Term before continued fraction
            ibeta = math.exp(Gamma.logGamma(alpha + beta) - Gamma.logGamma(alpha) - Gamma.logGamma(beta)
                    + alpha * math.log(x) + beta * math.log(1.0 - x))
            # Continued fraction
            if (x < (alpha + 1.0) / (alpha + beta + 2.0)) :
                ibeta = ibeta * incompleteFractionSummation(alpha, beta, x) / alpha
            else :
                # Use symmetry relationship
                ibeta = 1.0 - ibeta * incompleteFractionSummation(beta, alpha, 1.0 - x) / beta



    return ibeta


def logRegularizedIncompleteBetaFunction(alpha, beta, x) :

    dp = Pair.Pair(0., 0.)
    if (x < 0.0 or x > 1.0) :
        raise IllegalArgumentException("Invalid x: " + x)

    logIbeta = 0.0
    if (x == 0.0) :
        logIbeta = - sys.float_info.max # means infinity
        log1MinusBeta = 0
    else :
        if (x == 1.0) :
            logIbeta = 0
            log1MinusBeta = - sys.float_info.max
        else :
            # Term before continued fraction
            logIbeta = Gamma.logGamma(alpha + beta) - Gamma.logGamma(alpha) - Gamma.logGamma(beta) + alpha * math.log(x) + beta * math.log(1.0 - x)
            # Continued fraction
            if (x < (alpha + 1.0) / (alpha + beta + 2.0)) :
                logIbeta = logIbeta + math.log(incompleteFractionSummation(alpha, beta, x) / alpha)
                if (logIbeta < -800) :
                    log1MinusBeta = 0
                else :
                    log1MinusBeta = math.log(1 - math.exp(logIbeta))

            else :
                # Use symmetry relationship
                log1MinusBeta = logIbeta + math.log(incompleteFractionSummation(beta, alpha, 1.0 - x) / beta)
                if (log1MinusBeta<-800) :
                    logIbeta =0

                else :
                    logIbeta = math.log(1 - math.exp(log1MinusBeta))




    dp.first=logIbeta
    dp.second=log1MinusBeta
    return dp


def incompleteFractionSummation(alpha, beta, x) :
    MAXITER = 500

    aplusb = alpha + beta
    aplus1 = alpha + 1.0
    aminus1 = alpha - 1.0
    c = 1.0
    d = 1.0 - aplusb * x / aplus1
    if (abs(d) < 1e-300) :
        d = 1e-300

    d = 1.0 / d
    h = d
    aa = 0.0
    dele = 0.0
    i,i2 = 1,0
    test = True
    while (test) :
        i2 = 2 * i
        aa = i * (beta - i) * x / ((aminus1 + i2) * (alpha + i2))
        d = 1.0 + aa * d
        if (abs(d) < 1e-300) :
            d = 1e-300

        c = 1.0 + aa / c
        if (abs(c) < 1e-300) :
            c = 1e-300

        d = 1.0 / d
        h *= d * c
        aa = -(alpha + i) * (aplusb + i) * x / ((alpha + i2) * (aplus1 + i2))
        d = 1.0 + aa * d
        if (abs(d) < 1e-300) :
            d = 1e-300

        c = 1.0 + aa / c
        if (abs(c) < 1e-300) :
            c = 1e-300

        d = 1.0 / d
        dele= d * c
        h *= dele
        i+=1
        if (abs(dele- 1.0) < 3.0E-7) :
            test = False

        if (i > MAXITER) :
            test = False
            # logger.error("Beta.incompleteFractionSummation: Maximum number of iterations
            # wes exceeded")


    return h


def inverseRegularizedIncompleteBetaFunction(alpha, beta, p) :


    a1 = alpha - 1.
    b1 = beta - 1.

    if (p <= 0.0) :
        return 0.0


    if (p >= 1.0) :
        return 1.0


    if (alpha >= 1. and beta >= 1.) :
        pp = p if (p < 0.5) else 1. - p
        t = math.sqrt(-2. * math.log(pp))
        x = (2.30753 + t * 0.27061) / (1. + t * (0.99229 + t * 0.04481)) - t
        if (p < 0.5) :
            x = -x

        al = (x * x - 3.) / 6.
        h = 2. / (1. / (2. * alpha - 1.) + 1. / (2. * beta - 1.))
        w = (x * math.sqrt(al + h) / h)- (1. / (2. * beta - 1) - 1. / (2. * alpha - 1.)) * (al + 5. / 6. - 2. / (3. * h))
        x = alpha / (alpha + beta * math.exp(2. * w))
    else :
        lna = math.log(alpha / (alpha + beta))
        lnb = math.log(beta / (alpha + beta))
        t = math.exp(alpha * lna) / alpha
        u = math.exp(beta * lnb) / beta
        w = t + u
        if (p < t / w) :
            x = math.pow(alpha * w * p, 1. / alpha)
        else :
            x = 1. - math.pow(beta * w * (1. - p), 1. / beta)


    afac = -Gamma.logGamma(alpha) - Gamma.logGamma(beta) + Gamma.logGamma(alpha + beta)
    for j in range(10):
        if (x == 0. or x == 1.) :
            return x

        err = regularizedIncompleteBetaFunction(alpha, beta, x) - p
        t = math.exp(a1 * math.log(x) + b1 * math.log(1. - x) + afac)
        u = err / t
        x -= (u / (1. - 0.5 * math.min(1., u * (a1 / x - b1 / (1. - x)))))
        if (x <= 0.) :
            x = 0.5 * (x + t)

        if (x >= 1.) :
            x = 0.5 * (x + t + 1.)

        if (abs(t) < 1.0E-8 * x and j > 0) :
            break


    return x
