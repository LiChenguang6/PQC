# PQC

本仓库用于记录后量子密码（Post-Quantum Cryptography，PQC）的学习过程，包含 Kyber 相关的 Python 实验代码和学习总结。

## 目录说明

| 目录 | 说明 |
| --- | --- |
| [Kyber](Kyber/) | Kyber 密钥生成、加密与解密实验代码及示例数据 |
| [汇报](汇报/) | 学习总结与汇报材料 |

## 运行方法（Windows + VS Code）

需要 Python 3.12 和 VS Code 的 **Python** 扩展。实验入口是 [`Kyber/main.py`](Kyber/main.py)，执行密钥生成、加密和解密流程。

1. 在 VS Code 中打开仓库文件夹，通过 **终端 → 新建终端** 打开 PowerShell。
2. 在仓库根目录创建虚拟环境并安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. 按 `Ctrl+Shift+P`，选择 **Python: Select Interpreter**，选择 `.venv\Scripts\python.exe`。
4. 在终端运行实验：

```powershell
cd Kyber
..\.venv\Scripts\python.exe main.py
```

运行后，`Kyber/` 中会生成消息、密钥和密文等文本文件；原始消息为 `m.txt`，解密消息为 `m_decode.txt`。

> 重复运行会覆盖 `Kyber/` 中的同名示例数据，请提前备份需要保留的文件。

## 学习资料

- [学习总结](汇报/学习总结.docx)

> 本仓库代码用于学习和实验；运行结果验证不代表通过标准一致性或密码安全性评估。
