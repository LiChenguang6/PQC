# export9 白屏修复验证

APK SHA-256：`df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2`

原 ForbiddenPage::build 的 Obx 闭包调用 UserService.isForbiddenVip；其原 getter 通过 Rx.value 建立订阅。export8 的测试入口提前返回，未执行任何 Rx 读取；RxNotifier.notifyChildrens 检查 canUpdate，无依赖时抛出 [Get] the improper use of a GetX 异常。此缺陷可解释保留原生浮层、其他栏目正常的白色错误页，但没有读取用户设备运行日志，不能排除其他原因。

ARM64/x86_64 共 40 个完整 getter 指令执行用例，涵盖开关开／关及会员类型 0、1、7、8、9。export8 开启时零次 Rx 读取；export9 原始读取次数全部保留，结果和栈均通过。Rx.value 由测试桩记录调用并返回受控模型，并非实际 Dart VM 中运行整个 Obx。

原 getter 在返回尾部之前与原 APK 逐字一致，无新增分配或调用。所有 Java 源码、dex 和 assets 与 export8 一致。下载功能沿用 export8 的实测记录，本版未重复全部下载用例。

## comparison-results.json

```json
{
  "passed": true,
  "baseline_commit": "6adae13d4f03223f2b21a097e366a3cc0c2ddfb6",
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
  "apk_sha256": "df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2"
}
```

## machine-results.json

```json
[
  {
    "abi": "arm64-v8a",
    "four_preloaded_video_titles_retained": true,
    "unicode_title_and_URI_copy": true
  },
  {
    "abi": "arm64-v8a",
    "left_tab_requests_native_manager": true,
    "other_tab_indices_preserved": true
  },
  {
    "abi": "arm64-v8a",
    "only_activity_caption_replaced": true
  },
  {
    "abi": "arm64-v8a",
    "preview_timer_off_calls_original": true,
    "preview_timer_on_returns_without_marking_end": true
  },
  {
    "abi": "x86_64",
    "four_preloaded_video_titles_retained": true,
    "unicode_title_and_URI_copy": true
  },
  {
    "abi": "x86_64",
    "left_tab_requests_native_manager": true,
    "other_tab_indices_preserved": true
  },
  {
    "abi": "x86_64",
    "only_activity_caption_replaced": true
  },
  {
    "abi": "x86_64",
    "preview_timer_off_calls_original": true,
    "preview_timer_on_returns_without_marking_end": true
  }
]
```

## payload-results.json

```json
{
  "preserved_original_native_libraries": 19,
  "changed_original_native_libraries": {
    "lib/arm64-v8a/libapp.so": {
      "changed_bytes": 957,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    },
    "lib/x86_64/libapp.so": {
      "changed_bytes": 831,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    }
  },
  "output_sha256": "df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2"
}
```

## installed-results.json

```json
{
  "installed_sha256": "df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2",
  "matches_delivery": true
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2",
  "original_Flutter_activity_started": true,
  "patched_libapp_and_original_libflutter_mapped": true,
  "process_survived_startup": true,
  "no_native_fatal_or_snapshot_compatibility_error_in_process_log": true,
  "real_platform_related_page_not_tested": true
}
```

## entry-results.json

```json
{
  "passed": true,
  "production_manager_and_settings_open": true,
  "apk_sha256": "df3a608df7e939c39df58945ce194e39ca17cd8f84e3a7401deafb84ae5be1b2"
}
```

真实平台接口不可达；本报告不声称已经验证禁区列表恢复或完整视频播放。
