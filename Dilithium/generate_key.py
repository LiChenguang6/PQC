import numpy as np 
import hashlib
import os
q=8380417
def generate_seed():
    return os.urandom(32)#32个字节，256位
def derive_seeds(random_seed32, k, l):
    shake256 = hashlib.shake_256()
    shake256.update(random_seed32+bytes([k])+bytes([l]))
    buf=shake256.digest(128)
    rou=buf[0:32]
    rou1=buf[32:96]
    K=buf[96:128]
    return rou,rou1,K
def rej_ntt_poly(seed34):#生成256个合法系数0~8380417
    poly = np.zeros(256, dtype=np.int64)
    shake128 = hashlib.shake_128()
    shake128.update(seed34)
    pos=0
    buf=shake128.digest(3+pos*3)
    x=buf[0+pos*3]+(buf[1+pos*3]<<8)+((buf[2+pos*3]&0x7f)<<16)
    cnt=0
    while cnt<256:
        while x >= q :
            pos+=1
            buf=shake128.digest(3+pos*3)
            x=buf[0+pos*3]+(buf[1+pos*3]<<8)+((buf[2+pos*3]&0x7f)<<16)
        poly[cnt]=x
        cnt+=1
        x=q
    return poly
def generate_key_A(rho, k, l):#生成k*l*256个
    A_hat = np.zeros((k, l, 256), dtype=np.int64)
    for i in range(k):
        for j in range(l):
            seed=rho+bytes([j])+bytes([i])
            A_hat[i][j]=rej_ntt_poly(seed)
    return A_hat
    