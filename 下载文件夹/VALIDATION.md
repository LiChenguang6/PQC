# export13 验证记录

APK SHA-256：`9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82`

测试环境为Android API29 x86_64云端模拟器及ARM64/x86_64指令仿真；不是用户的红米Turbo4Pro/Android16。**真实禁区视频连续播放超过20秒仍未验证通过。**

## ui-results.json

```json
{
  "delete12": {
    "passed": true,
    "properties": {}
  },
  "apk_sha256": "9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82",
  "real_forbidden_video_over_20_seconds_verified": false,
  "appearance12": {
    "passed": true,
    "properties": {
      "launcher_pin_supported": "true",
      "launcher_pinned_and_updated": "true"
    }
  },
  "cover13": {
    "passed": true,
    "properties": {}
  },
  "diagnostic11": {
    "passed": true,
    "properties": {
      "numeric_state": "players=1 p0[pos=0.00 dur=2.02 pause=1 eof=0 idle=0]"
    }
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
  "apk_sha256": "9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82"
}
```

## installed-results.json

```json
{
  "installed_sha256": "9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82",
  "matches_delivery": true
}
```

## flutter-startup-results.json

```json
{
  "final_apk_sha256": "9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82",
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
  "output_sha256": "9e15cd584112ca9f571043e0f010cee032293f942d38e77a9cc44fcc50086f82"
}
```

文件操作用例使用真实SAF文档，检查记录删除保留文件、批量物理删除、失败保留记录、单项／批量菜单及确认。外观用例实际固定并更新桌面入口，检查导入、非法图片保护、可关闭封面、设置入口及恢复默认保留无关文件。封面关闭在受控原生宿主中检查；另在原Flutter启动Activity中用测试专用主页就绪标记验证封面保持及移除。该标记由测试注入，不代表真实平台首页已加载。真实平台冷启动仍受原网络初始化影响。

播放诊断用受控短MP4检查原MPV数值读取、失焦时同步、隐私字段不泄漏及复制；不是禁区播放证明。pause-results.json覆盖40个完整位置回调与计数，getter-results.json保留Rx读取回归。后台控制测试验证暂停、并发名额、取消／删除、重启保留暂停状态。

历史export12首次界面用例曾被模拟器SystemUI无响应弹窗遮挡，处理后重跑通过。未发布的诊断实现曾出现引用释放循环错误，已修正，最终APK诊断用例通过。本轮连续启动Flutter时，模拟器曾阻塞在原Flutter的nativeSurfaceCreated；结束该进程后单独重跑诊断。历史报告不作为本构建实测结论。
