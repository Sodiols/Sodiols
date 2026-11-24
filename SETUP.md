# GitHub profile setup

This is a complete GitHub-compatible profile README for **Sodiols**. The 3D-style elements are animated GIFs, not JavaScript or an interactive Three.js scene. They will animate when displayed as images in GitHub's README renderer.

## Publish

1. Open https://github.com/Sodiols/Sodiols . If your profile repository doesn't exist, create a **public** repository named `Sodiols` in the account `Sodiols`.
2. Upload `README.md` into the repository root and upload the entire `assets` directory without changing any filenames.
3. Commit both. The profile appears at https://github.com/Sodiols .
4. On desktop and mobile, verify that the hero GIF, terminal GIF, tool board, and all four project covers load.

Your final repository should look like:

```
Sodiols/
├── README.md
├── SETUP.md                 # optional; can remove after publishing
├── assets/
│   ├── hero-3d.gif
│   ├── hero-still.png
│   ├── terminal.gif
│   ├── toolkit.png
│   ├── cta-portfolio.png
│   ├── cta-github.png
│   ├── cta-email.png
│   ├── project-tara.png
│   ├── project-husnalogy.png
│   ├── project-portfolio.png
│   ├── project-prichat.png
│   └── divider.png          # optional spare asset
└── tools/
    └── generate_assets.py # optional, not needed for publishing
```

## Technical notes

- Do not paste the README without the `assets` folder. The README uses relative paths such as `./assets/hero-3d.gif`.
- Animated GIFs work without GitHub Actions, scripts, or a third-party animation host.
- GitHub sanitizes inline CSS, scripts and unsupported HTML. Do not try to embed `<canvas>`, JavaScript, or Three.js inside the README.
- The GitHub activity widgets come from the external `github-readme-stats` service. They are collapsed by default and may be unavailable due to service outages or limits. You can delete the `04 / GITHUB ACTIVITY` section if you want a fully self-contained profile.
- If you prefer an entirely static banner, replace `./assets/hero-3d.gif` with `./assets/hero-still.png` in `README.md`.
- All project and social URLs use the links given by the profile owner. Confirm they still point to the intended destinations before publishing.

## Editing the animated artwork

The included Python generator (`tools/generate_assets.py`) was used to create the art. It requires Pillow, NumPy and OpenCV, plus Inter and DejaVu Sans Mono font files at the paths configured at the top of the script. On Windows, change those font paths if you need to regenerate the visuals. **You do not need to run this script to publish the profile.**

Install generator dependencies only if modifying the illustrations:

```
pip install pillow numpy opencv-python
python tools/generate_assets.py
```
