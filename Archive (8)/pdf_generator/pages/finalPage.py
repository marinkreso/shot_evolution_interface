from pdf_generator.services.constants import *


class Final:
    visual_counter = 0
    table_counter = 0
    execution_cost = 8

    def __init__(self, fpdf, data_repo, variant):
        super().__init__()
        self.fpdf = fpdf
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.width = self.fpdf.w
        self.height = self.fpdf.h
        self.name = "Final Page"

    def build_page_body(self):
        self.fpdf.set_preset("cover")
        self.fpdf.add_page()

        self.fpdf.image(IMAGE_LOGO_PATH_BLACK, 66, 50, 85, 85)

        self.fpdf.image(FINAL_TEXT, 43, 120, 130, 28)

        self.fpdf.image(DIVIDER, 42, 150, 132, 0.15)

        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.set_font("helvetica", style="B", size=12)
        s = "Contact"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 166, s)
        self.fpdf.set_font("helvetica", style="", size=12)
        s = "3830 Valley Centre Dr., Suite 705-812"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 171, s)
        s = "San Diego, CA 92130"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 176, s)
        self.fpdf.set_font("helvetica", style="", size=11)
        s = "www.goldensetanalytics.com"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 181, s)
        self.fpdf.set_font("helvetica", style="", size=12)
        s = "info@goldensetanalytics.com"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 186, s)
        s = "1-818-430-8294"
        self.fpdf.text((self.width / 2) - self.fpdf.get_string_width(s) / 2, 191, s)

        # Footer text
        self.fpdf.set_font(family="Din", size=9)
        self.fpdf.set_y(-50)
        self.fpdf.multi_cell(0, 5.5, HEADER_FOOTER_TEXT, align="C")
