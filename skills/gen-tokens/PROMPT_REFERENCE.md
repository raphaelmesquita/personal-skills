# Prompt Reference

## Reference Look
Match bold official character-select portraits, large busts filling most of each square, three-quarter or forward-facing poses, strong facial expressions, glossy skin highlights, crisp anatomy, heavy ink-like contrast, painterly brush texture, and gritty but colorful game-promo rendering.

Use simple atmospheric backgrounds behind each character: textured paint, grunge walls, motion brush strokes, or soft color fields. Keep them low-detail so faces read immediately, but vary their palette across the grid: reds, blues, greens, yellows, purples, teals, oranges, and dark neutrals. Do not use identical background colors for adjacent cells when avoidable.

Use high-quality modern fighting game character-select portrait art inspired by Street Fighter 6, Capcom promotional illustrations, 1990s arcade brawlers, and gritty international tournament character art. Prioritize vibrant colors, strong contrast, dramatic rim light, memorable silhouettes, readable costume shapes, and professional videogame card-art finish.

Do not copy existing copyrighted characters exactly. Create original characters that fit the genre.

## Prompt Template
```text
Generate a square 1:1 high-resolution image containing exactly 9 original NPC character portraits arranged in a clean 3x3 grid.
The image is for Roll20 token creation in a Street Fighter RPG / White Wolf campaign. Each portrait must occupy one equal square cell, be centered, and use chest-up or upper-torso framing with safe margin for later hexagonal cropping.
Theme: [expanded user concept]
Create these 9 distinct original characters:
1. [role, age range, body type, visual influence, clothing, accessory, expression, fighting vibe, color accent]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
7. [...]
8. [...]
9. [...]
Style: high-quality modern fighting game character-select portrait art, 1990s arcade brawler energy, gritty urban action, dramatic lighting, bold silhouettes, expressive faces, vibrant controlled colors, painterly digital illustration, same artist for all portraits.
Composition: 3x3 grid, equal square cells, tight chest-up or upper-torso portraits, large readable faces near the center, consistent portrait scale, no text, no logos, no captions, no UI, no watermarks.
Backgrounds: each cell has a simple painted atmospheric background with a distinct accent color; vary reds, blues, greens, yellows, purples, teals, oranges, and dark neutrals; avoid detailed scenery.
Token safety: keep faces, eyes, hair, shoulders, hands, gloves, weapons, and iconic accessories inside the central safe area of each cell for circular or hexagonal Roll20 cropping.
Negative constraints: no duplicate characters, repeated outfits, repeated hairstyles, full-body shots, tiny faces, cropped heads, cropped shoulders, edge-crossing props, detailed scenery, text, names, letters, logos, or excessive background detail.
```

## Reference Image Template
Use this template when the user supplies an image reference.

```text
Generate a square 1:1 high-resolution image containing exactly 9 token-ready character portraits arranged in a clean 3x3 grid.
Use the provided image as visual reference only. Do not extend the original canvas, do not create a horizontal pose sheet, do not create a full-body lineup, and do not create a single wide scene.
Reference task: [same-character poses / related characters / same style or archetype]
Reference details to preserve: [identity or family traits, costume language, hairstyle, body type, color palette, silhouette, mood, drawing style]
Create exactly 9 square cells:
1. [pose, expression, angle, battle mood, accent/background]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
7. [...]
8. [...]
9. [...]
Style: match the reference drawing style while keeping high-quality fighting game character-select portrait art, 1990s arcade brawler energy, gritty urban action, dramatic lighting, bold silhouettes, expressive faces, painterly digital illustration, professional videogame card-art finish.
Composition: square 1:1 image, clean 3x3 grid, equal square cells, one centered character per cell, tight chest-up or upper-torso portraits, large readable faces near the center, consistent portrait scale, no text, no logos, no captions, no UI, no watermarks.
Token safety: keep faces, eyes, hair, shoulders, hands, gloves, weapons, and iconic accessories inside the central safe area of each cell for circular or hexagonal Roll20 cropping.
Negative constraints: no horizontal layout, no animation sheet, no full-body pose sheet, no single wide background scene, no cropped heads, no tiny faces, no edge-crossing props, no text, no letters, no logos.
```

## Reference Modes
- Single character image with no extra instruction: create 9 token-ready portrait poses of the same character.
- "Several poses": preserve the same character identity and vary expression, angle, stance, hand position, combat mood, and lighting.
- "Siblings", "relatives", "gang members", or "rivals": create 9 related original characters sharing visual DNA with the reference.
- "Same type" or "same style": create 9 original NPCs using the reference archetype, clothing language, palette, silhouette, and mood.
