import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt

PI = 3.1416


def trajPoly3(var, tf, tetaS, tetaF, velS, velF):
    (a3, a2, a1, a0) = var

    eq1 = a0 - tetaS
    eq2 = a0 + a1*tf + a2*tf**2 + a3*tf**3 - tetaF
    eq3 = a1 - velS
    eq4 = a1 + 2*a2*tf + 3*a3*tf**2 - velF

    return [eq1, eq2, eq3, eq4]


def trajPoly3Via(var, tf1, tf2, tetaS, tetaV, tetaF, velS, velF):
    (a13, a12, a11, a10, a23, a22, a21, a20) = var

    eq1 = a10 - tetaS
    eq2 = a10 + a11*tf1 + a12*tf1**2 + a13*tf1**3 - tetaV
    eq3 = a20 - tetaV
    eq4 = a20 + a21*tf2 + a22*tf2**2 + a23*tf2**3 - tetaF
    eq5 = a11 - velS
    eq6 = a21 + 2*a22*tf2 + 3*a23*tf2**2 - velF
    eq7 = a11 + 2*a12*tf1 + 3*a13*tf1**2 - a21
    eq8 = 2*a12 + 6*a13*tf1 - 2*a22

    return [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8]


def trajPoly5(var, tf, tetaS, tetaF, velS, velF, accS, accF):
    (a5, a4, a3, a2, a1, a0) = var

    eq1 = a0 - tetaS
    eq2 = a0 + a1*tf + a2*tf**2 + a3*tf**3 + a4*tf**4 + a5*tf**5 - tetaF
    eq3 = a1 - velS
    eq4 = a1 + 2*a2*tf + 3*a3*tf**2 + 4*a4*tf**3 + 5*a5*tf**4 - velF
    eq5 = 2*a2 - accS
    eq6 = 2*a2 + 6*a3*tf + 12*a4*tf**2 + 20*a5*tf**3 - accF

    return [eq1, eq2, eq3, eq4, eq5, eq6]


def buildGraph(tf1, tf2, firstPoly, SecondPoly5):
    x = np.arange(0, tf1, 0.001)
    y = firstPoly(x)
    plt.plot(x, y)

    x = np.arange(0, tf2, 0.001)
    y = SecondPoly5(x)
    plt.plot(x, y)


def saveResult(fileName, tf1, tf2, firstPoly, SecondPoly5):
    buildGraph(tf1, tf2, firstPoly, SecondPoly5)
    plt.savefig(fileName, bbox_inches='tight')
    plt.close("all")


def showResult(setionName, firstEqName, secondEqName, tf1, tf2, firstPoly, SecondPoly5):
    print(setionName)

    print(firstEqName)
    print(firstPoly)

    print(secondEqName)
    print(SecondPoly5)

    buildGraph(tf1, tf2, firstPoly, SecondPoly5)
    plt.show()
    plt.close("all")

def drawDevoir2():
    # A & B
    tfA = 1
    tetaSA = 2*PI/3
    tetaFA = PI/3
    velSA = 0
    velFA = 0
    accSB = 0
    accFB = 0

    # POSITION
    sol3 = opt.fsolve(trajPoly3, (1, 1, 1, 1), (tfA, tetaSA, tetaFA, velSA, velFA))
    posTrajPoly3 = np.poly1d(sol3)
    sol5 = opt.fsolve(trajPoly5, (1, 1, 1, 1, 1, 1), (tfA, tetaSA, tetaFA, velSA, velFA, accSB, accFB))
    posTrajPoly5 = np.poly1d(sol5)
    showResult("POSITION", "Polynomial order 3:", "Polynomial order 5:", tfA, tfA, posTrajPoly3, posTrajPoly5)
    saveResult('ab_pos.png', tfA, tfA, posTrajPoly3, posTrajPoly5)

    # VELOCITY
    velTrajPoly3 = posTrajPoly3.deriv()
    velTrajPoly5 = posTrajPoly5.deriv()
    showResult("VELOCITY", "Polynomial order 3:", "Polynomial order 5:", tfA, tfA, velTrajPoly3, velTrajPoly5)
    saveResult('ab_vel.png', tfA, tfA, velTrajPoly3, velTrajPoly5)

    # ACCELERATION
    accTrajPoly3 = velTrajPoly3.deriv()
    accTrajPoly5 = velTrajPoly5.deriv()
    showResult("ACCELERATION", "Polynomial order 3:", "Polynomial order 5:", tfA, tfA, accTrajPoly3, accTrajPoly5)
    saveResult('ab_acc.png', tfA, tfA, accTrajPoly3, accTrajPoly5)

    # JERK
    jerkTrajPoly3 = accTrajPoly3.deriv()
    jerkTrajPoly5 = accTrajPoly5.deriv()
    showResult("JERK", "Polynomial order 3:", "Polynomial order 5:", tfA, tfA, jerkTrajPoly3, jerkTrajPoly5)
    saveResult('ab_jerk.png', tfA, tfA, jerkTrajPoly3, jerkTrajPoly5)


    # C
    tf1C = 1
    tf2C = 1
    tetaSC = PI/3
    tetaVC = 2*PI/3
    tetaFC = PI/6
    velSC = 0
    velFC = 0

    # POSITION
    sol3v = opt.fsolve(trajPoly3Via, (1, 1, 1, 1, 1, 1, 1, 1), (tf1C, tf2C, tetaSC, tetaFC, velSC, velFC))
    posTrajPoly3v1 = np.poly1d(sol3v[:4])
    posTrajPoly3v2 = np.poly1d(sol3v[4:8])
    showResult("POSITION", "Polynomial 1:", "Polynomial 2:", tf1C, tf2C, posTrajPoly3v1, posTrajPoly3v2)
    saveResult('c_pos.png', tf1C, tf2C, posTrajPoly3v1, posTrajPoly3v2)

    # VELOCITY
    velTrajPoly3v1 = posTrajPoly3v1.deriv()
    velTrajPoly3v2 = posTrajPoly3v2.deriv()
    showResult("VELOCITY", "Polynomial 1:", "Polynomial 2:", tf1C, tf2C, velTrajPoly3v1, velTrajPoly3v2)
    saveResult('c_vel.png', tf1C, tf2C, velTrajPoly3v1, velTrajPoly3v2)

    # ACCELERATION
    accTrajPoly3v1 = velTrajPoly3v1.deriv()
    accTrajPoly3v2 = velTrajPoly3v2.deriv()
    showResult("ACCELERATION", "Polynomial 1:", "Polynomial 2:", tf1C, tf2C, accTrajPoly3v1, accTrajPoly3v2)
    saveResult('c_acc.png', tf1C, tf2C, accTrajPoly3v1, accTrajPoly3v2)

    # JERK
    jerkTrajPoly3v1 = accTrajPoly3v1.deriv()
    jerkTrajPoly3v2 = accTrajPoly3v2.deriv()
    showResult("JERK", "Polynomial 1:", "Polynomial 2:", tf1C, tf2C, jerkTrajPoly3v1, jerkTrajPoly3v2)
    saveResult('c_jerk.png', tf1C, tf2C, jerkTrajPoly3v1, jerkTrajPoly3v2)