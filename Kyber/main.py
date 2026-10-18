import generate_message
import generate_key
import encode
import numpy as np
import time
random_seed32_A=generate_key.generate_32seeds()
random_seed32_s=generate_key.generate_32seeds()
K,N,Mod=4,256,3329
m=generate_message.generate_message(time.time(),"m.txt",N)
# 公钥生成
A=generate_key.generate_key_A(random_seed32_A,K,N,Mod,"A.txt")
s=generate_key.generate_key_s(random_seed32_s,K,N,"s.txt")
e=generate_key.generate_key_e(random_seed32_s,K,N,"e.txt")
t=generate_key.generate_key_t(A,s,e,K,N,Mod,"t.txt")

#加密
random_seed32_r=generate_key.generate_32seeds()
r=generate_key.generate_key_s(random_seed32_r,K,N,"r.txt")
e_1=generate_key.generate_key_e(random_seed32_r,K,N,"e_1.txt")
u=generate_key.generate_key_t(np.swapaxes(A, 0, 1),r,e_1,K,N,Mod,"u.txt")
e_2=generate_key.generate_key_e(random_seed32_r,2*K,N,"e_2.txt")[0]
v=encode.generate_v(t,r,e_2,m,K,N,Mod,"v.txt")

#解密
m_decode_half=encode.generate_v(-s,u,v,np.zeros(N,dtype=np.int64),K,N,Mod,"m_decode_half.txt")
m_decode=encode.generate_m(m_decode_half,N,Mod,"m_decode.txt")

