# Publishing the GitHub profile

1. Open the public [Sodiols/Sodiols repository](https://github.com/Sodiols/Sodiols), or create it under that name.
2. Copy `README.md` to its root and upload the accompanying `assets` folder beside it.
3. Commit the files. Open the [profile](https://github.com/Sodiols) on desktop and mobile to check the layout and links.

Edit the introduction, project notes, toolkit and contact details directly in Markdown. Each project title and illustration links to the project. The hero uses the animated artwork by default and the static editorial cover when the viewer prefers reduced motion. The terminal animation and activity cards each have their own expandable section.

The artwork is bundled locally. The GitHub statistics and language cards load from an external service, so their availability depends on that service. The repository link works independently.

The optional Python generator in `tools/generate_assets.py` produces the original illustrated assets. It uses Pillow, NumPy and OpenCV and expects the fonts configured at the top of the script. The static editorial cover is a separate JPEG. Publishing requires no generator or build step.
