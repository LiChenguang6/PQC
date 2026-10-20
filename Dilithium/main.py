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

# Step 1：生成随机种子
xi = generate_seed()
rho, rho_prime, K = derive_seeds(xi, k, l)

# Step 2：生成 NTT 域矩阵,转换为普通多项式系数域
A_hat = generate_key_A_NTT(rho, k, l)
A = inverse_ntt_A(A_hat)

# Step 3：生成秘密向量
s1, s2 = generate_key_s(rho_prime, k, l, eta)

# Step 4：计算 t
t = generate_key_t(A, s1, s2, k, l, N, q)

# Step 5：Power2Round
t1, t0 = power2round(t, d=13)

# Step 6：公钥、私钥编码
pk = pk_encode(rho, t1)
tr = generate_tr(pk)
sk = sk_encode(rho, K, tr, s1, s2, t0)