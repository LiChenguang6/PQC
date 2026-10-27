import numpy as np
import hashlib

from parameters import *
from generate_key import generate_key_A_NTT, multiplier,generate_key_t
from ntt_utils import inverse_ntt_A
from sign import generate_sign_w
from sign import (
    sample_in_ball,
    decompose,
    w1_encode,
    generate_challenge_seed
)
def bit_unpack(data, bits, count):
    buf = int.from_bytes(data, "little")
    values=np.zeros(count, dtype=np.int64)
    for i in range(count):
        values[i] = (buf >> (i * bits)) & ((1 << bits) - 1)
    return values
def pk_decode(pk, k, N):
    if len(pk) != 32 + (k * N * 10 + 7) // 8:
        raise ValueError("pk长度不匹配")
    rho = pk[:32]
    t_buf = bit_unpack(pk[32:], 10, k*N)
    t1=t_buf.reshape(k, N) 
    return rho, t1
def z_decode(z_bytes, gamma1, l, N):
    if len(z_bytes)!=2304:
        raise ValueError("z_bytes长度不匹配")
    z_p = bit_unpack(z_bytes, 18, l*N)
    z_buf = gamma1 - z_p
    z=z_buf.reshape(l, N)
    return z
def hint_decode(h_bytes, omega, k, N):
    h = np.zeros((k, N), dtype=np.int64)
    if len(h_bytes) != omega + k:
        raise ValueError("h_bytes长度不匹配")
    
    for i in range(k):
        if((i<k-1)and (h_bytes[omega+i]>h_bytes[omega+i+1])):
            raise ValueError("索引总数非递增")
        if i==0:
            num_of_j=0
        else :
            num_of_j=h_bytes[omega+i-1]
    
        end = h_bytes[omega+i]
        if end < num_of_j or end > omega:
            raise ValueError("索引累计数量不合法")
        for index in range(num_of_j,h_bytes[omega+i]):
                if(index==num_of_j):
                    index_num=0
                else:
                    index_num=h_bytes[index-1]
                num=h_bytes[index]
                if index > num_of_j:
                    if(num<=index_num):
                        raise ValueError("多项式索引非严格递增") 
                h[i][num]=1
    index_num=h_bytes[omega+k-1]
    seg = h_bytes[index_num:omega]
    if np.any(seg): 
        raise ValueError("索引外存在非零项") 
    return h
def sig_decode(sig, gamma1, omega, k, l, N):
    if len(sig) != 2420:
        raise ValueError("长度不匹配")
    c_tilde=sig[:32]
    z_bytes = sig[32:2336]
    h_bytes = sig[2336:2420]
    z = z_decode(z_bytes, gamma1, l, N)
    h = hint_decode(h_bytes, omega, k, N)
    return c_tilde, z, h
def use_hint(h, r, gamma2):
    r1, r0 = decompose(r, gamma2)
    m = (q - 1) // (2 * gamma2)
    r1_new = np.zeros(r.shape, dtype=np.int64)
    r1_new =np.where(h==0, r1,np.where(r0>0,(r1+1)%m,(r1-1)%m))
    return r1_new
def verify(message, pk, sig, ctx=b""):
    try:
        rho, t1 = pk_decode(pk, k, N)
        c_tilde, z, h = sig_decode(sig, gamma1, omega, k, l, N)
    except ValueError:
        return False
    if not np.all(np.abs(z) < gamma1 - beta):
        return False
    if len(ctx) > 255:
        return False
    message1 = b"\x00" + bytes([len(ctx)]) + ctx + message
    mu_buf=hashlib.shake_256(pk).digest(64)+message1
    mu=hashlib.shake_256(mu_buf).digest(64)
    c=sample_in_ball(c_tilde, tau=39)
    A_hat = generate_key_A_NTT(rho, k, l)
    A = inverse_ntt_A(A_hat)
    #w_prime = A*z - c*(t1*2^d) (mod q)
    Az = generate_sign_w(A, z, k, l, N, q)
    ct1_d=np.zeros(t1.shape,np.int64)
    for i in range(k):
        ct1_d[i]+=multiplier(c, t1[i], N, q)
    w_prime = (Az - (1 << d) * ct1_d) % q
    w1_prime = use_hint(h, w_prime, gamma2)
    c_tilde_prime=hashlib.shake_256(mu+w1_encode(w1_prime,gamma2)).digest(32)
    return c_tilde_prime==c_tilde