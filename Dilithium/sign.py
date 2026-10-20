import numpy as np
import hashlib
import os

from generate_key import multiplier
from parameters import *#变量引入
def prepare_sign(message, tr, K, ctx=b""):
    if len(ctx) > 255:
        raise ValueError("ctx 长度不能超过255字节")
    if len(tr) != 64 or len(K) != 32:
        raise ValueError("输入维度不匹配")
    M_prime = b"\x00" + bytes([len(ctx)]) + ctx + message
    # shake256 = hashlib.shake_256()
    # shake256.update(tr+M_prime)
    # mu=shake256.digest(64)#消息摘要
    mu=hashlib.shake_256(tr+M_prime).digest(64)#消息摘要
    rnd = os.urandom(32)
    rho_double_prime=hashlib.shake_256(K+rnd+mu).digest(64)#临时采样种子
    return mu, rho_double_prime
def expand_mask(rho_double_prime, kappa, l, gamma1):#输出y
    y = np.zeros((l, N), dtype=np.int64)
    bits = gamma1.bit_length()
    for i in range(l):
        seed = rho_double_prime + (kappa + i).to_bytes(2, "little")
        buf = hashlib.shake_256(seed).digest((N * bits + 7) // 8)
        buf = int.from_bytes(buf, "little")
        for j in range(N):
            buf_num=(buf>>bits)<<bits
            y[i][j]=gamma1-(buf-buf_num)
            buf=buf_num>>bits
    return y
def generate_sign_w(A, y, k, l, N, q):#输出w=Ay
    w = np.zeros((k, N), dtype=np.int64)

    for i in range(k):
        for j in range(l):
            w[i] += multiplier(A[i][j], y[j], N, q)

    return w % q