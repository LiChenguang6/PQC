# export8 验证记录

最终 APK SHA-256：`522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24`。Android API 29 x86_64 云端模拟器；ARM64 指令仿真。真实平台内容不可达，测试媒体为受控 MP4，不代表真实平台完整播放。

## installed-results.json

```json
{
  "installed_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24",
  "matches_delivery": true
}
```

## ui-results.json

```json
{
  "ui8": {
    "passed": true,
    "metrics": {
      "cold_activity_ms": "3887",
      "warm_activity_ms": "1884",
      "warm_rows": "1"
    }
  },
  "entry8": {
    "passed": true,
    "metrics": {}
  },
  "apk_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24",
  "drag": {
    "passed": true,
    "host": "native DownloadTasksActivity with controlled scrolling content",
    "position_persisted": true,
    "underlying_scroll_preserved": true,
    "manage_tap_after_drag": true
  }
}
```

## service-results.json

```json
{
  "passed": true,
  "paused_progress_stable": true,
  "paused_state_persists_across_process_restart": true,
  "paused_task_frees_parallel_slot": true,
  "resume_waits_for_parallel_slot": true,
  "cancel_other_task_resumes_waiting_task": true,
  "delete_while_paused_completes": true,
  "rapid_idle_cancel_commands": 25,
  "process_survived_more_than_foreground_deadline": true,
  "apk_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24"
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
    "development_switch_off_preserves_original_getter": true,
    "switch_on_returns_local_test_gate": true
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
    "development_switch_off_preserves_original_getter": true,
    "switch_on_returns_local_test_gate": true
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
      "changed_bytes": 961,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    },
    "lib/x86_64/libapp.so": {
      "changed_bytes": 851,
      "only_declared_UI_scroll_launch_title_tasks_and_development_patches": true,
      "file_length_unchanged": true
    }
  },
  "output_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24"
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24",
  "original_Flutter_activity_started": true,
  "patched_libapp_and_original_libflutter_mapped": true,
  "process_survived_startup": true,
  "no_native_fatal_or_snapshot_compatibility_error_in_process_log": true,
  "real_platform_related_page_not_tested": true
}
```

## filename-download-results.json

```json
{
  "passed": true,
  "two_same_title_jobs_saved_separately": true,
  "both_MP4_decode": true,
  "continued_after_HOME": true,
  "output_names": [
    "中文命名测试😀_第一集 (6).mp4",
    "中文命名测试😀_第一集 (7).mp4"
  ],
  "output_sha256": "522df59009e97c96667860fe76bc1c28f3e6c8e765c7c200eece5eccaa0eed24"
}
```

已完成项测试验证了带读权限的 ACTION_VIEW / ClipData 请求；没有把外部播放器实际播放算作已完成的验证。拖动在独立原生宿主上测得，原 MainActivity 的双按钮管理／设置入口另有通过记录。一次重复 Flutter 仪器启动停留在启动画面，终止该次用例后改用原生宿主验证拖动；正常启动另测，真实平台首页仍不可达。

历史版本报告保存在源码包，不能作为本构建的实测结果。
