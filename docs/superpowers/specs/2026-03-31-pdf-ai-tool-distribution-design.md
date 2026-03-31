# PDF AI Tool Distribution & Website Design

> **Goal:** Package the tkinter PDF AI summarization tool as a distributable Windows installer (.exe) and build a product website for discovery and download.

---

## 1. Overview

Two deliverables:

1. **Windows Installer** — `PDF-AI-Tool-Setup-2.0.exe`, a one-click installation wizard with shortcuts, uninstall support, and license agreement.
2. **Product Website** — A complete static site (5 sections) deployed on GitHub Pages, serving as the official download hub and marketing page.

---

## 2. Packaging Strategy

### 2.1 Build Pipeline

```
main.py + dependencies
       │
       ▼
  PyInstaller
  (single .exe bundle, no Python needed)
       │
       ▼
  Inno Setup
  (installer wizard → PDF-AI-Tool-Setup-2.0.exe)
```

### 2.2 Tools

| Tool | Purpose | License |
|------|---------|---------|
| PyInstaller | Freeze Python app → standalone `.exe` | MIT |
| Inno Setup | Create Windows installer wizard | Free |

### 2.3 Installer Features

- License agreement page (GPL or custom)
- Custom install path (default: `C:\Program Files\PDF AI Tool\`)
- Desktop shortcut (optional)
- Start Menu entry
- Uninstaller with proper Windows "Add/Remove Programs" entry
- Bundled FFmpeg/dependencies if needed (currently none beyond pure Python stdlib + pip packages)

### 2.4 Output

- `dist/PDF-AI-Tool-Setup-2.0.exe` — final installer for distribution
- `dist/PDF-AI-Tool.exe` — the bundled application binary

---

## 3. Website Design

### 3.1 Page Structure

Single-page website with 5 sections + modal:

| Section | Purpose |
|---------|---------|
| **Hero** | Name, tagline, primary CTA ("立即下载"), background visual |
| **Features** | 6 feature cards (icon + title + description) |
| **Screenshots** | 3-4 app screenshot carousel/grid |
| **FAQ** | 3-5 collapsible Q&A items |
| **Footer** | Copyright, links |
| **Download Modal** | Appears on CTA click — shows version, file size, download button |

### 3.2 Visual Design

| Element | Value |
|---------|-------|
| Primary color | `#165DFF` (tech blue) |
| Accent color | `#FF7D00` (energetic orange) |
| Background | `#F5F7FA` (light) / `#1D2129` (dark, auto via `prefers-color-scheme`) |
| Card background | `#FFFFFF` / `#252B33` |
| Text primary | `#1D2129` / `#E8ECF0` |
| Border | `#E5E6EB` / `#3D4654` |
| Typography | System font stack; `"Microsoft YaHei", "PingFang SC", sans-serif` |
| Border radius | `12px` for cards, `8px` for buttons |
| Shadows | Soft box-shadow (`0 4px 24px rgba(0,0,0,0.08)`) |
| Motion | Subtle hover transitions (`0.25s ease`), FAQ accordion open/close |

### 3.3 Layout

- Max content width: `1200px`, centered
- Hero: full-width, vertically centered text + floating decorative shapes
- Features: 3-column grid on desktop, 2 on tablet, 1 on mobile
- Screenshots: side-scrolling carousel or 2-column masonry grid
- FAQ: accordion list, max-width `720px` centered
- Footer: simple centered text + links

### 3.4 Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Desktop | ≥1024px | Full 3-col features, side-by-side layouts |
| Tablet | 768px–1023px | 2-col features, stacked screenshots |
| Mobile | <768px | Single column, hamburger nav (if needed) |

### 3.5 Download Modal

- Triggered by any "下载" CTA button
- Shows: version (`v2.0`), release date, file size (~estimate), checksum (optional)
- Primary button: download installer directly
- Secondary link: view source on GitHub
- Close via X button or clicking backdrop

### 3.6 SEO & Metadata

- `<title>`: `PDF AI 智能摘要工具 - AI驱动的PDF文档摘要生成器`
- `<meta description>`: concise Chinese description
- Open Graph tags for social sharing
- Semantic HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`)

---

## 4. File Structure

```
d:/Pdf_ai_tool/
├── main.py                     # Existing application
├── theme.py                    # Existing theme system
├── installer/                  # New: packaging scripts
│   ├── pyinstaller.spec
│   └── setup.iss               # Inno Setup script
├── website/                    # New: static website
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/                 # Screenshots, icons
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-03-31-pdf-ai-tool-distribution-design.md
```

---

## 5. Deployment

- **Website**: GitHub Pages — push to `main` branch, serve from `/website/` directory
- **Installer**: Hosted alongside website for direct download link
- **Domain**: Optional — can use `username.github.io/pdf-ai-tool` initially

---

## 6. Dependencies for Build

```bash
pip install pyinstaller
# Inno Setup is a Windows GUI tool installed separately
```

---

## 7. Out of Scope

- Multi-platform builds (macOS .dmg, Linux .AppImage)
- Auto-update mechanism
- Analytics / tracking scripts
- Blog / changelog pages (can be added later)
- User accounts / cloud sync
