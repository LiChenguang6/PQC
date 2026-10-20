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
    rou_prime=buf[32:96]
    K=buf[96:128]
    return rou,rou_prime,K
def rej_ntt_poly(seed34):#生成256个合法系数0~q
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
def generate_key_A_NTT(rho, k, l):#生成k*l*256个0~q的矩阵A
    A_NTT = np.zeros((k, l, 256), dtype=np.int64)
    for i in range(k):
        for j in range(l):
            seed=rho+bytes([j])+bytes([i])
            A_NTT[i][j]=rej_ntt_poly(seed)
    return A_NTT
def rej_bounded_poly(seed66, eta):#生成256个范围-2~2的向量
    poly = np.zeros(256, dtype=np.int64)
    num=0
    if eta ==2 :
        num=2
    else:
        raise ValueError("目前仅支持 eta=2")
    shake256 = hashlib.shake_256()
    shake256.update(seed66)
    pos=0
    cnt=0
    output=shake256.digest(1+pos)
    buf=output[pos]
    z0=buf&0x0f
    z1=buf>>4
    z=z0
    z_cnt=0
    while cnt<256:
        if z<15 :
            poly[cnt]=num-z%5
            cnt+=1
        if z_cnt==1:
            pos+=1
            output=shake256.digest(1+pos)
            buf=output[pos]
            z0=buf&0x0f
            z1=buf>>4
            z=z0
            z_cnt=0
        else:
            z=z1
            z_cnt=1
    return poly
def generate_key_s(rho_prime, k, l, eta):
    s1 = np.zeros((l, 256), dtype=np.int64)
    s2= np.zeros((k, 256), dtype=np.int64)
    for i in range(l):
        seed66=rho_prime + (i).to_bytes(2, "little")#两字节小端序合并
        s1[i]=rej_bounded_poly(seed66,eta)
    for j in range(k):
        seed66=rho_prime + (l+j).to_bytes(2, "little")#两字节小端序合并
        s2[j]=rej_bounded_poly(seed66,eta)
    return s1, s2
def multiplier(A_x, B_x, N, Mod):
    Sum = np.zeros(N, dtype=np.int64)

    for i in range(N):
        for j in range(N):
            if i >= j:
                Sum[i] += A_x[j] * B_x[i-j]
            else:
                Sum[i] -= A_x[j] * B_x[N+i-j]
    return Sum % Mod
def generate_key_t(A, s1, s2, k, l, N, Mod):
    t = np.zeros((k, N), dtype=np.int64)

    for i in range(k):
        t[i] += s2[i]

        for j in range(l):
            t[i] += multiplier(A[i][j], s1[j], N, Mod)

    return t % Mod
def power2round(t, d=13):
    t1 = (t + (1 << (d - 1)) - 1) >> d
    t0 = t - (t1 << d)
    return t1, t0
