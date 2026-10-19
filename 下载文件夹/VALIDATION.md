# export3 验证记录

交付版本：`9.9.9-export3` / versionCode `11`，包名 `com.example.yinqishe_export`。

APK SHA-256：`88c253f049fd1ee697d05175f14b74276ac9742ec7f67f6d68b6ab24cfe81de2`。

签名证书 SHA-256：`19c423563275d66946f687449c13adf55e76e82a7381209b0aea2fe53f7e1a0b`，沿用导出版已有签名，APK v2/v3 验证通过。模拟器安装文件再次计算 SHA-256，与交付文件一致。

后台场景候选 APK 校验值为 `5c2cbc4a469e7b169328bb2a410405e304613f2fe5c0a9bbf78df9387aad197e`。之后唯一改动是 DownloadConfig 显示系统目录的实际名称；下载服务、任务队列、媒体组件与滚动补丁均未改变。目录与重试、捕获入口及启动检查使用最终包验证。源码包附带两个构建的源码摘要对比。

## 下载与管理

运行环境为官方 AOSP Android 10 / API 29 x86_64 模拟器；输入为本地 HTTP 受控合成视频，不使用平台账号或真实平台影片。测试 APK 与 UI 探针独立安装，仅用于验证，用户 APK 不包含测试入口、服务器地址或测试素材。

- 首次使用两个并排按钮，实际点击“下载”，经系统 ACTION_OPEN_DOCUMENT_TREE 选择目录 A；获得持久目录授权并保存第一份 MP4。
- 实际设置并发为 2。随后结束测试 instrumentation，启动生产下载管理页；真正执行传输的是生产 DownloadService，后台传输期间没有 instrumentation 驻留目标进程。
- 受控任务 A/B 同时传输，C/D 排队。UI 删除排队任务 D，服务端没有收到 D 请求；UI 取消并删除正在执行的 A，B/C 继续执行。
- 观察到 foreground `isForeground=true`、活动期间的 PARTIAL_WAKE_LOCK，并通过系统 power 状态确认退到桌面和屏幕 Asleep/Dozing。
- 屏幕熄灭后才放行剩余 B/C 的主体数据，检查其最终 MP4，而非仅检查通知。

最终包另外验证：通过系统目录选择器更改为目录 B，新任务确实写到 B，原 A 的输出仍保留；HTTP 403 错误明确显示，恢复受控服务后通过 UI 重试成功，生成的 MP4 完整解码；删除完成记录不会删除文件；结束并重启应用进程后目录 B 仍然可用。

详细结果以源码包 `validation/export3-tests/*-results.json` 为准。取消请求后服务端可能延迟发现 TCP 断开：本轮 A 的 socket 在 C 开始后约 1.82 秒才结束，因此服务端瞬时观测到 3 个连接；这包含已取消 A 的连接收尾，不是 3 个任务同时运行。生产服务按 `running` 集合控制并发，管理页活动任务保持上限 2。

模拟器在重启 Android 框架后出现过 System UI 无响应；恢复后重新建立受控任务。较早的自动化尝试受到系统弹窗、旧的 UI 刷新和恢复操作干扰，不记为通过。最终场景对实际 UI、后台文件、媒体解码和队列文件重新核对。

最终包也经原 MPV 播放器的受控播放源验证：两个按钮并排；点击“下载”后仍停留在原 Activity，使用记住的 B 目录输出第二份视频，不弹目录选择器。之后原壳弹出“网络不给力”阻挡按钮自动化，故由测试命令直接打开管理页核对“已保存 MP4”；未把这一步记作原平台在线播放或管理按钮点击测试。

## 推荐区域滚动

原 ARM64 AOT `_buildTabBarViewZeroChildWidget` 位于 `0x63bba4`，x86_64 对应 `0x6e1788`。返回 Padding，其 child 是 GetBuilder，builder 返回推荐 VideoBaseCell 的 Wrap；该结构位于 TabBarView 中，没有纵向滚动容器。

修复将此处外层 Padding 替换为 SingleChildScrollView，保留 padding 与 GetBuilder child，使用 vertical、reverse=false、dragStart=start、clip=hardEdge、hitTest=opaque、keyboardDismiss=manual，其余可空字段维持 null。

- 两架构均用 Unicorn 实际执行补丁初始化指令，验证 8 个字段、返回对象、固定寄存器与栈均正确。
- allocation call 留在原调用点，保留返回 PC 和现有 GC 栈图；外部初始化块不调用函数、不分配、不包含 safepoint。
- 输入快照按 SHA-256 锁定；修改被限制为分配调用、跳转、零填充区初始化块及 RX 段大小。文件长度不变。ARM64 实际改动 94 字节，x86_64 改动 78 字节。
- 原 21 个原生库中 19 个字节完全一致；仅上述两个 libapp.so 接受限定修复，原 libmpv/libflutter 保持不变。
- ARMv7（32 位）没有应用滚动补丁。

此项属于有依据的代码修复与指令验证。当前云机无法连接真实平台页面，尚未在真实相关推荐页端到端验证；不能保证这一个修复覆盖所有原生页面的滚动问题。按钮手势测试仅能证明新增按钮的事件转发，不作为原 Flutter 推荐页已修复的证据。

最终包已直接启动原 Flutter MainActivity，确认原 Flutter 画面渲染、libapp/libflutter 均加载、进程存活，日志没有 native fatal 或 snapshot 不兼容错误；当前停留在原应用选择网络线路阶段，未进入真实视频推荐页。新增按钮手势测试从按钮起始滑动后列表偏移 85 像素，重复滑动后偏移 2605 像素。目录 B 两份最终包生成的 MP4 均完整解码通过。

## 沿用的媒体组件回归证据

本次没有改变 MediaDownloader、PlaylistPreparer、PlayerCapture 或 NativeRemux 的媒体处理逻辑。源码保留此前 23 项本地 HTTP/TLS 下载测试、18 项真实 Android MPV 捕获测试及缓存/封装测试记录；这些用于说明未改动组件的覆盖范围，不将旧版 UI 测试误记为新版后台测试。

已支持普通有限 HLS、AES-128 和可探测时长的直接媒体；直播、DRM/SAMPLE-AES、复杂独立音轨、MAP/byterange 等仍不在支持范围内。真实平台链接的可用性、过期时间、权限和厂商后台省电策略仍会影响实际下载；没有关闭 TLS 校验或伪造平台权限。
