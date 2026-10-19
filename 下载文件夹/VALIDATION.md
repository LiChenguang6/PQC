# X2 保存导出版 export2：验证记录

交付 APK：`X2-cache-export.apk`，包名 `com.example.yinqishe_export`，版本码 10，版本名 `9.9.9-export2`。SHA-256：`09cafbca206859d4ea5f8f3292f965efd3530902ec13f65977e97ce8822f5106`。

## 本次改变

用户报告的是原界面里的视频下载失败。已审计原下载流程、鉴权拦截器、重签后的身份变化和补丁影响；原错误提示吞掉了具体异常，云端又无法连通平台，因此尚未确认该用户故障的唯一根因。没有把它归因于 APK 下载链接、FFmpeg 符号冲突或某个未经验证的权限条件。

export2 在同一 App 内增加“保存/导出 → 保存当前播放视频”，读取原播放器实际加载的 HTTP(S) 播放源，正常下载后合并成 MP4。它不依赖原下载按钮先缓存，不构造业务令牌或模拟设备身份；原浏览/播放和已有缓存导出保留。原下载按钮的业务错误仍可能出现。

## 当前产物的验证

以下均使用自行生成的短视频和本地受控 HTTP/HTTPS 服务，不是平台真实影片。Android 执行环境为官方 AOSP API29 x86_64 软件模拟器，未连接用户手机。

| 验证项 | 结果与证据 |
|---|---|
| 三架构编译与签名 | ARM64、ARMv7、x86_64 成功构建；APK v2/v3 验签通过，原 21 个媒体/Flutter 原生库逐字节保留。见 `build-info.json`、`signature-verification.txt`。 |
| 原地更新 | 从版本码 9 的前版更新到 10 成功，保留副本数据；不要求卸载原版。`runtime-logs/v2-install.log`。 |
| 真实播放器取源 | 原 libmpv 真实打开受控 HTTP 媒体，18 项通过：准确取出 URI、请求配置和 Unicode；暂停、未加载、多活跃源拒绝；weak client 关闭不挂起。`capture-tests/results/results.json`。 |
| HTTP 下载组件 | 23 项实际本地 HTTP/TLS 检查通过，涵盖无后缀 HLS、重定向最终基址、query-only/编码参数、Cookie、跨 host 凭据剥离、AES/IV/非零 sequence、简单 master、重试及错误清理。自签 TLS 被拒绝，未关闭验证。`download-tests/results.json`。 |
| 完整 App 明文 HLS 下载保存 | 原入口按钮 → 捕获真实 MPV 源 → HTTP 分片下载 → 本地合并 → Android 系统保存窗口 → MP4 成功。92,200 字节，2.043356 秒，H.264/AAC。 |
| 完整 App AES-128 HLS 下载保存 | 相同流程，包含真实密钥请求和显式 IV，生成 92,200 字节 H.264/AAC MP4。不是提前塞入缓存代替下载。 |
| 完整 App 直接 MP4 保存 | 无扩展名网关经重定向返回 MP4，实际下载并验证保存；72,367 字节、2 秒、H.264/AAC。 |
| 生成媒体完整性 | 三份文件音视频均完整解码；明文/加密各 48 帧，直接 MP4 30 帧，视频逐帧哈希与各自参考一致。`ui-download-tests/results/media-results.json`。 |
| 原有 AES-128 缓存导出复测 | 覆盖更新后，经正常入口、缓存列表和系统保存窗口成功保存原有合成缓存；92,200 字节、完整解码。`ui-download-tests/results/cache-regression.json`。 |
| 完整 App 失效链接 | 源捕获后受控服务改为 HTTP403；App 显示阶段和 HTTP 状态，删除系统目标文件及私有临时目录。`ui-download-tests/results/ui-results.json`、`clear-expired-failure.xml`。 |

完整 UI 截图、XML、实际拉回的 MP4 位于 `ui-download-tests/results/`。测试用 instrumentation APK 只用于云端验证，没有打入交付 APK。

## 原始载荷和行为边界

原 186 个 assets、21 个原生库与 53 个非签名 META-INF 项逐字节保留，见 `payload-audit.json`。新增播放器观察库仅依赖 libdl/libc，使用独立 weak client 和事件队列；新增本地 FFmpeg 隐藏符号并绑定在自身内部，原 libmpv 不变。源和请求凭据只在内存交接，不放入 Intent 或日志；临时媒体和密钥会在结束时清理。

保存支持普通有限 HLS、标准 AES-128、简单复用音视频的 master 和可探测时长的直接媒体；复杂独立音轨、fMP4 MAP、byterange、直播、DRM/SAMPLE-AES 及不服从 identity 请求的压缩响应会明确拒绝。连接/读取超时 10/15 秒，取消可能需等待阻塞网络返回。

原缓存导出的 21 项格式检查和首版完整 UI 证据保留在 `playlist-tests/results.json`、`runtime-logs/final-ui/`；其清单处理源未改变。本版旧缓存 UI 复测结果另见 `ui-download-tests/results/cache-regression.json`。

## 尚未验证

- 原版与导出版在云端都停在平台线路选择，未取得真实首页、账号或平台播放流。以上受控测试不能替代真实视频验证，也不能保证每个真实视频格式都支持。
- ARM64/ARMv7 完成编译，尚未在 ARM 手机执行；当前执行证据为 x86_64 Android。
- 并存副本使用独立签名和私有数据，不自动继承原版账号、设备身份和缓存。export2 沿用此前导出版签名，可覆盖更新那个副本。

云环境的 Android 启动/验证说明已追加保存到配置草稿；保存草稿不等于运行时应用或发布。需要后续复用时，在环境设置审阅保存并发布。

[安装包](X2-cache-export.apk) · [使用说明](使用说明.md) · [补丁和完整 FFmpeg 源码](X2-cache-export-source.zip)
