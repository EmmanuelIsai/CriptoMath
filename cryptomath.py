import math
from random import randint

# Criba de erastostenes
def primos(n):
    numeros = list(range(2, n+1))
    i = 0
    while numeros[i] <= math.sqrt(n):
        for numero in numeros[i+1:]:
            r = numero % numeros[i]
            if r == 0:
                numeros.remove(numero) 
        i += 1
    return numeros

# Algoritmo extendido de euclides
def gcd (a, b):
    u = 1 # Incognita x
          # v Incognita y
    g = a
    x = 0
    y = b
    while y != 0:
        q = g // y
        t = g % y
        s = u - q * x
        u, g = x, y
        x, y = s, t
    if b == 0:
        g, u, v = a, 1, 0
    else:
        v = (g - a * u) // b
        while u < 0:
            u = u + b // g
            v = v - a // g
    return g, u, v

# Algoritmo de exponenciacion rapida g^A mod N
def fastpower(g, A, N):
    a = g
    b = 1
    while A > 0:
        if A % 2 == 1:
            b = (b * a) % N
        a, A = (a ** 2) % N, math.floor(A/2)
    return(b)

# Calculo de raices primitivas
def potencias(numero, p, exponentes):
    resultados = []
    for exponente in exponentes:
        resultado = fastpower(numero, exponente, p)
        resultados.append(resultado)
    return resultados    
        
def raicesprimitivas(p):
    anillo = list(range(2, p))
    raices = []
    exponentes = list(range(1, p))
    for numero in anillo: 
        resultados = potencias(numero, p, exponentes)
        if set(exponentes) == set(resultados):
            raices.append(numero)
    return raices

# Logaritmo discreto
def DL(a, b, p):
    pot = potencias(a, p, list(range(1,p)))
    if b in pot:
        return pot.index(b) + 1
    else:
        print('No existe el logaritmo')

# Inverso multiplicativo
def inverso_mult(a, p):
    if a < 0:
        a = abs(a)
        neg = True
    else:
        neg=False
    opts = list(range(p))
    for opt in opts:
        res = a * opt % p
        if res == 1 and neg:
            return(-opt)
        elif res == 1:
            return(opt)

# Suma de puntos en curvas eliptica en campo finito
# Sea E: y^2 = x^3 + Ax + B (mod p)
# Sea P = [x1, y1], Q = [x2, y2]
def suma_Fp(A, p, P, Q):
    if P == Q:
        x3num = (((3*P[0]**2)%p + A)**2)%p
        x3den = ((2*P[1])**2)%p
        y3num = ((3*P[0]**2)%p + A)%p
        y3den = (2*P[1])%p
    else:
        x3num = ((Q[1]-P[1])**2)%p
        x3den = ((Q[0]-P[0])**2)%p
        y3num = ((Q[1]-P[1]))%p
        y3den = ((Q[0]-P[0]))%p

    xfracc = (inverso_mult(x3den,p)*x3num)%p
    yfracc = (inverso_mult(y3den,p)*y3num)%p
    x3 = (xfracc - P[0] - Q[0])%p
    y3 = (yfracc * (P[0]-x3) - P[1])%p
    R = [x3, y3]
    return(R)

# Encuentra el orden de un entero en modulo p
def orden(a, p):
    for opt in range(2, p):
        if fastpower(a, opt, p) == 1:
            return opt

# Algoritmo de Shank
def shank(g, h, p):
    N = orden(g, p) # ord(g)
    n = 1 + math.floor(math.sqrt(N))
    u = fastpower(inverso_mult(g, p), n, p)

    tmp = 1
    tmp2 = h 
    l1 = []
    l2 = []

    for i in range(0, n+1):
        tmp = (tmp * g) % p
        tmp2 = (tmp2 * u) % p
        l1.append(tmp)
        l2.append(tmp2)

    colision = list(set(l1).intersection(l2))

    i = l1.index(colision[0]) + 1
    j = l2.index(colision[0]) + 1
    #print(colision, i, j)

    x = i + j*n

    if fastpower(g, x, p) == h:
        return x
    else:
        print('Error')

# Prueba de primalidad de Miller Rabin
# Obtenido de:
# https://justyusblog.wordpress.com/2016/09/11/metodo-de-miller-rabin-en-python/

def millerrabin(p):
    #Primero comprobamos que sea impar.
    if 1&p==0:
        return False
        #False = no primo
        #True = primo

    #Expresamos p-1 como 2^u*s, con s impar.
    s = p-1
    #Dividir s por 2 hasta que el resultado sea impar.
    u = 0
    while 1&s==0:
        u= u+1
        s = s >> 1

    print(p,"= 2^",u,"*",s)

    for _ in range(20):#Ejecuciones para reducir las probabiliades de fallo.
        #Elegimos a al azar tal que 2 <= a <= p-2
        a = randint(2, p - 2)
        a = fastpower(a,s,p)

        if a == 1 or a == p-1:#p-1 = -1
            return True
        else:
            for i in [1,1,u-1]:
                a = fastpower(a,2,p)
                if a == p-1:
                    return True
                elif a == 1:
                    return False
                i=i+1
            return False