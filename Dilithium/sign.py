import numpy as np
import hashlib
import os
from key_encode import bit_pack
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
def decompose(w, gamma2):# w % q = (2*gamma2*w1+w0) % q
    m = (q - 1) // alpha
    alpha = 2 * gamma2
    r = w % q
    alpha1=(gamma2+r-1)//alpha
    alpha0=r-2*gamma2*alpha1
    alpha0 = np.where(alpha1 == m, alpha0 - 1, alpha0)
    alpha1 = np.where(alpha1 == m, 0, alpha1)
    w1=alpha1
    w0=alpha0
    return w1, w0
def w1_encode(w1, gamma2):
    if gamma2 == 95232:
        bits = 6
    elif gamma2 == 261888:
        bits = 4
    else:
        raise ValueError("不支持的 gamma2")
    w1_bytes = bit_pack(w1, bits)
    return w1_bytes
def generate_challenge_seed(mu, w1_bytes):
    c_tilde=hashlib.shake_256(mu+w1_bytes).digest(32)
    return c_tilde
def sample_in_ball(c_tilde, tau=39):
    c = np.zeros( N, dtype=np.int64)
    buf_cnt=0
    sign_buf=hashlib.shake_256(c_tilde).digest(8)
    signs = int.from_bytes(sign_buf[:8], "little")
    sign = signs & 1
    for i in range (N-tau,N):
        buf=hashlib.shake_256(c_tilde).digest(8+buf_cnt+1)
        j=buf[8+buf_cnt]
        while j > i:
            buf_cnt+=1
            buf=hashlib.shake_256(c_tilde).digest(8+buf_cnt+1)
            j=buf[8+buf_cnt]
        c[i] = c[j]
        c[j]=1 - 2 * sign
        signs >>= 1
        sign = signs & 1
        buf_cnt+=1
    return c
def center_mod(poly, q):#0中心化
        poly = np.asarray(poly, dtype=np.int64) % q
        return np.where(poly > q // 2, poly - q, poly)
def signed_poly_mul(a, b, N, q):
    return center_mod(multiplier(a, b, N, q), q)
def generate_sign_z(y, c, s1, l, N, q):
    z = y.copy()
    for i in range(l):
        z[i]+=signed_poly_mul(c,s1[i],N,q)
    return z
def check_z(z, gamma1, beta):
    return bool(np.all(np.abs(z) < gamma1 - beta))
def generate_sign_r_r0(w, c, s2, k, N, q, gamma2):
    r = generate_sign_z(w, -c, s2, k, N, q)
    _, r0=decompose(r,gamma2)
    return r,r0
def check_r0(r0, gamma2, beta):
    return bool(np.all(np.abs(r0) < gamma2 - beta))
def generate_sign_ct0(c, t0, k, N, q):
    zeros = np.zeros((k, N), dtype=np.int64)
    return generate_sign_z(zeros, c, t0, k, N, q)
def check_ct0(ct0, gamma2):
    return bool(np.all(np.abs(ct0) < gamma2))
def make_hint(z, r, gamma2):
    r1, _=decompose(r,gamma2)
    z_r1, _=decompose(r+z,gamma2)
    h = np.where(z_r1 == r1, 0, 1) 
    return h
def check_hint(h, omega):
    if np.count_nonzero(h) <= omega :
        accepted=True
    else :
        accepted=False
    return accepted
def z_encode(z, gamma1):
    z_p=gamma1-z

    if gamma1==131072:
        packed_n=18
    else :
        raise ValueError("不支持的 gamma1")

    z_packed=bit_pack(z_p,packed_n)

    return z_packed
def hint_encode(h, omega, k):
    buf = bytearray(omega + k)
    buf_num=0
    for i in range(k):
        for j in range(N):
            if h[i][j]!=0:
                if buf_num >= omega:
                    raise ValueError("Hint 数量超过 omega")
                buf[buf_num]=j
                buf_num+=1
        buf[omega +i]=buf_num        
    return bytes(buf)
def sig_encode(c_tilde, z, h, gamma1, omega, k):
    z_bytes=z_encode(z, gamma1)
    h_bytes=hint_encode(h, omega, k)
    sig = c_tilde + z_bytes + h_bytes
    return sig
def sign(message, A, s1, s2, t0, tr, K, ctx=b""):
    mu, rho_double_prime=prepare_sign(message,tr,K,ctx)
    kappa = 0
    num_of_while=1
    while(num_of_while):
        y=expand_mask(rho_double_prime, kappa, l, gamma1)
        kappa+=l
        w=generate_sign_w(A, y, k, l, N, q)
        w1,_=decompose(w, gamma2)
        w1_bytes=(w1, gamma2)
        c_tilde=generate_challenge_seed(mu, w1_bytes)
        c=sample_in_ball(c_tilde, tau=39)
        z=generate_sign_z(y, c, s1, l, N, q)
        r,r0=generate_sign_r_r0(w, c, s2, k, N, q, gamma2)
        if not(check_z(z, gamma1, beta) and check_r0(r0, gamma2, beta)):
            continue
        else :
            ct0=generate_sign_ct0(c, t0, k, N, q)
            if not(check_ct0(ct0, gamma2)):
                continue
            else :
                h=make_hint(z, r, gamma2)
                if not (check_hint(h, omega)):
                    continue
                else :
                    sig=sig_encode(c_tilde, z, h, gamma1, omega, k)
    return sig               

