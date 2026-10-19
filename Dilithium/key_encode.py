import numpy as np 
import hashlib
import os
def bit_pack(values, bits):
    values_fall = np.asarray(values).flatten()
    #packed=int.to_bytes(0)
    Sum_value=0
    cnt=0
    for value in values_fall:
        #sum+=(value).to_bytes(bits, "little")
        if not (0 <= value < (1 << bits)):
            raise ValueError("数据超出编码范围")
        Sum_value+=int(value)<<cnt
        cnt+=bits
    packed=Sum_value.to_bytes((cnt+7)//8, "little")
    return packed
def pk_encode(rho, t1):
    pk=rho+bit_pack(t1,10)
    return pk
def generate_tr(pk):
    shake256 = hashlib.shake_256()
    shake256.update(pk)
    tr=shake256.digest(64)
    return tr
def sk_encode(rho, K, tr, s1, s2, t0):
    sk=rho+K+tr+bit_pack(2 - s1, 3)+bit_pack(2 - s2, 3)+bit_pack(4096 - t0, 13)
    return sk