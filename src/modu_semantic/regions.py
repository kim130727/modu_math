from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


@dataclass
class Region:
    """Layout region in absolute canvas coordinates."""
    id: str
    x: float
    y: float
    width: float
    height: float
    children: list[object] = field(default_factory=list)
    padding: float = 0.0
    metadata: dict[str, object] = field(default_factory=dict)
    visible_debug: bool = False

    def add(self, child: object) -> "Region":
        self.children.append(child)
        return self

    def extend(self, children: Iterable[object]) -> "Region":
        self.children.extend(children)
        return self

    def inset(self, padding: float, *, id: str | None = None) -> "Region":
        if padding < 0:
            raise ValueError("padding must be non-negative")
        new_width = self.width - 2 * padding
        new_height = self.height - 2 * padding
        if new_width < 0 or new_height < 0:
            raise ValueError("inset padding exceeds region size")

        return Region(
            id=id or f"{self.id}_inset",
            x=self.x + padding,
            y=self.y + padding,
            width=new_width,
            height=new_height,
            metadata={"parent": self.id},
        )

    def split_v(
        self,
        *,
        heights: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["Region"]:
        return self._split(axis="v", sizes=heights, gap=gap, padding=padding, ids=ids)

    def split_h(
        self,
        *,
        widths: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["Region"]:
        return self._split(axis="h", sizes=widths, gap=gap, padding=padding, ids=ids)

    def split_v_ratio(
        self,
        *,
        ratios: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["Region"]:
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
    ) -> list["Region"]:
        usable_width = self._usable_width(padding)
        sizes = self._sizes_from_ratios(ratios, usable_width, gap)
        return self.split_h(widths=sizes, gap=gap, padding=padding, ids=ids)

    def contains(self, other: "Region") -> bool:
        return (
            other.x >= self.x
            and other.y >= self.y
            and other.x + other.width <= self.x + self.width
            and other.y + other.height <= self.y + self.height
        )

    def contains_point(self, x: float, y: float) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def intersects(self, other: "Region") -> bool:
        return not (
            self.x + self.width <= other.x
            or other.x + other.width <= self.x
            or self.y + self.height <= other.y
            or other.y + other.height <= self.y
        )

    def _split(
        self,
        *,
        axis: str,
        sizes: Sequence[float],
        gap: float,
        padding: float,
        ids: Sequence[str] | None,
    ) -> list["Region"]:
        if not sizes:
            raise ValueError("sizes must not be empty")
        if any(value <= 0 for value in sizes):
            raise ValueError("all sizes must be positive")
        if gap < 0:
            raise ValueError("gap must be non-negative")
        if padding < 0:
            raise ValueError("padding must be non-negative")

        count = len(sizes)
        region_ids = self._resolve_ids(count, ids)

        usable_width = self._usable_width(padding)
        usable_height = self._usable_height(padding)

        required = sum(sizes) + gap * (count - 1)
        capacity = usable_height if axis == "v" else usable_width
        if required > capacity + 1e-9:
            raise ValueError(
                f"split overflow in region '{self.id}': required={required}, capacity={capacity}"
            )

        regions: list[Region] = []
        cursor = padding
        for index, size in enumerate(sizes):
            if axis == "v":
                child = Region(
                    id=region_ids[index],
                    x=self.x + padding,
                    y=self.y + cursor,
                    width=usable_width,
                    height=size,
                    metadata={"parent": self.id},
                )
            else:
                child = Region(
                    id=region_ids[index],
                    x=self.x + cursor,
                    y=self.y + padding,
                    width=size,
                    height=usable_height,
                    metadata={"parent": self.id},
                )
            regions.append(child)
            cursor += size + gap

        self.children.extend(regions)
        return regions

    def split_rows(
        self,
        *,
        heights: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["Region"]:
        return self.split_v(heights=heights, gap=gap, padding=padding, ids=ids)

    def split_cols(
        self,
        *,
        widths: Sequence[float],
        gap: float = 0.0,
        padding: float = 0.0,
        ids: Sequence[str] | None = None,
    ) -> list["Region"]:
        return self.split_h(widths=widths, gap=gap, padding=padding, ids=ids)

    def _resolve_ids(self, count: int, ids: Sequence[str] | None) -> list[str]:
        if ids is None:
            return [f"{self.id}_{idx + 1}" for idx in range(count)]
        if len(ids) != count:
            raise ValueError("ids length must match number of split sections")
        return list(ids)

    def _usable_width(self, padding: float) -> float:
        usable = self.width - 2 * padding
        if usable <= 0:
            raise ValueError("padding leaves non-positive usable width")
        return usable

    def _usable_height(self, padding: float) -> float:
        usable = self.height - 2 * padding
        if usable <= 0:
            raise ValueError("padding leaves non-positive usable height")
        return usable

    def _sizes_from_ratios(self, ratios: Sequence[float], total: float, gap: float) -> list[float]:
        if not ratios:
            raise ValueError("ratios must not be empty")
        if any(value <= 0 for value in ratios):
            raise ValueError("all ratios must be positive")

        inner_total = total - gap * (len(ratios) - 1)
        if inner_total <= 0:
            raise ValueError("gap exceeds available size")

        ratio_sum = sum(ratios)
        return [inner_total * (value / ratio_sum) for value in ratios]
