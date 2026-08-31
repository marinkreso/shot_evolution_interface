from pdf_generator.services.drawingTables import AvgSpeedTable, ServeSpeedTable
from pdf_generator.services.constants import RETURN_SERVE_SPEED_TEXT, FOOTER_TEXT


class AppendixPage2:
    visual_counter = 0
    table_counter = 4
    execution_cost = 10

    def __init__(self, FPDF, data_repo, player_no):
        self.name = "Appendix Page 2"
        self.pdf = FPDF
        self.player_no = player_no
        self.avg_return_speed = data_repo.avg_return_speed(player_no)
        self.player_name, self.opponent_name = data_repo.players_name()
        self.return_v_serve_speed_data = data_repo.return_v_serve_speed(
            position="Deuce", player_no=self.player_no
        )

    def build_page_body(self):
        # TODO page_no, move container to super class
        # header and footer for footer_text,page_no
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Border
        left_margin = 20
        top_margin = 20

        # Title & subtitle
        self.pdf.set_font(family="Din", size=15)
        line_height = self.pdf.font_size
        self.pdf.set_y(20)

        if self.player_no == 1:
            self.pdf.set_font("ROCK Bold", "U", 13)
            self.pdf.cell(0, line_height, "Appendix", ln=True, align="C")
        else:
            self.pdf.ln(line_height)

        self.pdf.set_font("ROCK Bold", "", 13)
        self.pdf.cell(
            0, line_height, "Average Return Speeds by Location", ln=True, align="C"
        )

        # Current ball returner
        returned_by = self.player_name if self.player_no == 1 else self.opponent_name

        # AVG speed table
        # Table config
        offset = 40
        self.pdf.set_font_size(10)
        footer_data = ("Table A.1", f"Return: {returned_by}")

        # Table drawing
        AvgSpeedTable(
            self.pdf,
            self.avg_return_speed,
            offset,
            footer_data=f"Return: {returned_by}",
        ).draw("A", self.pdf.tables_start_num)
        self.pdf.tables_start_num += 1

        # Second section "Return v. Serve Speed"
        self.pdf.set_font("ROCK Bold", "", 14)
        self.pdf.cell(0, line_height * 1.2, "Return v. Serve Speed", ln=True, align="C")

        # Section's paragraph
        self.pdf.set_font("ROCK", size=9)
        self.pdf.set_x(30)
        self.pdf.multi_cell(155, 4.1, RETURN_SERVE_SPEED_TEXT)

        # Third section title
        self.pdf.ln(0)
        self.pdf.set_font("ROCK Bold", "", 11)
        self.pdf.cell(0, line_height * 1.2, "Deuce Court", ln=True, align="C")

        # Deuce Court Tables
        # Config
        offset = 30
        self.pdf.set_font("ROCK", size=11)
        self.pdf.set_fill_color(204, 204, 204)

        dc_table = ServeSpeedTable(
            self.pdf, None, None, x_offset=offset, line_height_scaler=1.15
        )

        # Building deuce court tables
        for type in self.return_v_serve_speed_data:
            # Bind deuce court table with data
            dc_table.data = self.return_v_serve_speed_data[type]
            dc_table.type = type

            dc_table.draw("A", self.pdf.tables_start_num)
            self.pdf.tables_start_num += 1

            # Update y_offset
            dc_table.y_offset = self.pdf.y

        self.pdf.cell(0, line_height, f"Return: {returned_by}", align="C")

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
