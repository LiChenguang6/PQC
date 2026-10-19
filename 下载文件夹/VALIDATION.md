# export10 候选修复验证

APK SHA-256：`50260d992df1821b1ac0a7c4692ecace261b4608de062aa9f6e4e5f6da8cd514`

**真实禁区视频播放 >20 秒：未通过验证（无法取得真实流，非已证明仍停止）。**

PlayerController 的位置回调在 >20 秒且 canWatch=false 时，独立调用 pause 后 seek。加入测试开关分支避免该本地停止路径；保持位置写入、进度回调、通知及开关关闭时的原行为。

40 个完整回调指令测试覆盖 ARM64/x86_64 × 开关开/关 × canWatch 开/关 × 19/20/21/25/65 秒。媒体调用由桩记录，不是实际播放，没有用测试视频替代平台视频。

## network-results.json

```json
[
  {
    "host": "d1r1vv8zvbqvut.cloudfront.net",
    "status": 403,
    "headers": {
      "content-type": "text/plain; charset=UTF-8",
      "server": "envoy",
      "x-cache": "Error from cloudfront"
    },
    "error_body": "error code: 1010\n"
  },
  {
    "host": "drlcjvmgp6ra1.cloudfront.net",
    "status": 403,
    "headers": {
      "content-type": "text/plain; charset=UTF-8",
      "server": "envoy",
      "x-cache": "Error from cloudfront"
    },
    "error_body": "error code: 1010\n"
  },
  {
    "host": "rea.5mv4d9bn.work",
    "error": "<urlopen error Tunnel connection failed: 403 Forbidden>"
  },
  {
    "host": "rea.5n4v4dkk.work",
    "error": "<urlopen error Tunnel connection failed: 403 Forbidden>"
  },
  {
    "host": "rea.66zif0m5.work",
    "error": "<urlopen error Tunnel connection failed: 403 Forbidden>"
  },
  {
    "host": "rea.68zvqszy.work",
    "error": "<urlopen error Tunnel connection failed: 403 Forbidden>"
  }
]
```

## comparison-results.json

```json
{
  "passed": true,
  "baseline_commit": "1c48f22b5ac8fb96a608edca33ffeae9fff92197",
  "all_dex_and_assets_byte_identical": true,
  "all_java_sources_byte_identical": true,
  "original_native_libraries_preserved_except_two_declared_snapshots": true,
  "changed_entries": [
    "AndroidManifest.xml",
    "lib/arm64-v8a/libapp.so",
    "lib/x86_64/libapp.so",
    "META-INF/X2-EXPOR.SF",
    "META-INF/X2-EXPOR.RSA",
    "META-INF/MANIFEST.MF"
  ],
  "apk_sha256": "50260d992df1821b1ac0a7c4692ecace261b4608de062aa9f6e4e5f6da8cd514"
}
```

## installed-results.json

```json
{
  "installed_sha256": "50260d992df1821b1ac0a7c4692ecace261b4608de062aa9f6e4e5f6da8cd514",
  "matches_delivery": true
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "50260d992df1821b1ac0a7c4692ecace261b4608de062aa9f6e4e5f6da8cd514",
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
      "changed_bytes": 985,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    },
    "lib/x86_64/libapp.so": {
      "changed_bytes": 854,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    }
  },
  "output_sha256": "50260d992df1821b1ac0a7c4692ecace261b4608de062aa9f6e4e5f6da8cd514"
}
```

完整 pause-results.json、getter-results.json、machine-results.json 在源码包 validation/export10-tests 中。下载功能字节码与 export9 完全一致，本次没有重复全部历史下载测试。
