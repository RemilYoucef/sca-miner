import math

def logGamma(x) :
    tmp = (x - 0.5) * math.log(x + 4.5) - (x + 4.5)
    ser = 1.0 + 76.18009173    / (x + 0)   - 86.50532033    / (x + 1)+ 24.01409822    / (x + 2)   -  1.231739516   / (x + 3)+  0.00120858003 / (x + 4)   -  0.00000536382 / (x + 5)
    return tmp + math.log(ser * math.sqrt(2 * math.pi))


def gamma(x) :
    return math.exp(logGamma(x));
