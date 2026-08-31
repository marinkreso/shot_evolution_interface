from pdf_generator.services.constants import RETURN_LOCATION_1C_PARAGRAPH


class RallyScatterPlotPage:
    visual_counter = 1
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 520

    def __init__(self, fpdf, data_repo, table_no, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.table_no = table_no
        self.report_metadata = self.data_repo.report_metadata()
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(f"Rallies and groundstrokes")
        sub_title = {
            9: f"{self.player1} Rally",
            10: f"{self.player1} FH",
            11: f"{self.player1} BH",
            12: f"{self.player2} Rally",
            13: f"{self.player2} FH",
            14: f"{self.player2} BH",
        }
        self.fpdf.set_header_sub_title(f"{sub_title[table_no]} Shot")
        self.title = f"{sub_title[table_no]} Shot"
        self.sub_title = f"player: {self.player1}"
        self.name = f"Scatter plot for table {table_no}"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(12)
        self.fpdf.add_page()
        self.fpdf.ln(9)

        # self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        # self.fpdf.ln(line_height * 2.85)

        self.fpdf.set_text_color(0, 0, 0)

        x, y, w = 17, 55, 182
        keys = {
            9: 112,
            10: 113,
            11: 114,
            12: 115,
            13: 116,
            14: 117,
        }
        key = keys[self.table_no]

        self.fpdf.set_font("Din Medium", size=11)
        self.fpdf.set_y(y - 7)
        self.fpdf.set_x(x)
        self.fpdf.cell(w, txt=self.title, align="C")

        self.fpdf.image(self.visuals_generator.generate_visual(key), x, y, w)

        self.fpdf.set_font("Din", size=10)
        self.fpdf.set_y(y + 160)
        self.fpdf.set_x(x)
        self.fpdf.cell(w, txt=f"Visual {self.fpdf.visuals_no}", align="C")
        self.fpdf.visuals_no += 1

        self.fpdf.set_font(family="Din Italic", size=8)
        self.fpdf.set_y(246)
        self.fpdf.cell(
            0,
            4,
            f"* {self.report_metadata['MT']} matches with return ball placement data (this page), vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        # self.fpdf.text(75, 260, self.title)
        self.fpdf.text(102, 260, self.sub_title)
