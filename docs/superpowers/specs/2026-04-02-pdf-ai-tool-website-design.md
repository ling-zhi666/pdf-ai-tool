# PDF AI 工具官网优化设计规范

**日期**: 2026-04-02
**状态**: 已批准实施

---

## 1. 技术方案

| 项目 | 方案 |
|------|------|
| CSS 动画 | CSS Variables + GSAP 3.12.5 (CDN) + ScrollTrigger |
| GSAP CDN | `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js` + `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js` |
| 主题系统 | CSS `prefers-color-scheme` 自动适配 + 右上角手动切换按钮 + localStorage 持久化 |
| 品牌色 | Primary `#165DFF`，明暗双模式独立调色板 |

---

## 2. 主题调色板

### Light Mode
- `--color-primary`: `#165DFF`
- `--color-primary-dark`: `#0E4ACC`
- `--color-primary-glow`: `rgba(22, 93, 255, 0.25)`
- `--color-accent`: `#FF7D00`
- `--color-bg`: `#F5F7FA`
- `--color-bg-card`: `#FFFFFF`
- `--color-text`: `#1D2129`
- `--color-text-secondary`: `#4E5969`
- `--color-border`: `#E5E6EB`

### Dark Mode
- `--color-primary`: `#4080FF`
- `--color-primary-dark`: `#165DFF`
- `--color-primary-glow`: `rgba(64, 128, 255, 0.3)`
- `--color-accent`: `#FF9D4D`
- `--color-bg`: `#0F1117`
- `--color-bg-card`: `#1A1D27`
- `--color-text`: `#E8ECF0`
- `--color-text-secondary`: `#A6C0E0`
- `--color-border`: `#2D3348`

---

## 3. GSAP 动画规格

### Hero 入场动画（页面加载时）
- Timeline: `title` fade-up(0, -30px) → `subtitle` fade-up(0.15s) → `hero-actions` fade-up(0.3s) → `hero-meta` fade-up(0.45s) → `hero-visual` fade-in(0.5s, scale 0.95→1)
- Duration: 0.8s, ease: `power3.out`

### 背景粒子动画（CSS keyframes）
- 3 个圆形 shape 缓慢漂移（translate + scale 变化）
- 动画周期 8-15s，infinite loop，opacity 0.06-0.12

### 功能卡片 ScrollTrigger
- trigger: `.features-grid`
- start: `top 80%`
- 每个卡片：fade-up + stagger 0.1s，ease: `power2.out`

### 截图区 ScrollTrigger
- trigger: `.screenshots-grid`
- 每个截图：fade-in-right，stagger 0.15s，ease: `power2.out`

### FAQ Accordion
- 高度动画用 `gsap.fromTo`，duration 0.3s
- 内容 `opacity 0→1`，delay 0.1s

### Modal 动画
- overlay: `opacity 0→1`，duration 0.25s
- modal: `y 60→0 + scale 0.92→1`，duration 0.4s，ease: `back.out(1.2)`
- 关闭：reverse

---

## 4. 各区域设计规格

### Hero
- 最小高度: 100vh
- 左右布局（桌面），垂直堆叠（移动）
- 左侧内容区 max-width: 640px
- 右侧软件截图卡片带光晕边框动画
- CTA 按钮悬浮时有上浮 + 阴影加深效果

### 功能卡片
- 3列网格（桌面）→ 2列（平板）→ 1列（手机）
- 卡片: 32px padding, 16px border-radius, hover时 `translateY(-6px)` + 边框发光
- 图标: 40px, hover时 `scale(1.15)`

### 截图区
- 2列网格 → 1列（手机）
- 截图盒子 hover: `scale(1.02)` + 阴影加深
- 底部 caption 14px

### FAQ
- 最大宽度 720px 居中
- 问题行 hover 背景微变 + 文字主题色
- 展开时 `+` 变 `×`（45deg旋转）
- 答案区 max-height 动画过渡

### 下载弹窗
- overlay: `rgba(0,0,0,0.6)` + `backdrop-filter: blur(8px)`
- 弹窗: 480px max-width, 居中
- 标题区: 渐变背景装饰条
- 版本号: 高亮 badge
- 主按钮: 全宽，悬浮时亮度提升 + 上浮
- 关闭按钮: 右上角 ×

---

## 5. 响应式断点

| 断点 | 宽度 | 布局变化 |
|------|------|----------|
| Desktop | ≥1024px | 3列卡片，Hero左右布局 |
| Tablet | 768-1023px | 2列卡片，Hero垂直 |
| Mobile | <768px | 1列卡片，全垂直堆叠 |

---

## 6. 转化率优化

- Hero 下载按钮：添加动画呼吸效果（pulse）
- 弹窗：更大图标 + 渐变标题背景 + 版本高亮badge + 限时免费标签
- 弹窗主按钮：全宽 + 渐变背景 + 悬停动效
- 弹窗关闭：ESC键 + 点击遮罩层 + ×按钮 三种方式
