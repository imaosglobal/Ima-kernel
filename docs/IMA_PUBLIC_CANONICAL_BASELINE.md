# IMA Public Canonical Baseline

**Status:** canonical source baseline established on 2026-11-03, pending public deployment verification.

## Baseline intent
Preserve the richer public IMA visual baseline that was verified before the recent visual regression, while reintroducing only the campaign identity changes required for the public site.

## Evidence used
- Historical visual baseline: commit `6374a1861097f497a0eb26ad0e0d1974eaf5e685`.
- The current `App.jsx` and `index.css` were compared with that baseline; the main layout/CSS was materially the same.
- The live public page previously showed the older HeyGen talking-photo asset, while the canonical campaign image reference is `https://dynamic.heygen.ai/image/f057cd08143342f2994f85d847572fa8/original.png`.
- Google Identity Services remains the official Google-rendered button and its existing client/origin configuration is preserved.
- The existing PWA install flow is preserved; no install logic was replaced.
- The service-worker shell cache was advanced to invalidate stale public assets.

## Canonical identity rules
1. The canonical campaign logo is the single visible IMA campaign identity inside the public site.
2. The same campaign identity is used for browser/PWA identity where the platform accepts the remote campaign asset.
3. The IMA logo remains linked to the public campaign destination, not an Ads management console.
4. Google login remains the official Google Identity Services button; do not replace it with a custom imitation.
5. The install action remains the existing browser-native `beforeinstallprompt` flow with a safe manual fallback.
6. Do not change the public visual system merely to repair authentication or installation.
7. Any future visual change must be isolated, regression-tested, and verified on the canonical public URL before being called live.

## Current source changes
- `ima-ui/src/App.jsx`: visible header brand mark uses the canonical campaign logo.
- `ima-ui/src/index.css`: campaign logo styling added without changing the layout system.
- `ima-ui/public/manifest.webmanifest`: PWA icons point to the canonical campaign image.
- `ima-ui/index.html`: favicon and Apple touch icon point to the canonical campaign image.
- `ima-ui/public/sw.js`: shell cache advanced to `ima-shell-v7` to prevent stale visual assets.

## Verification gate
This baseline is **not considered publicly live** until the deployment workflow succeeds and the public `version.json`, page, Google button, install control, campaign link, and visible logo are independently verified.
