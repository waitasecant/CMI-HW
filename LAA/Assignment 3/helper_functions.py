import numpy as np
import time

def luGEPP(A):
    n = len(A)
    A = A.astype(float)
    P = np.identity(n, dtype=float)
    L = np.zeros((n,n),dtype=float)
    U = np.copy(A)
    st = time.perf_counter()
    for i in range(n):
        max_pivot = abs(U[i:,i])
        if max(max_pivot) == 0:
            print("unable to find nonzero pivot")
            break
        max_row = np.argmax(abs(U[i:,i])) + i

        U[[i, max_row]] = U[[max_row, i]]
        P[[i, max_row]] = P[[max_row, i]]
        L[[i, max_row]] = L[[max_row, i]]
        
        for j in range(i+1, n):
            L[j,i] = U[j,i] / U[i,i]
            U[j,i:] -= L[j,i] * U[i,i:]
            
    np.fill_diagonal(L, 1.0)
    en = time.perf_counter()
    t = (en-st)*1000

    return P, L, U, t

def forward_sub(L, Pb):
    n = len(L)
    y = np.zeros(n, dtype=float)
    for i in range(n):
        y[i] = Pb[i] - sum(L[i,:i] * y[:i])
    return y

def backward_sub(U, y):
    n = len(U)
    x = np.zeros(n, dtype=float)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i,i+1:] * x[i+1:])) / U[i,i]
    return x

def luSolve(A, b):
    P, L, U, _ = luGEPP(A)
    Pb = np.dot(P, b)
    st = time.perf_counter()
    y = forward_sub(L, Pb)
    x = backward_sub(U, y)
    en = time.perf_counter()
    t = (en-st)*1000
    return x,t
