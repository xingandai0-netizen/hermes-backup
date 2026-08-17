#!/usr/bin/env swift
// clear-input.swift — 激活Claude Desktop并清空输入框
// 用法: swift clear-input.swift
import Cocoa
import Foundation

// 激活Claude
NSRunningApplication.runningApplications(withBundleIdentifier: "com.anthropic.claudefordesktop").first?.activate(options: .activateIgnoringOtherApps)
usleep(500000)

let src = CGEventSource(stateID: .hidSystemState)

// Cmd+A 全选
let cmdA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
cmdA.flags = .maskCommand
cmdA.post(tap: .cghidEventTap)
usleep(100000)
let cmdAUp = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: false)!
cmdAUp.flags = .maskCommand
cmdAUp.post(tap: .cghidEventTap)
usleep(200000)

// Delete
let delete = CGEvent(keyboardEventSource: src, virtualKey: 0x33, keyDown: true)!
delete.post(tap: .cghidEventTap)
usleep(100000)
let deleteUp = CGEvent(keyboardEventSource: src, virtualKey: 0x33, keyDown: false)!
deleteUp.post(tap: .cghidEventTap)

print("Input cleared")
