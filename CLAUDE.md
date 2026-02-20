# CLAUDE.md — AI-QA Blog Style Guidelines

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Local Server
- **Dev server:** `source venv/bin/activate && python manage.py runserver` from `/Users/mehul/Desktop/cblog/`
- Runs at `http://127.0.0.1:8000/`
- Do not start a second instance if already running.

## Template Structure
- All templates live in `blog/templates/blog/` (APP_DIRS=True)
- Extend `blog/base.html` — all design tokens, fonts, and CSS utilities are defined there
- Login template: `blog/templates/registration/login.html`
- Use `{% load blog_tags %}` for `strip_tags` and `reading_time` filters

## Design System

### Colors
```
brand:          #0D3B38  (forest green — primary)
brand-dark:     #082A27
brand-mid:      #1A5C57
brand-light:    #2E9D96
brand-pale:     #C8DEDC
brand-faint:    #EAF3F2

accent:         #C8601A  (burnt amber — CTA, highlights)
accent-dark:    #9E4A13
accent-mid:     #E0761F
accent-light:   #F5E2D0
accent-faint:   #FDF6F0

parchment:      #F8F4ED  (page background)
cream:          #FFFCF5  (card/surface background)
ink:            #1C1A16  (body text)
ink-muted:      #6B6458
ink-faint:      #9B9287
```
Never use default Tailwind blue/indigo/purple. Always use brand/accent tokens above.

### Typography
- **Display / Headings:** `Playfair Display` — `font-display` class, weights 500/700/900
- **Body / UI:** `DM Sans` — `font-sans` class, weights 300–700
- Large headings: `letter-spacing: -0.03em`, `line-height: 1.06`
- Body text: `line-height: 1.72–1.85`
- Never use the same font for headings and body.

### Shadows (CSS variables — brand-tinted, layered)
```css
--shadow-sm:     0 1px 3px rgba(13,59,56,0.07), 0 4px 8px rgba(13,59,56,0.05)
--shadow-md:     0 4px 12px rgba(13,59,56,0.09), 0 16px 32px rgba(13,59,56,0.06)
--shadow-lg:     0 8px 24px rgba(13,59,56,0.11), 0 32px 64px rgba(13,59,56,0.07)
--shadow-hover:  0 12px 32px rgba(13,59,56,0.15), 0 40px 72px rgba(13,59,56,0.09)
--shadow-accent: 0 4px 14px rgba(200,96,26,0.25), 0 12px 28px rgba(200,96,26,0.15)
```
Never use flat `shadow-md`. Always use `var(--shadow-*)` or inline layered shadows.

### Logo
- Badge: 38×38px, `border-radius: 10px`, `background: #0D3B38`, "AQ" in Playfair Display 700 amber `#C8601A`
- Stacked text: "AI-QA" in Playfair Display 700 `#0D3B38` + "Blog" in DM Sans uppercase `#9B9287`

### Hero Section (index.html)
- Dark forest green background with 3 layered radial gradients (amber top-right, teal bottom-left, dark center)
- SVG `feTurbulence` grain overlay at 18% opacity, `mix-blend-overlay`
- Underline hero pattern: SVG path `M2 9C32.8203 5.34032 108.769 -0.881146 166 3.51047` in `viewBox="0 0 170 30"`, stroke `#C8601A`, strokeWidth 6
- `.hero-underline` class: `position: absolute; top: 100%; margin-top: -5px; width: 100%`
- Staggered fade-in-up animations: `.anim-fiu`, `.anim-fiu-1` (0.2s), `.anim-fiu-2` (0.4s), `.anim-fiu-3` (0.6s)
- Animated lightbulb badge using `.bulb-glow` keyframe (drop-shadow pulse, 2.2s infinite)

### Post Cards (index.html)
- 16:9 aspect ratio images
- Category badge: absolute top-left overlay on image, cream bg, brand text
- Fallback (no image): gradient with first letter of title
- Animated arrow "Read more": exit arrow slides right + fades, enter arrow slides in from left; box fills `#0D3B38` on hover
- Grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`

## Animations
- Only animate `transform` and `opacity`. **Never `transition-all`.**
- Use spring easing: `cubic-bezier(0.34, 1.56, 0.64, 1)` for lift/pop
- Post card hover: `translateY(-5px)` + `--shadow-hover`
- Tag pill hover: `scale(1.08)`, active: `scale(0.96)`
- Buttons: `active:scale-[0.97]` or `active:scale-[0.98]`

## Interactive States
Every clickable element must have:
- **hover**: color or background change
- **focus-visible**: `focus-visible:ring-2 focus-visible:ring-brand/40` (or accent variant)
- **active**: scale down or opacity reduction

## Images
- Add `mix-blend-multiply` color treatment layer: `rgba(13,59,56,0.08–0.20)`
- Optional gradient overlay: `linear-gradient(to top, rgba(0,0,0,0.55) 0%, transparent 60%)`

## Reference Images
- If a reference image is provided: match layout, spacing, typography, and color exactly.
- Do not improve or add to the design — match it.
- If no reference image: design from scratch using the design system above.

## Hard Rules
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo/purple
- Do not add sections or features not requested
- Never use flat shadows — always layered brand-tinted
- Do not use the same font for headings and body
