import sys
import pathlib
import uuid

# https://stackoverflow.com/questions/19078969/python-getting-appdata-folder-in-a-cross-platform-way


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Local
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Local"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


# create your program's directory


try:
    my_datadir = get_datadir()
    TEMPFOLDER = str(my_datadir)
    my_datadir.mkdir(parents=True)
except FileExistsError:
    pass


CURDIRPATH = pathlib.Path(__file__).parent.parent.resolve()
ID = str(uuid.uuid4())
VERSION = "1.8.0"

# Paragraphs
# ------------------------------
FOOTER_TEXT = (
    "Confidential and proprietary. Absent permission of GSA, please do not share, disclose, store, copy, "
    "distribute, resell, disclose, or use in derivative works."
)

SERVER_LOCATION_PARAGRAPH = (
    "These visuals show serve direction (top visual, yellow arrows and %) and in % (top visual, "
    "green % and pie charts) and average serve speed (bottom visual). The width of the yellow "
    "arrows is sized according to % of serves by direction. When serve in % are not available "
    "in the dataset, this is stated in the chart."
)

SERVE_LOCATION_1B_PARAGRAPH = (
    "The visuals show serve direction (yellow arrows, yellow % and numbers) and points won by "
    "the server (pie charts and green %) for all points, non pressure points, pressure points "
    "and break points."
)
TC_SERVE_LOCATION_B_PARAGRAPH = (
    "The visuals show serve direction (yellow arrows, yellow % and numbers) and points won by "
    "the server (pie charts and green %) for non pressure points and break points."
)

RETURN_LOCATION_1C_PARAGRAPH = (
    "This visual shows exact return placement. The visual is based on a different data set "
    "than the other return visuals and will not always match exactly."
)

SERVER_LOCATION_1A_INV_PARGRAPH = (
    "These visuals show serve direction (grey arrows and %) and in % (green numbers and pie "
    "charts) and average serve speed (bottom visual). The width of the arrows is sized "
    "according to % of serves by direction. Any n/a values indicate that certain "
    "information was not available in the dataset."
)

SERVER_LOCATION_1C_INV_PARGRAPH = (
    "This page provides additional information on serve placement. The top visual shows the "
    "same information as the first visual in the previous page: serve direction and "
    "won/lost info by direction. The bottom visual shows exact serve placement. Visuals are "
    "based on different data sets and will not always match exactly."
)

GOOD_RETURNS_1A_PARAGRAPH = (
    "Arrows show direction of opponents serves, while the %s in black indicate the return location "
    "(top visual) and points won on return (bottom visual). "
    "A lower % indicates that the player is worse at returning serves hit to that location."
)

GOOD_RETURNS_1B_PARAGRAPH = (
    "Arrows show direction of opponents serves, while the %s in black indicate the return location "
    "and points won on return. A lower % indicates that the player is worse at returning serves hit to that location."
)

RALLY_ENDING_PARAGRAPH = (
    "These visuals indicate the court position where a player hit winners, forcing errors and "
    "unforced errors. Position is based on horizontal position (deuce, middle, ad) and vertical "
    "position (behind baseline, back court, fore court, volley). "
)

ALL_GROUNDSTROKES_PARAGRAPH = (
    "These visuals show the direction of all groundstroke shots hit by the player. Player "
    "position, shot direction and opponent shot type are indicated at the top of the visuals. The grey arrow indicates "
    "the direction of the previous shot by the opponent. Yellow arrows indicate the direction of the groundstroke shot hit by the player."
)

RALLY_ENDING_TABLE_PARAGRAPH = (
    "These statistics show how many winners, forcing errors and unforced errors the player "
    "and opponent hit. The table details stats by stroke type, position and running/stationary "
)

RALLY_ENDING_DIRECTION_PARAGRAPH = (
    "These visuals show the direction of the rally ending shot hit by the player. Player position"
    ", shot direction and opponent shot type are indiciated at the top of the visuals. The grey arrow indicates the direction of the opponent 2nd to last shot."
    " Yellow arrows indicate the direction of the rally ending shot hit by the player."
)

SHOT_AFTER_RETURN_LOCATION_PARAGRAPH = """These visuals show the direction of the first shot hit by the server after a return is hit back by the opponents. Server location is indicated in the title of each graphic. The grey arrow indicates the direction of return. Yellow arrows indicate the direction of the first groundstroke shot hit by the server. Pie charts show points won by the server (stated at the top of visuals) for each serve+1 direction."""

HEADER_FOOTER_TEXT = """The information in this report is provided solely under a restricted license from GSA. The material
in this report should be treated as confidential and should not be shared, disclosed, stored,
copied, distributed, resold, or used in derivative works without permission from GSA. GSA retains
all intellectual property rights and other rights in the report and the information contained within."""

RETURN_SERVE_SPEED_TEXT = """Indicates the impact of serve speeds of the opponent on the quality of return by the player. "In" is whether the player hit the ball back. "Good" means the returner either (1) won the point; or (2) at least got the point to 5 shots. "Winner" means the returner won the point."""

RALLY_ENDING_1_SHOT_DIRECTION_TEXT = """These tables show direction of point-ending groundstrokes tagged in our data: 2nd to last and last shot groundstrokes (for rallies of more than 3 shots). The position where the shot was hit from (Deuce, Middle or Ad) is shown at the top of the table, and shots can either be forehands or backhands. Shot directions (down the line, middle or cross-court) are reflected in the rows in light blue. The percentages indicate how often a player hit a shot in a given direction, by position and forehand/backhand."""

RALLY_ENDING_2_SHOT_DIRECTION_TEXT = """This table shows point-ending groundstroke combinations (rallies of more than 3 shots) where a player positioned in the deuce court hits the "second to last" shot to the opposing player (player names are listed below the table). The "second to last" shot player hits down the line, middle, or cross-court, and these shot directions are reflected in the rows in light blue. The opponent hits the "last shot," which can either be a forehand or backhand, and this shot can go line, middle, or cross. The tables reflect totals and percentages showing how the player who hit the last shot handled the incoming ball."""

GS_DIRECTION_SUCCESS_TEXT = """For the player listed below the table, it shows when that player was positioned in deuce court, the total number of shots (for the last and second-to-last shot) that were hit with the forehand and backhand, and how often the player won the point when the ball was hit with the forehand and backhand from deuce court in a particular direction (line, middle, or cross)."""
FIRST_SHOT_OFF_RETURN_PARAGRAPH = (
    "These visuals show return placement (grey arrows and %, returner is stated at "
    "bottom of each visual), depending on serve direction. Pie charts and black %s show "
    "points won by the server (server is stated at top of each visual). A lower win % "
    "indicates it is more effective to return in those locations.  "
)
RALLY_LENGTH_PARAGRAPH = (
    "These statistics show points won %’s of the player and opponent(s) based on whether the "
    "player was serving or returning and length of rally. "
)

RETURN_LOCATION_PARAGRAPH = """These visuals show return direction (yellow arrows and %) and won % (pie charts and green %).The width of the yellow arrows is sized according to % of returns by direction. """

SERVE_LOCATION_1C_PARAGRAPH = (
    "This page provides additional information on serve placement. The top visual shows the "
    "same information as the first visual in the previous page: serve direction and "
    "won/lost info by direction. The bottom visual shows exact serve placement. Visuals are "
    "based on different data sets and will not always match exactly. "
)

SERVE_LOCATION_1C_INV_PARAGRAPH = (
    "This page provides additional information on serve placement. The top visual shows "
    "the same information as the first visual in the previous page: serve direction and "
    "won/lost info by direction. The bottom visual shows exact serve placement. Visuals "
    "are based on different data sets and will not always match exactly. "
)

SERVE_RALLY_POINTS_PARAGRAPH = """This stat indicates points won % of groundstroke rallies by the player and his opponents by the length of the rally for 1st serves on non-pressure points. The remaining tables show the same stat by pressure points and for 2nd serves (non-pressure and pressure)."""

ARROW_DETAIL = "Arrow width sized according to % of serves by direction"
ARROW_DETAIL1 = "Arrow width sized"
ARROW_DETAIL2 = "according to % of"
ARROW_DETAIL3 = "{} by direction"

DRAW_PROGRAM_PATH = "images-builder-helper-app/graphics-builder-helper.exe"

APPENDIX_AVG_SPEED_HEADER_COL_1 = "\nReturn Speeds -- All Returns"
APPENDIX_AVG_SPEED_HEADER_COL_2 = "Speed\n(average of returned balls)"

# Paths
# ------------------------------
IMAGE_LOGO_PATH = f"{CURDIRPATH}/assets/logo.png"
IMAGE_LOGO_PATH_BLACK = f"{CURDIRPATH}/assets/logo_black.png"
FINAL_TEXT = f"{CURDIRPATH}/assets/FINAL_TEXT.png"
DIVIDER = f"{CURDIRPATH}/assets/divider.png"
