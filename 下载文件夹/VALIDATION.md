# export15 验证记录

APK SHA-256：`1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46`

测试为云端Android API29 x86_64及ARM64/x86_64指令仿真，**不是用户红米Android16的实际目标视频验证**。

## ui-results.json

```json
{
  "preview15": {
    "passed": true
  },
  "apk_sha256": "1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46",
  "real_target_video_over_20_seconds_verified": false,
  "source15": {
    "passed": true
  },
  "delete12": {
    "passed": true
  }
}
```

## installed-results.json

```json
{
  "installed_sha256": "1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46",
  "matches_delivery": true
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46",
  "original_Flutter_activity_started": true,
  "patched_libapp_and_original_libflutter_mapped": true,
  "process_survived_startup": true,
  "no_native_fatal_or_snapshot_compatibility_error_in_process_log": true,
  "real_platform_related_page_not_tested": true
}
```

## payload-results.json

```json
{
  "preserved_original_native_libraries": 19,
  "changed_original_native_libraries": {
    "lib/arm64-v8a/libapp.so": {
      "changed_bytes": 1160,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    },
    "lib/x86_64/libapp.so": {
      "changed_bytes": 1029,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    }
  },
  "output_sha256": "1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46"
}
```

## comparison-results.json

```json
{
  "compared_to_release": "export14",
  "core_download_queue_service_remux_settings_unchanged": true,
  "changed_native_files": [
    "lib/arm64-v8a/libapp.so",
    "lib/x86_64/libapp.so",
    "lib/arm64-v8a/libx2player.so",
    "lib/armeabi-v7a/libx2player.so",
    "lib/x86_64/libx2player.so"
  ],
  "unchanged_native_file_count": 22,
  "machine_test_payload_matches_delivered_AOT": true,
  "apk_sha256": "1c1fe3d61dd86b2067491f77739708da1e2d93a394def25caece0bee248a0e46"
}
```

## detail-machine-results.json

```json
{
  "passed": true,
  "cases": [
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "true",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "false",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "unknown_bool",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "wrong_class",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "null",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 0,
      "case": "large_ints",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "true",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "false",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "unknown_bool",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "wrong_class",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "null",
      "passed": true
    },
    {
      "abi": "arm64-v8a",
      "compressed_heap_high32": 1,
      "case": "large_ints",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "true",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "false",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "unknown_bool",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "wrong_class",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "null",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 0,
      "case": "large_ints",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "true",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "false",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "unknown_bool",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "wrong_class",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "null",
      "passed": true
    },
    {
      "abi": "x86_64",
      "compressed_heap_high32": 1,
      "case": "large_ints",
      "passed": true
    }
  ],
  "scope": "Dart leaf numeric copies, both ABIs; no real API response"
}
```


详情叶子拷贝覆盖两架构、两种压缩堆基址、true/false/未知布尔、空对象、错误类型及64位大整数，共24例；另重跑原任务/短标题/首屏标记、40例完整位置回调和40例getter响应式读取。交付AOT与指令测试文件逐字节对应。

手机端用测试专用辅助库在真实映射的AOT BSS中播种180时长、canWatch=false的合成详情，检查URI精确对应、错误URI、未完成序列及坏标记拒绝，然后通过原MPV/最近源缓存读取12秒HLS并复制结果。合成详情不是服务器返回结果；测试播种入口不在用户APK中。

封面测试使用真实SAF MP4，检查图像与时长、尺寸上限、16:9、驱逐内存并临时破坏测试源后仍能读取磁盘缓存、真实触摸点击携带URI授权播放、多选不播放、无效文件不误用其他封面。另回归单项/批量物理删除与失败保留记录。初次预览断言将ImageView空Bitmap占位当成已完成图像；直接提取测试证明媒体可读，修正空占位清除及断言后重新验证；卡片分页测试等待实际列表布局完成，再进行触摸与失败文件检查。

核心下载、任务服务、队列、封装和下载设置与export14源文件一致。变更限定为详情诊断、卡片及本地缩略图缓存。历史测试不冒充当前构建实测。
