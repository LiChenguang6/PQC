from sign import sign
from verify import verify
from generate_key import (
    generate_seed,
    derive_seeds,
    generate_key_A_NTT,
    generate_key_s,
    generate_key_t,
    power2round
)
from key_encode import (
    pk_encode,
    generate_tr,
    sk_encode
)
from ntt_utils import inverse_ntt_A
from parameters import *#变量引入
from sign import sign

xi = generate_seed()
rho, rho_prime, K = derive_seeds(xi, k, l)

#生成 NTT 域矩阵,转换为普通多项式系数域
A_hat = generate_key_A_NTT(rho, k, l)
A = inverse_ntt_A(A_hat)

#生成秘密向量
s1, s2 = generate_key_s(rho_prime, k, l, eta)

# 计算 t
t = generate_key_t(A, s1, s2, k, l, N, q)

# Power2Round
t1, t0 = power2round(t, d=13)

# 公钥、私钥编码
pk = pk_encode(rho, t1)
tr = generate_tr(pk)
sk = sk_encode(rho, K, tr, s1, s2, t0)

message = b"Hello Dilithium!"

# 使用已有的密钥数据生成签名
sig = sign(message, A, s1, s2, t0, tr, K)

# 正确消息
result1 = verify(message, pk, sig)

# 篡改消息
result2 = verify(b"Hello Dilithium?", pk, sig)

# 篡改签名
bad_sig = bytearray(sig)
bad_sig[0] ^= 1
result3 = verify(message, pk, bytes(bad_sig))

# 修改上下文
result4 = verify(message, pk, sig, ctx=b"Test")

print("正确消息验签：", result1)
print("篡改消息验签：", result2)
print("篡改签名验签：", result3)
print("修改上下文验签：", result4)

assert result1 is True
assert result2 is False
assert result3 is False
assert result4 is False

print("完整签名验签测试通过！")