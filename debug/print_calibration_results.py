import os
import shutil

from rmscene import read_blocks, SceneLineItemBlock

from remarkable import Remarkable

if os.path.exists("tmp/"):
    shutil.rmtree("tmp/")
# #
rm = Remarkable()
# # print(rm.stat("/Google Tasks marked.pdf"))
# rm.get("/calibration.pdf")
shutil.unpack_archive("calibration.pdf.zip", "tmp/")

for file in os.listdir("tmp/"):
    if os.path.isdir(os.path.join("tmp/", file)):
        directory = os.path.join("tmp/", file)
        rm_file = os.listdir(directory)[0]
        rm_file = os.path.join(directory, rm_file)
        print(rm_file)

points = []
with open(rm_file, 'rb') as f:
    result = read_blocks(f)
    for el in result:
        if isinstance(el, SceneLineItemBlock):
            if el.item.value is None:
                continue
            # print(el.item.value.points)
            min_x = 99999
            max_x = -99999
            min_y = 99999
            max_y = -99999

            for point in el.item.value.points:
                if point.x < min_x:
                    min_x = point.x
                if point.x > max_x:
                    max_x = point.x
                if point.y < min_y:
                    min_y = point.y
                if point.y > max_y:
                    max_y = point.y

            print((min_x + max_x) / 2, (min_y + max_y) / 2)
            points.append(((min_x + max_x) / 2, (min_y + max_y) / 2))

an_inch = abs(points[3][0]) + abs(points[5][0])

print(an_inch)