# 小道童扫地动画实现参考

> 基于小算项目实战经验，Canvas实现的动漫风格小道童扫地动画。

---

## 动画设计

### 角色设计
- **身体**：道袍（圆角矩形）
- **头部**：圆形
- **道士帽**：三角形+矩形底座
- **眼睛**：两个小圆点
- **微笑**：弧线
- **手臂**：矩形，随扫地动作摆动
- **腿**：两个矩形
- **鞋子**：两个小矩形

### 动画效果
- **扫地动作**：手臂左右摆动（sweepAngle）
- **呼吸效果**：身体轻微上下浮动（breathe）
- **灰尘粒子**：8个半透明白色圆点，随扫帚移动
- **扫帚**：杆+扫帚条，跟随手臂摆动

---

## Canvas实现代码

```typescript
function initMonkAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  let time = 0
  const width = canvas.width
  const height = canvas.height

  function draw() {
    ctx.clearRect(0, 0, width, height)
    time += 0.03

    const monkX = width / 2 + Math.sin(time * 0.8) * 15
    const monkY = height / 2 + 20
    const sweepAngle = Math.sin(time * 2) * 0.4
    const breathe = Math.sin(time * 1.5) * 3

    // 绘制灰尘粒子
    ctx.fillStyle = 'rgba(100, 100, 100, 0.3)'
    for (let i = 0; i < 8; i++) {
      const dustX = (i * 25 + time * 40) % width
      const dustY = height - 30 + Math.sin(time * 3 + i * 0.8) * 8
      ctx.beginPath()
      ctx.arc(dustX, dustY, 2, 0, Math.PI * 2)
      ctx.fill()
    }

    // 绘制小道童
    ctx.save()
    ctx.translate(monkX, monkY + breathe)

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

    // 手臂（持扫帚）
    ctx.fillStyle = 'rgba(80, 80, 80, 0.5)'
    ctx.save()
    ctx.translate(18, -15)
    ctx.rotate(-sweepAngle)
    ctx.fillRect(-4, 0, 10, 28)
    ctx.restore()

    // 腿
    ctx.fillStyle = 'rgba(70, 70, 70, 0.4)'
    ctx.fillRect(-12, 20, 10, 22)
    ctx.fillRect(2, 20, 10, 22)

    ctx.restore()

    // 绘制扫帚
    ctx.save()
    ctx.translate(monkX + 22, monkY - 10 + breathe)
    ctx.rotate(-sweepAngle + 0.6)

    ctx.strokeStyle = 'rgba(150, 130, 100, 0.6)'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.moveTo(0, 0)
    ctx.lineTo(0, 55)
    ctx.stroke()

    ctx.fillStyle = 'rgba(150, 130, 100, 0.5)'
    for (let i = -4; i <= 4; i++) {
      ctx.save()
      ctx.translate(0, 55)
      ctx.rotate(i * 0.12)
      ctx.fillRect(-1.5, 0, 3, 18)
      ctx.restore()
    }
    ctx.restore()

    requestAnimationFrame(draw)
  }

  draw()
}
```

---

## React组件集成

```tsx
'use client'
import { useRef, useEffect, useState } from 'react'

export default function MonkAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (canvasRef.current) {
      initMonkAnimation(canvasRef.current)
    }
  }, [mounted])

  return (
    <canvas 
      ref={canvasRef} 
      width={200} 
      height={200}
      className="opacity-70 hover:opacity-100 transition-opacity duration-500"
    />
  )
}
```

---

## 关键Pitfalls

### 1. Canvas不显示
**问题**：canvas元素存在但内容为空
**原因**：useEffect执行时canvasRef.current还未绑定
**解决**：使用单独的useEffect依赖mounted状态

### 2. 背景色覆盖
**问题**：Canvas背景透明但显示为黑色
**原因**：globals.css中body背景色覆盖
**解决**：设置body { background: transparent }

### 3. 颜色适配
**问题**：动画在深色/浅色背景上不可见
**解决**：使用半透明颜色，根据背景动态调整
- 深色背景：`rgba(255, 255, 255, 0.5)`
- 浅色背景：`rgba(80, 80, 80, 0.6)`

---

## 动画参数调优

| 参数 | 值 | 说明 |
|------|-----|------|
| time += 0.03 | 动画速度 | 越大越快 |
| Math.sin(time * 0.8) * 15 | 左右移动幅度 | 像素 |
| Math.sin(time * 2) * 0.4 | 扫地角度 | 弧度 |
| Math.sin(time * 1.5) * 3 | 呼吸幅度 | 像素 |
| 8个灰尘粒子 | 密度 | 可调整数量 |

---

**最后更新**: 2026-07-08
**基于项目**: 小算 v2
