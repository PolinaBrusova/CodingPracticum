from multiprocessing import Process, Pool
import numpy as np


def multiply(i_i, j_j, matrix1, matrix2, file):
    res = 0
    matrix = matrix2.copy()
    i, j = i_i, j_j
    for k in range(len(matrix1[0])):
        res += matrix1[i][k] * matrix2[k][j]
    matrix[i][j] = res
    print(" для", i, j, "результат", res)
    if i == j == 0:
        with open(file, "w", encoding='utf-8') as f:
            f.write(str(res) + " ")
    else:
        with open(file, "a+", encoding='utf-8') as f:
            if j == 0:
                f.write("\n" + str(res) + " ")
            else:
                f.write(str(res) + " ")
    return matrix


if __name__ == '__main__':
    try:
        matrix1, matrix2 = np.loadtxt("m1.txt"), np.loadtxt("m2.txt")
        p = Pool(9)
        print("Предварительно рассчитаное число процессов:", len(matrix1) * len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                proc = Process(target=multiply, args=(i, j, matrix1, matrix2, "m3.txt"))
                print("Запущен процесс!")
                proc.start()
                proc.join()
                p.apply(multiply, (i, j, matrix1, matrix2, "pool.txt"))
    except Exception:
        print("упс...")
