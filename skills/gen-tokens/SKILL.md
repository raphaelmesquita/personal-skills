---
name: gen-tokens
description: Generates Roll20-ready 3x3 NPC token grids, stores the generated grid, then extracts it into individual hex-safe PNG tokens with its bundled extractor. Use when the user asks to create, generate, split, extract, or prepare Roll20 tokens, NPC portrait grids, Street Fighter RPG token sheets, or token batches from a single generated image.
---

# Roll20 Street Fighter Token Generator

## Intent
Create one square 3x3 character portrait grid and turn it into nine individual Roll20-ready PNG tokens plus a downloadable ZIP. The image generation step should produce original Street Fighter RPG / White Wolf NPC portraits. The extraction step uses this skill's bundled Python script, so it works from any current workspace and does not depend on a specific repository.

## Quick Start
When the user gives a character group concept:
1. Expand the concept into nine distinct original NPC portraits.
2. Call the system `imagegen` skill to generate one square 1:1 3x3 grid image.
3. Save the generated grid in `input/` under the current working directory, using a slug derived from the user's request, for example `input/metro-city-punks.png`.
4. Extract tokens with the bundled script, passing a slug derived from the requested character type, faction, or concept, and create a ZIP. Resolve `scripts/extract_tokens.py` relative to this skill directory:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py input\metro-city-punks.png --slug metro_city_punk --zip
```

The command writes extracted tokens and a ZIP to `output/` in the current working directory. To choose another folder:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py input\metro-city-punks.png --output-dir output --slug metro_city_punk --zip
```

To process every supported image in the current directory's `input/` folder:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py
```

If Pillow is missing, install this skill's dependency:

```powershell
python -m pip install -r <gen-tokens-skill-dir>\requirements.txt
```

## Codex Native Image Generation Fallback
When the native Codex image generation tool saves the generated grid outside the workspace, copy the generated PNG into `input/<request-slug>.png` before extraction. In Codex desktop this image may be under:

```text
C:\Users\<user>\.codex\generated_images\<generation-id>\*.png
```

Leave the original generated image in place and copy it into the workspace.

## Workflow
1. Confirm or infer the faction, theme, location, and campaign tone.
2. If the user provides an image, infer whether it is a single-character reference, a style/type reference, or a related-character request.
3. Build a concise image prompt with fixed 3x3 grid requirements.
4. Generate exactly one square image with nine character portraits.
5. Save the grid to `input/<request-slug>.png` in the current workspace.
6. Run the bundled extraction command with `--slug <request-slug> --zip`.
7. Report the generated image path, output folder, and ZIP path.

## Hard Format Rule
Every generated image must be a square 1:1 clean 3x3 grid with exactly nine equal cells. This rule applies even when the user provides a reference image, asks for several poses, siblings, gang members, relatives, rivals, clones, upgrades, alternate costumes, variants, or characters in the same style. Never generate a horizontal pose sheet, animation sheet, full-body lineup, single wide scene, or expanded landscape canvas for this skill.

## Reference Image Behavior
When the user uploads or points to a character, creature, outfit, gang type, or art style image, use it as visual reference only and still produce a new square 3x3 token grid.

If the image appears to show one main character and the user does not specify another intent, generate nine token-ready portrait variations of that same character. Preserve identity, costume language, hairstyle, body type, color palette, silhouette, and drawing style. Vary expression, angle, stance, hand position, battle mood, and lighting while keeping each version chest-up or upper-torso and centered in its own cell.

If the user asks for siblings, relatives, gang members, rivals, variants, skins, upgrades, or characters in the same style, create nine related original characters or versions that share the relevant visual DNA from the reference without becoming exact clones unless the user explicitly asks for same-character poses.

For style/type references, extract the archetype, clothing language, silhouette, palette, mood, and drawing style, then create nine original NPCs that fit that type.

## Extraction And Naming
The extractor now supports concept-derived output names and ZIP packaging:

```powershell
python <gen-tokens-skill-dir>\scripts\extract_tokens.py input\metro-city-punks.png --slug metro_city_punk --zip
```

Use lowercase ASCII slugs derived from the user's requested character type, faction, or concept:

- "9 punks de Metro City" -> `metro_city_punk_01.png` through `metro_city_punk_09.png`, plus `metro_city_punk_tokens.zip`
- "capangas da Shadoloo" -> `shadoloo_capanga_01.png` through `shadoloo_capanga_09.png`, plus `shadoloo_capanga_tokens.zip`
- "poses do lutador de rua" -> `lutador_de_rua_pose_01.png` through `lutador_de_rua_pose_09.png`, plus `lutador_de_rua_pose_tokens.zip`

If the request is unclear, derive the slug from the source filename. If both are unclear, use `roll20_token`.

The extractor writes working files to `output/` by default. In Codex desktop projectless threads, user-facing deliverables should be copied to the thread's `outputs/` folder after extraction.

```powershell
Copy-Item -LiteralPath "input\<request-slug>.png" -Destination "outputs\<request-slug>_grid.png" -Force
Copy-Item -LiteralPath "output\<slug>_tokens.zip" -Destination "outputs\<slug>_tokens.zip" -Force
Copy-Item -Path "output\<slug>_*.png" -Destination "outputs" -Force
```

Use `-LiteralPath` for exact paths and `-Path` for the token PNG wildcard copy.

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

## Example Requests
- "Gangue de Metro City estilo Final Fight, punks dos anos 1990."
- "Lutadores do circuito clandestino de Las Vegas."
- "Capangas da Shadoloo."
- "Gere varias poses deste personagem, preservando o estilo."
- "Gere irmaos deste personagem em um grid 3x3."
- "Crie personagens neste mesmo tipo visual."
