---
name: ui-squared
description: House style for every interface Claude builds. Lean, square, no-slop UI on Catppuccin (Mocha dark / Latte light, crust background, lavender accent), with hierarchy from contrasting surfaces instead of borders, shadows or gradients. Use whenever you create or restyle anything visual — web pages, landing pages, dashboards, settings screens, forms, components (React, Vue, Svelte, HTML/CSS, Tailwind), artifacts, prototypes, desktop or mobile UI — even when the user doesn't mention design or style.
---

# ui²

Every element and every word on screen has a job. The interface is quiet, square and dense enough to be useful; the content is the loudest thing in it.

1. **Contrast, not lines.** A panel is visible because it is lighter or darker than what's behind it, not because something draws a box around it.
2. **Square.** `border-radius: 0` on everything, including native controls, badges, avatars and images. Round only what the user explicitly asks to be round, and only that.
3. **No decoration, no filler.** If an element or sentence could go without the user losing information or an action, it goes.

## Palette

Catppuccin Mocha in dark mode, Latte in light mode. The page background is the flavor's crust; lavender is the only accent. Use only these variables — no hex values elsewhere.

```css
:root {
  color-scheme: light dark;
  /*                 Latte    Mocha */
  --bg:       light-dark(#dce0e8, #11111b); /* crust */
  --panel:    light-dark(#eff1f5, #1e1e2e); /* base */
  --sunken:   light-dark(#dce0e8, #11111b); /* crust: inputs inside a panel */
  --raised:   light-dark(#ccd0da, #313244); /* surface0 */
  --raised-2: light-dark(#bcc0cc, #45475a); /* surface1 */
  --raised-3: light-dark(#acb0be, #585b70); /* surface2 */
  --text:     light-dark(#4c4f69, #cdd6f4);
  --text-2:   light-dark(#5c5f77, #a6adc8); /* subtext1 / subtext0 */
  --text-3:   light-dark(#8c8fa1, #7f849c); /* overlay1: placeholder, disabled */
  --accent:   light-dark(#7287fd, #b4befe); /* lavender */
  --on-accent: #11111b;
  --on-red:   light-dark(#eff1f5, #11111b);
  /* status */
  --red:      light-dark(#d20f39, #f38ba8); /* error, failed, destructive */
  --yellow:   light-dark(#df8e1d, #f9e2af); /* pending, warning */
  --green:    light-dark(#40a02b, #a6e3a1); /* success */
  --blue:     light-dark(#1e66f5, #89b4fa); /* info, in progress */
  /* categories: labels, event types, chart series */
  --cat-1:    light-dark(#179299, #94e2d5); /* teal */
  --cat-2:    light-dark(#8839ef, #cba6f7); /* mauve */
  --cat-3:    light-dark(#fe640b, #fab387); /* peach */
  --cat-4:    light-dark(#ea76cb, #f5c2e7); /* pink */
}
:root[data-theme="light"] { color-scheme: light; }
:root[data-theme="dark"]  { color-scheme: dark; }

*, *::before, *::after { border-radius: 0 !important; box-shadow: none; }
html, body { background: var(--bg); color: var(--text); }
```

Why:
- `--sunken` is crust and `--raised` is surface0 in both flavors. Surface0 is lighter than the panel in Mocha and darker in Latte; either way it differs, which is all contrast needs.
- Latte `--text-2` is subtext1 because subtext0 fails WCAG AA on crust (3.7:1) and surface0 (3.2:1). On `--raised` surfaces use `--text`.
- `--on-accent` is Mocha crust in both: no Latte text color passes contrast on Latte lavender. `--on-red` flips because dark text fails on Latte red.
- Lavender fails contrast as text in Latte, so it's a fill only. Links are `--text` with an underline.
- Status and category colors are separate sets so meaning never collides: a "health" category in red reads as an error, a "shipped" status in lavender reads as the primary action.

Colors that belong to the content rather than the interface — product swatches, brand logos, user-chosen colors, photos — stay as they are. Define them once as `--content-*` variables.

## Hierarchy with contrast

Surfaces step outward from the crust: `--bg` → `--panel` → `--raised` → `--raised-2`. Inputs step inward: `--sunken` on a panel.

- **Grouping:** related things share a `--panel`. Separate groups with a gap that shows crust, never a divider. `gap: 2px` between filled children gives clean seams.
- **Tables:** a grid of filled cells with crust seams instead of borders, so columns separate as clearly as rows:
  ```css
  table { border-collapse: separate; border-spacing: 2px; background: var(--bg); }
  th, td { background: var(--panel); padding: 10px 14px; }
  thead th { background: var(--raised); font-weight: 600; }
  ```
  Hover a row's cells `--raised`, selected `--raised-2`. Numbers right-aligned with `tabular-nums`, text left.
- **Table size:** fit the content. Value columns are as wide as their longest value; the label column takes the rest; stop around 760px unless the data needs more. A few columns stretched across the page read as empty.
- **Comparison tables:** values centered, ✓ for yes and – in `--text-3` for no. Group titles are plain bold rows on the background, not filled cells.
- **Emphasis**, weakest first: text color, then weight (400 → 600), then surface, then accent fill. At most one accent-filled element per view, and never on repeated markers like unread indicators — unread is bold text.
- **States:** hover one surface step up, pressed two. Selected `--raised-2`. Disabled `--text-3`.
- **Status and category:** an 8px square of the color before a label in `--text`, so color is never the only signal (several Latte colors are too light to stand alone). Never colored text, tinted backgrounds or colored borders. States beyond the four status colors and groups beyond the four categories get a plain label, not another color.
- **Charts:** one series may use `--accent`; several use `--cat-*` in order, with each series labelled directly. Gridlines `--raised`, axis labels `--text-2`.
- **Destructive:** a danger zone's heading is `--red` (the one status color that passes contrast as text in both flavors) and its buttons are `--red` with `--on-red`.
- **Invalid input:** the field's label and the message under it turn `--red`; the field itself keeps its surface. No red outline.
- **Code:** syntax colors are the exception to the single accent, inside code blocks only. Most Latte syntax colors fail contrast on light backgrounds, so Latte highlights with weight and style instead:
  ```css
  --syn-keyword: light-dark(#4c4f69, #cba6f7); /* + font-weight: 600 in Latte */
  --syn-function: light-dark(#4c4f69, #89b4fa);
  --syn-string:  light-dark(#5c5f77, #a6e3a1);
  --syn-number:  light-dark(#4c4f69, #fab387);
  --syn-comment: light-dark(#5c5f77, #7f849c); /* italic */
  ```
- **Focus:** `:focus-visible { outline: 2px solid var(--accent); }` — the one permitted line, because keyboard users must find focus.

If you reach for a border, shadow, `backdrop-filter` or colored edge stripe, the surfaces aren't stepping correctly.

## Square everything

The global reset misses native widgets and libraries:
- Restyle checkboxes, radios, selects and range inputs with `appearance: none`. A checkbox is a square `--sunken` box that fills with `--accent` when checked; radios are square too unless the user says otherwise.
- Tailwind: set `theme.borderRadius` to `{ none: '0', DEFAULT: '0' }`. Component libraries: set their radius token to 0.
- Avatars and thumbnails are square. Initials avatars are `--raised` with `--text`, the same for everyone — no per-user colors.

## Slop

Patterns now recognized on sight as AI-made. Leave every one out unless the user asks for that exact thing.

**Pills, badges, fake liveness**
- A pill above the headline ("✨ Now in beta", "v2.0 is here →", "Open source").
- A dot plus "Live" / "Online" / "All systems operational" with nothing live behind it. Pulsing or glowing dots, ever.
- Decorative tags ("New", "Beta", "Pro", "AI"). Badges are for real state: a version, a count, a failed check.
- Rows of tech-stack or keyword chips.
- Fake activity: "Updated 2s ago" tickers, live counters, typing effects, blinking cursors, marquees.

**Marketing template**
- Centered hero with a full-sentence display headline; one word in another font, color or gradient.
- Invented stats ("10k+ users", "99.9% uptime"), logo walls, testimonials, avatar stacks.
- Grids of identical icon + title + sentence cards.
- "01 / 02 / 03" on content that isn't a sequence.
- Unrequested sections: FAQ, closing CTA banner, newsletter, footer link columns, social icons.
- More than one primary action; "Watch demo", "No credit card required".

**Visual**
- Gradients, glows, blur, glass, noise, grid or dot backgrounds.
- Cards inside cards.
- Icons in tinted tiles, an icon on every heading, emoji as icons, sparkles for "AI".
- Hover lift or scale, `transition: all`, springy easing, scroll-reveal, looping animation other than a real spinner.
- A list of sentences boxed or striped like a table — use a dashed list.
- More than one accent color; tinted section backgrounds.

**Type**
- Eyebrows: small labels above a heading, including "Step 1" above a step name. Show progress once.
- Uppercase, positive letter-spacing on labels, crushed tracking on headlines. Sentence case everywhere.
- Reflex fonts (Inter, Geist, Space Grotesk, Manrope, Instrument Serif, Fraunces). Use the system UI stack unless told otherwise.
- Monospace as UI chrome. It's for code, commands, hashes and IDs.
- Flat hierarchy: headings at least ~1.25× the size below them.
- Random bold or colored words mid-paragraph.

**Words**
- Subtitles restating the heading, intros explaining the page, "Welcome back!", taglines.
- Hype words: supercharge, seamless, effortless, blazing, next-gen, unlock, elevate, game-changer, AI-powered.
- Slogan cadence: "Not just X, but Y", "Say goodbye to…", "Fast. Simple. Secure.", em-dashes everywhere.
- Helper text that repeats the label.
- Illustrated empty states, cute errors. One plain line plus the action.
- "Submit", "Click here", "Learn more". Name the action: "Save changes", "Copy command".

**Fake features and extras**
- `href="#"`, buttons without handlers, ⌘K hints without a shortcut, search that doesn't search. Don't invent link targets either: if you don't know where something goes, make it plain text and say so in your reply.
- Invented content. If something must be made up (sample data, a usage example), keep it plain and say so in your reply — not on the page.
- Features nobody asked for: theme toggles (follow the system), edit dialogs, extra settings. Build what was requested and suggest the rest in your reply.

**Lavender and dark mode are on slop lists too.** They're deliberate here, so avoid the forms that make them read as slop: lavender only as a flat fill on one element, never a glow, gradient or wash; full `--text` for body copy; Latte as polished as Mocha.

## Check before finishing

```bash
python3 <skill-dir>/scripts/slop_check.py <file-or-dir>
```

Fix every hit unless the user asked for that exact thing. The scanner can't see filler copy, sentence-case eyebrows or invented sections, so reread the visible text against the list above.

If a browser is available, render the page and look at it: every interactive state (panels and dialogs open, filters applied, empty results), in both Mocha and Latte, at desktop and phone width. Overlaps, misaligned panels and clipped columns only show up rendered.

## Layout

- Left-align. Center only a lone small element like a login form.
- 4px spacing scale; tighter inside panels, wider between them. Text inside any filled surface keeps at least 8px from its edges (badges 4px 8px).
- Controls 32–36px tall. Body text 14–15px in apps, 16px on reading pages. Prose max ~70ch.
- Narrow screens: stack panels, 16px gutters, no horizontal scroll. Wide code blocks and tables scroll inside their own box and keep the gutter.
- Content never overflows its panel or slides under another one. When a side panel or drawer opens, the content beside it must reflow: give flex children `min-width: 0`, wrap wide tables in `overflow-x: auto`, and hide or wrap columns with container queries on the space the table actually has, not media queries on the viewport.

## Components

| Element | Treatment |
|---|---|
| Card, section, sidebar, dialog | `--panel`, padding 16–24px |
| Input, select, textarea | `--sunken`, placeholder `--text-3`, hover `--raised` |
| Primary button | `--accent` fill, `--on-accent` text, weight 600 |
| Secondary button | `--raised`, hover `--raised-2` |
| Ghost button | no fill, `--text-2`, hover `--raised` |
| Nav item | `--text-2`, hover `--raised`, current `--raised-2` + `--text` |
| Badge | `--raised`, `--text`, padding ≥ 4px 8px |
| List of points | dashed list on the panel: `–` in `--text-2` via `li::before`, text in `--text`, 8px apart, no box |
| Code / command | monospace on `--sunken`, "Copy" ghost button beside it |
| Modal | `--panel` over a `--bg` scrim at ~80% |
| Tooltip | `--raised-2`, `--text` |

## Other platforms

Use the palette values directly, radius 0 on every view, no shadows or strokes, step surface colors for hierarchy. SwiftUI: `Rectangle` instead of `RoundedRectangle`. Qt: `border-radius: 0; border: none;`. TUIs: background blocks instead of box-drawing frames.
