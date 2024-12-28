import dataclasses

from items.base_item import BaseItem


@dataclasses.dataclass(frozen=True)
class Rack(BaseItem):
    item_list: list[BaseItem]

    def get_width(self) -> float:
        raise NotImplementedError

    def register_patches(self, origin: tuple[float, float], ax):
        cur_origin = origin
        for item in self.item_list:
            item.register_patches(cur_origin, ax)
            cur_origin = (cur_origin[0] + item.get_width(), cur_origin[1])
