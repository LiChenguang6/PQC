# 图表渲染

四份 `.mmd` 是独立 Mermaid 源文件，以 `flowchart` 声明开头。SVG 和 PNG 由同名源文件生成。图内的实线流程、虚线调用和补充说明以各图图例为准。

## 当前云环境

```bash
cd /workspace/PQC
bash diagrams/render.sh
```

环境使用 Mermaid CLI 12.0.0、系统 Chromium 和 Noto Sans CJK SC 字体。CLI 安装在仓库外的 `/workspace/pqc-environment/mermaid`；如需重新安装：

```bash
PUPPETEER_SKIP_DOWNLOAD=true npm install \
  --prefix /workspace/pqc-environment/mermaid \
  --cache /workspace/pqc-environment/npm-cache \
  --no-audit --no-fund @mermaid-js/mermaid-cli@12.0.0
```

`mermaid-config.json` 指定中文字体、420px 文本换行宽度及原生 SVG 文本。CLI 12 使用 `--size 4200`，PNG 使用 `-s 2` 提高像素分辨率。SVG 保留矢量图形，可继续放大。

此环境的受管 Chromium 禁止 `file://` 导航，但允许 HTTP。原版 CLI 12 固定以 `file://` 打开自身的 HTML 外壳，因此 `render.sh` 会通过 `patch_cli.py` 给仓库外的 CLI 加入一个 `MMDC_RENDER_HTML_URL` 入口；随后 `serve_cli.py` 在 `127.0.0.1` 随机端口提供同一份 HTML。该服务只响应 `/index.html`，不开放目录浏览，脚本退出时自动关闭。浏览器管理策略、网络策略和 TLS 校验均未修改。

如需撤销这一个外部 CLI 兼容修改：

```bash
python3 diagrams/patch_cli.py \
  /workspace/pqc-environment/mermaid/node_modules/@mermaid-js/mermaid-cli/src/index.js \
  --restore
```

下一次执行云环境的 `render.sh` 时，会再次按需应用该兼容修改。

## 本地机器

普通本地安装可直接使用 `.mmd` 和 `mermaid-config.json`；无需使用仅适用于当前云环境的 Chromium 路径与 HTTP 兼容脚本。例如 Mermaid CLI 12：

```bash
mmdc -i 03_sign_calls.mmd -o 03_sign_calls.svg -c mermaid-config.json --size 4200
mmdc -i 03_sign_calls.mmd -o 03_sign_calls.png -c mermaid-config.json --size 4200 -s 2
```

本地需已具备 Mermaid CLI 支持的浏览器和中文字体。旧版 CLI 可将 `--size 4200` 改为 `-w 2400 -H 1600`。
