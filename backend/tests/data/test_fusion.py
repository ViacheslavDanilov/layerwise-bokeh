from __future__ import annotations

import numpy as np

from layerwise_bokeh.core._fusion import (
    assign_depth_slots,
    bg_normalize,
    place_in_band,
    source_range,
)


def test_bg_normalize_maps_into_bg_band() -> None:
    disp = np.array([[0.0, 0.5], [1.0, 0.25]], dtype=np.float32)
    out = bg_normalize(disp, source_range(disp), bg_band_top=0.05)

    assert out.min() >= 0.0 - 1e-6
    assert out.max() <= 0.05 + 1e-6


def test_place_in_band_stretches_into_explicit_bounds() -> None:
    disp = np.array([[0.0, 1.0], [0.5, 0.5]], dtype=np.float32)
    alpha = np.ones_like(disp)
    out = place_in_band(
        disp, alpha, band_lo=0.30, band_hi=0.40, src_range=source_range(disp, alpha)
    )
    assert out[alpha > 0].min() >= 0.30 - 1e-6
    assert out.max() <= 0.40 + 1e-6


def test_place_in_band_fills_outside_alpha_with_band_lo() -> None:
    disp = np.array([[0.0, 1.0], [0.5, 0.5]], dtype=np.float32)
    alpha = np.array([[1.0, 1.0], [0.0, 0.0]], dtype=np.float32)
    out = place_in_band(
        disp, alpha, band_lo=0.20, band_hi=0.30, src_range=source_range(disp, alpha)
    )
    assert np.allclose(out[1, :], 0.20)


def test_place_in_band_does_not_look_at_the_frame_it_is_given() -> None:
    """The same value lands on the same disparity whatever else the frame holds."""
    disp = np.array([[0.1, 0.5, 0.9]], dtype=np.float32)
    whole = np.ones_like(disp)
    cropped = np.array([[1.0, 1.0, 0.0]], dtype=np.float32)
    src = source_range(disp)

    a = place_in_band(disp, whole, 0.30, 0.40, src)
    b = place_in_band(disp, cropped, 0.30, 0.40, src)

    assert np.allclose(a[0, :2], b[0, :2])


def test_source_range_counts_only_the_pixels_the_alpha_covers() -> None:
    disp = np.array([[0.0, 0.5, 1.0]], dtype=np.float32)
    alpha = np.array([[0.0, 1.0, 0.0]], dtype=np.float32)

    assert source_range(disp, alpha) == (0.5, 0.5)
    assert source_range(disp, np.zeros_like(alpha)) == (0.0, 0.0)


def test_a_range_a_few_float32_steps_wide_stays_inside_the_band() -> None:
    disp = np.full((10, 10), 0.8, dtype=np.float32)
    disp[9, 9] = np.float32(0.8 + 51 * 2**-24)
    src = source_range(disp)
    alpha = np.ones_like(disp)

    placed = place_in_band(disp, alpha, 0.30, 0.40, src)
    background = bg_normalize(disp, src, bg_band_top=0.05)

    assert placed.max() <= 0.40 + 1e-6
    assert background.max() <= 0.05 + 1e-6


def test_assign_depth_slots_are_disjoint_and_ordered() -> None:
    slots = assign_depth_slots(n_objects=3, bg_band_top=0.05, gap=0.02)
    assert len(slots) == 3
    for lo, hi in slots:
        assert 0.05 <= lo < hi <= 1.0
    # Disjoint with a gap between consecutive slots.
    for (_, hi_a), (lo_b, _) in zip(slots, slots[1:], strict=False):
        assert hi_a + 0.02 - 1e-6 <= lo_b
