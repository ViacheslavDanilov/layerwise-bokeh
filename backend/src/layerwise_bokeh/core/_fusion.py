"""Per-object disparity band normalization and the objects' starting depth slots."""

from __future__ import annotations

import numpy as np

BG_BAND_TOP = 0.05

_P_LO = 1.0
_P_HI = 99.0


def source_range(
    disp: np.ndarray, alpha: np.ndarray | None = None
) -> tuple[float, float]:
    """The 1st and 99th percentile of an asset's own disparity: the range its relief spans.

    Taken once per asset, from the map as the library stores it, never from a warped frame:
    a warp that crops, zooms or hides part of the asset would move the percentiles, and the
    same surface point would then get a different disparity from one frame to the next.
    With ``alpha``, only the pixels where ``alpha > 0`` count, as an object's relief does.
    """
    region = disp if alpha is None else disp[alpha > 0]
    if region.size == 0:
        return 0.0, 0.0
    p_lo, p_hi = np.percentile(region, [_P_LO, _P_HI])
    return float(p_lo), float(p_hi)


def place_in_band(
    disp: np.ndarray,
    alpha: np.ndarray,
    band_lo: float,
    band_hi: float,
    src_range: tuple[float, float],
) -> np.ndarray:
    """Stretch in-object disparity from ``src_range`` into the explicit [lo, hi] band.

    ``src_range`` is the asset's own :func:`source_range`, so a point keeps its place in
    the band however the object is warped. Pixels outside ``alpha > 0`` are set to
    ``band_lo``. A constant disparity map falls back to the band midpoint.
    """
    out = np.full_like(disp, band_lo, dtype=np.float32)
    mask = alpha > 0
    if not mask.any():
        return out

    p_lo, p_hi = src_range
    src_extent = p_hi - p_lo
    band_size = band_hi - band_lo
    band_mid = (band_lo + band_hi) / 2.0

    if src_extent <= 1e-8:
        out[mask] = band_mid
        return out

    clipped = np.clip(disp, p_lo, p_hi)
    scaled = (clipped - p_lo) / src_extent
    rescaled = band_lo + scaled * band_size
    out[mask] = rescaled[mask]
    return out


def bg_normalize(
    disp: np.ndarray,
    src_range: tuple[float, float],
    bg_band_top: float = BG_BAND_TOP,
) -> np.ndarray:
    """Rescale full-frame background disparity from ``src_range`` into [0, bg_band_top]."""
    p_lo, p_hi = src_range
    src_extent = p_hi - p_lo
    if src_extent <= 1e-8:
        return np.full_like(disp, bg_band_top / 2.0, dtype=np.float32)

    clipped = np.clip(disp, p_lo, p_hi)
    scaled = (clipped - p_lo) / src_extent
    return (scaled * bg_band_top).astype(np.float32)


def assign_depth_slots(
    n_objects: int,
    bg_band_top: float = BG_BAND_TOP,
    gap: float = 0.02,
) -> list[tuple[float, float]]:
    """Partition the disparity axis above the background into disjoint slots.

    Returns ``n_objects`` (lo, hi) bands from far to near (index 0 = farthest),
    separated by ``gap``. Each slot seeds one object's starting depth range; its
    trajectory may leave the slot, and the compositor paints objects by their
    current bands.
    """
    if n_objects <= 0:
        return []
    usable = 1.0 - bg_band_top - gap * (n_objects - 1)
    if usable <= 0.0:
        raise ValueError(
            f"no room for {n_objects} slots above bg_band_top={bg_band_top} "
            f"with gap={gap}",
        )
    width = usable / n_objects
    slots: list[tuple[float, float]] = []
    cursor = bg_band_top
    for _ in range(n_objects):
        lo = cursor
        hi = lo + width
        slots.append((lo, hi))
        cursor = hi + gap
    return slots
