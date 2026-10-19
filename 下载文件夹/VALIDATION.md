# export6 验证记录

版本 `9.9.9-export6` / versionCode `14`，包名 `com.example.yinqishe_export`。

APK SHA-256：`a01c1186d55c68a97dac0f26d80176caab73eb981c6e75473e226e371e8e460c`。

签名证书沿用此前版本：`19c423563275d66946f687449c13adf55e76e82a7381209b0aea2fe53f7e1a0b`。构建执行 APK v2/v3 签名验证。模拟器安装文件再次计算 SHA-256 与交付文件一致。

## 取消／删除重启

旧模拟器 crash 日志保留了明确证据：`playback-download-cancel` 线程抛出 `java.lang.IllegalStateException: Unbalanced enter/exit`，来自 Android OkHttp/Okio 关闭正在读取的流，最终落在 `MediaDownloader$Session$1.run`。旧代码只捕获 IOException，未捕获该运行时异常。现在关闭连接和流的取消线程捕获这些异常，工作线程继续按取消标记退出与清理。

`onStartCommand` 在每次新命令时立即恢复前台通知，防止空闲退出与新启动交错后未履行前台服务约束。没有通过吞掉整个进程的所有异常来掩盖错误。

生产服务实际回归：暂停 A 后进度不变、名额交给 B；A 请求继续时按并发上限等待，取消 B 后 A 恢复；删除暂停 A 正常完成；连续 25 次空闲取消指令并等待超过前台启动期限，测试进程仍存活。暂停持久化及重启后继续由独立 instrumentation 进程验证。测试只使用本地合成视频。

## 主页与标题

- ARM64/x86_64 Unicorn 执行短视频 getter 两处叶子补丁，连续处理 5 个中文／表情标题及 URI，确认 4 槽环形快照保留最近数据。
- 两种架构执行左侧标签选择：索引 0 发送本机管理事件并保持视频页，其他索引不变；仅“活动”标题替换为原已有“下载”字符串，不改写 Dart 字符串内容或哈希。
- 独立测试 APK 验证实际浮层只剩一个按钮，原生事件经生产 JNI/轮询打开 DownloadTasksActivity。原管理功能作为左侧入口的页面实现保留。
- 生产 PlayerCapture JNI、原 libmpv、真实合成视频播放验证：按完全相同 URI 匹配标题，错误 URI／写入中快照不用，下一部预加载标题不覆盖当前短视频标题；管理事件只消费一次。
- 输出命名和两份同名 MP4 完整下载、FFmpeg 解码回归；真实平台不可达，未直接验证真实短视频标题。

新增 AOT 叶子代码无调用、无分配和新 GC safepoint；不保留 Dart 堆指针。只在匿名 RW 空间复制有界 UTF-16；RW 内存增至 0x20000，文件长度不变。原 libmpv/libflutter 及其余 19 个原库字节一致；改动只覆盖两种 64 位 libapp 内声明范围。

## 禁区权限来源与本机测试开关

原 `UserService.updateAPIUserInfo` POST `user/base/info`，经 `UserInfo.fromJson` 更新用户资料。`isForbiddenVip` 读取 `vipType`，接受 7 或 8。未发现该入口只依靠一个设备本地白名单。

开发测试开关默认关闭，只影响客户端该 getter。两种架构测试关闭时走原判断，开启时本机入口返回允许。服务端登录、用户资料、播放接口和媒体授权未修改，也没有伪造服务端会员资料；这不是恢复服务器账号权限的证据。云端无法连通平台，真实禁区播放未验证。

## 证据范围

本次脚本与结果在源码包 `validation/export6-tests`。export5 及更早结果为历史证据，不能当作本次重跑。最初一次服务测试与 APK 覆盖安装交错，安装替换终止了测试进程；该次不计成功，最终版在安装校验完成后串行重测。

暂停不是持久化字节断点；原连接失效或进程重启后可能重下。最多额外保留暂停工作线程，使其他任务继续，但总工作线程上限为 64。真实平台、ARMv7 原有页面及 32 并发满负载没有实测。
