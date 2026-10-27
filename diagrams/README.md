# Dilithium 代码结构与调用关系

本目录根据 `../Dilithium/` 的实际 Python 代码绘图。分析范围为全部 **9 个 `.py` 文件、46 个顶层函数定义**；`output_txt.py` 还定义了 4 个嵌套辅助函数，因此连同嵌套定义共有 50 个函数。`main.py` 按顶层语句顺序执行，并没有名为 `KeyGen` 的函数；KeyGen、Sign、Verify 在整体流程图中表示阶段。

## 图表与源文件

Mermaid 源文件直接以 `flowchart` 声明开头，没有 Markdown 代码围栏，可单独下载后用本地 `mmdc` 渲染。

| 内容 | Mermaid 源文件 | 对应 SVG | 对应高清 PNG |
| --- | --- | --- | --- |
| 全部文件的依赖架构 | [01_file_architecture.mmd](01_file_architecture.mmd) | [01_file_architecture.svg](01_file_architecture.svg) | [01_file_architecture.png](01_file_architecture.png) |
| main.py 的密钥生成、签名、验签 | [02_main_workflow.mmd](02_main_workflow.mmd) | [02_main_workflow.svg](02_main_workflow.svg) | [02_main_workflow.png](02_main_workflow.png) |
| sign.py 的调用与拒绝采样 | [03_sign_calls.mmd](03_sign_calls.mmd) | [03_sign_calls.svg](03_sign_calls.svg) | [03_sign_calls.png](03_sign_calls.png) |
| verify.py 的调用与解码检查 | [04_verify_calls.mmd](04_verify_calls.mmd) | [04_verify_calls.svg](04_verify_calls.svg) | [04_verify_calls.png](04_verify_calls.png) |

[下载四份 Mermaid 源文件压缩包](dilithium_mermaid_sources.zip)。同名 SVG 和高清 PNG 已使用 Mermaid CLI 生成；可运行脚本重新生成。

图例按图表分别定义：文件架构图的实线表示项目内导入依赖，虚线表示第三方或标准库导入；流程与函数图的实线表示执行顺序，虚线才表示项目函数的直接调用。导入语句、数据传递和执行先后关系不能相互替代。图中明确标出了未使用导入，未把它们画成实际调用。

## 全部文件的职责

| 文件 | 顶层函数数 | 实际职责与入口关系 |
| --- | ---: | --- |
| `main.py` | 0 | 顺序生成密钥，签名，再执行 4 次验签和 4 项断言；是实际可执行实验入口。 |
| `generate_key.py` | 9 | 随机种子、SHAKE 派生、矩阵及秘密向量采样、负循环多项式乘法、公钥向量计算、`power2round` 分解。 |
| `key_encode.py` | 4 | `bit_pack` 位打包、`pk_encode` 公钥编码、`generate_tr` 公钥摘要、`sk_encode` 私钥编码。 |
| `ntt_utils.py` | 4 | `bit_reverse_8`、缓存的 `inverse_ntt_matrix`、单多项式变换 `inverse_ntt_poly`、矩阵批量变换 `inverse_ntt_A`。 |
| `sign.py` | 21 | `sign` 驱动消息预处理、掩码采样、挑战生成、响应及提示检查、签名编码，包含拒绝后重新采样的循环。 |
| `verify.py` | 7 | `bit_unpack`、`pk_decode`、`z_decode`、`hint_decode`、`sig_decode`、`use_hint` 和入口 `verify`。 |
| `parameters.py` | 0 | 定义 `k`、`l`、`eta`、`N`、`q`、`d`、`gamma1`、`gamma2`、`beta`、`tau`、`omega`。 |
| `output_txt.py` | 1 | 独立 UTF-8 文本导出工具 `output_txt`，内部含 4 个辅助函数；目前没有被其他项目文件导入或调用。 |
| `test.py` | 0 | 全部内容被注释，没有可执行导入、函数或测试；直接运行不能形成测试覆盖。 |

## 密钥生成及编码的直接调用

`generate_key.py` 中的函数为 `generate_seed`、`derive_seeds`、`rej_ntt_poly`、`generate_key_A_NTT`、`rej_bounded_poly`、`generate_key_s`、`multiplier`、`generate_key_t`、`power2round`。其中项目内部的直接调用只有：

- `generate_key_A_NTT → rej_ntt_poly`：按矩阵行列采样 NTT 域多项式。
- `generate_key_s → rej_bounded_poly`：分别生成 `s1`、`s2`。
- `generate_key_t → multiplier`：在行列循环中计算 `A·s1+s2 mod q`。

其余这些函数只调用 NumPy、`hashlib`、`os` 或 Python 内置能力。`generate_seed` 直接使用 `os.urandom`，`derive_seeds` 直接使用 SHAKE256；二者不是互相调用关系。

`key_encode.py` 的直接项目调用为 `pk_encode → bit_pack`，以及 `sk_encode → bit_pack`（源码调用 3 次，分别编码 `s1`、`s2`、`t0`）。`generate_tr` 使用 SHAKE256，不调用本文件的其他函数。该文件导入的 `os` 未被使用。

`ntt_utils.py` 的直接项目调用为：

- `inverse_ntt_matrix → bit_reverse_8`：构造单位根顺序；`inverse_ntt_matrix` 由 `lru_cache(maxsize=1)` 包装，缓存命中时不重新执行构造函数体。
- `inverse_ntt_poly → inverse_ntt_matrix`：对单个多项式做矩阵乘法。
- `inverse_ntt_A → inverse_ntt_matrix`：使用 `np.matmul` 对整组矩阵多项式批量变换。

`inverse_ntt_A` **不调用** `inverse_ntt_poly`；两者是共享逆变换矩阵的独立接口。

## main.py、sign.py 与 verify.py

`main.py` 依次调用 `generate_seed`、`derive_seeds`、`generate_key_A_NTT`、`inverse_ntt_A`、`generate_key_s`、`generate_key_t`、`power2round`、`pk_encode`、`generate_tr`、`sk_encode`，随后调用 `sign` 一次、`verify` 四次。生成的 `sk` 在本文件后续没有使用：签名时直接传入 `A`、`s1`、`s2`、`t0`、`tr`、`K`，没有私钥解码步骤。`from sign import sign` 在 `main.py` 中重复出现两次，架构图合并显示。

`sign.py` 的函数图覆盖全部 21 个函数及 28 对不同的直接项目函数调用关系。外层 `sign` 先执行 `prepare_sign`，再设置 `kappa=0`；每轮 `expand_mask` 后立即执行 `kappa += l`。`check_z` 为假时，Python 的 `and` 短路使 `check_r0` 不会被调用；`check_z`、`check_r0`、`check_ct0` 或 `check_hint` 拒绝候选后，都通过 `continue` 回到下一轮。`sample_in_ball` 自己还有读取字节并在 `j > i` 时重采样的内部循环。图中辅助调用还包括 `generate_key.multiplier` 和 `key_encode.bit_pack`，没有把相邻执行的函数误画成互相调用。

`verify.py` 在解码阶段依次调用 `pk_decode` 和 `sig_decode`，只在这一段 `try` 中捕获 `ValueError`；此后的计算不在该异常捕获范围内。`pk_decode` 和 `z_decode` 调用 `bit_unpack`，`sig_decode` 调用 `z_decode` 和 `hint_decode`；`use_hint` 调用 `sign.decompose`。验证阶段还实际调用 `sample_in_ball`、`generate_key_A_NTT`、`inverse_ntt_A`、`generate_sign_w`、`multiplier`、`w1_encode`。最终的挑战摘要由本文件直接调用 SHAKE256 计算，并与签名中的 `c_tilde` 比较。

`verify.py` 虽然导入了 `generate_key_t` 和 `generate_challenge_seed`，但没有调用它们。`sig_decode` 的 2420 字节长度和 `z_decode` 的 2304 字节长度检查按当前源码固定值展示，没有替换成推测的通用参数逻辑。

## output_txt.py 的嵌套辅助调用

这里只按每个函数自己的词法函数体判断直接调用，不把嵌套函数体中的调用归属到外层 `output_txt`：

- `output_txt → render`：调用渲染入口，再用 `Path` 创建目录并写入 UTF-8 文件。
- `render → render`：递归处理嵌套的映射、列表和元组。
- `render → render_array`、`wrap_items`、`scalar`：按数据类型选择对应格式化方式。
- `render_array → scalar`、`wrap_items`：处理不同维度的数组。
- `wrap_items → scalar`：格式化各个元素后按行宽折行。
- `scalar` 不调用其他项目函数，只进行类型判断和标量格式化。

NumPy 在 `output_txt` 中是可选导入；缺少 NumPy 时仍支持普通 Python 数据。`render_array` 只有在高维数组分支才导入 `itertools`。当前 `main.py` 没有调用此工具，也没有因此生成导出文件。

## 重新渲染

从仓库根目录运行：

```bash
bash diagrams/render.sh
```

[render.sh](render.sh) 优先使用 `MMDC` 指定的命令，其次查找 PATH 中的 `mmdc`，最后使用当前云环境的 `/workspace/pqc-environment/mermaid/node_modules/.bin/mmdc`。已核对该环境中的 Mermaid CLI 版本为 **12.0.0**；脚本按 CLI 支持的参数选择尺寸，并用 2 倍比例输出 PNG。

[mermaid-config.json](mermaid-config.json) 配置中文字体和图形样式；[puppeteer-config.json](puppeteer-config.json) 配置当前云环境的 `/usr/bin/chromium`。云环境的 CLI 兼容处理通过 [patch_cli.py](patch_cli.py) 和 [serve_cli.py](serve_cli.py) 从本地 HTTP 地址加载渲染页面。本地生成单份图表只需 `.mmd` 文件及可用的 `mmdc`；如使用本目录的 Chromium 配置，应先把浏览器路径调整为本机实际路径。

分析说明、图表和渲染辅助文件均保存在 `diagrams/`；`Dilithium/` 业务代码未修改。
