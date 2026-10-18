import numpy as np 
import hashlib
import os
# K = 4
# N = 256
# Mod = 3329
# random_seed32_A = os.urandom(32)
# random_seed32_s= os.urandom(32)
def generate_32seeds():
    return os.urandom(32)
def generate_key_A(random_seed32_A,K,N,Mod,filename):
    A=np.zeros((K,K,N),dtype=np.int64)
    file = open(filename,"w")
    for i in range(K):
        for j in range (K):
            shake128 = hashlib.shake_128()
            shake128.update(random_seed32_A+bytes([j])+bytes([i]))
            d1= d2 =0
            pos=0
            for n in range(N):
                if(n==0):
                    buf = shake128.digest(3)
                    d1=buf[0]+((buf[1]&0x0f)<<8)
                    d2=(buf[1]>>4)+(buf[2]<<4)
                while(1):
                    if(d1>=Mod):
                        if(d2>=Mod):
                            pos+=3
                            d1=shake128.digest(3+pos)[pos]+((shake128.digest(3+pos)[pos+1]&0x0f)<<8)
                            d2=(shake128.digest(3+pos)[pos+1]>>4)+(shake128.digest(3+pos)[pos+2]<<4)
                        else:
                            num=d2
                            pos+=3
                            d1=shake128.digest(3+pos)[pos]+((shake128.digest(3+pos)[3+pos-2]&0x0f)<<8)
                            d2=(shake128.digest(3+pos)[3+pos-2]>>4)+(shake128.digest(3+pos)[pos+2]<<4)
                            break 
                    else:
                        num=d1
                        d1=Mod
                        break
                A[i,j,n]=num
                file.write(str(num)+" ")
            file.write(",")
        file.write("\n")
    file.close()
    return A

def generate_key_s(random_seed32_s,K,N,filename):
    s=np.zeros((K,N),dtype=np.int64)
    file = open(filename,"w")
    for i in range(K):
        pos=0
        for n in range(0,N-1,2):
            shake256 = hashlib.shake_256()
            shake256.update(random_seed32_s+bytes([i]))

            buf=shake256.digest(1+pos)[pos]

            s[i,n]=(buf&1)+((buf>>1)&1)-((buf>>2)&1)-((buf>>3)&1)
            s[i,n+1]=((buf>>4)&1)+((buf>>5)&1)-((buf>>6)&1)-((buf>>7)&1)
            file.write(str(s[i,n])+" ")
            file.write(str(s[i,n+1])+" ")
            pos+=1
        file.write("\n")
    file.close()
    return s

def generate_key_e(random_seed32_s,K,N,filename):
    e=np.zeros((K,N),dtype=np.int64)
    file = open(filename,"w")
    for i in range(K):
        pos=0
        for n in range(0,N-1,2):
            shake256 = hashlib.shake_256()
            shake256.update(random_seed32_s+bytes([i+K]))

            buf=shake256.digest(1+pos)[pos]

            e[i,n]=(buf&1)+((buf>>1)&1)-((buf>>2)&1)-((buf>>3)&1)
            e[i,n+1]=((buf>>4)&1)+((buf>>5)&1)-((buf>>6)&1)-((buf>>7)&1)
            file.write(str(e[i,n])+" ")
            file.write(str(e[i,n+1])+" ")
            pos+=1
        file.write("\n")
    file.close()
    return e
def multiplier(A_x,B_x,N,Mod):
    Sum=np.zeros(N,dtype=np.int64)
    for i in range(N) :
        for j in range(N):
            if i - j >= 0:
                Sum[i]+=A_x[j]*B_x[i-j]
            else:
                Sum[i]-=A_x[j]*B_x[N + (i-j)]
    return Sum%Mod        
def generate_key_t(A,s,e,K,N,Mod,filename):
    t =np.zeros((K,N),dtype=np.int64)
    file = open(filename,"w")
    for i in range(K):
        t[i]+=e[i]
        for j in range(K):
            t[i]+=multiplier(A[i][j],s[j],N,Mod)
    for i in range(K):   
        for j in range(N):
            file.write(str((t[i,j]%Mod))+" ")
        file.write("\n")
    file.close()
    return t%Mod