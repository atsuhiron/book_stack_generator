import dataclasses

from matplotlib import patches as patch

from items.base_item import BaseItem


@dataclasses.dataclass(frozen=True)
class Rack(BaseItem):
    item_list: list[BaseItem]

    def get_width(self) -> float:
        raise NotImplementedError

    def generate_patches(self, origin: tuple[float, float]) -> list[patch.Patch]:
        cur_origin = origin
        patches = []
        for item in self.item_list:
            patches.extend(item.generate_patches(cur_origin))
            cur_origin = (cur_origin[0] + item.get_width(), cur_origin[1])
        return patches
