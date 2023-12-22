import json
import os
from typing import Dict, List

from rmscene import read_blocks, SceneLineItemBlock

from util.classes import XYCoordinate
from util.constants import RM_LETTER_WIDTH, RM_LETTER_HEIGHT, TEMP_DIRECTORY
from util.func import get_temp_file


def get_draw_points(rm_dir: str = TEMP_DIRECTORY) -> Dict[int, List[XYCoordinate]]:
    dir_name = ""
    pages = {}
    output = {}

    for file in os.listdir(rm_dir):
        if file.endswith(".content"):
            dir_name = file.split(".")[0]
            with open(get_temp_file(file), "r") as f:
                content = json.load(f)

                page_idx = 1
                _p = content['cPages']['pages'] if 'cPages' in content else content['pages']
                for page in _p:
                    pages[page_idx] = page['id'] if 'cPages' in content else page
                    page_idx = page_idx + 1

    for page in pages.keys():
        rm_file = os.path.join(os.path.join(rm_dir, dir_name), f"{pages[page]}.rm")

        points = []
        with open(rm_file, 'rb') as f:
            result = read_blocks(f)
            for el in result:
                # pprint.pprint(el)
                if isinstance(el, SceneLineItemBlock):
                    if el.item.value is None:
                        continue

                    for point in el.item.value.points:
                        # logging.debug(f"Original Coordinates: {point.x}, {point.y}")

                        x = ((point.x + (RM_LETTER_WIDTH / 2)) / RM_LETTER_WIDTH) * RM_LETTER_WIDTH
                        y = (point.y / RM_LETTER_HEIGHT) * RM_LETTER_HEIGHT

                        # Have to adjust for some reason...
                        x = x + 10
                        y = y + 25

                        # logging.debug(f"Adjusted Coordinates: {x}, {y}")

                        points.append(XYCoordinate(x=x, y=y))
                # else:
                #     logging.debug(f"Discarding block - {type(el).__name__}")

        # logging.debug(points)
        output[page] = points

    return output
