# PQC

本仓库用于记录后量子密码（Post-Quantum Cryptography，PQC）的学习过程，包含 Kyber 相关的 Python 实验代码和学习总结。

## 目录说明

| 目录 | 说明 |
| --- | --- |
| [Kyber](Kyber/) | Kyber 密钥生成、加密与解密实验代码及示例数据 |
| [汇报](汇报/) | 学习总结与汇报材料 |

## Kyber 实验

实验入口为 [`Kyber/main.py`](Kyber/main.py)，主要流程如下：

1. 生成随机消息和密钥。
2. 使用公钥加密消息。
3. 使用私钥解密，得到恢复后的消息。

主要代码文件：

| 文件 | 说明 |
| --- | --- |
| [`main.py`](Kyber/main.py) | 串联密钥生成、加密与解密流程 |
| [`generate_key.py`](Kyber/generate_key.py) | 生成密钥、噪声及相关多项式运算 |
| [`generate_message.py`](Kyber/generate_message.py) | 生成随机二进制消息 |
| [`encode.py`](Kyber/encode.py) | 计算密文分量并恢复消息比特 |

### 运行环境

- Python 3（已在 Python 3.12 下验证）
- NumPy（已验证版本：2.4.2）

### 安装与运行

以下命令适用于 Linux / macOS 的 Bash 终端，请从仓库根目录执行。

创建虚拟环境并安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "numpy==2.4.2"
```

在临时目录中运行实验，将输出与仓库中的示例数据分开：

```bash
project_dir="$PWD"
output_dir="$(mktemp -d)"
(
    cd "$output_dir" || exit 1
    PYTHONDONTWRITEBYTECODE=1 python "$project_dir/Kyber/main.py"
)
echo "实验输出目录：$output_dir"
```

> 程序会在当前工作目录写出 `m.txt`、`m_decode.txt`、密钥和密文等文件。直接在 `Kyber/` 中运行会覆盖该目录内的同名示例文件。

验证原始消息与解密消息是否一致：

```bash
python - "$output_dir" <<'PY'
from pathlib import Path
import sys
import numpy as np

output = Path(sys.argv[1])
message = np.loadtxt(output / "m.txt", dtype=int)
decoded = np.loadtxt(output / "m_decode.txt", dtype=int)
assert message.shape == decoded.shape == (256,)
np.testing.assert_array_equal(message, decoded)
print("验证通过：256 位消息全部正确恢复。")
PY
```

验证命令需要在运行实验的同一终端中执行，以保留 `output_dir` 变量。

## 学习资料

- [学习总结](汇报/学习总结.docx)

> 本仓库代码用于学习和实验；运行结果验证不代表通过标准一致性或密码安全性评估。
