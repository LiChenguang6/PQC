import numpy as np 
import hashlib
import os

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
    