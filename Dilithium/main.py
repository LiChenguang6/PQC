from generate_key import (
    generate_seed,
    derive_seeds,
    generate_key_A,
    generate_key_s
)
from ntt_utils import inverse_ntt_A
k = 4
l = 4
eta = 2
# Step 1：生成随机种子
xi = generate_seed()
rho, rho_prime, K = derive_seeds(xi, k, l)

# Step 2：生成 NTT 域矩阵,转换为普通多项式系数域
A_hat = generate_key_A(rho, k, l)
A = inverse_ntt_A(A_hat)

# Step 3：生成秘密向量
s1, s2 = generate_key_s(rho_prime, k, l, eta)