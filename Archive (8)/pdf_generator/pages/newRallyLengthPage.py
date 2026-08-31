from pdf_generator.services.constants import (
    CURDIRPATH,
    FOOTER_TEXT,
    RALLY_LENGTH_PARAGRAPH,
)


class RallyLengthPage:
    visual_counter = 3
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 990

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title("Rallies and groundstrokes ")
        self.fpdf.set_header_sub_title("Rally length")
        self.name = f"New Rally Length page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(12)
        self.fpdf.add_page()
        self.fpdf.ln(11)

        # writing paragraph
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.set_font("Din", size=11)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, RALLY_LENGTH_PARAGRAPH)

        visuals_keys = (77, 78, 79)
        for (
            key,
            y,
        ) in zip(
            visuals_keys,
            (47, 118, 189),
        ):
            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                50,
                y,
                w=116,
            )
            self.fpdf.set_font("Din", size=11)
            self.fpdf.set_y(y + 66.5)
            self.fpdf.set_x(55)
            self.fpdf.cell(105, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        # Number of shots annotation
        self.fpdf.set_font(family="Din Italic", size=9)
        self.fpdf.set_text_color(127, 127, 127)
        self.fpdf.set_y(55)
        self.fpdf.set_x(17)
        self.fpdf.multi_cell_normal(
            50,
            5,
            f"Number of shots in\nrally, but split by\nserver (e.g. 2 4\nshots = all rallies\nwith 2, 3 or 4 shots\nwhen {self.player1}\nwas serving",
            align="L",
        )
        # pointing arrow
        self.fpdf.image(f"{CURDIRPATH}/assets/RED_anno_24.png", 50, 61, 17)

        self.fpdf.set_font("Din", "", 12)
        self.fpdf.set_text_color(255, 255, 255)

        # self.fpdf.set_font("Din Italic", "", 8)
        # s = FOOTER_TEXT
        # self.fpdf.text(
        #     (self.fpdf.w / 2) - self.fpdf.get_string_width(s) / 2, self.fpdf.h - 3, s
        # )
