---
name: gen-tokens
description: Generates Roll20-ready 3x3 NPC token grids, stores the generated grid, then extracts it into individual hex-safe PNG tokens with its bundled extractor. Use when the user asks to create, generate, split, extract, or prepare Roll20 tokens, NPC portrait grids, Street Fighter RPG token sheets, or token batches from a single generated image.
---

# Roll20 Street Fighter Token Generator

## Intent
Create one square 3x3 character portrait grid and turn it into nine individual Roll20-ready PNG tokens. The image generation step should produce original Street Fighter RPG / White Wolf NPC portraits. The extraction step uses this skill's bundled Python script, so it works from any current workspace and does not depend on a specific repository.

## Quick Start
When the user gives a character group concept:
1. Expand the concept into nine distinct original NPC portraits.
2. Call the system `imagegen` skill to generate one square 1:1 3x3 grid image.
3. Save the generated grid in `input/` under the current working directory, using a slug derived from the user's request, for example `input/metro-city-punks.png`.
4. Extract tokens with the bundled script. Resolve `scripts/extract_tokens.py` relative to this skill directory:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py input\metro-city-punks.png
```

The command writes extracted tokens to `output/` in the current working directory. To choose another folder:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py input\metro-city-punks.png --output-dir output
```

To process every supported image in the current directory's `input/` folder:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py
```

If Pillow is missing, install this skill's dependency:

```powershell
python -m pip install -r <gen-tokens-skill-dir>\requirements.txt
```

## Workflow
1. Confirm or infer the faction, theme, location, and campaign tone.
2. Build a concise image prompt with fixed 3x3 grid requirements.
3. Generate exactly one square image with nine character portraits.
4. Save the grid to `input/<request-slug>.png` in the current workspace.
5. Visually inspect the generated grid before extraction when possible.
6. Run the bundled extraction command for the generated file.
7. Report the generated image path, output folder, and any visible token issues.

## Image Requirements
Always ask image generation for:
- one square 1:1 image
- exactly nine original character portraits
- a clean 3x3 grid with equal square cells
- one centered character per cell
- tight chest-up or upper-torso fighting game portrait framing
- no text, names, logos, captions, UI, borders, watermarks, or symbols
- consistent visual style, lighting language, and portrait scale
- varied simple painted backgrounds per cell, with different accent colors
- enough central safe margin for hexagonal token cropping with the bottom vertex pointing down

## Token Safety
Each portrait must keep the face, eyes, hair mass, head silhouette, upper torso, shoulders, hands, gloves, weapons, and iconic accessories inside the central safe area of its cell. The face should sit near the visual center, with the top of the head and shoulders clearly inside the crop. Avoid tiny heads, full-body poses, props crossing the cell edge, or hands/weapons becoming the main subject.

## Reference Look
Use bold fighting-game character-select portraits with large busts, expressive faces, strong contrast, painterly texture, varied simple backgrounds, and readable silhouettes. Do not copy existing copyrighted characters exactly. Create original characters that fit the genre.

## Character Variety
If the user does not provide nine characters, invent nine. Vary body type, age, ethnicity or regional visual influence, gender presentation, facial structure, hairstyle, costume, fighting role, personality, silhouette, and color accent. Avoid repeating the same archetype, outfit, pose, expression, or combat role.

## Prompt Template
Use the full template in [PROMPT_REFERENCE.md](PROMPT_REFERENCE.md) when calling `imagegen`.

## Quality Check
Before finishing, check for wrong aspect ratio, missing cells, more or fewer than nine portraits, duplicate characters, faces too close to the edge, tiny or off-center faces, important accessories outside the hex-safe center, repeated adjacent background colors, text artifacts, inconsistent style, and unreadable token faces. Regenerate or warn clearly when an issue cannot be fixed.

## Example Requests
- "Gangue de Metro City estilo Final Fight, punks dos anos 1990."
- "Lutadores do circuito clandestino de Las Vegas."
- "Capangas da Shadoloo."
