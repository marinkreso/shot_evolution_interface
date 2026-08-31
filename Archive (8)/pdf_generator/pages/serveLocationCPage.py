from pdf_generator.services.constants import SERVE_LOCATION_1C_PARAGRAPH


class ServeLocationCPage:
    visual_counter = 2
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 1220

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.fpdf.set_header_title(f"Where {self.player1} serves on {duplicates} ")
        self.fpdf.set_header_sub_title(f"{duplicates} serve: placement")
        self.title = f"Serve & in %: {self.player1}"
        self.sub_title = f"Return: {self.player2}"
        self.name = f"Serve Location C {duplicates} Page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(2 if self.duplicates == "1st" else 4)

        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(90, 39, self.title)
        self.fpdf.text(98.5, 39 + line_height, self.sub_title)
        self.fpdf.ln(line_height * 3.25)

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, SERVE_LOCATION_1C_PARAGRAPH)

        visuals_keys = (3, 8) if self.duplicates == "1st" else (18, 23)
        for key, x, y, width, title, id_y_offset, title_y_offset in zip(
            visuals_keys,
            (50, 17),
            (75, 150),
            (120, 185),
            (
                "serve - All points",
                "serve location - All points",
            ),
            (70, 93),
            (5, 0),
        ):
            # Writing visual title
            self.fpdf.set_font("Din Medium", size=11)
            self.fpdf.set_text_color(0, 0, 0)
            self.fpdf.set_y(y - title_y_offset)
            self.fpdf.set_x(x)
            self.fpdf.cell(width, txt=f"{self.duplicates} {title}", align="C")

            # Generating and placing the visual
            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                x,
                y,
                w=width,
            )

            # Writing visual number
            self.fpdf.set_font(family="Din", size=10)
            self.fpdf.set_y(y + id_y_offset)  #
            self.fpdf.set_x(x)
            self.fpdf.cell(width, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        self.fpdf.set_font(family="Din Italic", size=9)
        self.fpdf.set_y(248)
        self.fpdf.cell_normal(
            0,
            4,
            f"* {self.report_metadata['MT']} matches with serve ball placement data (bottom visual) vs. {self.report_metadata['Basic']} matches with data for serve direction (top visual) / other visuals in the report",
            align="C",
        )

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(90, 260, self.title)
        self.fpdf.text(98.5, 264, self.sub_title)
