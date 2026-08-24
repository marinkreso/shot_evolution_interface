from enum import Enum
from PIL import Image, ImageDraw
from typing import List, Optional, Tuple
from pdf_generator.services.constants import CURDIRPATH
from pdf_generator.visuals.utils import (
    generate_arrow,
    generate_barchart,
    generate_scatter_plot,
    get_barchart,
    get_font,
    generate_piechart,
    get_piechart,
    get_piechart_new
)
from pdf_generator.models.enums import (
    Fonts,
    Color,
    CourtSide,
    ReturnDirection,
    ServeDirection,
    Offset,
    ShotType,
    SurfaceCode,
)

ASSETS_PATH = CURDIRPATH / "visuals/assets/"
ENABLE_SURFACES = True


class ColorPreset(Enum):
    RED = ("#ff0000", "#4dac26")
    ORANGE = ("#f79646", "#008837")
    YELLOW = ("#ffff00", "#cccc00")
    WHITE = ("#f2f2f2", "#bfbfbf")
    RALLY_ENDING = ("#32cd32", "#008837", "#f79646")
    NEW_RALLY_ENDING = ("#ff6c00", "#00ff6c", "#005725")


def template_a(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    surface: SurfaceCode,
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_a/"
    # Arrows
    ARROWS_Y_OFFSET: int = 35
    ARROWS_X_OFFSETS: List[int] = (165, 220, 278, 330, 380, 433)
    ARROWS_ROTATION_ANGLES: List[int] = (332, 343, 354, 6, 17, 28)
    # Percentages
    PERCENTAGES_Y_OFFSET = 190
    PERCENTAGES_X_OFFSETS = (165, 235, 300, 368, 435, 500)
    # Totals
    TOTALS_Y_OFFSET = 220
    TOTALS_X_OFFSETS = (161, 232, 298, 368, 435, 502)
    # Pie charts
    PIES_Y_OFFSET = 80  # small offset because of pie chart transparent padding
    PIES_X_OFFSET = -175
    PIES_GAP_SIZE = 75
    PIES_X_OFFSETS = [i * PIES_GAP_SIZE + PIES_X_OFFSET for i in range(6)]
    # Fonts
    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 23)
    SEGO = get_font(Fonts.SEGO_UI, 23)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    GREEN = Color(red=0, green=136, blue=55)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = Image.open(f"{TEMPLATE_ASSETS_PATH}/court.jpg")

    # Drawing the arrows
    for name, x_offset, percent, angle in zip(
        range(1, 7), ARROWS_X_OFFSETS, arrows_widths, ARROWS_ROTATION_ANGLES
    ):
        if not percent:
            continue

        arrow = generate_arrow(
            path=f"{TEMPLATE_ASSETS_PATH}/{name}.png",
            width_ratio=percent,
            angle=angle,
        )
        arrow_x_offset = x_offset + arrow.relative_offset.x
        arrow_y_offset = ARROWS_Y_OFFSET + arrow.relative_offset.y
        offset = (arrow_x_offset, arrow_y_offset)
        # Combining images
        court.paste(arrow.image, offset, arrow.image)

    # Writing blue box values
    draw = ImageDraw.Draw(court)
    for percent, x_offset in zip(arrows_numbers, PERCENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PERCENTAGES_Y_OFFSET),
            percent,
            font=SEGO_BOLD,
            fill=YELLOW,
            anchor="ms",
        )

    # Writing totals
    if numbers and pies_percentages:
        for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
            offset = (x_offset, TOTALS_Y_OFFSET)
            draw.text(
                offset,
                f"{number}",
                font=SEGO,
                fill=YELLOW,
                anchor="ms",
            )

    # Text top and mid court
    draw.text(
        (325, 20),
        f"{player_name} {serve_no} serve",
        font=SEGO,
        fill=YELLOW,
        anchor="ms",
    )
    if not pies_percentages:
        draw.text(
            (320, 220),
            "MPH",
            font=SEGO,
            fill=YELLOW,
            anchor="ms",
        )

    draw.text(
        (320, 260 if pies_percentages else 320),
        f"{sum(numbers)} total serves IN {player_name}",
        font=SEGO,
        fill=YELLOW,
        anchor="ms",
    )

    # Pie charts
    if pies_percentages:
        # Legend selection & placement
        if preset == ColorPreset.RED:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/red_legend.png")
            court.paste(legend, (510, 0), legend)

        elif preset == ColorPreset.ORANGE:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/orange_legend.png")
            court.paste(legend, (525, 0), legend)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = generate_piechart(
                percentages=[100 - percent, percent],
                colors=[*preset.value],
                radius=0.175,
            )
            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            # Pie chart percentage
            draw.text(
                (x_offset + 330, PIES_Y_OFFSET + 295),
                f"{percent}%" if percent != -1 else "",
                font=SEGO_BOLD,
                fill=GREEN,
                anchor="ms",
            )
    draw.text(
        (340, 460),
        f"{opponent_name} returning",
        font=SEGO,
        fill=WHITE,
        anchor="ms",
    )

    # court.save("visual.jpg")  # 275ms, 37KB
    # court.save("visual95.jpg", quality=95)  # 280ms, 78KB
    # court.save("visual.png")  # 310 ms, 166KB
    # court.save("visualcom1.png", compress_level=1)  # 300ms, 184KB
    # court.save("visualcom9.png", compress_level=9)  # 425ms, 161K
    return court


def template_b(
    player_name: str,
    return_percentages: List[int],
    return_numbers: List[int],
    pies_percentages: List[int],
    court_side: CourtSide,
    surface: SurfaceCode,
    *,
    serve_no: Optional[str] = "1st",
    serve_direction: Optional[ServeDirection] = None,
    return_direction: Optional[ReturnDirection] = None,
    shot_type: Optional[ShotType] = None,
    is_left_handed: Optional[bool] = None,
    gd: Optional[bool] = None,
) -> Image:
    # Rally ending direction
    if shot_type:
        top_left = [(145, 225, 295), (348, 13, 33)]  # Deuce
        top_right = [(225, 300, 380), (328, 345, 10)]  # Ad

        if is_left_handed and shot_type == ShotType.BH:
            court_side = CourtSide.DEUCE

        arrows_data = top_left if court_side == CourtSide.DEUCE else top_right
        is_left = True if arrows_data == top_left else False

        cross_l = (4, 348, (180, 30))
        cross_r = (5, 13, (35, 25))
        line_l = (8, 350, (280, 25))
        line_r = (9, 13, (15, 20))
        return_arrow = {
            ReturnDirection.CROSS: cross_l if is_left else cross_r,
            ReturnDirection.LINE: line_r if is_left else line_l,
        }

    # Shot after return location
    elif return_direction:
        arrows_dict = {
            CourtSide.DEUCE: {
                ReturnDirection.CROSS: [(145, 225, 295), (348, 13, 33)],
                ReturnDirection.MIDDLE: [(170, 260, 350), (335, 360, 22)],
                ReturnDirection.LINE: [(205, 280, 365), (325, 345, 10)],
            },
            CourtSide.AD: {
                ReturnDirection.CROSS: [(225, 300, 380), (328, 345, 10)],
                ReturnDirection.MIDDLE: [(180, 260, 350), (340, 360, 25)],
                ReturnDirection.LINE: [(155, 235, 315), (353, 15, 37)],
            },
        }
        return_arrow = {
            CourtSide.DEUCE: {
                ReturnDirection.CROSS: (4, 348, (180, 30)),
                ReturnDirection.MIDDLE: (6, 345, (220, 20)),
                ReturnDirection.LINE: (8, 350, (280, 25)),
            },
            CourtSide.AD: {
                ReturnDirection.CROSS: (5, 13, (35, 25)),
                ReturnDirection.MIDDLE: (7, 13, (20, 20)),
                ReturnDirection.LINE: (9, 13, (15, 20)),
            },
        }
        arrows_data = arrows_dict[court_side][return_direction]

    # Return location
    else:
        arrows_dict = {
            CourtSide.DEUCE: {
                ServeDirection.WIDE: [(125, 205, 275), (350, 15, 37)],
                ServeDirection.BODY: [(150, 240, 320), (340, 7, 30)],
                ServeDirection.T: [(170, 260, 350), (335, 360, 25)],
            },
            CourtSide.AD: {
                ServeDirection.WIDE: [(240, 315, 410), (325, 345, 10)],
                ServeDirection.BODY: [(205, 285, 375), (330, 353, 20)],
                ServeDirection.T: [(170, 260, 350), (335, 360, 25)],
            },
        }
        arrows_data = arrows_dict[court_side][serve_direction]

    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_b/"

    ARROWS_Y_OFFSET = 10
    ARROWS_X_OFFSETS = arrows_data[0]
    ARROWS_ROTATION_ANGLES = arrows_data[1]

    PERCENTAGES_Y_OFFSET = 335
    PERCENTAGES_X_OFFSETS = (145, 310, 475)

    TOTALS_Y_OFFSET = 360
    TOTALS_X_OFFSETS = (145, 310, 475)

    PIES_Y_OFFSET = 155
    PIES_X_OFFSET = -180
    PIES_GAP_SIZE = 165
    PIES_X_OFFSETS = [i * PIES_GAP_SIZE + PIES_X_OFFSET for i in range(6)]

    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 32)
    SEGO_BOLD_SMALL = get_font(Fonts.SEGO_UI_BOLD, 20)
    SEGO = get_font(Fonts.SEGO_UI, 20)
    SEGO_MID = get_font(Fonts.SEGO_UI, 25)
    SEGO_TITLE = get_font(Fonts.SEGO_UI, 25)

    YELLOW = Color(red=255, green=255, blue=0)
    GREEN = Color(red=0, green=136, blue=55)

    court = Image.open(TEMPLATE_ASSETS_PATH / "court.jpg")
    draw = ImageDraw.Draw(court)

    # Draw arrows
    for name, x_offset, percent, angle in zip(
        range(1, 4), ARROWS_X_OFFSETS, return_percentages, ARROWS_ROTATION_ANGLES
    ):
        if not percent:
            continue

        arrow = generate_arrow(
            path=TEMPLATE_ASSETS_PATH / f"{name}.png",
            width_ratio=percent,
            angle=angle,
        )

        arrow_x_offset = x_offset + arrow.relative_offset.x
        arrow_y_offset = ARROWS_Y_OFFSET  # + arrow.relative_offset.y
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow.image, offset, arrow.image)

    # Draw return (white) arrow
    if return_direction:
        if shot_type:
            name, angle, offset = return_arrow[return_direction]

            swap_rackets = False
            fh_racket = ("racket_fh.png", "right")
            bh_racket = ("racket_bh.png", "left")
            if is_left_handed:
                fh_racket, bh_racket = bh_racket, fh_racket
                swap_rackets = True

            # Draw racket and shot type
            if shot_type == ShotType.FH:
                racket = Image.open(TEMPLATE_ASSETS_PATH / fh_racket[0])
                text_position = fh_racket[1]
                racket_text = "FH"
            else:
                racket = Image.open(TEMPLATE_ASSETS_PATH / bh_racket[0])
                text_position = bh_racket[1]
                racket_text = "BH"

            if is_left:
                racket_x = 10 if text_position == "right" else 20
                text_x = 85 if racket_x == 10 else 25
            else:
                racket_x = 540 if text_position == "left" else 530
                text_x = 545 if racket_x == 540 else 600

            court.paste(racket, (racket_x, 40), racket)
            draw.text(
                (text_x, 65), racket_text, font=SEGO_BOLD, fill=YELLOW, anchor="ms"
            )

        else:
            name, angle, offset = return_arrow[court_side][return_direction]

        arrow = generate_arrow(
            path=TEMPLATE_ASSETS_PATH / f"{name}.png",
            width_ratio=100,
            angle=angle,
        )
        court.paste(arrow.image, offset, arrow.image)

    # Draw header
    header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    court.paste(header, (0, 0), header)

    # Draw player name
    if gd:
        title = f"{player_name} all groundstrokes direction {shot_type.value}"
    elif shot_type:
        title = f"{player_name} rally ending direction {shot_type.value}"
    elif return_direction:
        title = f"{player_name} {serve_no} serve and serve+1"
    else:
        title = f"{player_name} returning"

    draw.text((310, 25), title, font=SEGO_TITLE, fill=YELLOW, anchor="ms")

    # Write return percentages
    for percent, x_offset in zip(return_percentages, PERCENTAGES_X_OFFSETS):
        offset = (x_offset, PERCENTAGES_Y_OFFSET)
        draw.text(
            offset,
            f"{percent}%" if percent != -1 else "",
            font=SEGO_BOLD,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return numbers
    for number, x_offset in zip(return_numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=SEGO_MID,
            fill=YELLOW,
            anchor="ms",
        )

    legend = Image.open(TEMPLATE_ASSETS_PATH / "legend.png")

    legend_position = (424, 35)
    if court_side == CourtSide.AD:
        legend_position = (0, 35)
    if shot_type:
        legend_position = (0, 35) if not is_left else (425, 35)
    court.paste(legend, legend_position, legend)

    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = generate_piechart(
            percentages=[100 - percent, percent],
            colors=[*ColorPreset.ORANGE.value],
            radius=0.150,
        )
        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 330, PIES_Y_OFFSET + 285),
            f"{percent}%" if percent != -1 else "",
            font=SEGO_BOLD_SMALL,
            fill=GREEN,
            anchor="ms",
        )

    return court


def template_c(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    court_side: CourtSide,
    serve_direction: ServeDirection,
    arrows_widths: List[int],
    numbers: List[int],
    pies_percentages: List[int],
    surface: SurfaceCode,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_c/"
    ARROWS_NAMES = range(1, 4) if court_side == CourtSide.AD else range(4, 7)
    ARROWS_Y_OFFSET: int = 190
    ARROWS_PRESETS = {
        CourtSide.AD: {
            ServeDirection.WIDE: (
                (Offset(x=300, y=220), Offset(x=360, y=210), Offset(x=410, y=230)),
                (349, 334, 323),
            ),
            ServeDirection.BODY: (
                (Offset(x=350, y=220), Offset(x=410, y=210), Offset(x=470, y=220)),
                (0, 347, 334),
            ),
            ServeDirection.T: (
                (Offset(x=405, y=220), Offset(x=465, y=210), Offset(x=525, y=220)),
                (15, 0, 345),
            ),
        },
        CourtSide.DEUCE: {
            ServeDirection.WIDE: (
                (Offset(x=560, y=220), Offset(x=610, y=210), Offset(x=660, y=215)),
                (39, 28, 17),
            ),
            ServeDirection.BODY: (
                (Offset(x=465, y=205), Offset(x=530, y=205), Offset(x=585, y=205)),
                (26, 14, 0),
            ),
            ServeDirection.T: (
                (Offset(x=420, y=220), Offset(x=485, y=210), Offset(x=545, y=220)),
                (18, 2, 347),
            ),
        },
    }
    ARROWS_OFFSETS, ARROWS_ROTATION_ANGLES = ARROWS_PRESETS[court_side][serve_direction]
    # Percentages
    PERCENTAGES_Y_OFFSET = 220
    PERCENTAGES_X_OFFSETS = (440, 565, 685)
    # Totals
    TOTALS_Y_OFFSET = 250
    TOTALS_X_OFFSETS = (440, 565, 685)
    # Pie charts
    PIES_Y_OFFSET = -150  # small offset because of pie chart transparent padding
    PIES_X_OFFSETS = [100, 230, 355]
    # Fonts
    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 35)
    SEGO = get_font(Fonts.SEGO_UI, 35)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    BLACK = Color(red=0, green=0, blue=0)

    # Opening court (background image)
    court: Image = Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")

    # Drawing the arrows
    for name, offset, percent, angle in zip(
        ARROWS_NAMES, ARROWS_OFFSETS, arrows_widths, ARROWS_ROTATION_ANGLES
    ):
        if not percent:
            continue

        arrow = generate_arrow(
            path=f"{TEMPLATE_ASSETS_PATH}/{name}.png",
            width_ratio=percent,
            angle=angle,
        )
        arrow_x_offset = offset.x + arrow.relative_offset.x
        arrow_y_offset = offset.y + arrow.relative_offset.y
        offset = (arrow_x_offset, arrow_y_offset)
        # Combining images
        court.paste(arrow.image, offset, arrow.image)

    # Writing blue box values
    draw = ImageDraw.Draw(court)
    for percent, x_offset in zip(arrows_widths, PERCENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PERCENTAGES_Y_OFFSET),
            f"{percent}%" if percent != -1 else "",
            font=SEGO_BOLD,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=SEGO,
            fill=WHITE,
            anchor="ms",
        )

    # Writing title
    draw.text(
        (560, 35),
        f"{player_name} {serve_no} serve and serve+1",
        font=SEGO,
        fill=YELLOW,
        anchor="ms",
    )

    # Pie charts
    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = generate_piechart(
            percentages=[100 - percent, percent],
            colors=[*ColorPreset.ORANGE.value],
            radius=0.25,
        )
        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 330, PIES_Y_OFFSET + 310),
            f"{percent}%" if percent != -1 else "",
            font=SEGO_BOLD,
            fill=BLACK,
            anchor="ms",
        )
        draw.text(
            (560, 691),
            f"{opponent_name} returning",
            font=SEGO,
            fill=WHITE,
            anchor="ms",
        )

    return court


def template_d(
    player_name: str,
    points_x_coordinates: List[float],
    points_y_coordinates: List[float],
    surface: SurfaceCode,
    *,
    inv: Optional[bool] = False,
) -> Image:
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_d/"

    # Plot configuration
    dimensions = (25.9, 14.5)
    xlim = (-6, 6)
    if not inv:
        court_name = "court"
        ylim = (-8, 0)
        offset = (-233, -100)
        preset = ColorPreset.YELLOW
    else:
        court_name = "court-inv"
        ylim = (0, 8)
        offset = (-200, -190)
        preset = ColorPreset.WHITE

    # Opening court (background image)
    court = Image.open(f"{TEMPLATE_ASSETS_PATH}/{court_name}.png")

    # Generating scatter plot points
    scatter = generate_scatter_plot(
        points_x_coordinates,
        points_y_coordinates,
        xlim,
        ylim,
        *preset.value,
        dimensions=dimensions,
    )

    court.paste(scatter, offset, scatter)

    return court


def template_e(
    player_name: str,
    points_x_coordinates: List[float],
    points_y_coordinates: List[float],
    surface: SurfaceCode,
    *,
    inv: Optional[bool] = False,
) -> Image:
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_e/"

    # Plot configuration
    xlim = (-8, 8)
    dimensions = (34.5, 25.58)
    if not inv:
        court_name = "court"
        ylim = (-14, 0)
        offset = (-670, -190)
    else:
        court_name = "court-inv"
        ylim = (0, 14)
        offset = (-640, -460)

    # Opening court (background image)
    court = Image.open(f"{TEMPLATE_ASSETS_PATH}/{court_name}.png")

    # Generating scatter plot points
    scatter = generate_scatter_plot(
        points_x_coordinates,
        points_y_coordinates,
        xlim,
        ylim,
        *ColorPreset.YELLOW.value,
        dimensions=dimensions,
    )

    court.paste(scatter, offset, scatter)

    return court


def template_f(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    surface: SurfaceCode,
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    clear: Optional[bool] = False,
    speed: Optional[List[int]] = None,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_f/"
    # Arrows
    ARROWS_Y_OFFSET = 700
    ARROWS_X_OFFSETS = (240, 370, 490, 630, 750, 860)
    ARROWS_ROTATION_ANGLES = (208, 197, 186, 174, 163, 152)
    # ARROWS_ROTATION_ANGLES: List[int] = (332, 343, 354, 6, 17, 28)
    # Percentages
    PRECENTAGES_Y_OFFSET = 665
    PRECENTAGES_X_OFFSETS = (305, 455, 595, 750, 885, 1035)
    # Totals
    TOTALS_Y_OFFSET = 600
    TOTALS_X_OFFSETS = (305, 455, 595, 748, 882, 1030)
    # Pie charts
    PIES_Y_OFFSET = -30  # small offset because of pie chart transparent padding
    PIES_X_OFFSETS = (-180, 30, 238, 445, 650, 857)
    # Fonts
    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 40)
    SEGO = get_font(Fonts.SEGO_UI, 40)
    SEGO_BOLD_large = get_font(Fonts.SEGO_UI_BOLD, 50)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    BLACK = Color(red=0, green=0, blue=0)
    GREEN = Color(red=67, green=151, blue=33)

    if clear:
        PIES_Y_OFFSET = 130  # small offset because of pie chart transparent padding
        PIES_X_OFFSETS = (-40, 110, 260, 410, 560, 710)

    # Opening court (background image)
    court_name = "court" if not clear else "clear-court"
    court: Image = Image.open(f"{TEMPLATE_ASSETS_PATH}/{court_name}.jpg")

    # Drawing the arrows
    for name, x_offset, percent, angle in zip(
        range(1, 7), ARROWS_X_OFFSETS, arrows_widths, ARROWS_ROTATION_ANGLES
    ):
        if not percent:
            continue

        arrow = generate_arrow(
            path=f"{TEMPLATE_ASSETS_PATH}/{name}.png",
            width_ratio=percent,
            angle=angle - 180,
            width_scaler=1,
        )
        arrow_x_offset = x_offset + arrow.relative_offset.x
        arrow_y_offset = ARROWS_Y_OFFSET + arrow.relative_offset.y
        offset = (arrow_x_offset, arrow_y_offset)
        # Combining images
        court.paste(arrow.image, offset, arrow.image)

    # Writing gray box values
    draw = ImageDraw.Draw(court)
    for percent, x_offset in zip(arrows_numbers, PRECENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PRECENTAGES_Y_OFFSET),
            percent,
            font=SEGO_BOLD,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    if numbers:
        for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
            offset = (x_offset, TOTALS_Y_OFFSET)
            draw.text(
                offset,
                f"{number}",
                font=SEGO,
                fill=WHITE,
                anchor="ms",
            )

    if speed:
        for speed_value, x_offset in zip(speed, PIES_X_OFFSETS):
            offset = (x_offset + 325, PIES_Y_OFFSET + 315)
            speed_value = str(speed_value) if speed_value else ""
            draw.text(
                offset,
                speed_value,
                font=SEGO_BOLD_large,
                fill=WHITE,
                anchor="ms",
            )

    # Text top and bottom court
    draw.text(
        (650, 38),
        f"{player_name} returning",
        font=SEGO,
        fill=YELLOW,
        anchor="ms",
    )

    if not clear:
        draw.text(
            (650, 93),
            (
                ("Return Speed" if speed else "Return IN %")
                if preset == ColorPreset.RED
                else "Points WON %"
            ),
            font=SEGO,
            fill=BLACK,
            anchor="ms",
        )
    # Writing total serves
    elif numbers:
        draw.text(
            (650, 540),
            f"{sum(numbers)} total serves IN {opponent_name}",
            font=SEGO,
            fill=WHITE,
            anchor="ms",
        )

    if not pies_percentages:
        draw.text(
            (650, 600 - (180 if speed else 0)),
            "MPH",
            font=SEGO_BOLD_large if speed else SEGO,
            fill=WHITE,
            anchor="ms",
        )
    draw.text(
        (650, 1072),
        f"{opponent_name} {serve_no} serve",
        font=SEGO,
        fill=WHITE,
        anchor="ms",
    )

    # Pie charts
    if pies_percentages:
        # legend selection & placement
        if preset == ColorPreset.RED:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/red_legend.png")
            court.paste(legend, (1032, 51), legend)

        elif preset == ColorPreset.ORANGE:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/orange_legend.png")
            court.paste(legend, (981, 51), legend)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = generate_piechart(
                percentages=[100 - percent, percent],
                colors=[*preset.value],
                radius=0.45 if not clear else 0.3,
                border_width=1.5,
            )
            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            # Pie chart percentage
            draw.text(
                (x_offset + 330, PIES_Y_OFFSET + 350),
                f"{percent}%" if percent != -1 else "",
                font=SEGO_BOLD,
                fill=GREEN if clear else BLACK,
                anchor="ms",
            )
    return court


def template_g(
    player_name: str,
    pies_percentages: List[List[int]],
    shot_type: ShotType,
    is_left_handed: bool,
    surface: SurfaceCode,
) -> Image:
    YELLOW = Color(red=255, green=255, blue=0)
    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 36)
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_g/"

    court = Image.open(TEMPLATE_ASSETS_PATH / "court.jpg")
    draw = ImageDraw.Draw(court)

    # Draw pie charts
    pie_x = start_x = -60
    pie_y = -110
    for i, percentages in enumerate(pies_percentages):
        pie = generate_piechart(percentages, [*ColorPreset.RALLY_ENDING.value], 0.3)
        if i and i % 3 == 0:
            pie_x = start_x
            pie_y += 160
        court.paste(pie, (pie_x, pie_y), pie)
        pie_x += 215

    # Draw racket and shot type
    swap_rackets = False
    fh_racket = ("racket_fh.png", "right")
    bh_racket = ("racket_bh.png", "left")
    if is_left_handed:
        fh_racket, bh_racket = bh_racket, fh_racket
        swap_rackets = True

    if shot_type == ShotType.FH:
        racket = Image.open(TEMPLATE_ASSETS_PATH / fh_racket[0])
        text_position = fh_racket[1]
        racket_text = "FH"
    else:
        racket = Image.open(TEMPLATE_ASSETS_PATH / bh_racket[0])
        text_position = bh_racket[1]
        racket_text = "BH"

    if swap_rackets:
        racket_x = 10 if text_position == "right" else 835
        text_x = 110 if racket_x == 10 else 850
    else:
        racket_x = 835 if text_position == "left" else 10
        text_x = 850 if racket_x == 835 else 110

    court.paste(racket, (racket_x, 10), racket)
    draw.text((text_x, 35), racket_text, font=SEGO_BOLD, fill=YELLOW, anchor="ms")

    return court


def template_h(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    labels: List[str],
    points: List[Tuple],
    surface: SurfaceCode,
    player_no: Optional[int] = None,
):
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "template_h/"
    SEGO_BOLD = get_font(Fonts.SEGO_UI_BOLD, 25)
    SEGO = get_font(Fonts.SEGO_UI, 30)

    BLACK = Color(red=0, green=0, blue=0)

    BARS_Y_OFFSETS = (100, 150, 200, 280, 335, 385)
    # Opening court (background image)
    court: Image = Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    for point, label, y in zip(points, labels, BARS_Y_OFFSETS):
        barchart = generate_barchart(
            label,
            [point],
            ["#008837", "#F79646"],
            ["white", "black"],
            width=7,
            height=0.55,
        )
        court.paste(barchart, (200, y), barchart)

    serve_term = "Serves" if serve_no == "All" else "Serve"
    draw = ImageDraw.Draw(court)
    draw.text(
        (960, 115),
        f"{serve_no} {serve_term} Win % by server and rally length",
        font=SEGO,
        fill=BLACK,
        anchor="ms",
    )
    for player, y_offset in zip((player_name, opponent_name), (175, 360)):
        draw.multiline_text(
            (105, y_offset),
            f"{player}\nserving",
            font=SEGO_BOLD,
            fill=BLACK,
            anchor="ms",
            align="center",
        )
    for player, x_offset, color in zip(
        (player_name, opponent_name), (310, 560), ["#008837", "#F79646"]
    ):
        draw.text(
            (x_offset, 450),
            f"Win % {player}",
            font=SEGO_BOLD,
            fill=BLACK,
        )
        draw.rectangle([x_offset - 30, 455, x_offset - 10, 475], fill=color)

    return court


def template_i(
    player_name: str, pdf_buffer: bytes, left: int, top: int, right: int, bottom: int
):
    import fitz

    doc = fitz.open("pdf", pdf_buffer)
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(150 / 72, 150 / 72))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img.crop((left, top, right, bottom))


from io import BytesIO
from functools import lru_cache
import requests
from PIL import Image, ImageDraw

def serve_location_template(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    surface: SurfaceCode,
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    is_new: Optional[bool] = False,
    all_serves: Optional[bool] = False,
    serve_speed: Optional[bool] = False,
    serve_speed_values: Optional[List[int]] = None,
) -> Image:
    # === New: remote assets base (Azure Blob Storage) ===
    TEMPLATE_ASSETS_BASE_URL = (
        "https://operationslakedb.blob.core.windows.net/"
        "shot-evolution-report/pdf_generator/serve_location_template"
    )

    @lru_cache(maxsize=256)
    def open_image(rel_path: str) -> Image.Image:
        """
        Fetch an image from Azure Blob Storage and return a PIL Image with alpha preserved.
        Uses a small LRU cache to avoid duplicate network fetches within one render.
        """
        try:
            url = f"{TEMPLATE_ASSETS_BASE_URL}/{rel_path.lstrip('/')}"
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return Image.open(BytesIO(resp.content)).convert("RGBA")
        except:
            print('open_image error', rel_path)
            raise Exception

    # Template constants
    # (unchanged – only the asset loading is different)
    PERCENTAGES_Y_OFFSET = 430
    PERCENTAGES_X_OFFSETS = (545, 715, 875, 1050, 1205, 1375)

    TOTALS_Y_OFFSET = 505
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS

    SPEEDS_Y_OFFSET = 790
    SPEEDS_X_OFFSETS = (470, 670, 870, 1070, 1270, 1470)

    PIES_Y_OFFSET = 630  # small offset because of pie chart transparent padding
    PIES_X_OFFSET = 200
    PIES_GAP_SIZE = 210
    PIES_X_OFFSETS = [i * PIES_GAP_SIZE + PIES_X_OFFSET for i in range(6)]

    DIN_BIG = get_font(Fonts.DIN, 70)
    DIN = get_font(Fonts.DIN, 65)
    DIN_SMALL = get_font(Fonts.DIN, 55)

    YELLOW = Color(red=238, green=226, blue=11)
    GREEN = Color(red=26, green=230, blue=103)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image) – now from Azure
    court: Image = (
        open_image(f"court/{surface.value}.png") if ENABLE_SURFACES
        else open_image("court.png")
    )
    print('OPENED COURT')

    # Drawing the arrows (from Azure)
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue
        arrow_percent = ((percent // 5) + 1) * 5 if percent < 100 else 100
        arrow = open_image(f"{name}/{arrow_percent}.png")
        court.paste(arrow, (0, 0), arrow)

    # Header (from Azure)
    header = open_image("header-serve-speed.png" if is_new and serve_speed else "header.png")
    court.paste(header, (0, 0), header)
        
    # Writing blue box values
    draw = ImageDraw.Draw(court)

    # Writing totals
    if numbers:
        if not (serve_speed and not is_new):
            for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
                draw.text((x_offset, TOTALS_Y_OFFSET), f"{number}", font=DIN, fill=YELLOW, anchor="ms")

        top_annotation_text = (
            f"{serve_no} SERVES IN" if serve_speed else f"ALL {serve_no} SERVES"
        )
        bottom_annotation_text = f"{serve_no} SERVES IN" if serve_speed else "IN %"
        if is_new:
            draw.text((260, PERCENTAGES_Y_OFFSET - 60), top_annotation_text.upper(), font=DIN_SMALL, fill=YELLOW, anchor="ms")
            draw.text((250, PERCENTAGES_Y_OFFSET), "DIRECTION", font=DIN_SMALL, fill=YELLOW, anchor="ms")
            draw.text((220, SPEEDS_Y_OFFSET - 30), bottom_annotation_text.upper(), font=DIN_SMALL, fill=YELLOW, anchor="ms")

    if serve_speed and not is_new:
        draw.text((960, 500), "MPH", font=DIN, fill=YELLOW, anchor="ms")

    if serve_speed and serve_speed_values and is_new:
        for speed_value, x_offset in zip(serve_speed_values, SPEEDS_X_OFFSETS):
            draw.text((x_offset, SPEEDS_Y_OFFSET), f"{speed_value}", font=DIN, fill=YELLOW, anchor="ms")
        draw.text((230, SPEEDS_Y_OFFSET + 30), "SPEED (MPH)", font=DIN_SMALL, fill=YELLOW, anchor="ms")

    draw.text(
        (960, 640 if serve_speed and not is_new else 650),
        f"{sum(numbers)} total serves {'IN '  if not all_serves else ''}{player_name}",
        font=DIN if pies_percentages else DIN_BIG,
        fill=YELLOW,
        anchor="ms",
    )
    print('BEFORE PIE')
    # Pie charts (legends/annotations now from Azure)
    if pies_percentages:
        annotations = None
        if preset == ColorPreset.RED:
            legend = open_image("red_legend.png")
            court.paste(legend, (0, 0), legend)
            if not is_new:
                annotations = open_image("an-in.png")
        elif preset == ColorPreset.ORANGE:
            legend = open_image("orange_legend.png")
            court.paste(legend, (0, 0), legend)
            annotations = open_image("an-won.png")

        if annotations:
            court.paste(annotations, (0, 0), annotations)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart(
                percentages=[100 - percent, percent],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            new_width = 480
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            pie = pie.resize((new_width, new_height))
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)
            draw.text((x_offset + 250, PIES_Y_OFFSET + 275), f"{percent}%" if percent != -1 else "", font=DIN_BIG, fill=YELLOW, anchor="ms")

    for percent, x_offset in zip(arrows_numbers, PERCENTAGES_X_OFFSETS):
        draw.text((x_offset, PERCENTAGES_Y_OFFSET), percent, font=DIN_BIG, fill=YELLOW, anchor="ms")
    print('TOP AND MID COURT')
    # Text top and mid court
    draw.text(
        (960, 55),
        (
            f"{player_name} {serve_no} serve".upper()
            if not is_new
            else f"{player_name} {top_annotation_text}".upper()
        ),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.text((960, 1000), f"{opponent_name} returning".upper(), font=DIN, fill=WHITE, anchor="ms")

    return court


def serve_location_template_aces2(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    surface: SurfaceCode,
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    is_new: Optional[bool] = False,
    all_serves: Optional[bool] = False,
    serve_speed: Optional[bool] = False,
    serve_speed_values: Optional[List[int]] = None,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "serve_location_template/"
    # Percentages
    PERCENTAGES_Y_OFFSET = 430
    PERCENTAGES_X_OFFSETS = (545, 715, 875, 1050, 1205, 1375)
    # Totals
    TOTALS_Y_OFFSET = 505
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS
    # SPEEDS
    SPEEDS_Y_OFFSET = 790
    SPEEDS_X_OFFSETS = (470, 670, 870, 1070, 1270, 1470)
    # Pie charts
    PIES_Y_OFFSET = 630  # small offset because of pie chart transparent padding
    PIES_X_OFFSET = 200
    PIES_GAP_SIZE = 210
    PIES_X_OFFSETS = [i * PIES_GAP_SIZE + PIES_X_OFFSET for i in range(6)]
    # Fonts
    DIN_BIG = get_font(Fonts.DIN, 70)
    DIN = get_font(Fonts.DIN, 65)
    DIN_SMALL = get_font(Fonts.DIN, 55)
    # Colors
    YELLOW = Color(red=238, green=226, blue=11)
    GREEN = Color(red=26, green=230, blue=103)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )

    # Drawing the arrows
    
    for name, percent in zip(range(1, 7), [50]*6):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)
        # Combining images
        court.paste(arrow, offset, arrow)

    header = Image.open(
        TEMPLATE_ASSETS_PATH
        / ("header-serve-speed.png" if is_new and serve_speed else "header.png")
    )
    court.paste(header, (0, 0), header)

    # Writing blue box values
    draw = ImageDraw.Draw(court)

    # Writing totals
    if numbers:
        if not (serve_speed and not is_new):
            for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
                offset = (x_offset, TOTALS_Y_OFFSET)
                draw.text(
                    offset,
                    f"{number}",
                    font=DIN,
                    fill=YELLOW,
                    anchor="ms",
                )

        top_annotation_text = (
            f"{serve_no} SERVES IN" if serve_speed else f"ALL {serve_no} SERVES"
        )
        bottom_annotation_text = f"{serve_no} SERVES IN" if serve_speed else "IN %"
        if is_new:
            draw.text(
                (260, PERCENTAGES_Y_OFFSET - 60),
                top_annotation_text.upper(),
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )
            draw.text(
                (250, PERCENTAGES_Y_OFFSET),
                "DIRECTION",
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )

            draw.text(
                (220, SPEEDS_Y_OFFSET - 30),
                bottom_annotation_text.upper(),
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )

    if serve_speed and not is_new:
        draw.text(
            (960, 500),
            "ACES %",
            font=DIN,
            fill=YELLOW,
            anchor="ms",
        )

    if serve_speed and serve_speed_values and is_new:
        for speed_value, x_offset in zip(serve_speed_values, SPEEDS_X_OFFSETS):
            offset = (x_offset, SPEEDS_Y_OFFSET)
            draw.text(
                offset,
                f"{speed_value}",
                font=DIN,
                fill=YELLOW,
                anchor="ms",
            )

        draw.text(
            (230, SPEEDS_Y_OFFSET + 30),
            "ACES",
            font=DIN_SMALL,
            fill=YELLOW,
            anchor="ms",
        )

    draw.text(
        (960, 640 if serve_speed and not is_new else 650),
        f"{sum(numbers)} total serves {player_name}",
        font=DIN if pies_percentages else DIN_BIG,
        fill=YELLOW,
        anchor="ms",
    )

    

    for percent, x_offset in zip(arrows_numbers, PERCENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PERCENTAGES_Y_OFFSET),
            percent,
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Text top and mid court
    draw.text(
        (960, 55),
        (
            f"{player_name} {serve_no} serve".upper()
            if not is_new
            else f"{player_name} {top_annotation_text}".upper()
        ),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.text(
        (960, 1000),
        f"{opponent_name} returning".upper(),
        font=DIN,
        fill=WHITE,
        anchor="ms",
    )

    return court


def serve_location_template_new(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    surface: SurfaceCode,
    *,
    numbers: Optional[List[int]] = None,
    full_numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    is_new: Optional[bool] = False,
    all_serves: Optional[bool] = False,
    serve_speed: Optional[bool] = False,
    serve_speed_values: Optional[List[int]] = None,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "serve_location_template/"
    # Percentages
    PERCENTAGES_Y_OFFSET = 430
    PERCENTAGES_X_OFFSETS = (545, 715, 875, 1050, 1205, 1375)
    # Totals
    TOTALS_Y_OFFSET = 505
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS
    # SPEEDS
    SPEEDS_Y_OFFSET = 790
    SPEEDS_X_OFFSETS = (470, 670, 870, 1070, 1270, 1470)
    # Pie charts
    PIES_Y_OFFSET = 630  # small offset because of pie chart transparent padding
    PIES_X_OFFSET = 200
    PIES_GAP_SIZE = 210
    PIES_X_OFFSETS = [i * PIES_GAP_SIZE + PIES_X_OFFSET for i in range(6)]
    # Fonts
    DIN_BIG = get_font(Fonts.DIN, 70)
    DIN = get_font(Fonts.DIN, 65)
    DIN_SMALL = get_font(Fonts.DIN, 55)
    # Colors
    YELLOW = Color(red=238, green=226, blue=11)
    GREEN = Color(red=26, green=230, blue=103)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )

    # Drawing the arrows
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)
        # Combining images
        court.paste(arrow, offset, arrow)

    header = Image.open(
        TEMPLATE_ASSETS_PATH
        / ("header-serve-speed.png" if is_new and serve_speed else "header.png")
    )
    court.paste(header, (0, 0), header)

    # Writing blue box values
    draw = ImageDraw.Draw(court)

    # Writing totals
    
    if numbers:
        if not (serve_speed and not is_new):
            counter = 0
            for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
                offset = (x_offset, TOTALS_Y_OFFSET)
                if preset == ColorPreset.RED:
                   
                    
                    
                    draw.text(
                        offset,
                        f"{number}/{full_numbers[counter]}",
                        font=DIN,
                        fill=YELLOW,
                        anchor="ms",
                    )

                    
                    counter = counter + 1
                else:
                    draw.text(
                        offset,
                        f"{full_numbers[counter]}/{number}",
                        font=DIN,
                        fill=YELLOW,
                        anchor="ms",
                    )

                    
                    counter = counter + 1
                   
                    


        top_annotation_text = (
            f"{serve_no} SERVES IN" if serve_speed else f"ALL {serve_no} SERVES"
        )
        bottom_annotation_text = f"{serve_no} SERVES IN" if serve_speed else "IN %"
        if is_new:
            draw.text(
                (260, PERCENTAGES_Y_OFFSET - 60),
                top_annotation_text.upper(),
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )
            draw.text(
                (250, PERCENTAGES_Y_OFFSET),
                "DIRECTION",
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )

            draw.text(
                (220, SPEEDS_Y_OFFSET - 30),
                bottom_annotation_text.upper(),
                font=DIN_SMALL,
                fill=YELLOW,
                anchor="ms",
            )

    if serve_speed and not is_new:
        draw.text(
            (960, 500),
            "MPH",
            font=DIN,
            fill=YELLOW,
            anchor="ms",
        )

    if serve_speed and serve_speed_values and is_new:
        for speed_value, x_offset in zip(serve_speed_values, SPEEDS_X_OFFSETS):
            offset = (x_offset, SPEEDS_Y_OFFSET)
            draw.text(
                offset,
                f"{speed_value}",
                font=DIN,
                fill=YELLOW,
                anchor="ms",
            )

        draw.text(
            (230, SPEEDS_Y_OFFSET + 30),
            "SPEED (MPH)",
            font=DIN_SMALL,
            fill=YELLOW,
            anchor="ms",
        )

    draw.text(
        (960, 640 if serve_speed and not is_new else 650),
        f"{sum(numbers)} total serves {'IN '  if not all_serves else ''}{player_name}",
        font=DIN if pies_percentages else DIN_BIG,
        fill=YELLOW,
        anchor="ms",
    )

    # Pie charts
    if pies_percentages:
        annotations = None
        # Legend selection & placement
        if preset == ColorPreset.RED:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/red_legend.png")
            court.paste(legend, (0, 0), legend)

            # TODO: new annotations required
            if not is_new:
                annotations = Image.open(f"{TEMPLATE_ASSETS_PATH}/an-in.png")

        elif preset == ColorPreset.ORANGE:
            legend = Image.open(f"{TEMPLATE_ASSETS_PATH}/orange_legend.png")
            court.paste(legend, (0, 0), legend)
            annotations = Image.open(f"{TEMPLATE_ASSETS_PATH}/an-won.png")

        if annotations:
            court.paste(annotations, (0, 0), annotations)
        counter = 0
        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart_new(
                percentages=[100 - percent, percent],
                number=numbers[counter],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            counter = counter+1
            new_width = 480
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            pie = pie.resize((new_width, new_height))

            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            # Pie chart percentage
            draw.text(
                (x_offset + 250, PIES_Y_OFFSET + 275),
                f"{percent}%" if percent != -1 else "",
                font=DIN_BIG,
                fill=YELLOW,
                anchor="ms",
            )

    for percent, x_offset in zip(arrows_numbers, PERCENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PERCENTAGES_Y_OFFSET),
            percent,
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Text top and mid court
    draw.text(
        (960, 55),
        (
            f"{player_name} {serve_no} serve".upper()
            if not is_new
            else f"{player_name} {top_annotation_text}".upper()
        ),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.text(
        (960, 1000),
        f"{opponent_name} returning".upper(),
        font=DIN,
        fill=WHITE,
        anchor="ms",
    )

    return court

def return_location_template(
    player_name: str,
    return_percentages: List[int],
    return_numbers: List[int],
    pies_percentages: List[int],
    court_side: CourtSide,
    surface: SurfaceCode,
    *,
    serve_no: Optional[str] = "1st",
    serve_direction: Optional[ServeDirection] = None,
    return_direction: Optional[ReturnDirection] = None,
    shot_type: Optional[ShotType] = None,
    is_left_handed: Optional[bool] = None,
    gd: Optional[bool] = None,
):
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "return_location_template/"
    PERCENTAGES_Y_OFFSET = 760
    PERCENTAGES_X_OFFSETS = (550, 970, 1370)

    TOTALS_Y_OFFSET = 820
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS

    PIES_Y_OFFSET = 780
    PIES_X_OFFSETS = [300, 725, 1120]

    DIN_BIG = get_font(Fonts.DIN, 85)
    DIN_MID = get_font(Fonts.DIN, 85)
    DIN_SMALL = get_font(Fonts.DIN, 70)
    DIN_TITLE = get_font(Fonts.DIN, 55)

    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    starting_point = None
    return_arrow_name = None

    # Return direction
    if serve_direction:
        if court_side == CourtSide.DEUCE and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "left"
        elif court_side == CourtSide.AD and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "right"
        else:
            starting_point = "center"

    # Rally ending direction
    elif shot_type:
        if is_left_handed and shot_type == ShotType.BH:
            court_side = CourtSide.DEUCE

        if court_side == court_side.AD:
            starting_point = "right"
        else:
            starting_point = "left"

        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            return_arrow_name = "right"
        else:
            return_arrow_name = "left"

        if return_direction == ReturnDirection.CROSS:
            return_arrow_name += "_3"
        else:
            return_arrow_name += "_1"

    # Serve+1
    else:
        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            starting_point = "left"
        elif (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.LINE
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.CROSS):
            starting_point = "right"
        else:
            starting_point = "center"

        return_arrow_name = f"{'right' if court_side == court_side.DEUCE else 'left'}_{3 if return_direction == ReturnDirection.CROSS else 2 if return_direction == ReturnDirection.MIDDLE else 1}"

    if return_arrow_name:
        arrow = Image.open(f"{TEMPLATE_ASSETS_PATH}/return/{return_arrow_name}.png")
        court.paste(arrow, (0, 0), arrow)

    for name, percent in zip(range(1, 4), return_percentages):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{starting_point}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)

    header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    court.paste(header, (0, 0), header)
    if starting_point == "right":
        legend_name = "left_legend"
    elif starting_point == "left":
        legend_name = "right_legend"
    else:
        if court_side == CourtSide.DEUCE:
            legend_name = "right_legend"
        else:
            legend_name = "left_legend"

    legend = Image.open(TEMPLATE_ASSETS_PATH / f"{legend_name}.png")
    court.paste(legend, (0, 0), legend)

    # Racket legend
    if shot_type:
        racket_orientation = (
            "left"
            if (shot_type.FH and not is_left_handed)
            or (shot_type.BH and is_left_handed)
            else "right"
        )
        racket_name = f"{starting_point}_{racket_orientation}_racket"

        racket = Image.open(TEMPLATE_ASSETS_PATH / f"{racket_name}.png")
        court.paste(racket, (0, 0), racket)

    draw = ImageDraw.Draw(court)
    # Draw player name
    if gd:
        title = f"{player_name} all groundstrokes direction {shot_type.value}"
    elif shot_type:
        title = f"{player_name} rally ending direction {shot_type.value}"
    elif return_direction:
        title = f"{player_name} {serve_no} serve and serve+1"
    else:
        title = f"{player_name} returning"

    draw.text((960, 50), title.upper(), font=DIN_TITLE, fill=YELLOW, anchor="ms")

    # Racket shot type
    if shot_type:
        racket_shot_type_offset = {
            "left_right": 150,
            "left_left": 275,
            "right_right": 1650,
            "right_left": 1785,
        }
        draw.text(
            (racket_shot_type_offset[f"{starting_point}_{racket_orientation}"], 80),
            shot_type.value,
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return percentages
    for percent, x_offset in zip(return_percentages, PERCENTAGES_X_OFFSETS):
        offset = (x_offset, PERCENTAGES_Y_OFFSET)
        draw.text(
            offset,
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return numbers
    for number, x_offset in zip(return_numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=DIN_SMALL,
            fill=WHITE,
            anchor="ms",
        )

    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = get_piechart(
            percentages=[100 - percent, percent],
        )

        # Calculate the height using aspect ratio
        new_width = 500
        width, height = pie.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        pie = pie.resize((new_width, new_height))

        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 260, PIES_Y_OFFSET + 285),
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=WHITE,
            anchor="ms",
        )

    return court

def return_plus_location_template(
    player_name: str,
    return_percentages: List[int],
    return_numbers: List[int],
    pies_percentages: List[int],
    court_side: CourtSide,
    surface: SurfaceCode,
    *,
    serve_no: Optional[str] = "1st",
    serve_direction: Optional[ServeDirection] = None,
    return_direction: Optional[ReturnDirection] = None,
    shot_type: Optional[ShotType] = None,
    is_left_handed: Optional[bool] = None,
    gd: Optional[bool] = None,
):
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "return_location_template/"
    PERCENTAGES_Y_OFFSET = 760
    PERCENTAGES_X_OFFSETS = (550, 970, 1370)

    TOTALS_Y_OFFSET = 820
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS

    PIES_Y_OFFSET = 780
    PIES_X_OFFSETS = [300, 725, 1120]

    DIN_BIG = get_font(Fonts.DIN, 85)
    DIN_MID = get_font(Fonts.DIN, 85)
    DIN_SMALL = get_font(Fonts.DIN, 70)
    DIN_TITLE = get_font(Fonts.DIN, 55)

    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    starting_point = None
    return_arrow_name = None

    # Return direction
    if serve_direction:
        if court_side == CourtSide.DEUCE and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "left"
        elif court_side == CourtSide.AD and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "right"
        else:
            starting_point = "center"

    # Rally ending direction
    elif shot_type:
        if is_left_handed and shot_type == ShotType.BH:
            court_side = CourtSide.DEUCE

        if court_side == court_side.AD:
            starting_point = "right"
        else:
            starting_point = "left"

        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            return_arrow_name = "right"
        else:
            return_arrow_name = "left"

        if return_direction == ReturnDirection.CROSS:
            return_arrow_name += "_3"
        else:
            return_arrow_name += "_1"

    # Serve+1
    else:
        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            starting_point = "left"
        elif (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.LINE
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.CROSS):
            starting_point = "right"
        else:
            starting_point = "center"

        return_arrow_name = f"{'right' if court_side == court_side.DEUCE else 'left'}_{3 if return_direction == ReturnDirection.CROSS else 2 if return_direction == ReturnDirection.MIDDLE else 1}"

    if return_arrow_name:
        arrow = Image.open(f"{TEMPLATE_ASSETS_PATH}/return/{return_arrow_name}.png")
        court.paste(arrow, (0, 0), arrow)

    for name, percent in zip(range(1, 4), return_percentages):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{starting_point}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)

    header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    court.paste(header, (0, 0), header)
    if starting_point == "right":
        legend_name = "left_legend"
    elif starting_point == "left":
        legend_name = "right_legend"
    else:
        if court_side == CourtSide.DEUCE:
            legend_name = "right_legend"
        else:
            legend_name = "left_legend"

    legend = Image.open(TEMPLATE_ASSETS_PATH / f"{legend_name}.png")
    court.paste(legend, (0, 0), legend)

    # Racket legend
    if shot_type:
        racket_orientation = (
            "left"
            if (shot_type.FH and not is_left_handed)
            or (shot_type.BH and is_left_handed)
            else "right"
        )
        racket_name = f"{starting_point}_{racket_orientation}_racket"

        racket = Image.open(TEMPLATE_ASSETS_PATH / f"{racket_name}.png")
        court.paste(racket, (0, 0), racket)

    draw = ImageDraw.Draw(court)
    # Draw player name
    if gd:
        title = f"{player_name} return+1"
    elif shot_type:
        title = f"{player_name} return+1 "
    elif return_direction:
        title = f"{player_name} return+1"
    else:
        title = f"{player_name} return+1"

    draw.text((960, 50), title.upper(), font=DIN_TITLE, fill=YELLOW, anchor="ms")

    # Racket shot type
    if shot_type:
        racket_shot_type_offset = {
            "left_right": 150,
            "left_left": 275,
            "right_right": 1650,
            "right_left": 1785,
        }
        draw.text(
            (racket_shot_type_offset[f"{starting_point}_{racket_orientation}"], 80),
            shot_type.value,
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return percentages
    for percent, x_offset in zip(return_percentages, PERCENTAGES_X_OFFSETS):
        offset = (x_offset, PERCENTAGES_Y_OFFSET)
        draw.text(
            offset,
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return numbers
    for number, x_offset in zip(return_numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=DIN_SMALL,
            fill=WHITE,
            anchor="ms",
        )

    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = get_piechart(
            percentages=[100 - percent, percent],
        )

        # Calculate the height using aspect ratio
        new_width = 500
        width, height = pie.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        pie = pie.resize((new_width, new_height))

        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 260, PIES_Y_OFFSET + 285),
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=WHITE,
            anchor="ms",
        )

    return court

def last_shot_template(
    player_name: str,
    return_percentages: List[int],
    return_numbers: List[int],
    pies_percentages: List[int],
    court_side: CourtSide,
    surface: SurfaceCode,
    *,
    serve_no: Optional[str] = "1st",
    serve_direction: Optional[ServeDirection] = None,
    return_direction: Optional[ReturnDirection] = None,
    shot_type: Optional[ShotType] = None,
    is_left_handed: Optional[bool] = None,
    gd: Optional[bool] = None,
):
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "return_location_template/"
    PERCENTAGES_Y_OFFSET = 760
    PERCENTAGES_X_OFFSETS = (550, 970, 1370)

    TOTALS_Y_OFFSET = 820
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS

    PIES_Y_OFFSET = 780
    PIES_X_OFFSETS = [300, 725, 1120]

    DIN_BIG = get_font(Fonts.DIN, 85)
    DIN_MID = get_font(Fonts.DIN, 85)
    DIN_SMALL = get_font(Fonts.DIN, 70)
    DIN_TITLE = get_font(Fonts.DIN, 55)

    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    starting_point = None
    return_arrow_name = None

    # Return direction
    if serve_direction:
        if court_side == CourtSide.DEUCE and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "left"
        elif court_side == CourtSide.AD and serve_direction in (
            ServeDirection.WIDE,
            ServeDirection.BODY,
        ):
            starting_point = "right"
        else:
            starting_point = "center"

    # Rally ending direction
    elif shot_type:
        if is_left_handed and shot_type == ShotType.BH:
            court_side = CourtSide.DEUCE

        if court_side == court_side.AD:
            starting_point = "right"
        else:
            starting_point = "left"

        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            return_arrow_name = "right"
        else:
            return_arrow_name = "left"

        if return_direction == ReturnDirection.CROSS:
            return_arrow_name += "_3"
        else:
            return_arrow_name += "_1"

    # Serve+1
    else:
        if (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.CROSS
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.LINE):
            starting_point = "left"
        elif (
            court_side == CourtSide.DEUCE and return_direction == ReturnDirection.LINE
        ) or (court_side == CourtSide.AD and return_direction == ReturnDirection.CROSS):
            starting_point = "right"
        else:
            starting_point = "center"

        return_arrow_name = f"{'right' if court_side == court_side.DEUCE else 'left'}_{3 if return_direction == ReturnDirection.CROSS else 2 if return_direction == ReturnDirection.MIDDLE else 1}"

    if return_arrow_name:
        arrow = Image.open(f"{TEMPLATE_ASSETS_PATH}/return/{return_arrow_name}.png")
        court.paste(arrow, (0, 0), arrow)

    for name, percent in zip(range(1, 4), return_percentages):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{starting_point}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)

    header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    court.paste(header, (0, 0), header)
    if starting_point == "right":
        legend_name = "left_legend"
    elif starting_point == "left":
        legend_name = "right_legend"
    else:
        if court_side == CourtSide.DEUCE:
            legend_name = "right_legend"
        else:
            legend_name = "left_legend"

    legend = Image.open(TEMPLATE_ASSETS_PATH / f"{legend_name}.png")
    court.paste(legend, (0, 0), legend)

    # Racket legend
    if shot_type:
        racket_orientation = (
            "left"
            if (shot_type.FH and not is_left_handed)
            or (shot_type.BH and is_left_handed)
            else "right"
        )
        racket_name = f"{starting_point}_{racket_orientation}_racket"

        racket = Image.open(TEMPLATE_ASSETS_PATH / f"{racket_name}.png")
        court.paste(racket, (0, 0), racket)

    draw = ImageDraw.Draw(court)
    # Draw player name
    if gd:
        title = f"{player_name} all groundstrokes direction {shot_type.value}"
    elif shot_type:
        title = f"{player_name} rally ending direction {shot_type.value}"
    elif return_direction:
        title = f"{player_name} {serve_no} serve and serve+1"
    else:
        title = f"{player_name} returning"

    draw.text((960, 50), title.upper(), font=DIN_TITLE, fill=YELLOW, anchor="ms")

    # Racket shot type
    if shot_type:
        racket_shot_type_offset = {
            "left_right": 150,
            "left_left": 275,
            "right_right": 1650,
            "right_left": 1785,
        }
        draw.text(
            (racket_shot_type_offset[f"{starting_point}_{racket_orientation}"], 80),
            shot_type.value,
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return percentages
    for percent, x_offset in zip(return_percentages, PERCENTAGES_X_OFFSETS):
        offset = (x_offset, PERCENTAGES_Y_OFFSET)
        draw.text(
            offset,
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=YELLOW,
            anchor="ms",
        )

    # Write return numbers
    for number, x_offset in zip(return_numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=DIN_SMALL,
            fill=WHITE,
            anchor="ms",
        )

    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = get_piechart(
            percentages=[100 - percent, percent],
        )

        # Calculate the height using aspect ratio
        new_width = 500
        width, height = pie.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        pie = pie.resize((new_width, new_height))

        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 260, PIES_Y_OFFSET + 285),
            f"{percent}%" if percent != -1 else "",
            font=DIN_BIG,
            fill=WHITE,
            anchor="ms",
        )

    return court
def first_shot_off_return_template(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    court_side: CourtSide,
    serve_direction: ServeDirection,
    arrows_widths: List[int],
    numbers: List[int],
    pies_percentages: List[int],
    surface: SurfaceCode,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "first_shot_off_return_template/"
    starting_point = None

    if court_side == CourtSide.DEUCE and serve_direction in (
        ServeDirection.WIDE,
        ServeDirection.BODY,
    ):
        starting_point = "right"
    elif court_side == CourtSide.AD and serve_direction in (
        ServeDirection.WIDE,
        ServeDirection.BODY,
    ):
        starting_point = "left"
    else:
        starting_point = "center"

    # Percentages
    PERCENTAGES_Y_OFFSET = 330
    PERCENTAGES_X_OFFSETS = (785, 950, 1130)
    # Totals
    TOTALS_Y_OFFSET = 385
    TOTALS_X_OFFSETS = PERCENTAGES_X_OFFSETS
    # Pie charts
    PIES_Y_OFFSET = -40  # small offset because of pie chart transparent padding
    PIES_X_OFFSETS = [540, 720, 890]
    # Fonts
    DIN = get_font(Fonts.DIN, 70)
    DIN_TITLE = get_font(Fonts.DIN, 60)
    DIN_SMALL = get_font(Fonts.DIN, 50)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    DARK_BLUE = Color(red=35, green=79, blue=102)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.jpg")
    )
    net = Image.open(TEMPLATE_ASSETS_PATH / "net.png")

    # Drawing the arrows
    for name, percent in zip((1, 2, 3), arrows_widths):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{starting_point}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = (
            0
            if not (court_side == CourtSide.AD and serve_direction == ServeDirection.T)
            else -40
        )
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)

    court.paste(net, (0, 0), net)

    header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    court.paste(header, (0, 0), header)

    # Writing blue box values
    draw = ImageDraw.Draw(court)
    for percent, x_offset in zip(arrows_widths, PERCENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PERCENTAGES_Y_OFFSET),
            f"{percent}%" if percent != -1 else "",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
        offset = (x_offset, TOTALS_Y_OFFSET)
        draw.text(
            offset,
            f"{number}",
            font=DIN_TITLE,
            fill=WHITE,
            anchor="ms",
        )

    # Writing title
    draw.text(
        (1550, 100),
        f"{player_name} {serve_no} serve and serve+1".upper(),
        font=DIN_TITLE if len(player_name) < 10 else DIN_SMALL,
        fill=YELLOW,
        anchor="ms",
    )

    # Pie charts
    for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
        pie = get_piechart(
            percentages=[100 - percent, percent],
        )
        # Placing the pie chart on the court
        # Calculate the height using aspect ratio
        new_width = 480
        width, height = pie.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
        pie = pie.resize((new_width, new_height))

        # Placing the pie chart on the court
        court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

        # Pie chart percentage
        draw.text(
            (x_offset + 245, PIES_Y_OFFSET + 260),
            f"{percent}%" if percent != -1 else "",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )

    draw.text(
        (1550, 190),
        f"{opponent_name} returning".upper(),
        font=DIN_TITLE if len(player_name) < 10 else DIN_SMALL,
        fill=WHITE,
        anchor="ms",
    )

    return court

def good_returns_template_new2(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    clear: Optional[bool] = False,
    speed: Optional[List[int]] = None,
    surface: SurfaceCode,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "good_returns_template/"
    # Percentages
    PRECENTAGES_Y_OFFSET = 565
    PRECENTAGES_X_OFFSETS = (540, 710, 890, 1040, 1220, 1380)
    # Totals
    TOTALS_Y_OFFSET = 485
    TOTALS_X_OFFSETS = PRECENTAGES_X_OFFSETS
    # Pie charts
    PIES_Y_OFFSET = 40
    PIES_X_OFFSETS = (140, 370, 600, 830, 1060, 1290)
    # Fonts
    DIN = get_font(Fonts.DIN, 50)
    DIN_MID = get_font(Fonts.DIN, 75)
    DIN_LARGE = get_font(Fonts.DIN, 60)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    DARK_BLUE = Color(red=35, green=79, blue=102)
    # GREEN = Color(red=67, green=151, blue=33)

    # if clear:
    #     PIES_Y_OFFSET = 130
    #     PIES_X_OFFSETS = (-40, 110, 260, 410, 560, 710)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    # net = Image.open(TEMPLATE_ASSETS_PATH / "net.png")
    # court.paste(net, (0, 0), net)

    # Drawing the arrows
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)
    draw = ImageDraw.Draw(court)
    # Pie charts
    if pies_percentages:
        # legend selection & placement
        header = Image.open(
            TEMPLATE_ASSETS_PATH
            / f"{'red' if preset == ColorPreset.RED else 'orange'}_header.png"
        )
        court.paste(header, (0, 0), header)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart(
                percentages=[100 - percent, percent],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            # Calculate the height using aspect ratio
            new_width = 500
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            # Placing the pie chart on the court
            pie = pie.resize((new_width, new_height))

            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            # Pie chart percentage
            draw.text(
                (x_offset + 250, PIES_Y_OFFSET + 270),
                f"{percent}%" if percent != -1 else "",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )
        # Text top and bottom court

    # Writing gray box values
    for percent, x_offset in zip(arrows_numbers, PRECENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PRECENTAGES_Y_OFFSET),
            percent,
            font=DIN_MID,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    if numbers:
        for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
            offset = (x_offset, TOTALS_Y_OFFSET)
            draw.text(
                offset,
                f"{number}",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )

    if speed:
        for speed_value, x_offset in zip(speed, PIES_X_OFFSETS):
            offset = (x_offset + 325, PIES_Y_OFFSET + 315)
            speed_value = str(speed_value) if speed_value else ""
            draw.text(
                offset,
                speed_value,
                font=DIN_LARGE,
                fill=WHITE,
                anchor="ms",
            )

    if not pies_percentages:
        draw.text(
            (960, 485 - (180 if speed else 0)),
            "MPH",
            font=DIN_LARGE if speed else DIN_MID,
            fill=WHITE,
            anchor="ms",
        )
    # draw.text(
    #     (650, 1072),
    #     f"{opponent_name} {serve_no} serve",
    #     font=DIN_MID,
    #     fill=WHITE,
    #     anchor="ms",
    # )

    draw.text(
        (960, 45),
        f"{player_name} returning {serve_no} SERVE".upper(),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.rectangle([650, 980, 1270, 1060], fill="#113362")
    draw.text(
        (960, 1050),
        f"{opponent_name} serving".upper(),
        font=DIN_MID,
        fill=WHITE,
        anchor="ms",
    )

    if not clear:
        draw.text(
            (960, 95),
            (
                ("Return Speed" if speed else "Return IN %").upper()
                if preset == ColorPreset.RED
                else "Points WON %"
            ),
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )
    # Writing total serves
    elif numbers:
        draw.text(
            (960, 95),
            f"{sum(numbers)} total serves IN {opponent_name}",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )

    return court

from io import BytesIO
from functools import lru_cache
import requests
from PIL import Image, ImageDraw

def good_returns_template(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    clear: Optional[bool] = False,
    speed: Optional[List[int]] = None,
    surface: SurfaceCode,
) -> Image:
    # === New: remote assets base (Azure Blob Storage) ===
    TEMPLATE_ASSETS_BASE_URL = (
        "https://operationslakedb.blob.core.windows.net/"
        "shot-evolution-report/pdf_generator/good_returns_template"
    )

    @lru_cache(maxsize=256)
    def open_image(rel_path: str) -> Image.Image:
        """
        Fetch an image from Azure Blob Storage and return a PIL Image with alpha preserved.
        """
        print('FETCHING IMAGE')
        url = f"{TEMPLATE_ASSETS_BASE_URL}/{rel_path.lstrip('/')}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()

        return Image.open(BytesIO(resp.content)).convert("RGBA")

    # Template constants
    PRECENTAGES_Y_OFFSET = 565
    PRECENTAGES_X_OFFSETS = (540, 710, 890, 1040, 1220, 1380)
    TOTALS_Y_OFFSET = 485
    TOTALS_X_OFFSETS = PRECENTAGES_X_OFFSETS
    PIES_Y_OFFSET = 40
    PIES_X_OFFSETS = (140, 370, 600, 830, 1060, 1290)

    DIN = get_font(Fonts.DIN, 50)
    DIN_MID = get_font(Fonts.DIN, 75)
    DIN_LARGE = get_font(Fonts.DIN, 60)

    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    DARK_BLUE = Color(red=35, green=79, blue=102)

    # Opening court (background image) – now from Azure
    court: Image = (
        open_image(f"court/{surface.value}.png") if ENABLE_SURFACES
        else open_image("court.png")
    )
    # net = open_image("net.png")
    # court.paste(net, (0, 0), net)

    # Drawing the arrows
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue
        arrow_percent = ((percent // 5) + 1) * 5 if percent < 100 else 100
        arrow = open_image(f"{name}/{arrow_percent}.png")
        court.paste(arrow, (0, 0), arrow)

    draw = ImageDraw.Draw(court)

    # Pie charts
    if pies_percentages:
        # legend selection & placement
        header = open_image(f"{'red' if preset == ColorPreset.RED else 'orange'}_header.png")
        court.paste(header, (0, 0), header)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart(
                percentages=[100 - percent, percent],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            new_width = 500
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            pie = pie.resize((new_width, new_height))

            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            draw.text(
                (x_offset + 250, PIES_Y_OFFSET + 270),
                f"{percent}%" if percent != -1 else "",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )

    # Writing gray box values
    for percent, x_offset in zip(arrows_numbers, PRECENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PRECENTAGES_Y_OFFSET),
            percent,
            font=DIN_MID,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    if numbers:
        for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):
            draw.text(
                (x_offset, TOTALS_Y_OFFSET),
                f"{number}",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )

    if speed:
        for speed_value, x_offset in zip(speed, PIES_X_OFFSETS):
            offset = (x_offset + 325, PIES_Y_OFFSET + 315)
            speed_value = str(speed_value) if speed_value else ""
            draw.text(
                offset,
                speed_value,
                font=DIN_LARGE,
                fill=WHITE,
                anchor="ms",
            )

    if not pies_percentages:
        draw.text(
            (960, 485 - (180 if speed else 0)),
            "MPH",
            font=DIN_LARGE if speed else DIN_MID,
            fill=WHITE,
            anchor="ms",
        )

    draw.text(
        (960, 45),
        f"{player_name} returning".upper(),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.rectangle([650, 980, 1270, 1060], fill="#113362")
    draw.text(
        (960, 1050),
        f"{opponent_name} {serve_no} serve".upper(),
        font=DIN_MID,
        fill=WHITE,
        anchor="ms",
    )

    if not clear:
        draw.text(
            (960, 95),
            (
                ("Return Speed" if speed else "Return IN %").upper()
                if preset == ColorPreset.RED
                else "Points WON %"
            ),
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )
    elif numbers:
        draw.text(
            (960, 95),
            f"{sum(numbers)} total serves IN {opponent_name}",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )

    return court

def return_speed_template(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    *,
    numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    clear: Optional[bool] = False,
    speed: Optional[List[int]] = None,
    surface: SurfaceCode,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "good_returns_template/"
    # Percentages
    PRECENTAGES_Y_OFFSET = 565
    PRECENTAGES_X_OFFSETS = (540, 710, 890, 1040, 1220, 1380)
    # Totals
    TOTALS_Y_OFFSET = 485
    TOTALS_X_OFFSETS = PRECENTAGES_X_OFFSETS
    # Pie charts
    PIES_Y_OFFSET = 40
    PIES_X_OFFSETS = (140, 370, 600, 830, 1060, 1290)
    # Fonts
    DIN = get_font(Fonts.DIN, 50)
    DIN_MID = get_font(Fonts.DIN, 75)
    DIN_LARGE = get_font(Fonts.DIN, 60)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    DARK_BLUE = Color(red=35, green=79, blue=102)
    # GREEN = Color(red=67, green=151, blue=33)

    # if clear:
    #     PIES_Y_OFFSET = 130
    #     PIES_X_OFFSETS = (-40, 110, 260, 410, 560, 710)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    # net = Image.open(TEMPLATE_ASSETS_PATH / "net.png")
    # court.paste(net, (0, 0), net)

    
        # Text top and bottom court

    # Drawing the arrows
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)
    draw = ImageDraw.Draw(court)
    # Pie charts
    if pies_percentages:
        # legend selection & placement
        header = Image.open(
            TEMPLATE_ASSETS_PATH
            / f"{'red' if preset == ColorPreset.RED else 'orange'}_header.png"
        )
        court.paste(header, (0, 0), header)

        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart(
                percentages=[100 - percent, percent],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            # Calculate the height using aspect ratio
            new_width = 500
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            # Placing the pie chart on the court
            pie = pie.resize((new_width, new_height))

            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)

            # Pie chart percentage
            draw.text(
                (x_offset + 250, PIES_Y_OFFSET + 270),
                f"{percent}%" if percent != -1 else "",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )
    # Writing gray box values
    if speed:
        for percent, x_offset in zip(speed, PRECENTAGES_X_OFFSETS):
            draw.text(
                (x_offset, PRECENTAGES_Y_OFFSET),
                percent,
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )

    

    
    
    # draw.text(
    #     (650, 1072),
    #     f"{opponent_name} {serve_no} serve",
    #     font=DIN_MID,
    #     fill=WHITE,
    #     anchor="ms",
    # )

    draw.text(
        (960, 45),
        f"{player_name} returning".upper(),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.rectangle([650, 980, 1270, 1060], fill="#113362")
    draw.text(
        (960, 1050),
        f"{opponent_name} {serve_no } serve".upper(),
        font=DIN_MID,
        fill=WHITE,
        anchor="ms",
    )

    if not clear:
        draw.text(
            (960, 95),
            (
                ("Return Speed" if speed else "Return IN %").upper()
                if preset == ColorPreset.RED
                else "Points WON %"
            ),
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )
    # Writing total serves
    elif numbers:
        draw.text(
            (960, 95),
            f"{sum(numbers)} total serves IN {opponent_name}",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )
    if not pies_percentages:
        draw.text(
            (960, 485 - (180 if speed else 0)),
            "KMH",
            font=DIN_LARGE if speed else DIN_MID,
            fill=WHITE,
            anchor="ms",
        )

    return court

def good_returns_template_new(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    arrows_widths: List[int],
    arrows_numbers: List[str],
    *,
    numbers: Optional[List[int]] = None,
    full_numbers: Optional[List[int]] = None,
    pies_percentages: Optional[List[int]] = None,
    preset: Optional[ColorPreset] = ColorPreset.RED,
    clear: Optional[bool] = False,
    speed: Optional[List[int]] = None,
    surface: SurfaceCode,
) -> Image:
    # Template constants
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "good_returns_template/"
    # Percentages
    PRECENTAGES_Y_OFFSET = 565
    PRECENTAGES_X_OFFSETS = (540, 710, 890, 1040, 1220, 1380)
    # Totals
    TOTALS_Y_OFFSET = 485
    TOTALS_X_OFFSETS = PRECENTAGES_X_OFFSETS
    # Pie charts
    PIES_Y_OFFSET = 40
    PIES_X_OFFSETS = (140, 370, 600, 830, 1060, 1290)
    # Fonts
    DIN = get_font(Fonts.DIN, 50)
    DIN_MID = get_font(Fonts.DIN, 75)
    DIN_LARGE = get_font(Fonts.DIN, 60)
    # Colors
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    DARK_BLUE = Color(red=35, green=79, blue=102)
    # GREEN = Color(red=67, green=151, blue=33)

    # if clear:
    #     PIES_Y_OFFSET = 130
    #     PIES_X_OFFSETS = (-40, 110, 260, 410, 560, 710)

    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    # net = Image.open(TEMPLATE_ASSETS_PATH / "net.png")
    # court.paste(net, (0, 0), net)

    # Drawing the arrows
    for name, percent in zip(range(1, 7), arrows_widths):
        if not percent:
            continue

        arrow = Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{name}/{((percent//5)+1)*5 if percent < 100 else 100}.png"
        )
        arrow_x_offset = 0
        arrow_y_offset = 0
        offset = (arrow_x_offset, arrow_y_offset)

        court.paste(arrow, offset, arrow)
    draw = ImageDraw.Draw(court)
    # Pie charts
    if pies_percentages:
        # legend selection & placement
        header = Image.open(
            TEMPLATE_ASSETS_PATH
            / f"{'red' if preset == ColorPreset.RED else 'orange'}_header.png"
        )
        court.paste(header, (0, 0), header)

        counter = 0
        for percent, x_offset in zip(pies_percentages, PIES_X_OFFSETS):
            pie = get_piechart_new(
                percentages=[100 - percent, percent],
                number=numbers[counter],
                color="red" if preset == ColorPreset.RED else "orange",
            )
            # Calculate the height using aspect ratio
            new_width = 500
            width, height = pie.size
            aspect_ratio = height / width
            new_height = int(new_width * aspect_ratio)
            # Placing the pie chart on the court
            pie = pie.resize((new_width, new_height))

            # Placing the pie chart on the court
            court.paste(pie, (x_offset, PIES_Y_OFFSET), pie)
            counter = counter+1
            # Pie chart percentage
            draw.text(
                (x_offset + 250, PIES_Y_OFFSET + 270),
                f"{percent}%" if percent != -1 else "",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )
        # Text top and bottom court

    # Writing gray box values
    for percent, x_offset in zip(arrows_numbers, PRECENTAGES_X_OFFSETS):
        draw.text(
            (x_offset, PRECENTAGES_Y_OFFSET),
            percent,
            font=DIN_MID,
            fill=WHITE,
            anchor="ms",
        )

    # Writing totals
    if numbers:
        counter = 0
        for number, x_offset in zip(numbers, TOTALS_X_OFFSETS):

            offset = (x_offset, TOTALS_Y_OFFSET)
            draw.text(
                offset,
                f"{full_numbers[counter]}/{number}",
                font=DIN_MID,
                fill=WHITE,
                anchor="ms",
            )
            counter = counter + 1

    if speed:
        for speed_value, x_offset in zip(speed, PIES_X_OFFSETS):
            offset = (x_offset + 325, PIES_Y_OFFSET + 315)
            speed_value = str(speed_value) if speed_value else ""
            draw.text(
                offset,
                speed_value,
                font=DIN_LARGE,
                fill=WHITE,
                anchor="ms",
            )

    if not pies_percentages:
        draw.text(
            (960, 485 - (180 if speed else 0)),
            "MPH",
            font=DIN_LARGE if speed else DIN_MID,
            fill=WHITE,
            anchor="ms",
        )
    # draw.text(
    #     (650, 1072),
    #     f"{opponent_name} {serve_no} serve",
    #     font=DIN_MID,
    #     fill=WHITE,
    #     anchor="ms",
    # )

    draw.text(
        (960, 45),
        f"{player_name} returning {serve_no} SERVE".upper(),
        font=DIN,
        fill=YELLOW,
        anchor="ms",
    )

    draw.rectangle([650, 980, 1270, 1060], fill="#113362")
    draw.text(
        (960, 1050),
        f"{opponent_name} serving".upper(),
        font=DIN_MID,
        fill=WHITE,
        anchor="ms",
    )

    if not clear:
        draw.text(
            (960, 95),
            (
                ("Return Speed" if speed else "Return IN %").upper()
                if preset == ColorPreset.RED
                else "Points WON %"
            ),
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )
    # Writing total serves
    elif numbers:
        draw.text(
            (960, 95),
            f"{sum(numbers)} total serves IN {opponent_name}",
            font=DIN,
            fill=WHITE,
            anchor="ms",
        )

    return court

def rally_length_template(
    player_name: str,
    opponent_name: str,
    serve_no: str,
    labels: List[str],
    points: List[Tuple],
    surface: SurfaceCode,
    player_no: Optional[int] = None,
):
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "rally_length_template/"
    DIN = get_font(Fonts.DIN, 45)
    DIN_LARGE = get_font(Fonts.DIN, 70)

    DARK_BLUE = Color(red=35, green=79, blue=102)

    BARS_Y_OFFSETS = (-275, -165, -55, 60, 170, 280)
    # Opening court (background image)
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/{'half-court' if player_no else 'court'}/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(
            f"{TEMPLATE_ASSETS_PATH}/{'half-' if player_no else ''}court.png"
        )
    )
    header = Image.open(
        TEMPLATE_ASSETS_PATH / f"{'half-' if player_no else '' }header.png"
    )
    court.paste(header, (0, 0), header)

    draw = ImageDraw.Draw(court)
    serve_term = "Serves" if serve_no == "All" else "Serve"
    draw.text(
        (1050, 130),
        f"{serve_no} {serve_term} Win % by server and rally length".upper(),
        font=DIN_LARGE,
        fill=DARK_BLUE,
        anchor="ms",
    )

    legend_y_offset = 950 if not player_no else 630
    draw.text(
        (600, legend_y_offset),
        f"{player_name} Win%".upper(),
        font=DIN,
        fill=DARK_BLUE,
        anchor="ls",
    )

    draw.text(
        (1270, legend_y_offset),
        f"{opponent_name} Win%".upper(),
        font=DIN,
        fill=DARK_BLUE,
        anchor="ls",
    )

    for point, y in zip(points, BARS_Y_OFFSETS):
        barchart = get_barchart(
            point,
        )
        court.paste(barchart, (0, y), barchart)

        draw.text(
            (1700, y + 560),
            f"{sum(point)}",
            font=DIN_LARGE,
            fill=DARK_BLUE,
            anchor="ms",
        )
    displayed_players = (
        [player_name, opponent_name]
        if not player_no
        else [player_name] if player_no == 1 else [opponent_name]
    )
    for player, y_offset in zip(displayed_players, (370, 700)):
        draw.multiline_text(
            (200, y_offset),
            f"{player}\nserving".upper(),
            font=DIN,
            fill=DARK_BLUE,
            anchor="ms",
            align="center",
        )
    # for player, x_offset in zip((player_name, opponent_name), (740, 1475)):
    #     draw.text(
    #         (x_offset, 920),
    #         player,
    #         font=DIN,
    #         fill=DARK_BLUE,
    #     )

    return court


def rally_ending_template(
    player_name: str,
    pies_percentages: List[List[int]],
    shot_type: ShotType,
    is_left_handed: bool,
    surface: SurfaceCode,
) -> Image:
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "rally_ending_template/"

    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    #header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    #court.paste(header, (0, 0), header)

    # draw = ImageDraw.Draw(court)

    # Draw pie charts
    pie_x = start_x = 295
    pie_y = 25
    for i, percentages in enumerate(pies_percentages):
        # in percentages ending stroke 1 : "winner" , 2 : "forcing error" , 4 : "unforced error"
        pie = generate_piechart(
            [percentages[1], percentages[2], percentages[4]],
            [*ColorPreset.RALLY_ENDING.value],
            0.6,
        )
        if i and i % 3 == 0:
            pie_x = start_x
            pie_y += 230
        court.paste(pie, (pie_x, pie_y), pie)
        pie_x += 340

    # Draw racket and shot type
    racket = Image.open(TEMPLATE_ASSETS_PATH / f"{shot_type.value}_racket.png")
    court.paste(racket, (0, 0), racket)

    return court

def rally_ending_template_marin(
    player_name: str,
    pies_percentages: List[List[int]],
    shot_type: ShotType,
    is_left_handed: bool,
    surface: SurfaceCode,
) -> Image:
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "rally_ending_template/"

    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/court/{surface.value}.png")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/court.png")
    )
    #header = Image.open(TEMPLATE_ASSETS_PATH / "header.png")
    #court.paste(header, (0, 0), header)

    # draw = ImageDraw.Draw(court)

    # Draw pie charts
    pie_x = start_x = 200
    pie_y = -150   
    for i, percentages in enumerate(pies_percentages):
        # in percentages ending stroke 1 : "winner" , 2 : "forcing error" , 4 : "unforced error"
        pie = generate_piechart(
            [percentages[1], percentages[2], percentages[4]],
            [*ColorPreset.RALLY_ENDING.value],
            0.4,
        )
        if i and i % 7 == 0:
            pie_x = start_x
            if i != 0:
                pie_y += 150
        court.paste(pie, (pie_x, pie_y), pie)
        pie_x += 150

    # Draw racket and shot type
    racket = Image.open(TEMPLATE_ASSETS_PATH / f"{shot_type.value}_racket.png")
    court.paste(racket, (0, 0), racket)

    return court


def scatter_plot_template(
    player_name: str,
    points_x_coordinates: List[float],
    points_y_coordinates: List[float],
    *,
    half_court: Optional[bool] = False,
    inv: Optional[bool] = False,
    surface: SurfaceCode,
) -> Image:
    TEMPLATE_ASSETS_PATH = ASSETS_PATH / "scatter_plot_template/"

    # Opening court (background image)
    court_name = "half_court" if half_court else "court"
    court: Image = (
        Image.open(f"{TEMPLATE_ASSETS_PATH}/{court_name}/{surface.value}.jpg")
        if ENABLE_SURFACES
        else Image.open(f"{TEMPLATE_ASSETS_PATH}/{court_name}.jpg")
    )

    # Plot configuration
    dimensions = (26.1, 17.3) if half_court else (23.6, 23.47)
    xlim = (-6, 6)

    ylim = (
        ((0, 8) if inv else (-8, 0)) if half_court else ((0, 12) if inv else (-12, 0))
    )
    offset = (
        ((-210, -450) if inv else (-243, -195))
        if half_court
        else ((-77, -195) if inv else (-115, -245))
    )
    court = court.rotate(180) if not inv else court
    draw = ImageDraw.Draw(court)
    DIN = get_font(Fonts.DIN, 55)
    YELLOW = Color(red=255, green=255, blue=0)
    WHITE = Color(red=255, green=255, blue=255)
    text_color = WHITE if inv else YELLOW
    preset = ColorPreset.WHITE if inv else ColorPreset.YELLOW

    if half_court:
        labels = ("Wide", "Body", "T")
        for x, text in zip((555, 780, 1010, 1250, 1470, 1700), labels + labels[::-1]):
            draw.text(
                (x - 37 if not inv else x, 75 if not inv else court.height - 75),
                text,
                font=DIN,
                fill=text_color,
                anchor="ms",
            )
    else:
        draw.text(
            (1130 - 37 if not inv else 1130, 75 if not inv else court.height - 75),
            "Middle",
            font=DIN,
            fill=text_color,
            anchor="ms",
        )

    # Generating scatter plot points
    scatter = generate_scatter_plot(
        points_x_coordinates,
        points_y_coordinates,
        xlim,
        ylim,
        *preset.value,
        dimensions=dimensions,
    )

    court.paste(scatter, offset, scatter)

    return court
