# PDF AI Tool Distribution & Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two deliverables — a Windows installer (.exe) and a static product website — so users can discover and download the tool.

**Architecture:**
- **Installer:** PyInstaller freezes the Python app into a standalone binary; Inno Setup wraps it in a professional Windows installer wizard.
- **Website:** Single-page static HTML/CSS/JS site, responsive, deployed on GitHub Pages, with a download modal.

**Tech Stack:**
- PyInstaller, Inno Setup (packaging)
- HTML5, CSS3, Vanilla JS (website)
- GitHub Pages (hosting)

---

## File Structure

```
d:/Pdf_ai_tool/
├── main.py                     # Existing application entry point
├── theme.py                    # Existing theme system
├── config.py                   # Existing config
├── installer/                  # New: packaging
│   ├── pyinstaller.spec        # PyInstaller config
│   └── setup.iss               # Inno Setup script
├── website/                    # New: static website
│   ├── index.html              # Main page (all sections)
│   ├── styles.css              # All styles
│   ├── script.js               # Interactions (modal, FAQ, carousel)
│   └── assets/                 # Screenshots, icons (placeholders)
└── docs/superpowers/plans/2026-03-31-pdf-ai-tool-distribution-implementation-plan.md
```

---

## PHASE 1: Installer Packaging

### Task 1: Create installer directory and PyInstaller spec

**Files:**
- Create: `d:/Pdf_ai_tool/installer/pyinstaller.spec`
- Check: `d:/Pdf_ai_tool/main.py` (entry point)

- [ ] **Step 1: Read main.py to confirm entry point**

Run: `head -5 d:/Pdf_ai_tool/main.py`
Expected: `def main():` and `if __name__ == '__main__':` blocks present

- [ ] **Step 2: Create installer directory**

Run: `mkdir -p d:/Pdf_ai_tool/installer`

- [ ] **Step 3: Write pyinstaller.spec**

```spec
# d:/Pdf_ai_tool/installer/pyinstaller.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include theme.py, db_manager.py, etc. as non-binary data
    ],
    hiddenimports=[
        'tkinter', 'tkinterdnd2', 'tkinter.ttk', 'tkinter.scrolledtext',
        'tkinter.messagebox', 'tkinter.filedialog',
        'PyPDF2', 'docx', 'openpyxl',
        'db_manager', 'document_processor', 'ai_summarizer', 'theme', 'exporter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF-AI-Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Optional: add icon.ico
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF-AI-Tool',
)
```

- [ ] **Step 4: Commit**

```bash
git add installer/pyinstaller.spec
git commit -m "feat: add PyInstaller spec for standalone exe build"
```

---

### Task 2: Create Inno Setup installer script

**Files:**
- Create: `d:/Pdf_ai_tool/installer/setup.iss`

- [ ] **Step 1: Write Inno Setup script**

```iss
; d:/Pdf_ai_tool/installer/setup.iss
#define MyAppName "PDF AI 智能摘要工具"
#define MyAppVersion "2.0"
#define MyAppPublisher "PDF AI Tool"
#define MyAppURL "https://github.com/<your-username>/pdf-ai-tool"
#define MyAppExeName "PDF-AI-Tool.exe"

[Setup]
AppId={{A5B3C4D5-E6F7-8901-A2B3-C4D5E6F78901}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=PDF-AI-Tool-Setup-{#MyAppVersion}
SetupIconFile=
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "..\dist\PDF-AI-Tool\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
```

- [ ] **Step 2: Create placeholder LICENSE file**

```bash
echo "PDF AI 智能摘要工具
Copyright (c) 2024-2026 PDF AI Tool
This software is provided under MIT License." > d:/Pdf_ai_tool/LICENSE
git add LICENSE
git commit -m "chore: add LICENSE file for installer"
```

- [ ] **Step 3: Commit**

```bash
git add installer/setup.iss
git commit -m "feat: add Inno Setup installer script"
```

---

## PHASE 2: Website Development

### Task 3: Create website directory and index.html

**Files:**
- Create: `d:/Pdf_ai_tool/website/index.html`
- Create: `d:/Pdf_ai_tool/website/styles.css`
- Create: `d:/Pdf_ai_tool/website/script.js`
- Create: `d:/Pdf_ai_tool/website/assets/` (screenshot placeholders noted)

- [ ] **Step 1: Create website directory**

```bash
mkdir -p d:/Pdf_ai_tool/website/assets
```

- [ ] **Step 2: Write index.html — Hero section + full page structure**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PDF AI 智能摘要工具 - AI驱动的PDF文档摘要生成器</title>
  <meta name="description" content="PDF AI 智能摘要工具，一款基于AI技术的PDF文档智能摘要生成器，支持批量处理、标签分类、暗黑模式，导出Excel/Word。">
  <meta property="og:title" content="PDF AI 智能摘要工具 v2.0">
  <meta property="og:description" content="AI驱动的PDF文档摘要生成器，让阅读更高效。">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="styles.css">
</head>
<body>

  <!-- ===== HERO ===== -->
  <header class="hero">
    <div class="hero-bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    <div class="hero-content">
      <div class="hero-badge">v2.0 全新发布</div>
      <h1 class="hero-title">PDF AI<br>智能摘要工具</h1>
      <p class="hero-subtitle">基于 AI 技术，一键生成结构化摘要<br>支持 PDF、Word、Excel、TXT 多格式文档</p>
      <div class="hero-actions">
        <button class="btn btn-primary btn-download" data-target="download-modal">
          立即下载 Windows 版
        </button>
        <a href="https://github.com/<your-username>/pdf-ai-tool" class="btn btn-secondary" target="_blank">
          查看源码
        </a>
      </div>
      <div class="hero-meta">
        <span>免费</span>
        <span class="dot">·</span>
        <span>Windows</span>
        <span class="dot">·</span>
        <span>约 180 MB</span>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-screenshot">
        <div class="screenshot-placeholder">软件界面预览</div>
      </div>
    </div>
  </header>

  <!-- ===== FEATURES ===== -->
  <section class="features" id="features">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">核心功能</h2>
        <p class="section-desc">专为高效阅读与信息管理打造</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>AI 智能摘要</h3>
          <p>基于 GLM-4 大模型，自动分析文档内容，生成结构化摘要，提炼核心主题、关键数据和核心结论。</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📂</div>
          <h3>多格式支持</h3>
          <p>支持 PDF、Word、Excel、TXT 等常见文档格式，批量导入处理，一次选择多个文件。</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🏷️</div>
          <h3>标签分类</h3>
          <p>为文档打标签，支持按标签筛选查找，轻松管理大量文献资料，构建个人知识库。</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔍</div>
          <h3>全文检索</h3>
          <p>支持按标题、内容、标签快速检索，输入关键词即刻定位目标文档，不遗漏任何重要信息。</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💾</div>
          <h3>导出分享</h3>
          <p>一键导出摘要为 Excel 或 Word 格式，方便整理、分享和归档，适配各种办公场景。</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌓</div>
          <h3>深浅主题</h3>
          <p>支持暗黑/明亮模式一键切换，适配不同使用环境，保护视力，使用更舒适。</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== SCREENSHOTS ===== -->
  <section class="screenshots" id="screenshots">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">软件截图</h2>
        <p class="section-desc">简洁直观的操作界面</p>
      </div>
      <div class="screenshots-grid">
        <div class="screenshot-item">
          <div class="screenshot-box">
            <div class="screenshot-placeholder">截图 1：文件列表</div>
          </div>
          <p class="screenshot-caption">文件列表与状态管理</p>
        </div>
        <div class="screenshot-item">
          <div class="screenshot-box">
            <div class="screenshot-placeholder">截图 2：摘要展示</div>
          </div>
          <p class="screenshot-caption">结构化摘要展示</p>
        </div>
        <div class="screenshot-item">
          <div class="screenshot-box">
            <div class="screenshot-placeholder">截图 3：暗黑模式</div>
          </div>
          <p class="screenshot-caption">暗黑模式界面</p>
        </div>
        <div class="screenshot-item">
          <div class="screenshot-box">
            <div class="screenshot-placeholder">截图 4：标签管理</div>
          </div>
          <p class="screenshot-caption">标签分类管理</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== FAQ ===== -->
  <section class="faq" id="faq">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">常见问题</h2>
        <p class="section-desc">使用前请先阅读</p>
      </div>
      <div class="faq-list">
        <div class="faq-item">
          <button class="faq-question">
            <span>下载安装需要收费吗？</span>
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-answer">
            <p>PDF AI 智能摘要工具完全免费使用。如需批量处理或高级功能，请自行部署或联系开发者。</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-question">
            <span>需要联网使用吗？</span>
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-answer">
            <p>生成摘要需要连接互联网（调用智谱AI的GLM-4模型）。文档导入和本地管理功能可离线使用。</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-question">
            <span>支持哪些文件格式？</span>
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-answer">
            <p>目前支持 PDF、Word（.doc/.docx）、Excel（.xls/.xlsx）和纯文本（.txt）格式。</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-question">
            <span>如何获取 API Key？</span>
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-answer">
            <p>软件首次运行时会提示配置 API Key。您需要在智谱AI开放平台（open.bigmodel.cn）注册并创建 API Key。</p>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-question">
            <span>如何卸载软件？</span>
            <span class="faq-icon">+</span>
          </button>
          <div class="faq-answer">
            <p>通过 Windows「设置」→「应用」找到「PDF AI 智能摘要工具」，点击卸载即可完全移除。</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== CTA ===== -->
  <section class="cta-section">
    <div class="container">
      <h2>开始使用 PDF AI 工具</h2>
      <p>提升阅读效率，让信息管理更轻松</p>
      <button class="btn btn-primary btn-download" data-target="download-modal">
        立即下载
      </button>
    </div>
  </section>

  <!-- ===== FOOTER ===== -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        <a href="https://github.com/<your-username>/pdf-ai-tool" target="_blank">GitHub</a>
        <span class="dot">·</span>
        <a href="#features">功能介绍</a>
        <span class="dot">·</span>
        <a href="#screenshots">截图</a>
        <span class="dot">·</span>
        <a href="#faq">常见问题</a>
      </div>
      <p class="footer-copy">© 2024-2026 PDF AI Tool. MIT License.</p>
    </div>
  </footer>

  <!-- ===== DOWNLOAD MODAL ===== -->
  <div class="modal-overlay" id="download-modal">
    <div class="modal">
      <button class="modal-close" id="modal-close">×</button>
      <div class="modal-icon">📦</div>
      <h2 class="modal-title">PDF AI 智能摘要工具 v2.0</h2>
      <div class="modal-info">
        <div class="modal-info-row">
          <span class="modal-label">版本</span>
          <span class="modal-value">v2.0</span>
        </div>
        <div class="modal-info-row">
          <span class="modal-label">更新日期</span>
          <span class="modal-value">2026-03-31</span>
        </div>
        <div class="modal-info-row">
          <span class="modal-label">文件大小</span>
          <span class="modal-value">约 180 MB</span>
        </div>
        <div class="modal-info-row">
          <span class="modal-label">适用系统</span>
          <span class="modal-value">Windows 10/11 (64-bit)</span>
        </div>
      </div>
      <a href="https://github.com/<your-username>/pdf-ai-tool/releases/download/v2.0/PDF-AI-Tool-Setup-2.0.exe"
         class="btn btn-primary btn-block" id="download-btn">
        ⬇️ 下载安装包 (.exe)
      </a>
      <p class="modal-note">下载完成后双击运行，按向导提示完成安装</p>
      <div class="modal-github">
        <a href="https://github.com/<your-username>/pdf-ai-tool" target="_blank">或在 GitHub 查看源码</a>
      </div>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 3: Commit**

```bash
git add website/index.html
git commit -m "feat: create website with all sections and download modal"
```

---

### Task 4: Write styles.css

**Files:**
- Create: `d:/Pdf_ai_tool/website/styles.css`

- [ ] **Step 1: Write styles.css**

```css
/* ===== CSS VARIABLES ===== */
:root {
  --color-primary: #165DFF;
  --color-primary-dark: #4080FF;
  --color-accent: #FF7D00;
  --color-success: #00B42A;
  --color-bg: #F5F7FA;
  --color-bg-card: #FFFFFF;
  --color-text: #1D2129;
  --color-text-secondary: #4E5969;
  --color-text-tertiary: #86909C;
  --color-border: #E5E6EB;
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.08);
  --shadow-hover: 0 8px 32px rgba(22, 93, 255, 0.15);
  --radius-card: 12px;
  --radius-btn: 8px;
  --transition: 0.25s ease;
  --max-width: 1200px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #4080FF;
    --color-accent: #FF9D4D;
    --color-bg: #1D2129;
    --color-bg-card: #252B33;
    --color-text: #E8ECF0;
    --color-text-secondary: #A6C0E0;
    --color-text-tertiary: #6B8BAD;
    --color-border: #3D4654;
    --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
    --shadow-hover: 0 8px 32px rgba(64, 128, 255, 0.2);
  }
}

/* ===== RESET ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", -apple-system, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--color-primary); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; display: block; }
button { cursor: pointer; font-family: inherit; }

/* ===== UTILITY ===== */
.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
}

/* ===== BUTTONS ===== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: var(--radius-btn);
  font-size: 15px;
  font-weight: 600;
  border: none;
  transition: var(--transition);
  cursor: pointer;
  text-decoration: none;
}
.btn-primary {
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 4px 16px rgba(22, 93, 255, 0.3);
}
.btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  text-decoration: none;
  color: #fff;
}
.btn-secondary {
  background: var(--color-bg-card);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}
.btn-secondary:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  text-decoration: none;
}
.btn-block { width: 100%; }

/* ===== HERO ===== */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  background: linear-gradient(135deg, var(--color-bg) 0%, #E8F3FF 100%);
}
.hero-bg-shapes { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
}
.shape-1 {
  width: 600px; height: 600px;
  background: var(--color-primary);
  top: -200px; right: -100px;
}
.shape-2 {
  width: 400px; height: 400px;
  background: var(--color-accent);
  bottom: -100px; left: -100px;
}
.shape-3 {
  width: 200px; height: 200px;
  background: var(--color-primary);
  top: 40%; left: 60%;
}
.hero-content {
  position: relative;
  z-index: 1;
  flex: 1;
  padding: 80px 24px 80px max(24px, calc((100vw - var(--max-width)) / 2 + 24px));
  max-width: 700px;
}
.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(22, 93, 255, 0.1);
  color: var(--color-primary);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}
.hero-title {
  font-size: clamp(40px, 6vw, 72px);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
  background: linear-gradient(135deg, var(--color-text) 0%, var(--color-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  margin-bottom: 36px;
  line-height: 1.8;
}
.hero-actions { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.hero-meta {
  font-size: 13px;
  color: var(--color-text-tertiary);
  display: flex;
  align-items: center;
  gap: 8px;
}
.hero-meta .dot { color: var(--color-border); }
.hero-visual {
  flex: 1;
  padding: 40px max(24px, calc((100vw - var(--max-width)) / 2 + 24px)) 40px 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.hero-screenshot {
  width: 100%;
  max-width: 480px;
  aspect-ratio: 4/3;
  background: var(--color-bg-card);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
}
.screenshot-placeholder {
  color: var(--color-text-tertiary);
  font-size: 14px;
  text-align: center;
}

/* ===== SECTIONS ===== */
section { padding: 80px 0; }
.section-header {
  text-align: center;
  margin-bottom: 56px;
}
.section-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 12px;
}
.section-desc {
  font-size: 16px;
  color: var(--color-text-secondary);
}

/* ===== FEATURES ===== */
.features { background: var(--color-bg); }
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.feature-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: 32px;
  transition: var(--transition);
}
.feature-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-hover);
  transform: translateY(-4px);
}
.feature-icon { font-size: 36px; margin-bottom: 16px; }
.feature-card h3 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 10px;
}
.feature-card p {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.7;
}

/* ===== SCREENSHOTS ===== */
.screenshots { background: var(--color-bg-card); }
.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.screenshot-item { text-align: center; }
.screenshot-box {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  aspect-ratio: 16/10;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: var(--transition);
}
.screenshot-box:hover { border-color: var(--color-primary); }
.screenshot-caption {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* ===== FAQ ===== */
.faq { background: var(--color-bg); }
.faq-list {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.faq-item {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-btn);
  overflow: hidden;
}
.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: none;
  border: none;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  text-align: left;
  cursor: pointer;
  transition: var(--transition);
}
.faq-question:hover { color: var(--color-primary); }
.faq-icon { font-size: 18px; transition: var(--transition); }
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.faq-item.open .faq-answer { max-height: 200px; }
.faq-answer p {
  padding: 0 24px 20px;
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.7;
}

/* ===== CTA ===== */
.cta-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, #0E4ACC 100%);
  padding: 80px 0;
  text-align: center;
  color: #fff;
}
.cta-section h2 { font-size: 32px; font-weight: 700; margin-bottom: 12px; }
.cta-section p { font-size: 16px; opacity: 0.85; margin-bottom: 32px; }
.cta-section .btn-primary {
  background: #fff;
  color: var(--color-primary);
  font-size: 16px;
  padding: 14px 36px;
}
.cta-section .btn-primary:hover {
  background: #f0f0f0;
  color: var(--color-primary-dark);
}

/* ===== FOOTER ===== */
.site-footer {
  background: var(--color-bg-card);
  border-top: 1px solid var(--color-border);
  padding: 40px 0;
  text-align: center;
}
.footer-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.footer-links a { color: var(--color-text-secondary); font-size: 14px; }
.footer-links a:hover { color: var(--color-primary); text-decoration: none; }
.footer-links .dot { color: var(--color-border); }
.footer-copy { font-size: 13px; color: var(--color-text-tertiary); }

/* ===== MODAL ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}
.modal-overlay.open { opacity: 1; pointer-events: all; }
.modal {
  background: var(--color-bg-card);
  border-radius: 16px;
  padding: 40px;
  max-width: 420px;
  width: calc(100% - 48px);
  text-align: center;
  position: relative;
  transform: translateY(20px);
  transition: transform 0.25s ease;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.modal-overlay.open .modal { transform: translateY(0); }
.modal-close {
  position: absolute;
  top: 16px; right: 16px;
  background: none;
  border: none;
  font-size: 24px;
  color: var(--color-text-tertiary);
  cursor: pointer;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  transition: var(--transition);
}
.modal-close:hover { background: var(--color-bg); color: var(--color-text); }
.modal-icon { font-size: 48px; margin-bottom: 16px; }
.modal-title { font-size: 22px; font-weight: 700; margin-bottom: 24px; }
.modal-info {
  background: var(--color-bg);
  border-radius: var(--radius-btn);
  padding: 16px;
  margin-bottom: 24px;
  text-align: left;
}
.modal-info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
}
.modal-info-row:last-child { border-bottom: none; }
.modal-label { color: var(--color-text-secondary); }
.modal-value { font-weight: 600; color: var(--color-text); }
.modal-note { font-size: 12px; color: var(--color-text-tertiary); margin-top: 12px; }
.modal-github { margin-top: 16px; font-size: 13px; }

/* ===== RESPONSIVE ===== */
@media (max-width: 1023px) {
  .hero { flex-direction: column; min-height: auto; padding: 60px 0; }
  .hero-content { padding: 0 24px 40px; max-width: 100%; }
  .hero-visual { padding: 0 24px; width: 100%; }
  .hero-screenshot { max-width: 100%; }
  .features-grid { grid-template-columns: repeat(2, 1fr); }
  .screenshots-grid { grid-template-columns: 1fr; }
}
@media (max-width: 767px) {
  section { padding: 60px 0; }
  .section-title { font-size: 28px; }
  .features-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: 36px; }
  .hero-actions { flex-direction: column; }
  .btn { width: 100%; justify-content: center; }
  .modal { padding: 32px 24px; }
}
```

- [ ] **Step 2: Commit**

```bash
git add website/styles.css
git commit -m "feat: add responsive CSS with dark mode support"
```

---

### Task 5: Write script.js

**Files:**
- Create: `d:/Pdf_ai_tool/website/script.js`

- [ ] **Step 1: Write script.js**

```javascript
/* ===== DOWNLOAD MODAL ===== */
document.addEventListener('DOMContentLoaded', () => {
  // Modal elements
  const modal = document.getElementById('download-modal');
  const modalClose = document.getElementById('modal-close');

  // Open modal on any .btn-download click
  document.querySelectorAll('.btn-download').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  // Close modal on X button
  if (modalClose) {
    modalClose.addEventListener('click', closeModal);
  }

  // Close modal on backdrop click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // Close modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
    }
  });

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  /* ===== FAQ ACCORDION ===== */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

      // Toggle current
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  /* ===== SMOOTH SCROLL for anchor links ===== */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
```

- [ ] **Step 2: Commit**

```bash
git add website/script.js
git commit -m "feat: add JS for modal, FAQ accordion, smooth scroll"
```

---

## PHASE 3: Build & Deployment

### Task 6: Verify website works locally

**Files:**
- Check: `d:/Pdf_ai_tool/website/index.html`

- [ ] **Step 1: Open website in browser**

Run: `start d:/Pdf_ai_tool/website/index.html` (Windows)
Expected: Page loads without errors, modal opens on button click, FAQ expands/collapses

- [ ] **Step 2: Test responsiveness (resize browser window)**

Check: 3-column → 2-column → 1-column layout changes correctly at breakpoints

- [ ] **Step 3: Test modal close behavior**

Check: Close via X, backdrop click, Escape key all work

---

### Task 7: Configure GitHub Pages deployment

**Files:**
- Modify: (GitHub repo settings, no local files)

- [ ] **Step 1: Create a GitHub repository (if not exists)**

Instructions only (user must do in GitHub UI):
1. Go to github.com → New Repository
2. Name: `pdf-ai-tool`
3. Make it public
4. Push existing code

```bash
# Example (adjust remote URL):
git remote add origin https://github.com/<username>/pdf-ai-tool.git
git push -u origin master
```

- [ ] **Step 2: Enable GitHub Pages**

In GitHub repo → Settings → Pages:
- Source: Deploy from a branch
- Branch: `main` / `(root)`
- Save

- [ ] **Step 3: Wait ~2 minutes for deployment, then verify**

Open: `https://<username>.github.io/pdf-ai-tool/`
Expected: Website loads correctly

---

### Task 8: Build the installer (Windows only)

**Prerequisites:** Must be run on Windows with Python and Inno Setup installed.

**Files:**
- Run: `d:/Pdf_ai_tool/installer/pyinstaller.spec`
- Run: `d:/Pdf_ai_tool/installer/setup.iss`

- [ ] **Step 1: Install PyInstaller**

```bash
pip install pyinstaller
```

- [ ] **Step 2: Run PyInstaller**

```bash
cd d:/Pdf_ai_tool/installer
pyinstaller pyinstaller.spec --clean
```
Expected: `d:/Pdf_ai_tool/dist/PDF-AI-Tool/` directory created with `PDF-AI-Tool.exe`

- [ ] **Step 3: Install Inno Setup**

Download from: https://jrsoftware.org/isdl.php
Install with default options

- [ ] **Step 4: Compile Inno Setup script**

```bash
"C:/Program Files (x86)/Inno Setup 6/ISCC.exe" d:/Pdf_ai_tool/installer/setup.iss
```
Expected: `d:/Pdf_ai_tool/dist/PDF-AI-Tool-Setup-2.0.exe` created

- [ ] **Step 5: Verify installer exists and has reasonable size**

```bash
ls -lh d:/Pdf_ai_tool/dist/
```
Expected: `PDF-AI-Tool-Setup-2.0.exe` exists, size ~150-250 MB

---

## Implementation Order

1. Task 1: PyInstaller spec
2. Task 2: Inno Setup script
3. Task 3: Website HTML
4. Task 4: Website CSS
5. Task 5: Website JS
6. Task 6: Verify website locally
7. Task 7: GitHub Pages deployment
8. Task 8: Build installer (Windows)

---

**Plan complete.** Total: 8 tasks across 3 phases — installer packaging (2), website (3), build & deploy (3).
