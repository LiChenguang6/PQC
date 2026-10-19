
import numpy as np
from functools import lru_cache

Q = 8380417
N = 256
ZETA = 1753  # ML-DSA 使用的 512 次单位根


def bit_reverse_8(x):
    """将 8 位二进制整数的位顺序反转。"""
    return int(f"{x:08b}"[::-1], 2)


@lru_cache(maxsize=1)
def inverse_ntt_matrix():
    """
    构造 256×256 的逆 NTT 变换矩阵。
    只计算一次，后续可以重复使用。
    """
    inv_n = pow(N, -1, Q)

    roots = [
        pow(ZETA, 2 * bit_reverse_8(i) + 1, Q)
        for i in range(N)
    ]

    matrix = np.array([
        [
            (inv_n * pow(roots[i], -j, Q)) % Q
            for i in range(N)
        ]
        for j in range(N)
    ], dtype=np.int64)

    return matrix


def inverse_ntt_poly(poly_hat):
    """
    输入：一个 NTT 域多项式，shape=(256,)
    输出：普通系数域多项式，shape=(256,)
    """
    poly_hat = np.asarray(poly_hat, dtype=np.int64)

    if poly_hat.shape != (N,):
        raise ValueError("输入多项式的形状必须为 (256,)")

    matrix = inverse_ntt_matrix()

    return (matrix @ (poly_hat % Q)) % Q


def inverse_ntt_A(A_hat):
    """
    输入：NTT 域矩阵，shape=(k, l, 256)
    输出：普通系数域矩阵，shape=(k, l, 256)
    """
    A_hat = np.asarray(A_hat, dtype=np.int64)

    if A_hat.ndim != 3 or A_hat.shape[2] != N:
        raise ValueError("输入矩阵形状必须为 (k, l, 256)")

    matrix = inverse_ntt_matrix()

    # 对全部矩阵元素分别执行逆 NTT
    A = np.matmul(A_hat % Q, matrix.T) % Q

    return A
