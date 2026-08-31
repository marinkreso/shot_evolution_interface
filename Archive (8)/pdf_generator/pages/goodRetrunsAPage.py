from pdf_generator.services.constants import (
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
    CURDIRPATH,
    GOOD_RETURNS_1A_PARAGRAPH,
)


class GoodReturnsA:
    visual_counter = 2
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 1550

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(
            f"Where to serve to {self.player1} on {self.duplicates}"
        )
        self.fpdf.set_header_sub_title(
            f"Return of {self.duplicates} serve: in and points won"
        )
        self.title = f"Return & points won: {self.player1}"
        self.sub_title = f"Serve: {self.player2}"
        self.name = f"Good Returns A {self.duplicates} Page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(6 if self.duplicates == "1st" else 8)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(77, 38, self.title)
        self.fpdf.text(105, 38 + line_height, self.sub_title)
        self.fpdf.ln(line_height * 2.75)

        self.fpdf.set_font(family="Din", size=12)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, GOOD_RETURNS_1A_PARAGRAPH)

        self.fpdf.ln(5)
        visuals_keys = (35, 36) if self.duplicates == "1st" else (52, 53)
        for key, y, title in zip(
            visuals_keys, (68, 163), ("In returns", "Points won on return")
        ):
            self.fpdf.set_font("Din Medium", size=11)
            self.fpdf.set_y(y - 5)
            self.fpdf.set_x(55)
            self.fpdf.cell(105, txt=f"{title} - {self.duplicates} serve", align="C")

            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                35,
                y,
                w=145,
            )
            self.fpdf.set_font("Din", size=11)
            self.fpdf.set_y(y + 84)
            self.fpdf.set_x(55)
            self.fpdf.cell(105, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(77, 260, self.title)
        self.fpdf.text(105, 260 + line_height, self.sub_title)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_GR.jpg", 155, 252, 7.5, 13, type="jpg"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("serves"))

        # Reset font color
        self.fpdf.set_text_color(0, 0, 0)
