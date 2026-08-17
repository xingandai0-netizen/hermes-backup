# Canvas动画在React中的实现模式

## 基本模式

```typescript
'use client'
import { useRef, useEffect } from 'react'

export default function Component() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (canvasRef.current) {
      initAnimation(canvasRef.current)
    }
  }, [])

  return (
    <canvas 
      ref={canvasRef} 
      width={200} 
      height={200}
      className="opacity-70 hover:opacity-100 transition-opacity"
    />
  )
}

function initAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  let time = 0
  const width = canvas.width
  const height = canvas.height

  function draw() {
    ctx.clearRect(0, 0, width, height)
    time += 0.03

    // 绘制逻辑...

    requestAnimationFrame(draw)
  }

  draw()
}
```

## 小道童角色绘制

```typescript
// 身体
ctx.fillStyle = 'rgba(80, 80, 80, 0.6)'
ctx.beginPath()
ctx.roundRect(-18, -25, 36, 45, 8)
ctx.fill()

// 头
ctx.fillStyle = 'rgba(100, 100, 100, 0.7)'
ctx.beginPath()
ctx.arc(0, -35, 14, 0, Math.PI * 2)
ctx.fill()

// 道士帽
ctx.fillStyle = 'rgba(70, 70, 70, 0.5)'
ctx.beginPath()
ctx.moveTo(-14, -40)
ctx.lineTo(0, -58)
ctx.lineTo(14, -40)
ctx.closePath()
ctx.fill()

// 眼睛
ctx.fillStyle = 'rgba(200, 200, 200, 0.8)'
ctx.beginPath()
ctx.arc(-5, -36, 2, 0, Math.PI * 2)
ctx.arc(5, -36, 2, 0, Math.PI * 2)
ctx.fill()

// 微笑
ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)'
ctx.lineWidth = 1.5
ctx.beginPath()
ctx.arc(0, -32, 5, 0.1 * Math.PI, 0.9 * Math.PI)
ctx.stroke()
```

## 动画效果

```typescript
// 左右移动
const monkX = width / 2 + Math.sin(time * 0.8) * 15

// 呼吸效果
const breathe = Math.sin(time * 1.5) * 3

// 扫地动作
const sweepAngle = Math.sin(time * 2) * 0.4

// 灰尘粒子
ctx.fillStyle = 'rgba(100, 100, 100, 0.3)'
for (let i = 0; i < 8; i++) {
  const dustX = (i * 25 + time * 40) % width
  const dustY = height - 30 + Math.sin(time * 3 + i * 0.8) * 8
  ctx.beginPath()
  ctx.arc(dustX, dustY, 2, 0, Math.PI * 2)
  ctx.fill()
}
```

## 工具绘制

```typescript
// 扫帚杆
ctx.save()
ctx.translate(monkX + 22, monkY - 10 + breathe)
ctx.rotate(-sweepAngle + 0.6)

ctx.strokeStyle = 'rgba(150, 130, 100, 0.6)'
ctx.lineWidth = 3
ctx.beginPath()
ctx.moveTo(0, 0)
ctx.lineTo(0, 55)
ctx.stroke()

// 扫帚头
ctx.fillStyle = 'rgba(150, 130, 100, 0.5)'
for (let i = -4; i <= 4; i++) {
  ctx.save()
  ctx.translate(0, 55)
  ctx.rotate(i * 0.12)
  ctx.fillRect(-1.5, 0, 3, 18)
  ctx.restore()
}
ctx.restore()
```

## ⚠️ 已知问题

1. **Canvas元素可能不被浏览器snapshot工具检测到**，但实际在页面上是正常渲染的
2. **useRef可能返回null**，需要检查`if (canvasRef.current)`后再调用
3. **透明背景**：Canvas默认透明，角色颜色需要有足够的不透明度才能在浅色背景上可见
