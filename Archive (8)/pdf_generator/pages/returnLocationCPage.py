from pdf_generator.services.constants import RETURN_LOCATION_1C_PARAGRAPH


class ReturnLocationCPage:
    visual_counter = 1
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 600

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.report_metadata = self.data_repo.report_metadata()
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(
            f"Where to return {self.player1} {duplicates} serve "
        )
        self.fpdf.set_header_sub_title(f"Return of {duplicates} serve: placement")
        self.title = f"Return placement: {self.player2}"
        self.sub_title = f"Serve: {self.player1}"
        self.name = f"return Location C {duplicates} page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(3 if self.duplicates == "1st" else 5)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(81, 38, self.title)
        self.fpdf.text(105, 38 + line_height, self.sub_title)
        self.fpdf.ln(line_height * 3.2)

        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.set_font("Din", size=13)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, RETURN_LOCATION_1C_PARAGRAPH)

        x, y, w = 17, 70, 182
        key = 15 if self.duplicates == "1st" else 30

        self.fpdf.set_font("Din Medium", size=11)
        self.fpdf.set_y(y - 5)
        self.fpdf.set_x(x + 3)
        self.fpdf.cell(
            w, txt=f"Return of {self.duplicates} serve - Placement", align="C"
        )

        self.fpdf.image(self.visuals_generator.generate_visual(key), x, y, w)

        self.fpdf.set_font("Din", size=10)
        self.fpdf.set_y(y + 162)
        self.fpdf.set_x(x + 3)
        self.fpdf.cell(w, txt=f"Visual {self.fpdf.visuals_no}", align="C")
        self.fpdf.visuals_no += 1

        self.fpdf.set_font(family="Din Italic", size=9)
        self.fpdf.set_y(246)
        self.fpdf.cell_normal(
            0,
            4,
            f"* {self.report_metadata['MT']} matches with return ball placement data (this page) vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(81, 260, self.title)
        self.fpdf.text(105, 264, self.sub_title)
