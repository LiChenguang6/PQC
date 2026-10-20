# export14 验证记录

**真实指定视频超过20秒尚未验证，不能把受控素材当作成功。**

APK SHA-256：`5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266`

## inspection-results.json

```json
{
  "passed": true,
  "cases": [
    {
      "case": "short",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=0\nvariant_policy=original_media_playlist\nsegments=2\nmanifest_seconds=12.070\nendlist=1\nencrypted=0\nnonstandard_encryption=0\n"
    },
    {
      "case": "long",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=0\nvariant_policy=original_media_playlist\nsegments=15\nmanifest_seconds=90.000\nendlist=1\nencrypted=0\nnonstandard_encryption=0\n"
    },
    {
      "case": "live",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=0\nvariant_policy=original_media_playlist\nsegments=3\nmanifest_seconds=18.000\nendlist=0\nencrypted=0\nnonstandard_encryption=0\n"
    },
    {
      "case": "encrypted",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=0\nvariant_policy=original_media_playlist\nsegments=2\nmanifest_seconds=12.000\nendlist=1\nencrypted=1\nnonstandard_encryption=0\n"
    },
    {
      "case": "master",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=1\nvariant_policy=highest_bandwidth\nsegments=15\nmanifest_seconds=90.000\nendlist=1\nencrypted=0\nnonstandard_encryption=0\n"
    },
    {
      "case": "redirect",
      "passed": true,
      "report": "http=200\nkind=hls\nmanifest_depth=0\nvariant_policy=original_media_playlist\nsegments=15\nmanifest_seconds=90.000\nendlist=1\nencrypted=0\nnonstandard_encryption=0\n"
    },
    {
      "case": "direct",
      "passed": true,
      "report": "http=200\nkind=direct_or_unknown\nmanifest_depth=0\n"
    },
    {
      "case": "json",
      "passed": true,
      "report": "http=200\nkind=json\nmanifest_depth=0\n"
    },
    {
      "case": "invalid",
      "passed": true,
      "report": "error=ReportedException"
    },
    {
      "case": "huge",
      "passed": true,
      "report": "error=ReportedException"
    },
    {
      "case": "denied",
      "passed": true,
      "report": "error=ReportedException"
    }
  ],
  "segment_and_key_requests": 0,
  "cross_origin_auth_stripped": true,
  "report_excludes_fixture_credentials": true,
  "temporary_directories_cleaned": true
}
```

## ui-results.json

```json
{
  "source14": {
    "passed": true
  },
  "delete12": {
    "passed": true
  },
  "apk_sha256": "5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266",
  "real_target_video_over_20_seconds_verified": false
}
```

## installed-results.json

```json
{
  "installed_sha256": "5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266",
  "matches_delivery": true
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266",
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
      "changed_bytes": 1023,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    },
    "lib/x86_64/libapp.so": {
      "changed_bytes": 872,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    }
  },
  "output_sha256": "5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266"
}
```

## comparison-results.json

```json
{
  "compared_to_release": "export13",
  "existing_media_download_implementation_unchanged": true,
  "all_native_libraries_identical_to_export13": true,
  "native_library_count": 27,
  "unchanged_source_files": [
    "src/org/x2/export/VideoFilename.java",
    "src/org/x2/export/CacheExportActivity.java",
    "src/org/x2/export/PlaylistPreparer.java",
    "src/org/x2/export/DownloadConfig.java",
    "src/org/x2/export/AppearanceActivity.java",
    "src/org/x2/export/NativeRemux.java",
    "src/org/x2/export/PlayerCapture.java",
    "src/org/x2/export/Appearance.java",
    "src/org/x2/export/DownloadService.java",
    "src/org/x2/export/PlayingExportActivity.java",
    "src/org/x2/export/DownloadTasksActivity.java",
    "src/org/x2/export/ExportEntry.java",
    "src/org/x2/export/DownloadStore.java",
    "src/org/x2/export/DownloadQueueCache.java",
    "native/player_capture.c",
    "native/page_title.h",
    "native/export_bridge.c"
  ],
  "apk_sha256": "5b75155bf9f4316c5ed55806c96112bf7fcdf1602f3b7e2232887e2d6412c266"
}
```


主机用11种清单/传输场景验证时长、ENDLIST、主清单选择、错误响应、长度限制、跨域凭据隔离及复制报告脱敏，未请求分片/密钥。Android API29 x86_64上用受控12秒HLS、原MPV和背景采样，先播放再暂停，验证设置入口、最近源回退、清单统计与复制；同时回归实际SAF文件删除。

首次手机端检查暴露了暂停后原snapshot不再返回地址的问题，已加入开启开发测试时的30秒内存快照，并重新构建验证。历史export13的完整后台/外观/两架构指令用例是基线，未冒充本构建重跑。comparison-results记录现有下载器实现和所有原生库与export13逐字节相同；新增代码为Java检查与诊断采样。
