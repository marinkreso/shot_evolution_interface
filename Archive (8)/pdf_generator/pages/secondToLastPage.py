from pdf_generator.services.drawingTables import DirectionTable
from pdf_generator.services.constants import (
    FOOTER_TEXT,
    RALLY_ENDING_2_SHOT_DIRECTION_TEXT,
)


class SecondToLast:
    visual_counter = 0
    table_counter = 2
    execution_cost = 10

    def __init__(self, FPDF, data_repo, variant):
        self.name = "Appendix Page 2"
        self.pdf = FPDF
        self.variant = variant
        self.GS_pair_deuce = data_repo.GS_pair(pos="Deuce", player_no=variant)
        self.GS_pair_ad = data_repo.GS_pair(pos="Ad", player_no=variant)
        self.player_name, self.opponent_name = data_repo.players_name()
        self.name = "Appendix Page5"

    def build_page_body(self):
        # TODO page_no, move container to super class
        # header and footer for footer_text,page_no
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Border
        left_margin = 20
        top_margin = 20

        current_player, current_opponent = (
            (self.player_name, self.opponent_name)
            if self.variant == 1
            else (self.opponent_name, self.player_name)
        )
        # Title
        self.pdf.set_font(family="Din", size=11)
        line_height = self.pdf.font_size * 1.25
        self.pdf.set_y(30)
        self.pdf.set_font("ROCK Bold", "U", 13)
        self.pdf.cell(
            0,
            line_height,
            f"Rally ending 2-shot direction:   {current_player}",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height)

        # Paragraph
        self.pdf.set_font("ROCK", size=10)
        self.pdf.set_x(30)
        self.pdf.multi_cell(
            155,
            4,
            "These tables show a variety of direction and points won %'s by the player and the opponent and explained for each table below",
        )
        self.pdf.ln(line_height * 1.75)

        # Deuce court gs tables
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.cell(
            0,
            line_height,
            "Deuce Court Groundstroke Response Directions",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height * 0.75)

        # Table explanation
        self.pdf.set_font("ROCK", size=10)
        self.pdf.set_x(30)
        self.pdf.multi_cell(155, 4, RALLY_ENDING_2_SHOT_DIRECTION_TEXT)
        self.pdf.ln(line_height)

        # Deuce court data tables
        offset = 30

        for type in ("C", "P"):
            dir_table = DirectionTable(
                self.pdf, self.GS_pair_deuce[type], 2, type, offset
            )

            footer = (None, None)
            if type == "P":
                footer = ("A", self.pdf.tables_start_num)
                dir_table.footer_data = (
                    f"Second to last shot (Deuce): {current_opponent}"
                )

            dir_table.draw(*footer)

        self.pdf.tables_start_num += 1
        self.pdf.cell(0, line_height, f"Last shot: {current_player}", align="C")

        self.pdf.ln(line_height * 2)

        # Running data tables
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.cell(
            0,
            line_height,
            "Ad Court Groundstroke Response Directions",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height)

        # Table explanation
        self.pdf.set_font("ROCK", size=10)
        self.pdf.set_x(30)
        self.pdf.multi_cell(
            155,
            4,
            'This table is the same as Table 8.1.1 but now the player hitting the "second to last" shot is positioned in the ad court.',
        )
        self.pdf.ln(line_height)

        for type in ("C", "P"):
            dir_table = DirectionTable(self.pdf, self.GS_pair_ad[type], 2, type, offset)

            footer = (None, None)
            if type == "P":
                footer = ("A", self.pdf.tables_start_num)
                dir_table.footer_data = f"Second to last shot (Ad): {current_opponent}"

            dir_table.draw(*footer)

        self.pdf.tables_start_num += 1

        self.pdf.cell(0, line_height, f"Last shot: {current_player}", align="C")
        self.pdf.ln(line_height)

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
