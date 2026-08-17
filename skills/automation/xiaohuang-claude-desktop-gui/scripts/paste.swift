#!/usr/bin/env swift
// paste.swift — 激活Claude Desktop并粘贴剪贴板内容
// 用法: pbcopy < task.txt && swift paste.swift
import Cocoa
import Foundation

// 激活Claude
NSRunningApplication.runningApplications(withBundleIdentifier: "com.anthropic.claudefordesktop").first?.activate(options: .activateIgnoringOtherApps)
usleep(500000)

// 从剪贴板读取内容
let pasteboard = NSPasteboard.general
guard let content = pasteboard.string(forType: .string), !content.isEmpty else {
    print("ERROR: 剪贴板为空")
    exit(1)
}

let src = CGEventSource(stateID: .hidSystemState)

// Cmd+A 全选（清空输入框旧内容）
let cmdA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
cmdA.flags = .maskCommand
cmdA.post(tap: .cghidEventTap)
usleep(100000)
let cmdAUp = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: false)!
cmdAUp.flags = .maskCommand
cmdAUp.post(tap: .cghidEventTap)
usleep(200000)

// Delete 清空
let delete = CGEvent(keyboardEventSource: src, virtualKey: 0x33, keyDown: true)!
delete.post(tap: .cghidEventTap)
usleep(100000)
let deleteUp = CGEvent(keyboardEventSource: src, virtualKey: 0x33, keyDown: false)!
deleteUp.post(tap: .cghidEventTap)
usleep(200000)

// Cmd+V 粘贴
let cmdV = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: true)!
cmdV.flags = .maskCommand
cmdV.post(tap: .cghidEventTap)
usleep(100000)
let cmdVUp = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: false)!
cmdVUp.flags = .maskCommand
cmdVUp.post(tap: .cghidEventTap)

usleep(300000)
print("Paste sent (\(content.count) chars)")
