# Uniform Workshop Image Display

## Goal

A consistent workshop grid where every card shows an image in the **same width and height** (same visual box), with **no stretch or distortion**, whether the upload is portrait, landscape, or square.

## HTML Structure (Image Cards)

```html
<div class="card workshop-card h-100 shadow-sm">
  <div class="workshop-card-image position-relative">
    <img src="..." class="workshop-card-image__img" alt="...">
    <span class="badge ...">Category</span>
  </div>
  <div class="card-body">...</div>
  <div class="card-footer">...</div>
</div>
```

- **`.workshop-card`** — Card wrapper; `overflow: hidden` keeps content inside.
- **`.workshop-card-image`** — **Fixed-size image container** (same dimensions for every card). Uses `aspect-ratio: 16/9` so width and height stay proportional without a fixed pixel height.
- **`.workshop-card-image__img`** — The actual `<img>`. Fills the container using `object-fit: cover` and `object-position: center`.

Badges or overlays stay in the same place by using `position-relative` on the container and `position-absolute` on the badge.

## How Distortion Is Prevented

1. **Fixed container, not fixed image dimensions**  
   The **container** has a fixed proportion (e.g. 16∶9). The image file is never resized or modified; only the **visible area** is defined by the box.

2. **`object-fit: cover`**  
   - The image is scaled so it **fully covers** the container while keeping its **original aspect ratio**.  
   - No squashing or stretching: if the image is portrait, the top and bottom may be cropped; if landscape, the sides may be cropped.  
   - No excessive zoom: the smallest scale that still covers the box is used.

3. **`object-position: center`**  
   Cropping is centered, so the most important part of the image (center) stays visible for both portrait and landscape.

4. **No server-side image changes**  
   All behavior is done in the browser with CSS; original uploaded images are not modified.

## CSS Summary

| Concern | Approach |
|--------|----------|
| Same width/height for all | Container has `width: 100%` and `aspect-ratio: 16/9` (or 4/3 on small screens). |
| No stretch/distortion | `object-fit: cover` on the img. |
| No excessive zoom | `cover` uses the minimum scale that fills the box. |
| Aspect ratio preserved | Browser scales uniformly; `object-fit` avoids stretch. |
| Graceful crop | `object-position: center`; overflow is hidden by the container. |
| Grid alignment | Bootstrap grid + `.workshop-card` + `.workshop-card-image` keep cards and image boxes aligned. |

## Responsive Behavior

- **Desktop:** 16∶9 image container; cards in a multi-column grid (e.g. 3 columns).
- **≤ 768px:** 4∶3 image container (slightly taller) and single-column card layout (handled by existing Bootstrap/responsive rules).

Fallback for browsers that don’t support `aspect-ratio`: the same proportions are achieved with `padding-bottom: 56.25%` (16∶9) or `75%` (4∶3) and `position: absolute` on the image.

## Files

- **CSS:** `version1/static/css/index.css` — `.workshop-card`, `.workshop-card-image`, `.workshop-card-image__img`, fallbacks, and media query.
- **HTML:** `version1/templates/index.html` — Workshop loop uses the classes above for each card image.
