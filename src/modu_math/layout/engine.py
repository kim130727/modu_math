from __future__ import annotations

from typing import Iterable, Sequence
from .models.node import LayoutNode
from .models.group import LayoutGroup

class LayoutRegion(LayoutGroup):
    """Layout region in absolute canvas coordinates for grid/split math."""

    def __init__(self, id: str, x: float, y: float, width: float, height: float):
        super().__init__(id=id, x=x, y=y, width=width, height=height)

    def add(self, child: LayoutNode) -> "LayoutRegion":
        self.children.append(child)
        return self

    def split_v(
        self,
        *,
        heights: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["LayoutRegion"]:
        return self._split(axis="v", sizes=heights, gap=gap, padding=padding, ids=ids)

    def split_h(
        self,
        *,
        widths: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["LayoutRegion"]:
        return self._split(axis="h", sizes=widths, gap=gap, padding=padding, ids=ids)

    def split_v_ratio(
        self,
        *,
        ratios: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["LayoutRegion"]:
        usable_height = self._usable_height(padding)
        sizes = self._sizes_from_ratios(ratios, usable_height, gap)
        return self.split_v(heights=sizes, gap=gap, padding=padding, ids=ids)

    def split_h_ratio(
        self,
        *,
        ratios: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["LayoutRegion"]:
        usable_width = self._usable_width(padding)
        sizes = self._sizes_from_ratios(ratios, usable_width, gap)
        return self.split_h(widths=sizes, gap=gap, padding=padding, ids=ids)

    def _split(
        self,
        *,
        axis: str,
        sizes: Sequence[float],
        gap: float,
        padding: float,
        ids: Sequence[str] | None,
    ) -> list["LayoutRegion"]:
        if not sizes:
            raise ValueError("sizes must not be empty")
        if any(value <= 0 for value in sizes):
            raise ValueError("all sizes must be positive")

        count = len(sizes)
        region_ids = self._resolve_ids(count, ids)

        usable_width = self._usable_width(padding)
        usable_height = self._usable_height(padding)

        required = sum(sizes) + gap * (count - 1)
        capacity = usable_height if axis == "v" else usable_width
        if required > capacity + 1e-9:
            raise ValueError(f"split overflow in region '{self.id}'")

        regions: list[LayoutRegion] = []
        cursor = padding
        for index, size in enumerate(sizes):
            if axis == "v":
                child = LayoutRegion(
                    id=region_ids[index],
                    x=self.x + padding,
                    y=self.y + cursor,
                    width=usable_width,
                    height=size,
                )
            else:
                child = LayoutRegion(
                    id=region_ids[index],
                    x=self.x + cursor,
                    y=self.y + padding,
                    width=size,
                    height=usable_height,
                )
            regions.append(child)
            cursor += size + gap

        self.children.extend(regions)
        return regions

    def _resolve_ids(self, count: int, ids: Sequence[str] | None) -> list[str]:
        if ids is None:
            return [f"{self.id}_{idx + 1}" for idx in range(count)]
        return list(ids)

    def _usable_width(self, padding: float) -> float:
        return self.width - 2 * padding if self.width else 0.0

    def _usable_height(self, padding: float) -> float:
        return self.height - 2 * padding if self.height else 0.0

    def _sizes_from_ratios(self, ratios: Sequence[float], total: float, gap: float) -> list[float]:
        inner_total = total - gap * (len(ratios) - 1)
        ratio_sum = sum(ratios)
        return [inner_total * (value / ratio_sum) for value in ratios]
