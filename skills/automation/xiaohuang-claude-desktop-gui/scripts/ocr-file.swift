#!/usr/bin/env swift
// ocr-file.swift — macOS Vision OCR识别图片中的文字
// 用法: swift ocr-file.swift <image.png>
// 注意: Retina截图需要先 sips -z 900 1440 缩放
import Cocoa
import Vision
import Foundation

guard CommandLine.arguments.count > 1 else {
    print("用法: swift ocr-file.swift <image.png>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let image = NSImage(contentsOfFile: imagePath) else {
    print("ERROR: 无法加载图片 \(imagePath)")
    exit(1)
}

guard let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERROR: 无法转换为CGImage")
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
request.recognitionLanguages = ["zh-Hans", "en-US"]

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try handler.perform([request])

guard let observations = request.results else {
    print("OCR: 无识别结果")
    exit(0)
}

for obs in observations {
    guard let candidate = obs.topCandidates(1).first else { continue }
    let box = obs.boundingBox
    let x = Int(box.origin.x * CGFloat(cgImage.width))
    let y = Int((1 - box.origin.y - box.height) * CGFloat(cgImage.height))
    print("(\(x),\(y)) \(candidate.string)")
}
