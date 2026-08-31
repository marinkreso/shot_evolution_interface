import io
from typing import List, Optional, Tuple, Union
from PIL import Image, ImageFont, ImageDraw

from pdf_generator.models.enums import Fonts, Offset, VisualElement, Color
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pdf_generator.services.constants import CURDIRPATH

ZERO_PIE = Image.open(f"{CURDIRPATH}/visuals/assets/zero-pie.png")
ZERO_PIE_BIG = Image.open(f"{CURDIRPATH}/visuals/assets/zero-pie-big.png")
LATEST_RADIUS = 0


def get_font(font: Fonts, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{CURDIRPATH}/fonts/{font.value.lower()}.ttf", size)


def figure_to_image(figure: Figure) -> Image:
    buffer = io.BytesIO()
    figure.savefig(buffer, transparent=True)
    buffer.seek(0)
    image = Image.open(buffer)

    return image


def generate_arrow(
    path: str,
    width_ratio: int,  # ValueRange(1, 100)
    angle: int,  # Counter clockwise
    *,
    width_scaler: Optional[float] = 1.2,
) -> VisualElement:
    arrow = Image.open(path)

    original_width, original_height = arrow.size

    # Size & rotation manipulation
    arrow = arrow.resize(
        (round(width_ratio / 100 * width_scaler * original_width), original_height)
    )
    arrow = arrow.rotate(angle, expand=True, resample=Image.BICUBIC)

    # Calculate the resulted offset of manipulating the arrow
    x_offset = int((original_width - arrow.width) / 2)
    y_offset = int((original_height - arrow.height) / 2)

    return VisualElement(image=arrow, relative_offset=Offset(x=x_offset, y=y_offset))


def generate_piechart(
    percentages: List[int],
    colors: List[str],  # hexcodes
    radius: float,  # ValueRange(0.0, 1.0)
    *,
    border_width: Optional[float] = 1,  # ValueRange(0, 10)
    border_color: Optional[str] = "white",  # color name or hex code
) -> Image:
    labeled = True if len(percentages) > 2 else False
    # No observations
    if (percentages[0] == 101 and not labeled) or sum(percentages) == 0:
        if len(percentages) > 2:
            if radius > 0.5:
                return ZERO_PIE_BIG
            return ZERO_PIE
        else:
            img = Image.new("RGBA", (640, 480), (255, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            line_length = radius * 143
            draw.line((327, 242 - line_length, 327, 242), "white", 2)
            return img

    global LATEST_RADIUS
    if LATEST_RADIUS > radius or labeled:
        plt.clf()
    LATEST_RADIUS = radius

    plt.pie(
        percentages,
        radius=radius,
        colors=colors,
        wedgeprops={"edgecolor": border_color, "linewidth": border_width},
        startangle=90,
        normalize=True,
        autopct=lambda value: int(value / 100 * sum(percentages)) if labeled else None,
        textprops={"color": "w", "fontsize": int(radius * 100 / 2), "weight": "bold"}
        if labeled
        else None,
    )
    # Convert the plot to Image instance
    pie_figure = plt.gcf()
    pie_image = figure_to_image(pie_figure)
    return pie_image


from io import BytesIO
from functools import lru_cache
import requests
from PIL import Image

def get_piechart(
    percentages: List[int], *, color: str = "orange"  # TODO: add enum
) -> Image.Image:
    # === New: Azure Blob Storage base URL ===
    BASE_URL = (
        "https://operationslakedb.blob.core.windows.net/"
        "shot-evolution-report/pdf_generator/piechart"
    )

    @lru_cache(maxsize=256)
    def open_image(rel_path: str) -> Image.Image:
        """
        Fetch image from Azure Blob Storage and return a PIL Image with alpha preserved.
        """
        try:
            url = f"{BASE_URL}/{rel_path.lstrip('/')}"
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return Image.open(BytesIO(resp.content)).convert("RGBA")
        except:
            print('open_image error', rel_path)
            raise Exception

    # Handle edge cases
    if percentages[0] == 101 or sum(percentages) == 0:
        target_pie = -1
    else:
        target_pie = percentages[1]

    # Load pie chart image from Azure
    pie = open_image(f"{target_pie}.png")
    return pie

def get_piechart_new(
    percentages: List[int], number, *, color: str = "orange"  # TODO add enum
) -> Image:
    target_pie = None
    # No observations
    if percentages[0] == 101 or sum(percentages) == 0:
        target_pie = -1
    
    # Convert the plot to Image instance
    target_pie = percentages[1]
    if number == 0:
        target_pie = 'empty'
    pie = Image.open(f"{CURDIRPATH}/visuals/assets/piechart/{color}/{target_pie}.png")
    return pie

def generate_scatter_plot(
    x_coordinates: List[float],
    y_coordinates: List[float],
    xlim: Tuple[float, float],
    ylim: Tuple[float, float],
    color: str,
    edge_color: str,
    *,
    radius: Optional[float] = 125,
    dimensions: Optional[Tuple[float, float]] = (25.9, 12),
) -> Image:
    plt.clf()
    plt.scatter(
        x_coordinates,
        y_coordinates,
        s=radius,
        color=color,
        edgecolors=edge_color,
    )

    # plot Configuration
    plt.ylim(*ylim)
    plt.xlim(*xlim)
    plt.axis("off")

    # Convert the plot to Image instance
    scatter = plt.gcf()

    # Resize
    scatter.set_size_inches(*dimensions)

    # Convert the plot to Image instance
    plot = figure_to_image(scatter)

    plt.close()

    return plot


def generate_barchart(
    labels: Union[List, int],
    data: Union[List[Tuple], List[int]],
    colors: List[str],
    font_colors: List[str],
    width: float,
    height: float,
):
    plt.clf()
    FONT_SIZE = 14
    # Calculate bars lengths
    bars_percentages = [[] for _ in data[0]]
    totals = []
    for points in data:
        total = sum(points)
        totals.append(total)
        for i, point in enumerate(points):
            bars_percentages[i].append(point / total * 100 if total else 0)

    # Draw bars side by side
    bars = []
    left_margins = [0 for _ in bars_percentages[0]]
    for i, percentages in enumerate(bars_percentages):
        if i != 0 and len(percentages) == 1 and not percentages[0]:
            continue
        bars.append(
            plt.barh(
                labels, percentages, left=left_margins, color=colors[i], height=0.55
            )
        )
        for i, percent in enumerate(percentages):
            left_margins[i] += percent

    if len(totals) > 1 or (len(totals) == 1 and totals[0] != 0):
        # Write total points
        for i, total in enumerate(totals):
            plt.text(
                105, i - 0.08, str(total), color="black", ha="center", size=FONT_SIZE
            )

        # Write each bar percentage
        for color, bar in zip(font_colors, bars):
            if bar.datavalues[0]:
                plt.bar_label(
                    bar, label_type="center", color=color, fmt="%.1f%%", size=FONT_SIZE
                )

    # Modify y axis label size
    plt.yticks(size=FONT_SIZE / 1.2)

    # Hide unnecessary axes
    ax = plt.gca()

    ax.axes.get_xaxis().set_visible(False)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)

    fig = plt.gcf()
    fig.set_size_inches(width, height)
    barchart = figure_to_image(fig)
    plt.close()
    return barchart


def get_barchart(data: List[int]):
    # Calculate bars lengths
    percent = data[0] / sum(data) * 100 if sum(data) else 0
    return Image.open(f"{CURDIRPATH}/visuals/assets/barchart/{round(percent)}.png")


def get_ellipses_percentages_pies(
    relative_width: float,
    relative_height: float,
    relative_x_offset: List[float],
    relative_y_offset: float,
    indices: List[int],
):
    visual_ellipses = []
    for index in indices:
        percentage_ellipse = {
            "width": relative_width,
            "height": relative_height,
            "x_offset": relative_x_offset[index - 1],
            "y_offset": relative_y_offset,
        }
        visual_ellipses.append(percentage_ellipse)
    return visual_ellipses
