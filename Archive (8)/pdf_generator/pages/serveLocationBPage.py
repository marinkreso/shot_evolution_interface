from pdf_generator.services.constants import (
    SERVE_LOCATION_1B_PARAGRAPH,
    CURDIRPATH,
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
)


class ServeLocationB:
    visual_counter = 4
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 2800

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(f"Where {self.player1} serves on {self.duplicates}")
        self.fpdf.set_header_sub_title(f"{self.duplicates} serve:  direction and win %")
        self.title = f"Serve & points won:  {self.player1}"
        self.sub_title = f"Return:  {self.player2}"
        self.name = f"Serve Location B {self.duplicates} Page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(2 if self.duplicates == "1st" else 4)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(81, 39, self.title)
        self.fpdf.text(103, 39 + line_height, self.sub_title)
        self.fpdf.ln(line_height * 3.25)

        self.fpdf.set_font("Din", size=10)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, SERVE_LOCATION_1B_PARAGRAPH)

        self.fpdf.ln(5)

        visuals_keys = (3, 4, 5, 6) if self.duplicates == "1st" else (18, 19, 20, 21)

        for key, x, y, title in zip(
            visuals_keys,
            (10, 110, 10, 110),
            (70, 70, 155, 155),
            (
                "All points",
                "Non pressure points",
                "Pressure points\u00B9",
                "Break points",
            ),
        ):
            # Writing visual title
            self.fpdf.set_font(family="Din Medium", size=11)
            self.fpdf.set_text_color(0, 0, 0)
            self.fpdf.set_y(y - 5)
            self.fpdf.set_x(x + 5)
            self.fpdf.cell(85, txt=f"{self.duplicates} serve - {title}", align="C")

            # Generating and placing the visual
            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                x,
                y,
                w=96,
            )

            # Writing visual number
            self.fpdf.set_font(family="Din", size=10)
            self.fpdf.set_y(y + 55)
            self.fpdf.set_x(x + 5)
            self.fpdf.cell(85, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        self.fpdf.set_font("Din", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.ln(10)
        self.fpdf.set_left_margin(20)
        self.fpdf.set_right_margin(20)
        self.fpdf.set_y(230)
        # self.fpdf.set_x(25)
        self.fpdf.multi_cell_normal(
            0,
            6,
            "\u00B9 Pressure point: any point that can lead to a break point (0-30, 15-30, 30-30, deuce), all break points, and all tiebreak points.",
        )
        self.fpdf.set_right_margin(8)

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(81, 260, self.title)
        self.fpdf.text(103, 260 + line_height, self.sub_title)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_A.jpg", 155, 252, 7.5, 13, type="jpg"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("serves"))
