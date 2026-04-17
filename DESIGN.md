```markdown
# Design System: The Kinetic Cipher

## 1. Overview & Creative North Star
**Creative North Star: "The Neon Architect"**
This design system moves away from the static, "boxed-in" nature of traditional portfolios. It is built to feel like a living terminal—a sophisticated, high-end digital environment that captures the intersection of Computer Science and high-fidelity art. 

To break the "template" look, we utilize **intentional asymmetry** and **kinetic layering**. We avoid traditional grids in favor of overlapping elements where text occasionally bleeds over image boundaries, and depth is created through atmospheric glows rather than structural dividers. The experience should feel like a custom-coded interface: precise, futuristic, and deeply intentional.

## 2. Colors: The Luminescent Void
The palette is rooted in `surface` (#0b0e14), a deep, obsidian base that allows the neon accents to vibrate.

*   **Primary & Secondary Dynamic:** `primary` (#69daff) and `secondary` (#ebb2ff) are not just accents; they are light sources. Use them to draw the eye to critical CTAs and active code snippets.
*   **The "No-Line" Rule:** 1px solid borders are strictly prohibited for sectioning. To separate the "About" section from "Projects," transition from `surface` to `surface-container-low`. Boundaries must be felt, not seen.
*   **Surface Hierarchy & Nesting:** Treat the UI as a series of stacked obsidian sheets. 
    *   Base: `surface`
    *   Sectioning: `surface-container-low`
    *   Component Cards: `surface-container-high`
    *   Interactive Pop-overs: `surface-container-highest`
*   **The "Glass & Gradient" Rule:** Floating elements (like navigation bars or code-preview cards) must utilize Glassmorphism. Combine `surface_variant` at 40% opacity with a `backdrop-filter: blur(12px)`.
*   **Signature Textures:** Apply subtle linear gradients (e.g., `primary` to `primary_container`) for primary buttons. For a "soulful" feel, use a radial gradient of `secondary` at 5% opacity in the background to mimic a distant nebula or "screen glow."

## 3. Typography: Technical Elegance
The typography strategy pairs the mathematical precision of **Space Grotesk** with the clean, readable utility of **Inter**.

*   **Display & Headline (Space Grotesk):** These are your "Brand Moments." Use `display-lg` for hero statements. The wide apertures and geometric shapes of Space Grotesk communicate a futuristic, CS-centric aesthetic. Use tighter letter-spacing (-0.02em) for headlines to create an editorial feel.
*   **Title & Body (Inter):** Inter handles the heavy lifting. It provides a grounded, professional contrast to the expressive headlines. `body-md` should be used for project descriptions to ensure maximum legibility against the dark background.
*   **Label (Space Grotesk):** Small labels (e.g., "Tech Stack" or "Commit History") should be in `label-md` uppercase with increased letter-spacing (+0.05em) to mimic a high-end command-line interface.

## 4. Elevation & Depth: Tonal Layering
We reject the "drop shadow" of the 2010s. Depth in this system is achieved through light and atmospheric density.

*   **The Layering Principle:** Instead of shadows, use `surface-container` tiers. A `surface-container-highest` card sitting on a `surface-dim` background creates a natural, sophisticated lift.
*   **Ambient Shadows:** If a card must float (e.g., a modal), use a shadow tinted with `primary` at 8% opacity. Use a massive blur (40px+) to simulate a soft glow rather than a hard edge.
*   **The "Ghost Border" Fallback:** For accessibility in input fields, use a "Ghost Border": `outline_variant` at 15% opacity. This defines the edge without breaking the "No-Line" rule.
*   **Kinetic Glow:** Interactive elements should utilize an "Inner Glow" on hover—a subtle `box-shadow: inset 0 0 10px` using the `primary_dim` token.

## 5. Components

### Buttons
*   **Primary:** High-contrast. Gradient from `primary` to `primary_fixed`. No border. On hover: Increase `primary` glow intensity.
*   **Secondary:** Ghost style. `surface-container-high` background with a `primary` Ghost Border (20% opacity).
*   **Tertiary:** Text only using `primary` color. On hover: a subtle `secondary_container` (10% opacity) background pill shape appears.

### Cards (Project/Experience)
*   **Rule:** No dividers. Use `surface-container-low` for the card body. 
*   **Interaction:** On hover, the card should scale slightly (1.02x) and the background should shift to `surface-container-high` with a 1px `primary` Ghost Border fade-in.

### Chips (Skills/Tags)
*   **Style:** `surface-variant` background, `primary` text. Use `full` roundedness. 
*   **Context:** Use these for "React," "Python," or "AWS" tags.

### Input Fields
*   **Style:** `surface-container-lowest` background. No bottom line; instead, a full-surround Ghost Border that illuminates to 100% `primary` opacity when focused.

### Custom Component: The "Terminal Header"
*   For project sections, use a `label-md` header with a flickering cursor animation (using `secondary`) to lean into the CS student identity.

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical layouts. Let an image be 60% width and the text 40%, slightly overlapping the image edge.
*   **Do** use `primary` and `secondary` for "Hover States." The UI should feel like it's reacting to the user's touch with light.
*   **Do** ensure high contrast for code snippets. Use `surface-container-lowest` for code blocks to make them feel "recessed" into the page.

### Don't
*   **Don't** use 100% white (#FFFFFF). Always use `on-surface` (#e0e5f5) to prevent eye strain and maintain the premium dark-mode aesthetic.
*   **Don't** use standard easing. All transitions must be `cubic-bezier(0.22, 1, 0.36, 1)` (Expo Out) for a "snappy yet smooth" futuristic feel.
*   **Don't** use divider lines to separate content. Use 80px - 120px of vertical whitespace (from the spacing scale) instead.