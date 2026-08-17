# p5.js 角色动画参考

> 用于命理网站的动漫风格角色动画

## 技术选型

| 方案 | 适用场景 | 复杂度 |
|------|---------|--------|
| CSS动画 | 简单移动、旋转、缩放 | 低 |
| HTML5 Canvas | 角色动画、粒子效果 | 中 |
| p5.js | 复杂生成艺术、交互式动画 | 高 |

## Canvas动画基础模板

```typescript
// React组件中使用
const canvasRef = useRef<HTMLCanvasElement>(null)

useEffect(() => {
  if (canvasRef.current) initAnimation(canvasRef.current)
}, [])

return <canvas ref={canvasRef} width={200} height={250} className="opacity-60"/>
```

```typescript
// 动画函数（组件外定义，避免重复创建）
function initAnimation(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  let time = 0

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    time += 0.02

    // 角色位置（带摇摆）
    const x = canvas.width / 2 + Math.sin(time * 0.5) * 10
    const y = canvas.height / 2 + 30
    const sweepAngle = Math.sin(time * 3) * 0.3

    // 绘制角色...
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
    // 身体、头部、手臂、腿...

    // 绘制道具（扫帚等）...
    ctx.save()
    ctx.translate(x + 20, y - 5)
    ctx.rotate(sweepAngle + 0.5)
    // 扫帚绘制...
    ctx.restore()

    // 粒子效果（灰尘等）...
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)'
    for (let i = 0; i < 10; i++) {
      const dustX = (i * 20 + time * 30) % canvas.width
      const dustY = canvas.height - 40 + Math.sin(time * 2 + i) * 5
      ctx.beginPath()
      ctx.arc(dustX, dustY, 2, 0, Math.PI * 2)
      ctx.fill()
    }

    requestAnimationFrame(draw)
  }
  draw()
}
```

## p5.js 完整动画模板

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
  <style>html, body { margin: 0; overflow: hidden; background: transparent; }</style>
</head>
<body>
<script>
p5.disableFriendlyErrors = true;

function setup() {
  createCanvas(200, 250);
  pixelDensity(2);
}

function draw() {
  clear();
  // 角色动画逻辑...
}

function keyPressed() {
  if (key === 's') saveCanvas('output', 'png');
}
</script>
</body>
</html>
```

## 小道士角色设计参考

```
身体：rect(-15, -20, 30, 40, 8)
头部：ellipse(0, -30, 24, 24)
帽子：triangle(-12, -35, 0, -50, 12, -35) + rect(-18, -38, 36, 8)
手臂：rect(0, 0, 12, 35, 4) - 旋转跟随扫地动作
腿部：rect(-10, 20, 8, 20) + rect(2, 20, 8, 20)
扫帚：line(0, 0, 0, 60) + 多条扫帚条
```

## 动画参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| 扫地周期 | 4秒 | sweep动画时长 |
| 身体摇摆 | ±5px, 0.5Hz | 左右轻微摇摆 |
| 手臂摆动 | ±0.5rad | 跟随扫地节奏 |
| 灰尘数量 | 10-15个 | 不影响性能 |
| Canvas透明度 | 60% | 不抢主体视觉 |
