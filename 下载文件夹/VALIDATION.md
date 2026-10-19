# export4 验证记录

版本 `9.9.9-export4` / versionCode `12`；包名 `com.example.yinqishe_export`。

APK SHA-256：`f5a1e541151c0441dadd5379bf6e81e6df8a1791cfb9e59a21323a55b0c3bbe2`。

沿用此前导出版签名，证书 SHA-256：`19c423563275d66946f687449c13adf55e76e82a7381209b0aea2fe53f7e1a0b`。APK v2/v3 验证通过，安装后的文件再次计算 SHA-256 与交付文件一致，模拟器正常覆盖安装，原目录设置和记录保留。

## 本次实际验证

使用官方 AOSP API 29 x86_64 模拟器、独立测试 APK 和本地合成视频。用户 APK 不含测试入口或本地测试服务地址。

- 通过真实触摸事件把两个按钮作为一组拖动，确认没有触发按钮点击、没有把拖动变成底层页面滚动。重建页面及结束进程后重新打开均恢复位置；移动后的“管理”按钮仍可打开管理页。未覆盖位置正常滑动，受控列表偏移 286 像素。
- 下载设置的整数输入框拒绝 0；输入 5 并保存，结束并重启进程后配置仍为 5。
- 加入 7 个独立任务，测试 instrumentation 结束后由生产前台服务执行。管理页显示进行中 5、等待 2；服务端实际观测到同时传输 5 路。
- 确认服务 `isForeground=true`；返回桌面并使屏幕进入 Asleep/Dozing 后，才放行剩余主体数据。7 个任务全部完成，所有新生成 MP4 均经 FFmpeg 完整解码通过。
- 最终 APK 直接启动原 Flutter MainActivity，确认 libapp/libflutter 加载、进程存活，无 native fatal 或快照不兼容错误。

32 个并发请求未在模拟器中实际压测；1–32 的范围由输入校验、配置和动态线程池共同执行。较大的数值会增加设备资源占用。减少并发不会中断已开始的任务。

## 英文网络提示与切换视频弹层

静态定位到原 `ApiExceptionHandler._debugPrintError` 将网络异常原始文本传给 showToast。只移除了这一个显示调用，后续日志、网络失败传播和其他错误提示保留。没有关闭 TLS 检查或修改登录、权限和播放授权判断。

原 VideoPlayByVideoIdController.onInit 会创建推广弹层，再由关闭动作触发 `_showAllEntranceAdsDismissAction` 初始化播放。本补丁将该调用直接转向原关闭后的初始化方法，跳过入场推广容器，保留视频详情更新、播放器事件绑定等原逻辑。这与用户描述的可关闭空白遮罩相符，但由于真实平台页面在云端不可达，未直接复现该具体弹窗。

ARM64 和 x86_64 均使用 Unicorn 执行 patched onInit 指令路径：基础 onInit 执行、原推广容器未调用、同一个 controller 传给原关闭后初始化方法，栈与返回值正确。原错误 toast 调用改为 NOP，后续处理代码保持原字节。保留原 call 返回 PC，不引入新的 GC safepoint。

这些是精确代码与指令验证，并不等于真实平台影片的端到端验证。上述两项及原相关推荐滚动补丁覆盖 ARM64/x86_64；ARMv7 保留原页面行为。

## “更多同类视频”为什么只有 12 个

原客户端每次打开视频只请求一次 `video/guessLike`，查询参数只有 videoId。完整返回列表直接赋给推荐数据，未发现本地 take(12) 或对应截断，也没有页码、游标、触底续载逻辑。

用户观察到单批 12 项；当前无法确认服务器是否支持分页或更大批次。因此本版没有实现无限相关推荐，不能声称已突破 12 项。原来的推荐区域纵向滚动补丁保留。

## 原有组件与修改范围

用户确认下载队列可见，本次恢复并保留 export3 的 DownloadTasksActivity 源码。MediaDownloader、DownloadStore、PlaylistPreparer、PlayerCapture、NativeRemux 和两个新增原生媒体库的源码未修改；本次下载服务改为按配置调整线程池。

原 21 个原生库中 19 个字节完全一致。仅 ARM64 与 x86_64 的 libapp.so 包含限定滚动及两处 UI 调用修改：分别改变 99 和 84 字节，文件长度不变。原 libmpv/libflutter 保持不变。

源码包 `validation/export4-tests` 包含本次脚本与结果；`export3-tests` 和其他历史结果用于保留未修改媒体组件的先前覆盖，不能当作本次新增功能的测试。后台限制、链接过期以及不支持的直播/DRM/复杂 HLS 格式仍按使用说明处理。
