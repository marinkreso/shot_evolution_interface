from pdf_generator.services.drawingTables import DirectionTable
from pdf_generator.services.constants import (
    FOOTER_TEXT,
    RALLY_ENDING_1_SHOT_DIRECTION_TEXT,
)


class LastShot:
    visual_counter = 0
    table_counter = 2
    execution_cost = 10

    def __init__(self, FPDF, data_repo, variant):
        self.name = "Appendix Page 2"
        self.pdf = FPDF
        self.variant = variant
        self.GS_stationary_stats = data_repo.GS_stats(
            mode="Stationary", player_no=variant
        )
        self.GS_running_stats = data_repo.GS_stats(mode="Running", player_no=variant)
        self.player_name, self.opponent_name = data_repo.players_name()

    def build_page_body(self):
        # TODO page_no, font, move container to super class
        # header and footer for footer_text,page_no
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Border
        left_margin = 20
        top_margin = 20

        current_player = self.player_name if self.variant == 1 else self.opponent_name

        # Title
        self.pdf.set_font(family="Din", size=7)
        line_height = self.pdf.font_size * 1.25
        self.pdf.set_y(30)
        self.pdf.set_font("ROCK Bold", "U", 13)
        self.pdf.cell(
            0,
            line_height,
            f"Rally ending 1-shot direction:   {current_player}",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height)

        # Paragraph
        self.pdf.set_font("ROCK", size=9)
        self.pdf.set_x(30)
        self.pdf.multi_cell(155, 4, RALLY_ENDING_1_SHOT_DIRECTION_TEXT)
        self.pdf.ln(line_height)

        # Tables explanation
        self.pdf.set_x(30)
        self.pdf.multi_cell(
            155,
            4,
            "The first two tables show stationary groundstroke directions. The following two tables show running groundstroke tables.",
        )
        self.pdf.ln(line_height * 2)

        # Stationary data tables
        self.pdf.set_font("ROCK Bold", "", 11)
        self.pdf.cell(
            0,
            line_height,
            "Stationary Groundstroke Direction from Backcourt and Behind Baseline",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height)

        offset = 30

        for type in ("C", "P"):
            dir_table = DirectionTable(
                self.pdf, self.GS_stationary_stats[type], 1, type, offset
            )

            footer = (None, None)
            if type == "P":
                footer = ("A", self.pdf.tables_start_num)
                dir_table.footer_data = f"Last shot: {current_player}"

            dir_table.draw(*footer)

        self.pdf.tables_start_num += 1

        self.pdf.ln(line_height)

        # Running data tables
        self.pdf.set_font("ROCK Bold", "", 11)
        self.pdf.cell(
            0,
            line_height,
            "Running Groundstroke Direction from Backcourt and Behind Baseline",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height)

        for type in ("C", "P"):
            dir_table = DirectionTable(
                self.pdf, self.GS_running_stats[type], 1, type, offset
            )

            footer = (None, None)
            if type == "P":
                footer = ("A", self.pdf.tables_start_num)
                dir_table.footer_data = f"Last shot: {current_player}"
            dir_table.draw(*footer)

        self.pdf.tables_start_num += 1
        self.pdf.ln(line_height)

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
