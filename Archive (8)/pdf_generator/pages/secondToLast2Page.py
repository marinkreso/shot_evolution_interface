from pdf_generator.services.drawingTables import DirectionSuccessTable
from pdf_generator.services.constants import FOOTER_TEXT, GS_DIRECTION_SUCCESS_TEXT


class SecondToLast:
    visual_counter = 0
    table_counter = 2
    execution_cost = 5

    def __init__(self, FPDF, data_repo, variant):
        self.name = "Appendix Page 2"
        self.pdf = FPDF
        self.variant = variant
        self.GS_deuce_shots = data_repo.GS_all_shots("Deuce", variant)
        self.GS_ad_shots = data_repo.GS_all_shots("Ad", variant)
        self.player_name, self.opponent_name = data_repo.players_name()
        self.name = "Appendix Page6"

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
        self.pdf.set_font(family="Din", size=11)
        line_height = self.pdf.font_size * 1.25
        self.pdf.set_y(50)

        # Deuce court gs tables
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.cell(
            0,
            line_height,
            "Deuce Court Groundstroke Direction success",
            ln=True,
            align="C",
        )
        self.pdf.ln(line_height * 0.75)

        # Table explanation
        self.pdf.set_font("ROCK", size=10)
        self.pdf.set_x(30)
        self.pdf.multi_cell(155, 4, GS_DIRECTION_SUCCESS_TEXT)
        self.pdf.ln(line_height)

        # Deuce court data tables
        offset = 30

        DirectionSuccessTable(
            self.pdf,
            self.GS_deuce_shots,
            offset,
            footer_data=f"Last & second to last shots (Deuce): {current_player}",
        ).draw(
            "A",
            self.pdf.tables_start_num,
        )
        self.pdf.tables_start_num += 1

        self.pdf.ln(line_height * 2)

        # Ad data tables
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.cell(
            0,
            line_height,
            "Ad Court Groundstroke Direction success",
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
            "This is the same as Table 8.1.3 but the player is now hitting from the ad court.",
        )
        self.pdf.ln(line_height)

        DirectionSuccessTable(
            self.pdf,
            self.GS_ad_shots,
            offset,
            footer_data=f"Last & second to last shots (Deuce): {current_player}",
        ).draw("A", self.pdf.tables_start_num)
        self.pdf.tables_start_num += 1

        self.pdf.ln(line_height)

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
