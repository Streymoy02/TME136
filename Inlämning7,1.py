#Rune Streymoy 020517

import numpy as np
import matplotlib.pyplot as plt 

def taylor(x, z, r): #(a)
    #funktionen tar in x-värde, polynomgrad-r och om uträkningen ska göras för sin eller cos

    tecken = 1

    # skifta intervall till [-pi, pi] 
    while True:
        if x < -np.pi:
            x = x + (2*np.pi)
        elif x > np.pi:
            x = x - (2*np.pi)
        else:
            break

    # ändrar faktor och skiftning av intervall för antingen sin eller cos
    if z == 'cos':
        faktor = 0
        # skifta intervall till [-pi/2, pi/2]
        if x > np.pi/2:
            x = np.pi - x 
            tecken = -1
        elif x < -np.pi/2:
            x = -np.pi - x 
            tecken = -1
        # skifta intervall till [0, pi/2] 
        if x < 0:
            x = -x  
    elif z =='sin':
        faktor = 1
        # skifta intervall till [0, pi] 
        if x < 0:
            x = -x
            tecken = -1
        # skifta intervall till [0, pi/2] 
        if x > np.pi/2:
            x = np.pi - x

    # Väljer polynomgrad
    if r == '':
        r = 12

    # approx taylorpolynom
    y = 0
    for k in range(r):
        y = y + ((-1)**k * (x)**(2*k+faktor)) / np.math.factorial(2*k+faktor)

    y = y*tecken
    return(y)

def sin_taylor(x, r):
    # funktonen tar in x-värde och polynomgrad-r
    # den anropar funktonen taylor och returnar ett estimerat y-värde för sin
    y = taylor(x, 'sin', r)
    return(y)

def cos_taylor(x, r):
    # funktonen tar in x-värde och polynomgrad-r
    # den anropar funktonen taylor och returnar ett estimerat y-värde för cos
    y = taylor(x, 'cos', r)
    return(y)

def approxError(): #(b)
    # funktionen skapar en plott som visar skillnaden mellan datorns och ens egna sin/cos estimeringarna

    fig, (ax1, ax2) = plt.subplots(2,1)
    x = np.linspace(-10, 10, 201)
    y1 = []
    y2 = []

    for n in np.linspace(-10, 10, 201):     
        sinFel = sin_taylor(n, '') - np.sin(n)
        cosFel = cos_taylor(n, '') - np.cos(n)
        y1.append(sinFel)
        y2.append(cosFel)
    # sparar felet för varje x inom intervallet

    ax1.plot(x, y1, color = 'b')
    ax2.plot(x, y2, color = 'r')

    ax1.set_title('Error för Sin')
    ax2.set_title('Error för Cos')
    plt.grid()
    plt.tight_layout()
    fig.show()

    E = 10**-16
    errorSin = 1
    n = 0
    m = 0
    while errorSin > E:
        n = n + 1
        errorSin = (np.pi/2)**(n+1)/(np.math.factorial(n+1))
    # undersöker vilken polynomgrad som krävs för specifierad noggrannhet

    # plynomgradSin(n) => PolynomgradCos(m) = n - 1
    m = n - 1

    print(f'Vi uppnår noggrannheten 10**-16 efter {n} iterationer för sin och {m} iterationer för cos')

    return()

def approxError_one(): #(c)
    # plottar hur stort felet blir för specifikt x som funktion av polynomgraden-r

    fig, (ax1,ax2) = plt.subplots(1,2)
    ax1.set_yscale("log")
    ax2.set_yscale("log")
    y1 = []
    y2 = []

    r = 0
    while True: 
        r = r + 1
        sinFel = abs(sin_taylor(1, r) - np.sin(1))
        y1.append(sinFel)
        if sinFel < 10**-15:
            break
    r = 0
    while True: 
        r = r + 1
        cosFel = abs(cos_taylor(1, r) - np.cos(1))
        y2.append(cosFel)
        if cosFel < 10**-15:
            break
    # sparar felet i varje iteration, bryter när godtycklig noggrannhet uppnås
   
    r = np.arange(0, r)
    ax1.plot(r, y1, color = 'b', marker = 'o')
    ax1.set_title('Fel för Sin i punkten x = 1')

    ax2.plot(r, y2, color = 'r', marker = 'o')
    ax2.set_title('Fel för Cos i punkten x = 1')

    plt.tight_layout()
    plt.show()

    return()

approxError()
approxError_one()
