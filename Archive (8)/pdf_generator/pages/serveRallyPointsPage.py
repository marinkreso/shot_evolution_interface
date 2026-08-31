import pdf_generator.services.drawingTables as TableDrawing
from pdf_generator.services.constants import SERVE_RALLY_POINTS_PARAGRAPH, FOOTER_TEXT


class AppendixPage4:
    visual_counter = 0
    table_counter = 2
    execution_cost = 10

    def __init__(self, FPDF, data_repo, serve_no) -> None:
        """
        serve_no is one of ('1st', '2nd')
        """
        self.name = f"Appendix Page 4 for {serve_no} serve"
        self.pdf = FPDF
        self.data_repo = data_repo
        self.serve_no = serve_no
        self.player_name, self.player2_name = data_repo.players_name()

    def build_page_body(self):
        # TODO page_no, move container to super class
        # header and footer for footer_text,page_no
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Border
        left_margin = 20
        top_margin = 20

        # Title & subtitle
        line_height = 7
        self.pdf.set_y(25)

        if self.serve_no == "1st":
            self.pdf.set_font("ROCK Bold", size=13)
            self.pdf.cell(0, line_height, "Serve rally Points Won", ln=True, align="C")

        for is_pressure_pts in (False, True):
            # Config
            self.pdf.set_font("ROCK Bold", size=12)

            points_type = "" if is_pressure_pts else "Non "
            self.pdf.cell(
                0,
                line_height,
                f"{self.serve_no} Serve Rally Pts Won ({points_type}Pressure Points)",
                align="C",
                ln=True,
            )

            # Paragraph section
            if self.serve_no == "1st" and not is_pressure_pts:
                self.pdf.set_font("ROCK", size=10)
                self.pdf.set_x(22.9)
                self.pdf.multi_cell(165, 4.1, SERVE_RALLY_POINTS_PARAGRAPH)
                self.pdf.ln(line_height * 0.75)

            # Table config
            offset = 22.9
            self.pdf.set_font_size(11)
            table_data = self.data_repo.serve_rally_points(
                self.serve_no, is_pressure_pts
            )

            self.pdf.set_fill_color(204, 204, 204)
            TableDrawing.RallyPointsTable(
                self.pdf,
                table_data,
                x_offset=offset,
                is_pressure_pts=is_pressure_pts,
                player_name=self.player_name,
                opponent_name=self.player2_name,
            ).draw("A", self.pdf.tables_start_num)
            self.pdf.tables_start_num += 1

        # Page footer
        self.pdf.set_y(-23)
        self.pdf.set_font("Calibrii", size=7)
        self.pdf.cell(0, self.pdf.font_size, FOOTER_TEXT, align="C")
