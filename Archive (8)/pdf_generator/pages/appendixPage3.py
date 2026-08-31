from pdf_generator.services.drawingTables import ServeSpeedTable
from pdf_generator.services.constants import FOOTER_TEXT


class AppendixPage3:
    visual_counter = 0
    table_counter = 3
    execution_cost = 8

    def __init__(self, FPDF, data_repo, player_no):
        self.name = "Appendix Page 3"
        self.pdf = FPDF
        self.player_name, self.player2_name = data_repo.players_name()
        self.player_no = player_no
        self.return_v_serve_speed_data = data_repo.return_v_serve_speed(
            position="Ad", player_no=self.player_no
        )
        self.name = "Appendix Page3"

    def build_page_body(self):
        # TODO page_no, font, move container to super class
        # header and footer for footer_text,page_no
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Border
        left_margin = 20
        top_margin = 20

        # Section title
        self.pdf.set_y(25)
        self.pdf.set_font(family="Din", size=15)
        line_height = self.pdf.font_size * 2
        self.pdf.set_font("ROCK Bold", "", 11)
        self.pdf.cell(0, line_height, "Ad Court", ln=True, align="C")

        # Ad Court Tables
        # Config
        self.pdf.set_y(self.pdf.y + 5)
        offset = 30
        self.pdf.set_font("ROCK", size=11)
        self.pdf.set_fill_color(204, 204, 204)

        ac_table = ServeSpeedTable(
            self.pdf, None, None, x_offset=offset, line_height_scaler=1.15
        )

        # Building Ad court tables
        for i, type in enumerate(self.return_v_serve_speed_data):
            # Bind deuce court table with data
            ac_table.data = self.return_v_serve_speed_data[type]
            ac_table.type = type

            ac_table.draw("A", self.pdf.tables_start_num)
            self.pdf.tables_start_num += 1

            # Update y_offset
            ac_table.y_offset = self.pdf.y

        # Current ball returner
        returned_by = self.player_name if self.player_no == 1 else self.player2_name

        self.pdf.cell(0, line_height, f"Return: {returned_by}", align="C")

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
