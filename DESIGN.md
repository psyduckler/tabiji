# Design System: tabiji.ai

## 1. Visual Theme & Atmosphere

Tabiji is a warm, earthy travel planning site that feels like a vintage field journal meets modern web — a cream-white canvas (`#FEFCF9`) where terracotta accents (`#C4704B`) and deep indigo (`#2D3A5C`) create a palette that evokes desert sunsets and old maps. The overall impression is of trusted expertise wrapped in handcrafted warmth: this is not a tech startup's marketing page, it's a travel companion that earns trust through quiet confidence and natural tones.

The typography is built on the system font stack (`-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, sans-serif`) — no custom fonts, no loading delays. This is intentional: the site prioritizes performance and legibility over typographic personality, letting the warm color palette and generous spacing carry the brand. Weight range spans 400–800, with 700 (bold) dominating headings and 400–500 for body text. The absence of letter-spacing manipulation or OpenType features keeps the reading experience clean and familiar — like a well-typeset magazine article rather than a designed artifact.

What distinguishes tabiji visually is its earth-tone palette system using CSS custom properties (`--indigo`, `--terracotta`, `--warm-cream`, `--sand`, `--earth`, `--sage`). Terracotta (`#C4704B`) functions as both brand accent and primary CTA color — buttons, links, and key interactive elements all use it. Indigo (`#2D3A5C`) serves as the secondary brand color for navigation and structural elements. The shadow system is minimal and warm: `rgba(0,0,0,0.06)` ambient lift, `rgba(196,112,75,0.1)` terracotta-tinted glow for featured elements, and `rgba(0,0,0,0.3)` for hero overlays. Combined with border-radius values of 8px–16px, the interface feels approachable and organic — rounded enough to feel friendly, structured enough to feel trustworthy.

**Key Characteristics:**
- Warm cream canvas (`#FEFCF9`) — not white, not gray, a paper-like off-white with a barely-warm tint
- Terracotta (`#C4704B`) as singular brand accent and CTA color
- Deep indigo (`#2D3A5C`) for navigation and structural text
- System font stack — performance-first, no custom fonts
- CSS custom property palette system (`--indigo`, `--terracotta`, `--warm-cream`, etc.)
- Earth-tone palette: cream, sand, terracotta, earth brown, sage green, deep brown
- Minimal shadow system with terracotta-tinted glow for featured elements
- Conservative border-radius: 8px–16px (nothing pill-shaped except specific badges)
- Near-transparent frosted nav: `rgba(254,252,249,0.92)` with backdrop blur
- Photography used sparingly — text and color carry the brand

## 2. Color Palette & Roles

### CSS Custom Properties (defined on `:root`)
```css
--indigo: #2D3A5C;
--indigo-light: #3D4E7A;
--warm-cream: #F5F0E8;
--sand: #E8DFD0;
--earth: #8B7355;
--earth-light: #A6906F;
--terracotta: #C4704B;
--deep-brown: #3E2F23;
--sage: #7A8B6F;
--white: #FEFCF9;
--text: #2C2419;
--text-muted: #6B5D4F;
```

### Primary Brand
- **Terracotta** (`#C4704B`): Primary brand accent, CTA buttons, active links, highlights. A warm orange-brown that evokes desert clay and sunset tones.
- **Deep Indigo** (`#2D3A5C`): Navigation text, structural headings, secondary brand color. A sophisticated blue-gray that grounds the warm palette.
- **Indigo Light** (`#3D4E7A`): Hover state for indigo elements, slightly lifted variant.

### Background Surfaces
- **Paper White** (`#FEFCF9`): `--white`. Primary page background — barely off-white with a warm cream undertone.
- **Frosted Nav** (`rgba(254,252,249,0.92)`): Semi-transparent navigation backdrop with blur.
- **Frosted Surface** (`rgba(254,252,249,0.98)`): Near-opaque surface for elevated sections.
- **Warm Cream** (`#F5F0E8`): `--warm-cream`. Secondary surface, card backgrounds, section fills.
- **Sand** (`#E8DFD0`): `--sand`. Borders, dividers, badge backgrounds, tertiary surface.
- **Light Sand** (`rgba(245,240,232,0.3–0.45)`): Subtle tinted backgrounds for comparison tables and info blocks.
- **Sage Tint** (`rgba(122,139,111,0.08)`): Very subtle green tint for nature/eco-related highlights.

### Text Scale
- **Primary Text** (`#2C2419`): `--text`. Near-black with warm brown undertone — never pure black.
- **Text Muted** (`#6B5D4F`): `--text-muted`. Secondary text, descriptions, metadata.
- **Earth** (`#8B7355`): `--earth`. Tertiary text, subtle labels, de-emphasized content.
- **Earth Light** (`#A6906F`): `--earth-light`. Lightest text variant, timestamps, fine print.
- **Deep Brown** (`#3E2F23`): `--deep-brown`. Maximum emphasis in body context — darker than `--text`.
- **White Text** (`#FFFFFF`): On terracotta/indigo backgrounds, hero overlays.
- **Soft White** (`rgba(255,255,255,0.8–0.85)`): Secondary text on dark/image backgrounds.

### Accent & Status
- **Sage Green** (`#7A8B6F`): `--sage`. Nature-themed accents, eco indicators, subtle highlights.
- **Gold Highlight** (`#F4C87A` / `rgb(244,200,122)`): Star ratings, premium indicators.
- **Info Blue** (`#0696D7` / `rgb(6,150,215)`): Information links, external reference indicators.

### Border & Divider
- **Sand Border** (`#E8DFD0`): Primary border color for cards, dividers, containers.
- **Soft Border** (`#E0D6C8` / `rgb(224,214,200)`): Slightly lighter border variant.
- **Light Border** (`#D4C5B0` / `rgb(212,197,176)`): Subtle structural borders.

### Shadow Colors
- **Ambient** (`rgba(0,0,0,0.06)`): Standard card lift, subtle elevation.
- **Terracotta Glow** (`rgba(196,112,75,0.1)`): Brand-tinted shadow for featured/CTA elements.
- **Hero Overlay** (`rgba(0,0,0,0.3)`): Dark overlay on hero images.

## 3. Typography Rules

### Font Family
- **Primary**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif`
- **No custom fonts** — the system font stack is intentional for performance and native platform feel.
- **No OpenType features** — no stylistic sets, no tabular numbers, no custom features.

### Hierarchy

| Role | Size | Weight | Line Height | Letter Spacing | Color | Notes |
|------|------|--------|-------------|----------------|-------|-------|
| Hero Display | 48px (3.00rem) | 800 | tight | normal | `#2C2419` | Homepage hero headline |
| Display Large | 38px (2.375rem) | 800 | tight | normal | `#2C2419` | Secondary hero / feature headlines |
| Destination Hero | 96px (6.00rem) | 800 | tight | normal | `#FFFFFF` | Destination page city name (on image) |
| Section Heading | 32px (2.00rem) | 700 | tight | normal | `#2C2419` | Section titles (destination pages) |
| Heading 2 | 24px (1.50rem) | 700 | 1.3 | normal | `#2C2419` | Sub-section headings |
| Heading 3 | 22.4px (1.40rem) | 700 | 1.3 | normal | `#2C2419` | Card titles, feature headings |
| Compare Title | 34.2px (2.14rem) | 700 | tight | normal | `#2C2419` | Compare page main heading |
| Body Large | 19.2px (1.20rem) | 400 | 1.5 | normal | `#2C2419` | Introduction text, feature descriptions |
| Body | 16px (1.00rem) | 400 | 1.5–1.6 | normal | `#2C2419` | Standard reading text |
| Body Emphasis | 16px (1.00rem) | 600–700 | 1.5 | normal | `#2C2419` | Bold body, restaurant names |
| Small | 14.4px (0.90rem) | 400–500 | 1.4 | normal | `#6B5D4F` | Secondary text, descriptions |
| Caption | 13.6px (0.85rem) | 400–500 | 1.4 | normal | `#8B7355` | Metadata, subtle labels |
| Micro | 12.8px (0.80rem) | 400 | 1.3 | normal | `#6B5D4F` | Fine print, disclaimers |
| Tag | 12px (0.75rem) | 600 | 1.2 | normal | various | Tags, badges, category labels |
| Tiny | 11.2px (0.70rem) | 400–500 | 1.2 | normal | `#8B7355` | Smallest labels |
| Button | 16px (1.00rem) | 600 | 1.0 | normal | `#FFFFFF` | CTA button text |
| Nav Link | 14.4–15.2px | 500 | 1.0 | normal | `#2D3A5C` | Navigation links |

### Principles
- **System fonts as identity**: No custom font loading. The system font stack means tabiji renders instantly and looks native on every platform — the brand identity is in the color palette, not the letterforms.
- **Weight 700 dominates headings**: Unlike sites using light weights for elegance, tabiji uses bold (700) and extra-bold (800) for headings, creating a strong, confident, guide-like voice.
- **Warm text colors**: Body text uses `#2C2419` (warm near-black) and `#6B5D4F` (muted earth), never cold gray or pure black. Even the text feels warm.
- **No letter-spacing tricks**: No negative tracking on headlines, no expanded tracking on small caps. Clean, natural spacing throughout.

## 4. Component Stylings

### Buttons

**Primary CTA (Terracotta)**
- Background: `#C4704B` (terracotta)
- Text: `#FFFFFF`
- Padding: 12px 24px
- Radius: 8px
- Font: 16px weight 600
- Shadow: `rgba(196,112,75,0.1) 0px 4px 24px`
- Hover: darken background slightly
- Use: Primary actions ("Get Your Free Custom Itinerary", "Get Started")

**Secondary (Indigo)**
- Background: `#2D3A5C` (indigo)
- Text: `#FFFFFF`
- Padding: 10px 20px
- Radius: 8px
- Font: 14px weight 500
- Use: Secondary navigation, category links

**Ghost/Outline**
- Background: transparent or `rgba(255,255,255,0.15)`
- Text: `#FEFCF9` or `#2D3A5C`
- Border: `1px solid #E8DFD0`
- Radius: 8px
- Use: Tertiary actions on light backgrounds, filter controls

### Cards & Containers

**Standard Card**
- Background: `#FEFCF9` or `#F5F0E8`
- Border: none (relies on shadow) or `1px solid #E8DFD0`
- Radius: 14px
- Shadow: `rgba(0,0,0,0.06) 0px 8px 30px`
- Use: Itinerary previews, feature cards

**Featured Card**
- Background: `#FEFCF9`
- Radius: 16px
- Shadow: `rgba(0,0,0,0.06) 0px 2px 12px`
- Use: Compare tables, pricing cards

**Comparison Table Cell**
- Background: `rgba(245,240,232,0.3–0.45)` or `rgba(45,58,92,0.05)` or `rgba(196,112,75,0.08)`
- Radius: 12px
- Border: `1px solid #E8DFD0`
- Use: Side-by-side comparison data blocks

### Badges & Tags

**Category Badge**
- Background: `#E8DFD0` (sand)
- Text: `#2C2419`
- Padding: 4px 12px
- Radius: 100px (pill)
- Font: 12px weight 600
- Use: Category labels, destination tags

**Highlight Pill**
- Background: `rgba(122,139,111,0.08)` (sage tint)
- Text: `#7A8B6F`
- Radius: 999px
- Font: 12px weight 500
- Use: Eco/nature tags, feature indicators

### Navigation
- Sticky header with frosted glass: `rgba(254,252,249,0.92)` + `backdrop-filter: blur(10px)`
- Logo: "tabiji" text in indigo/terracotta, ".ai" suffix
- Links: 14–15px weight 500, `#2D3A5C` text
- CTA: terracotta button right-aligned
- Mobile: hamburger toggle (☰)
- Radius: 10px on nav container

### Testimonial Cards
- Background: `#F5F0E8` or `#FEFCF9`
- Radius: 14px
- Border: `1px solid #E8DFD0`
- Quote text: 16px weight 400, `#2C2419`
- Attribution: 13.6px weight 500, `#6B5D4F`
- Source label: "via Reddit" in `#8B7355`

### Pricing Card
- Background: `#FEFCF9`
- Border: `1px solid #E8DFD0`
- Radius: 16px
- Heading: 22.4px weight 700
- Price: "Free" in terracotta
- Checkmarks: ✓ in terracotta
- CTA: full-width terracotta button at bottom

## 5. Layout Principles

### Spacing System
- Base unit: 8px
- Scale: 4px, 8px, 10px, 12px, 14px, 16px, 20px, 24px, 32px, 40px, 48px, 64px, 80px
- The system favors generous vertical spacing between sections (48px–80px)

### Grid & Container
- Max content width: approximately 1200px
- Hero: centered single-column with generous vertical padding
- Feature sections: 3-column card grid
- Compare pages: 2-column side-by-side layout
- Destination pages: full-width hero image → single-column content
- Itinerary cards: 3-column grid on desktop

### Whitespace Philosophy
- **Travel-magazine pacing**: Generous section spacing (48px–80px) creates a leisurely scroll — you're browsing destinations, not scanning a dashboard.
- **Warm emptiness**: The cream background means whitespace isn't cold — it's the color of paper, inviting you to linger.
- **Content-first density**: Within cards and content blocks, spacing is tighter (8px–16px), but cards themselves breathe with generous margins.
- **Alternating rhythm**: Cream sections alternate with sand-tinted sections, creating visual rhythm without hard dividers.

### Border Radius Scale
- Standard (8px): Buttons, inputs, small cards
- Comfortable (10px): Navigation, medium containers
- Card (12px): Comparison cells, dropdown panels
- Large (14px): Standard cards, testimonials, badges
- Featured (16px): Featured cards, pricing, hero elements
- Full (18px): Large containers on compare pages
- Pill (100px/999px): Tags, category badges
- Circle (50%): Avatars, icons

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat (Level 0) | No shadow | Page background, inline text |
| Subtle (Level 1) | `rgba(0,0,0,0.06) 0px 2px 12px` | Comparison cards, subtle containers |
| Standard (Level 2) | `rgba(0,0,0,0.06) 0px 8px 30px` | Standard cards, content panels |
| Brand Glow (Level 3) | `rgba(196,112,75,0.1) 0px 4px 24px` | CTA buttons, featured terracotta elements |
| Hero Overlay (Level 4) | `rgba(0,0,0,0.3) 0px 4px 20px` | Hero image overlays, dark-background elements |
| Frosted Glass | `backdrop-filter: blur(10px)` + semi-transparent bg | Navigation bar, sticky headers |

**Shadow Philosophy**: Tabiji's shadow system is deliberately understated. Standard shadows use very low opacity (`0.06`) to create a gentle, paper-like lift — elements feel like they're resting on the page, not floating above it. The brand-tinted shadow (`rgba(196,112,75,0.1)`) on CTA elements adds a warm terracotta glow that subtly draws the eye without flashy elevation. The frosted glass navigation creates depth through transparency rather than shadow, keeping the warm cream palette visible beneath.

## 7. Do's and Don'ts

### Do
- Use `#FEFCF9` (paper white) as the page background — not pure white, the warmth matters
- Apply terracotta (`#C4704B`) only for CTAs, links, and key brand moments — it's the singular accent
- Use `#2C2419` (warm near-black) for body text — never pure black or cold gray
- Use the CSS custom property system (`--indigo`, `--terracotta`, etc.) for all colors
- Keep shadows warm and subtle: `0.06` opacity for standard, `rgba(196,112,75,0.1)` for brand elements
- Use generous border-radius: 8px for buttons, 14px for cards, pill for badges
- Use system font stack — no custom font loading
- Use weight 700–800 for headings — bold and confident, not light and whispered
- Maintain the frosted glass nav: semi-transparent cream + backdrop blur

### Don't
- Don't use pure white (`#FFFFFF`) as page background — always `#FEFCF9` (warm cream)
- Don't use pure black (`#000000`) for text — always `#2C2419` (warm near-black)
- Don't use cold grays (blue-gray, neutral gray) — all grays are warm earth tones
- Don't introduce blue as an accent color — the only blues are indigo (`#2D3A5C`) for structure and info blue sparingly
- Don't use heavy shadows (>0.1 opacity) — keep elevation gentle and paper-like
- Don't load custom web fonts — the system stack IS the brand's typographic choice
- Don't use sharp corners (0–4px radius) on cards — the generous rounding (14px+) is core
- Don't use terracotta for large background fills — it's an accent, use cream/sand for surfaces
- Don't skip the frosted glass effect on navigation — the transparency is intentional

## 8. Responsive Behavior

### Breakpoints
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | <640px | Single column, stacked cards, compact padding |
| Tablet | 640–1024px | 2-column card grids, moderate padding |
| Desktop | 1024–1280px | Full layout, 3-column grids |
| Large Desktop | >1280px | Centered content with generous margins |

### Touch Targets
- CTA buttons: generous padding (12px 24px minimum)
- Navigation: hamburger menu on mobile
- Cards: full-card tap target on mobile
- Category badges: comfortable pill padding for touch

### Collapsing Strategy
- Hero: 48px headline → 32px on mobile, weight maintained
- Navigation: horizontal links + CTA → hamburger toggle
- Itinerary cards: 3-column → 2-column → single column stacked
- Compare layout: side-by-side → stacked vertically
- Testimonials: horizontal scroll → stacked
- Section spacing: 64px+ → 40px on mobile
- Pricing cards maintain single-column through all sizes

### Image Behavior
- Destination hero images: full-width with dark overlay for text legibility
- Card images: maintain aspect ratio, contained within border-radius
- Itinerary preview images: responsive sizing with consistent 14px radius

## 9. Agent Prompt Guide

### Quick Color Reference
- Page Background: Paper White (`#FEFCF9`)
- Primary CTA: Terracotta (`#C4704B`)
- Navigation/Structure: Indigo (`#2D3A5C`)
- Heading text: Warm Black (`#2C2419`)
- Body text: Warm Black (`#2C2419`)
- Secondary text: Muted Earth (`#6B5D4F`)
- Tertiary text: Earth (`#8B7355`)
- Card surface: Paper White (`#FEFCF9`) or Warm Cream (`#F5F0E8`)
- Border: Sand (`#E8DFD0`)
- Nature accent: Sage (`#7A8B6F`)
- Star/rating: Gold (`#F4C87A`)

### Example Component Prompts
- "Create a hero section on `#FEFCF9` background. Headline at 48px system font weight 800, color `#2C2419`. Emphasized phrase in italic. Subtitle at 16px weight 400, color `#6B5D4F`. Terracotta CTA button (`#C4704B`, 8px radius, 12px 24px padding, white text weight 600). Below CTA: 13.6px muted text `#8B7355`."
- "Design a card: `#FEFCF9` background, 14px radius, shadow `rgba(0,0,0,0.06) 0px 8px 30px`. Title at 22.4px system font weight 700, color `#2C2419`. Description at 14.4px weight 400, color `#6B5D4F`."
- "Build a category badge: `#E8DFD0` background, `#2C2419` text, 100px radius (pill), 4px 12px padding, 12px weight 600."
- "Create navigation: sticky header with `rgba(254,252,249,0.92)` background + `backdrop-filter: blur(10px)`. Logo in `#2D3A5C` with terracotta `.ai` suffix. Links at 15px weight 500, `#2D3A5C` text. Terracotta CTA right-aligned (`#C4704B` bg, white text, 8px radius)."
- "Design a compare section: two columns on `#FEFCF9`. Each column has `rgba(245,240,232,0.4)` background, 12px radius, `1px solid #E8DFD0` border. Headers at 22.4px weight 700, data at 14.4px weight 400."

### Iteration Guide
1. Start with `#FEFCF9` — never pure white, the warm paper tone is the foundation
2. Terracotta (`#C4704B`) is the singular accent — use for CTAs, links, highlights only
3. Indigo (`#2D3A5C`) for structural text (nav, category labels) — never for decoration
4. All text uses warm tones: `#2C2419` → `#6B5D4F` → `#8B7355` (dark → medium → light)
5. System font stack, no custom fonts — weight 700–800 for headings, 400–500 for body
6. Shadows at 0.06 opacity — gentle paper-like lift, not dramatic elevation
7. Border-radius: 8px buttons, 14px cards, pill for badges — generous but not extreme
8. Frosted glass nav with blur — the semi-transparency shows the warm background beneath
9. Sand (`#E8DFD0`) for all borders and dividers — warm, never cold gray
10. Use CSS custom properties (`--terracotta`, `--indigo`, `--white`, etc.) for maintainability
