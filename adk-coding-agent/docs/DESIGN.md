# Web UI design language

The UI (`web/`) borrows the visual language of https://horse-powertrain.com/. The page HTML and its
linked stylesheets were downloaded and analysed to extract tokens; no scripts, images, logos,
copy or fonts were copied.

## Extracted tokens

Source: `template_theme.min.css` and the component stylesheets referenced by the page.

| Token | Value | Used for |
|---|---|---|
| `--color-orange` | `#ff6400` | Single accent: bullets, quote bars, tool-call bars, focus ring, selection |
| `--color-dark-navy` | `#192227` | Headings, primary button, logo tile |
| `--color-slate` | `#36454d` | Body text |
| `--color-steel` | `#455960` | Secondary text |
| `--color-cool-gray-02` | `#29353d` | Dark "key figures" section |
| `--color-cool-gray-01` | `#6a7e8e` | Button hover wipe |
| `--color-warm-gray-01` | `#f7f7f7` | Header, panels, code blocks |
| `--color-warm-gray-02` | `#d9d9d9` | Hairline dividers, nav hover |
| `--color-teal` | `#00a4bd` | Defined, unused |

| Rule | Value |
|---|---|
| Typeface | Proportional sans for text, monospace for navigation, buttons, eyebrows (uppercase) |
| Headings | Regular weight, `line-height: 120%`, 28 / 32 / 36 px; hero 32 / 40 px uppercase |
| Body | 16 px, `line-height: 150%`, `letter-spacing: .01em` |
| Key figures | Weight 300, 48 px on mobile, 92-96 px on tablet and desktop |
| Shape | No border radius, no shadows; 1 px hairlines instead |
| Layout | Max width 1440 px, side padding 16 / 24 / 32 px, 12-column grid, header 61 / 71 px |
| Section spacing | 32 / 54 / 64 px |
| Motion | Left-to-right clip-path wipe on buttons (0.35 s), image zoom 1.07 on card hover (0.5 s) |

## Deliberate differences

- **Fonts**: the site uses the commercial ABC Repro / ABC Repro Mono families. They are listed first in
  the font stack (so a licensed copy installed locally is picked up), with the free Hanken Grotesk and
  DM Mono as bundled fallbacks.
- **Brand assets**: the logo is a neutral `>_` mark, the hero is a CSS-generated blurred gradient and
  all copy is original.

## shadcn/ui mapping

shadcn components live in `web/src/components/ui`. Tokens map onto shadcn's CSS variables in
`web/src/index.css` (`--primary` = dark navy, `--border` = warm gray 02, `--ring` = orange,
`--radius` = 0). `Button` has the wipe hover and mono uppercase style; `Badge` is mono uppercase.
