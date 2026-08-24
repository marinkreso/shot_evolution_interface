from typing import List, Dict
from pdf_generator.visuals.utils import get_ellipses_percentages_pies


def serve_location_template(ellipses: Dict[str, List[int]]) -> List[Dict[str, float]]:
    PERCENTAGES_ELLIPSE_HEIGHT = 0.16203703703703703
    PERCENTAGES_ELLIPSE_WIDTH = 0.07552083333333333
    PERCENTAGES_ELLIPSE_Y_OFFSET = 0.3287037037037037
    PERCENTAGES_ELLIPSE_X_OFFSETS = [
        0.24479166666666666,
        0.3385416666666667,
        0.4192708333333333,
        0.5104166666666666,
        0.5911458333333334,
        0.6770833333333334,
    ]
    PIES_ELLIPSE_HEIGHT = 0.24074074074074073
    PIES_ELLIPSE_WIDTH = 0.09895833333333333
    PIES_ELLIPSE_Y_OFFSET = 0.6203703703703703
    PIES_ELLIPSE_X_OFFSETS = [
        0.1796875,
        0.2890625,
        0.3984375,
        0.5078125,
        0.6171875,
        0.7265625,
    ]

    visual_ellipses = []
    for key in ellipses:
        if key == "percentages":
            result = get_ellipses_percentages_pies(
                PERCENTAGES_ELLIPSE_WIDTH,
                PERCENTAGES_ELLIPSE_HEIGHT,
                PERCENTAGES_ELLIPSE_X_OFFSETS,
                PERCENTAGES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)
        if key == "pies":
            result = get_ellipses_percentages_pies(
                PIES_ELLIPSE_WIDTH,
                PIES_ELLIPSE_HEIGHT,
                PIES_ELLIPSE_X_OFFSETS,
                PIES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)

    return visual_ellipses


def good_returns_template(ellipses: Dict[str, List[int]]) -> List[Dict[str, float]]:
    PERCENTAGES_ELLIPSE_HEIGHT = 0.17592592592592593
    PERCENTAGES_ELLIPSE_WIDTH = 0.078125
    PERCENTAGES_ELLIPSE_Y_OFFSET = 0.375
    PERCENTAGES_ELLIPSE_X_OFFSETS = [
        0.24479166666666666,
        0.3307291666666667,
        0.4244791666666667,
        0.5052083333333334,
        0.5989583333333334,
        0.6796875,
    ]
    PIES_ELLIPSE_HEIGHT = 0.26851851851851855
    PIES_ELLIPSE_WIDTH = 0.109375
    PIES_ELLIPSE_Y_OFFSET = 0.07407407407407407
    PIES_ELLIPSE_X_OFFSETS = [
        0.1484375,
        0.2682291666666667,
        0.3880208333333333,
        0.5078125,
        0.6276041666666666,
        0.7473958333333334,
    ]

    visual_ellipses = []
    for key in ellipses:
        if key == "percentages":
            result = get_ellipses_percentages_pies(
                PERCENTAGES_ELLIPSE_WIDTH,
                PERCENTAGES_ELLIPSE_HEIGHT,
                PERCENTAGES_ELLIPSE_X_OFFSETS,
                PERCENTAGES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)
        if key == "pies":
            result = get_ellipses_percentages_pies(
                PIES_ELLIPSE_WIDTH,
                PIES_ELLIPSE_HEIGHT,
                PIES_ELLIPSE_X_OFFSETS,
                PIES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)

    return visual_ellipses

def return_location_template(ellipses: Dict[str, List[int]]) -> List[Dict[str, float]]:
    PERCENTAGES_ELLIPSE_HEIGHT = 0.16666666666666666
    PERCENTAGES_ELLIPSE_WIDTH = 0.078125
    PERCENTAGES_ELLIPSE_Y_OFFSET = 0.6157407407407407
    PERCENTAGES_ELLIPSE_X_OFFSETS = [0.24739583333333334, 0.4635416666666667, 0.671875]
    
    PIES_ELLIPSE_HEIGHT = 0.2361111111111111
    PIES_ELLIPSE_WIDTH = 0.09895833333333333
    PIES_ELLIPSE_Y_OFFSET = 0.7712962962962963
    PIES_ELLIPSE_X_OFFSETS = [0.23697916666666666, 0.4583333333333333, 0.6640625]

    visual_ellipses = []
    for key in ellipses:
        if key == "percentages":
            result = get_ellipses_percentages_pies(
                PERCENTAGES_ELLIPSE_WIDTH,
                PERCENTAGES_ELLIPSE_HEIGHT,
                PERCENTAGES_ELLIPSE_X_OFFSETS,
                PERCENTAGES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)
        if key == "pies":
            result = get_ellipses_percentages_pies(
                PIES_ELLIPSE_WIDTH,
                PIES_ELLIPSE_HEIGHT,
                PIES_ELLIPSE_X_OFFSETS,
                PIES_ELLIPSE_Y_OFFSET,
                ellipses[key],
            )
            visual_ellipses.extend(result)

    return visual_ellipses