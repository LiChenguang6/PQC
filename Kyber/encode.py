import numpy as np
import math 
def multiplier(A_x,B_x,N,Mod):#1*1的N循环卷积
    Sum=np.zeros(N,dtype=np.int64)
    for i in range(N) :
        for j in range(N):
            if i - j >= 0:
                Sum[i]+=A_x[j]*B_x[i-j]
            else:
                Sum[i]-=A_x[j]*B_x[N + (i-j)]
    return Sum%Mod
def multiplier_1(t,r,K,N,Mod):#两个K维向量的N循环卷积
    Sum=np.zeros(N,dtype=np.int64)
    for i in range(K):
        Sum+= multiplier(t[i],r[i],N,Mod)
    return Sum%Mod
def generate_v(t,r,e_2,m,K,N,Mod,filename):
    m=np.array(m, dtype=np.int64)  
    v=(multiplier_1(t,r,K,N,Mod)+e_2+m*((Mod+1)//2))%Mod
    file = open(filename,"w")
    for i in range(N):
        file.write(str(v[i])+" ")
    return v
def generate_m(message,N,Mod,filename):
    m=np.zeros(N,dtype=np.int64)
    file = open(filename,"w")
    for i in range(N):
        if(message[i]>int(Mod*3/4)):
            m[i]=0
        elif(message[i]<int(Mod/4)):
            m[i]=0
        else:
            m[i]=1
        file.write(str(m[i])+" ")
    return m