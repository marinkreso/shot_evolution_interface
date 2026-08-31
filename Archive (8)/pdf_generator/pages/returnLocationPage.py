from pdf_generator.services.constants import (
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
    CURDIRPATH,
    RETURN_LOCATION_PARAGRAPH,
)


class ReturnLocationPage:
    visual_counter = 6
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 3140

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.serve_number = "1st" if duplicates == "First" else "2nd"
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(
            f"Where {self.player1} returns {self.serve_number} serve"
        )
        self.fpdf.set_header_sub_title(
            f"Return of {self.serve_number} serve: direction"
        )
        self.title = f"Return & points won:  {self.player1}"
        self.subtitle = f"Serve:  {self.player2}"
        self.name = f"return location {duplicates} page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(7 if self.serve_number == "1st" else 9)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(73, 38, self.title)
        self.fpdf.text(101, 38 + line_height, self.subtitle)
        self.fpdf.ln(line_height * 3)
        self.fpdf.set_font("Din", style="", size=10)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 4, RETURN_LOCATION_PARAGRAPH)

        self.fpdf.ln(7)

        w = 96
        visual_keys = (
            (41, 42, 43, 44, 45, 46)
            if self.serve_number == "1st"
            else (58, 59, 60, 61, 62, 63)
        )
        for key, x, y, title in zip(
            visual_keys,
            (8, 112) * 3,  # 6, 4
            (64, 64, 129, 129, 194, 194),
            ("Deuce Wide", "Ad Wide", "Deuce Body", "Ad Body", "Deuce T", "Ad T"),
        ):
            self.fpdf.set_font("Din Medium", size=10)
            self.fpdf.set_y(y - 4)
            self.fpdf.set_x(x)
            self.fpdf.cell(
                w, txt=f"Return direction - {self.serve_number} {title}", align="C"
            )

            self.fpdf.image(self.visuals_generator.generate_visual(key), x, y, w)

            self.fpdf.set_font("Din", size=9)
            self.fpdf.set_y(y + 55)
            self.fpdf.set_x(x)
            self.fpdf.cell(w, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(73, 260, self.title)
        self.fpdf.text(101, 260 + line_height, self.subtitle)
        self.fpdf.ln(line_height * 2)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_A.jpg", 155, 252, 7.5, 13, type="jpg"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("returns"))
