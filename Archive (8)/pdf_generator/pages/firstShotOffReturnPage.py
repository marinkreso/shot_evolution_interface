from pdf_generator.services.constants import (
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
    CURDIRPATH,
    FIRST_SHOT_OFF_RETURN_PARAGRAPH,
)


class FirstShotOffReturnPage:
    visual_counter = 6
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 2800

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.serve_number = "1st" if duplicates == "First" else "2nd"
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(
            f"Where to return {self.player1} {self.serve_number} serve"
        )
        self.fpdf.set_header_sub_title(
            f"Serve+1 after {self.serve_number} serve: quality"
        )
        self.title = f"Serve, Serve+1 & points won:  {self.player1}"
        self.subtitle = f"Return:  {self.player2}"
        self.name = f"first shot off return {duplicates} page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(3 if self.serve_number == "1st" else 5)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(63, 39, self.title)
        self.fpdf.text(101.3, 39 + line_height, self.subtitle)
        self.fpdf.ln(line_height * 2.7)

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_x(16)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.multi_cell_normal(175, 5, FIRST_SHOT_OFF_RETURN_PARAGRAPH)

        visual_keys = (
            (9, 10, 11, 12, 13, 14)
            if self.serve_number == "1st"
            else (24, 25, 26, 27, 28, 29)
        )
        for key, x, y, title in zip(
            visual_keys,
            (8, 112) * 3,
            (67, 67, 130, 130, 193, 193),
            ("Deuce Wide", "Ad Wide", "Deuce Body", "Ad Body", "Deuce T", "Ad T"),
        ):
            self.fpdf.set_font("Din Medium", size=9)
            self.fpdf.set_y(y - 4)
            self.fpdf.set_x(x + 5)
            self.fpdf.cell(
                85,
                txt=f"Serve+1 win% after {self.serve_number} {title} Serve",
                align="C",
            )

            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                x,
                y,
                w=96,
            )

            self.fpdf.set_font("Din", size=9)
            self.fpdf.set_y(y + 55)
            self.fpdf.set_x(x + 5)
            self.fpdf.cell(85, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        # Footer
        # Player info
        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.text(63, 257, self.title)
        self.fpdf.text(101.3, 261, self.subtitle)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_fs.png", 155, 252, 7.5, 13, type="png"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("returns"))
