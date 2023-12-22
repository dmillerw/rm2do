import datetime
import math
from typing import List

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from util.classes import TaskData, GoogleTask, XYCoordinate, TaskCoordinates
from util.constants import RM_LETTER_WIDTH, RM_LETTER_HEIGHT
from util.func import get_output_file


def create_pdf(tasks: List[GoogleTask], file: str = "Google Tasks.pdf") -> TaskData:
    task_data: TaskData = TaskData(pages={})

    max_pages = math.ceil(len(tasks) / 20)

    # canvas = Canvas(get_output_file(file), pagesize=LETTER)
    canvas = Canvas(file, pagesize=LETTER)

    if len(tasks) == 0:
        canvas.drawString(inch / 2, LETTER[1] - (inch / 2), f"Page: 1/1")
        canvas.drawRightString(LETTER[0] - inch / 2, LETTER[1] - (inch / 2),
                               f"Generated On: {datetime.datetime.now()}")
        canvas.drawCentredString(LETTER[0] / 2, LETTER[1] / 2, "No Tasks")
    else:
        y_start = (inch / 2)

        for index, t in enumerate(tasks):
            draw_index = index % 20
            page = math.ceil((index / 20) + 0.01)

            if draw_index == 0:
                if index != 0:
                    canvas.showPage()
                canvas.drawString(inch / 2, LETTER[1] - (inch / 2), f"Page: {page}/{max_pages}")
                canvas.drawRightString(LETTER[0] - inch / 2, LETTER[1] - (inch / 2),
                                       f"Generated On: {datetime.datetime.now()}")

            x_offset = inch
            y_offset = (LETTER[1] - y_start - (inch / 2) - (draw_index * (inch / 2)))
            spacing = inch * .125
            text_spacing = inch * .25

            path = canvas.beginPath()
            path.moveTo(x_offset, y_offset)
            path.lineTo(x_offset, y_offset + spacing)
            path.lineTo(x_offset + spacing, y_offset + spacing)
            path.lineTo(x_offset + spacing, y_offset)
            path.lineTo(x_offset, y_offset)
            canvas.drawPath(path)

            # if t in complete:
            #     path = canvas.beginPath()
            #     path.moveTo(x_offset, y_offset)
            #     path.lineTo(x_offset + spacing, y_offset + spacing)
            #     path.moveTo(x_offset + spacing, y_offset)
            #     path.lineTo(x_offset, y_offset + spacing)
            #     canvas.drawPath(path)

            # string = ("↳ " if t.parent != "" else "") + t.title
            string = t.title
            canvas.drawString(x_offset + text_spacing, y_offset, string)

            start_x = (x_offset / LETTER[0]) * RM_LETTER_WIDTH
            start_y = ((LETTER[1] - y_offset) / LETTER[1]) * RM_LETTER_HEIGHT
            end_x = ((x_offset + spacing) / LETTER[0]) * RM_LETTER_WIDTH
            end_y = ((LETTER[1] - (y_offset - spacing)) / LETTER[1]) * RM_LETTER_HEIGHT

            start = XYCoordinate(x=start_x, y=start_y)
            end = XYCoordinate(x=end_x, y=end_y)

            obj = TaskCoordinates(id=t.id, start=start, end=end)

            if page not in task_data.pages:
                task_data.pages[page] = []
            task_data.pages[page].append(obj)

    canvas.save()

    return task_data
