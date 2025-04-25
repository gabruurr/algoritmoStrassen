import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd


def multiplicacarPadrao(A, B):
    n = len(A)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def strassen(A, B):
    n = A.shape[0]
    if n == 1:
        return A * B
    else:
        mid = n // 2
        A11 = A[:mid, :mid]
        A12 = A[:mid, mid:]
        A21 = A[mid:, :mid]
        A22 = A[mid:, mid:]
        B11 = B[:mid, :mid]
        B12 = B[:mid, mid:]
        B21 = B[mid:, :mid]
        B22 = B[mid:, mid:]

        M1 = strassen(A11 + A22, B11 + B22)
        M2 = strassen(A21 + A22, B11)
        M3 = strassen(A11, B12 - B22)
        M4 = strassen(A22, B21 - B11)
        M5 = strassen(A11 + A12, B22)
        M6 = strassen(A21 - A11, B11 + B12)
        M7 = strassen(A12 - A22, B21 + B22)

        C11 = M1 + M4 - M5 + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = M1 - M2 + M3 + M6

        cima = np.hstack((C11, C12))
        baixo = np.hstack((C21, C22))
        return np.vstack((cima, baixo))


def run_tests(tamanhos):
    resultados = []
    for n in tamanhos:
        A = np.random.randint(0, 10, size=(n, n))
        B = np.random.randint(0, 10, size=(n, n))

        start = time.time()
        multiplicacarPadrao(A, B)
        standard_time = time.time() - start

        start = time.time()
        strassen(A, B)
        strassen_time = time.time() - start

        resultados.append({
            'Tamanho': n,
            'Tempo_Padrão': standard_time,
            'Tempo_Strassen': strassen_time
        })

    return pd.DataFrame(resultados)

tamanhoMatriz = [32, 64, 128, 256, 512]
df_results = run_tests(tamanhoMatriz)
df_results.to_csv('resultados_multiplicacao.csv', index=False)


plt.figure(figsize=(10, 6))
plt.plot(df_results['Tamanho'], df_results['Tempo_Padrão'], label='Multiplicação Padrão (n³)', marker='o')
plt.plot(df_results['Tamanho'], df_results['Tempo_Strassen'], label='Strassen', marker='o')
plt.xlabel('Tamanho da Matriz (n x n)')
plt.ylabel('Tempo (s)')
plt.title('Comparação de Tempo: Padrão vs Strassen')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

df_results