from generate_key import (
    generate_seed,
    derive_seeds,
    generate_key_A_NTT,
    generate_key_s,
    generate_key_t
)
from ntt_utils import inverse_ntt_A
k = 4
l = 4
eta = 2
N = 256
q = 8380417

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