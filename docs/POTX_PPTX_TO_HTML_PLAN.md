# POTX / PPTX → HTML Conversion — Implementation Plan

## Verdict

**Yes, it is possible** to convert `.potx` / `.pptx` into HTML while preserving (to a useful degree):

| Target | Feasible? | Notes |
|--------|-----------|--------|
| Layout (positions, sizes, z-order) | Yes | EMUs → CSS `px`/`%` absolute positioning |
| Colors | Yes | Theme color scheme + local overrides |
| Fonts & font sizes | Yes (mostly) | Theme fonts + `a:rPr` / `a:defRPr`; embed or fallback |
| Transitions | Partial | Slide transitions map to CSS/JS; complex morph/3D limited |
| Images / figures / media | Yes | Extract `ppt/media/` and rewrite URLs |
| Headers | Yes | Master/layout placeholders (`hdr`) + date/slide number |
| Footers | Yes | Master/layout placeholders (`ftr`) |

**Hard limits (expect imperfect fidelity):** SmartArt, charts (need SVG/canvas rebuild), OLE embeddings, WordArt, complex FreeForm paths, some animations (motion paths, emphasis), and exact PowerPoint text wrapping. Aim for **visual fidelity for templates and typical decks**, not bit-perfect PowerPoint parity.

---

## Why it works

A `.pptx` / `.potx` file is a **ZIP** of Open XML (PresentationML):

```text
presentation.xml
  ├── slideMaster(s)  → theme + slideLayout(s)
  ├── slide(s)        → each uses one slideLayout (+ shapes in slideN.xml)
  ├── notesMaster
  └── (optional) handoutMaster

slideN.xml  ──rels──►  media/, charts/, diagrams/, …
```

Templates (`.potx`) often lack `slides/` and rely on **masters + layouts + theme**. Decks (`.pptx`) add concrete slides and media. The converter should treat both the same: resolve the inheritance chain **Theme → Master → Layout → Slide**.

---

## Goals & non-goals

### Goals

1. CLI Python tool: `potx2html input.(potx|pptx) -o out_dir/`
2. Self-contained HTML output (one `index.html` + `assets/` + CSS/JS)
3. Preserve slide size, shape geometry, text runs, theme colors/fonts
4. Extract and link images and other binary media
5. Render header/footer placeholders (date, footer text, slide number)
6. Approximate slide transitions in a simple HTML slideshow viewer
7. For `.potx` with no slides: emit **one HTML page per layout** (template preview mode)

### Non-goals (v1)

- Round-trip edit back to PPTX
- Perfect chart / SmartArt / equation rendering
- Full PowerPoint animation timeline (build-order, triggers, motion paths)
- Embedded Excel / OLE live objects
- Collaborative comments / revision XML

---

## Output contract

```text
out_dir/
  index.html          # slideshow shell (keyboard nav, transitions)
  css/
    theme.css         # CSS variables from theme colors/fonts
    slides.css        # per-slide / shared layout rules
  js/
    viewer.js         # navigation + transition playback
  assets/
    media/            # extracted images, video, audio
    fonts/            # optional embedded fonts (if licensed/available)
  slides/
    slide-001.html    # optional fragment includes, or inlined in index
  meta.json           # slide count, size, theme summary (debug / tooling)
```

**Slide model in HTML:** each slide is a fixed-aspect box (`sldSz` from `presentation.xml`) with absolutely positioned shapes:

```html
<section class="slide" data-transition="fade" style="width:…; height:…;">
  <div class="shape" style="left:…; top:…; width:…; height:…; z-index:…;">
    …
  </div>
  <footer class="ph-ftr">…</footer>
</section>
```

---

## Architecture

```text
┌─────────────┐   unzip    ┌──────────────┐   parse    ┌────────────────┐
│ .pptx/.potx │ ─────────► │ PackageTree  │ ─────────► │ IR (intermediate│
└─────────────┘            │ (files+rels) │            │  representation)│
                           └──────────────┘            └────────┬───────┘
                                                                │
                    ┌───────────────────────────────────────────┘
                    ▼
           ┌────────────────┐   render    ┌────────────────┐
           │ ThemeResolver  │ ──────────► │ HTML / CSS / JS│
           │ ShapeComposer  │             │ + assets/      │
           └────────────────┘             └────────────────┘
```

### Intermediate representation (IR)

Keep parsing separate from rendering. Suggested dataclasses:

- `Presentation` — size (`cx`, `cy`), slide list, masters, theme refs
- `Theme` — `ColorScheme`, `FontScheme`, format scheme (fills/lines)
- `SlideMaster` / `SlideLayout` — backgrounds, placeholders, common shapes
- `Slide` — layout id, shapes, transition, timing
- `Shape` — type (`sp`, `pic`, `grpSp`, `graphicFrame`, `cxnSp`), transform (`xfrm`), style, text body
- `TextBody` / `Paragraph` / `Run` — alignment, bullets, fonts, sizes, colors
- `Placeholder` — type (`title`, `body`, `hdr`, `ftr`, `dt`, `sldNum`, …), index
- `MediaAsset` — relationship id → extracted path
- `Transition` — type, speed, advance

Inheritance merge order for each visual property:

```text
theme defaults → master → layout → slide shape overrides
```

---

## Module layout

```text
potx2html/
  __init__.py
  __main__.py              # python -m potx2html
  cli.py                   # argparse entry
  package/
    unzip.py               # open ZIP, list parts
    relationships.py       # parse .rels → Target map
    namespaces.py          # a:, p:, r: namespaces
  parsers/
    presentation.py        # presentation.xml + sldSz + sldIdLst
    theme.py               # theme/themeN.xml
    master.py              # slideMasters/
    layout.py              # slideLayouts/
    slide.py               # slides/slideN.xml (+ timing/transition)
    shapes.py              # shared shape tree walker
    text.py                # a:txBody → paragraphs/runs
    media.py               # copy ppt/media → assets/
  ir/
    models.py              # dataclasses
    resolve.py             # placeholder merge, color/font resolve
  render/
    css_theme.py           # --accent-1, --dk1, major/minor fonts
    html_slide.py          # shape → HTML
    html_text.py           # runs → spans with inline styles
    transitions.py         # map p:transition → CSS/JS
    viewer.py              # index.html + viewer.js
  units.py                 # EMU ↔ px (914400 EMU = 1 inch)
  exceptions.py
tests/
  fixtures/                # small .pptx / .potx samples
  test_*.py
pyproject.toml
README.md                  # tool usage (separate from profile README if needed)
```

---

## Feature mapping (PresentationML → HTML/CSS)

### 1. Layout

| Source | Target |
|--------|--------|
| `p:sldSz/@cx,@cy` | Slide viewport size (CSS px via DPI, default 96) |
| `a:off` / `a:ext` in `p:xfrm` | `left`, `top`, `width`, `height` |
| `a:rot` | `transform: rotate(…deg)` (OOXML: 60000ths of a degree) |
| `a:flipH` / `a:flipV` | `scaleX(-1)` / `scaleY(-1)` |
| Shape tree order | `z-index` |
| `p:grpSp` | nested relatively positioned container; child offsets relative to group |
| Background (`p:bg` / theme fill) | `background` / `background-image` on `.slide` |

**Coordinate system:** PowerPoint uses EMUs. Convert with:

```text
px = emu * dpi / 914400
```

Use a fixed DPI (96) so CSS matches screen browsers; optionally expose `--dpi`.

### 2. Colors

Parse `theme/themeN.xml`:

- `a:clrScheme` → CSS variables: `--dk1`, `--lt1`, `--dk2`, `--lt2`, `--accent1`…`--accent6`, `--hlink`, `--folHlink`
- Resolve `a:schemeClr`, `a:srgbClr`, `a:sysClr` with transforms (`lumMod`, `lumOff`, `tint`, `shade`, `alpha`)
- Apply master `clrMap` (`bg1`→`lt1`, etc.)

Output example:

```css
:root {
  --dk1: #1a1a2e;
  --accent1: #0d7377;
  --major-latin: "Arial";
  --minor-latin: "Calibri";
}
```

### 3. Fonts & font sizes

| Source | Target |
|--------|--------|
| `a:fontScheme` major/minor | CSS `--major-*` / `--minor-*` |
| `a:rPr/@sz` (hundredths of a point) | `font-size: Npt` or `px` (`sz/100` pt) |
| `a:latin`, `a:ea`, `a:cs` | `font-family` with fallbacks |
| Bold / italic / underline | `font-weight`, `font-style`, `text-decoration` |
| Embedded fonts (`ppt/fonts/` if present) | `@font-face` when extractable and licensed |

**POTX tip:** many templates only set fonts on master/layout placeholders; resolve via placeholder type + `lstStyle` levels.

### 4. Transitions

Read `p:transition` on each slide (and optionally presentation defaults):

| OOXML (examples) | HTML strategy |
|------------------|----------------|
| `p:fade` | CSS `opacity` transition / `@keyframes` |
| `p:push` / `p:wipe` | `transform: translateX` / clip |
| `p:cover` / `p:pull` | slide-over animations |
| `p:cut` | instant swap |
| `spd` / `advTm` | duration + auto-advance timer |
| Morph / complex 3D | **fallback to fade** in v1 |

`viewer.js` responsibilities: Prev/Next, keyboard, apply `data-transition` class between sections.

**Animations (`p:timing`):** v1 can ignore or only support simple entrance `appear`/`fade`. Document as Phase 3.

### 5. Graphical resources

| Part | Handling |
|------|----------|
| `p:pic` + `a:blip` | Resolve `r:embed` via slide `.rels` → copy file → `<img src="assets/media/…">` |
| Vector shapes (`a:prstGeom`, `a:custGeom`) | CSS border-radius / SVG path for custom geometry |
| Lines / connectors | SVG `<line>` / `<path>` overlay or border tricks |
| Tables (`a:graphic` table) | HTML `<table>` |
| Charts | Phase 2: SVG via chart XML or placeholder image |
| Diagrams / SmartArt | Phase 2+: placeholder or simplified SVG |
| Video / audio | `<video>` / `<audio>` with extracted media |

### 6. Headers & footers

Placeholders live on **master/layout** (and may be overridden on slide):

| Placeholder type | Typical role |
|------------------|--------------|
| `hdr` | Header text |
| `ftr` | Footer text |
| `dt` | Date/time (fixed or auto) |
| `sldNum` | Slide number |

Also respect `p:hf` flags on master/layout (`hdr`, `ftr`, `dt`, `sldNum` show/hide).

**Rendering rules:**

1. Collect placeholder frames from layout (geometry + style)
2. Fill text from slide field values / presentation properties / computed slide index
3. Skip placeholders disabled by `p:hf`
4. Emit semantic wrappers: `<header class="ph-hdr">`, `<footer class="ph-ftr">`, `<time class="ph-dt">`, `<span class="ph-sldnum">`

For **template-only POTX**, show sample header/footer text from layout defaults so the preview looks complete.

---

## Pipeline (step by step)

1. **Open package** — validate ZIP; require `[Content_Types].xml` and `ppt/presentation.xml`
2. **Parse relationships** — build graph from `presentation.xml.rels` and per-part `.rels`
3. **Parse theme** — colors, fonts, format scheme
4. **Parse masters & layouts** — backgrounds, placeholders, common shapes, `clrMap`, `hf`
5. **Enumerate slides** — from `sldIdLst`; if empty (typical POTX), synthesize slides from each layout
6. **Parse each slide** — shape tree, transition, notes (optional)
7. **Extract media** — copy referenced binaries to `assets/media/`
8. **Resolve IR** — merge inheritance; resolve colors/fonts; bind placeholders
9. **Render CSS** — theme variables + per-shape rules (prefer classes + data attrs over huge inline styles where practical)
10. **Render HTML** — slides + viewer shell
11. **Write `meta.json`** — for debugging and downstream tools

---

## Phased delivery

### Phase 0 — Spike (validate approach)

- Unzip sample `.pptx` / `.potx`
- Print slide size, theme colors, layout count, media list
- One hard-coded HTML slide with absolute-positioned title + image

**Exit criteria:** confirmed EMU math and theme color resolution on a real file.

### Phase 1 — MVP converter

- Package + rels + theme + master/layout/slide parsers
- Text boxes, pictures, basic rectangles / rounded rects
- Theme CSS variables, fonts/sizes on runs
- Headers/footers/date/slide number
- Simple viewer: fade + cut transitions, keyboard navigation
- CLI + unit tests on fixtures

### Phase 2 — Visual fidelity

- Groups, connectors, more preset geometries (SVG)
- Table rendering
- Background fills (solid, gradient, blip)
- Better list styles / bullets
- Transition set expansion (push, wipe, cover)
- Optional font embedding

### Phase 3 — Rich objects & polish

- Charts → SVG (or static PNG fallback via optional LibreOffice)
- SmartArt simplified tree
- Entrance animations subset
- Notes panel toggle
- Accessibility: heading structure, alt text from `descr`/`title` on pictures

---

## CLI sketch

```bash
python -m potx2html deck.pptx -o ./out
python -m potx2html template.potx -o ./out --mode layouts   # one page per layout
python -m potx2html deck.pptx -o ./out --dpi 96 --embed-fonts
```

```text
usage: potx2html [-h] -o OUT [--mode {slides,layouts,auto}] [--dpi DPI] input
```

- `--mode auto`: slides if present, else layouts
- Exit non-zero on missing required parts; warn on unsupported shapes

---

## Dependencies (suggested)

| Package | Role |
|---------|------|
| stdlib `zipfile`, `xml.etree.ElementTree` | Core I/O (keep deps light) |
| `lxml` (optional) | Faster/XPath-friendly parsing if needed |
| `jinja2` | HTML templates |
| `Pillow` (optional) | Image metadata / format normalize |
| `pytest` | Tests |

Prefer **stdlib-first** for the core path; add libraries only when they reduce complexity.

---

## Testing strategy

Fixtures under `tests/fixtures/`:

1. Minimal blank `.pptx` (one title slide)
2. Themed deck with accents + custom fonts
3. Deck with images + footer/header/slide number
4. `.potx` with multiple layouts, no slides
5. Deck with `p:fade` / `p:push` transitions

Test naming (per project conventions): `{method}_{state}_{expected}`.

Sections in each test module:

- Mocks, fixtures & helpers
- Happy path
- Error paths
- Edge cases

Assert:

- EMU→px conversion
- Theme color resolution (including `lumMod`/`shade`)
- Placeholder merge master→layout→slide
- Media files present in output
- HTML contains expected header/footer text and slide count

Manual visual check: open `index.html` in a browser against screenshots of PowerPoint.

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Inheritance bugs (wrong font/color) | Explicit resolve layer + golden IR JSON fixtures |
| Custom geometry too hard | Fallback: bounding box + solid fill; SVG later |
| Charts/SmartArt incomplete | Placeholder box labeled “unsupported”; Phase 3 |
| Font licensing / missing fonts | CSS fallback stacks; document `--embed-fonts` limits |
| Large decks / memory | Stream parse per slide; don’t keep all XML strings |
| Transition fidelity | Map known types; default fade |

---

## Success metrics

Phase 1 is done when:

1. A sample `.pptx` and `.potx` convert without crash
2. Slide dimensions and theme colors match the source
3. Titles, body text, and images appear in correct regions
4. Headers/footers/slide numbers render when enabled
5. Viewer advances slides with at least fade/cut
6. Automated tests cover parsers + resolve + a smoke render

---

## Recommended first implementation slice

After this plan is approved, implement in order:

1. `units.py` + `package/` + theme parser
2. Shape/text IR for title + body + pic only
3. HTML renderer + minimal viewer
4. Header/footer placeholders
5. Transition attributes + JS
6. Expand geometry and tables

This delivers a working demo quickly while keeping the IR clean for later fidelity work.
