from pdf_generator.services.constants import IMAGE_LOGO_PATH_BLACK


class Appendix:
    visual_counter = 0
    table_counter = 0
    execution_cost = 1

    def __init__(self, FPDF, data_repo, title):
        self.name = "Appendix Page"
        self.fpdf = FPDF
        self.title = title
        self.player1, self.player2 = data_repo.players_name()
        self.sub_titles = data_repo.cover_page_sub_titles()
        self.name = "Appendix Page"

    def build_page_body(self):
        self.fpdf.set_preset("cover")
        self.fpdf.add_page()
        # Draw black background
        self.fpdf.set_fill_color(0, 0, 0)
        self.fpdf.rect(0, 0, self.fpdf.w, self.fpdf.h, style="F")
        self.fpdf.set_y(5)
        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(200, 200, 200)

        # Draw white page overlapping the black background
        self.fpdf.set_fill_color(255, 255, 255)
        self.fpdf.rect(7, 17, self.fpdf.w - 14, self.fpdf.h - 28, style="F")

        # Draw Title gray box
        self.fpdf.set_fill_color(217, 217, 217)
        self.fpdf.rect(26, 45, self.fpdf.w - 52, self.fpdf.h / 6.2, style="F")

        # Write title box content
        title = "Appendix"
        self.fpdf.set_font(family="Din", size=19)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.set_y(50)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.set_font_size(19)
        self.fpdf.cell(0, 10, title, align="C", ln=True)

        # Subtitle
        self.fpdf.cell(
            0,
            line_height,
            f'- {self.player1} vs. {self.player2 if not self.player2[0].isdigit() else "Opponents"} -',
            align="C",
        )
        self.fpdf.ln(line_height)

        self.fpdf.set_font("Din", style="", size=15)
        is_scouting = True if "Scouting" in self.title else False
        if is_scouting:
            subTitle = f'({",".join(self.sub_titles["subTitle"].split(",")[:2])})'
        else:
            subTitle = self.sub_titles["subTitle"]

        self.fpdf.cell(0, line_height, subTitle, align="C", ln=True)

        opponent_handedness = {
            0: " Against Right-Handed Players",
            1: " Against Left-Handed Players",
            2: "",
            3: "",
        }

        matches_count = f'{self.sub_titles["noOfMatches"]} Match{"es" if self.sub_titles["noOfMatches"]>1 else""}{opponent_handedness[self.sub_titles["OpponentHandedness"]]}'
        self.fpdf.cell(0, line_height, matches_count, align="C")

        # Company logo
        self.fpdf.image(IMAGE_LOGO_PATH_BLACK, 67, 100, 85, 85)
