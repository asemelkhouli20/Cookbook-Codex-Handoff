# Visual rebuild handoff

Give ChatGPT the complete `prompt.md` file. It contains 356 individual image briefs and the required ZIP delivery instructions. Attach `asset-manifest.json` too for a machine-readable inventory.

Expected output: 4 character references + 8 site images + 6 textures + 5 decorative PNG cutouts + 35 recipe covers + 288 cooking steps + 10 guide illustrations = 356 separate PNGs.

The recipe instructions and ingredients were extracted from the current `source/book.json`. No generated images or website changes are included in this handoff. The JSON here is an input brief manifest; the image generator must supply actual dimensions and statuses in its delivery manifest.

Start with the chef reference and review the character before producing hundreds of images. Large image-generation jobs may require multiple sessions; `prompt.md` requires explicit batch checkpoints, honest completion counts and a final consolidated ZIP.
