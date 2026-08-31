from pdf_generator.services.constants import IMAGE_LOGO_PATH_BLACK, HEADER_FOOTER_TEXT


class Header:
    visual_counter = 0
    table_counter = 0
    execution_cost = 23

    def __init__(self, FPDF, data_repo, title):
        self.name = "Cover Page"
        self.pdf = FPDF
        self.title = title
        self.game_selection = data_repo.get_game_selection()
        self.set_selection = data_repo.get_set_selection()
        self.serve_selection = data_repo.get_serve_selection()
        self.sub_titles = data_repo.cover_page_sub_titles()
        self.player1, self.player2 = data_repo.players_name()

    def build_page_body(self):
        self.pdf.set_preset("cover")
        self.pdf.add_page()

        # Config
        self.pdf.set_fill_color(217, 217, 217)
        self.pdf.set_font(family="Din", size=19)
        line_height = self.pdf.font_size * 1.25

        # Page headers
        # Gray rectangle
        self.pdf.rect(26, 45, self.pdf.w - 52, self.pdf.h / 6.2, style="F")

        # Title
        self.pdf.set_y(51)
        self.pdf.cell(0, line_height, self.title, align="C")
        self.pdf.ln(line_height * 1.25)

        # Subtitle
        self.pdf.cell(
            0,
            line_height,
            f'- {self.player1} vs. {self.player2 if not (self.player2[0].isdigit() and "Opponents" in self.player2) else "Opponents"} -',
            align="C",
        )
        self.pdf.ln(line_height)

        # Details
        self.pdf.set_font(family="Din", size=15)

        is_scouting = True if "Scouting" in self.title else False
        if is_scouting:
            subTitle = f'({",".join(self.sub_titles["subTitle"].split(",")[:-1])})'
        else:
            subTitle = self.sub_titles["subTitle"]

        if self.game_selection.value == "All":
            if self.serve_selection.value != "All":
                subTitle = (
                    subTitle
                    + ", "
                    + f"({self.game_selection.value} Games as {self.serve_selection.value})"
                )
        else:
            if self.serve_selection.value != "All":
                subTitle = (
                    subTitle
                    + ", "
                    + f"({self.game_selection.value} Games as {self.serve_selection.value})"
                )
            else:
                subTitle = subTitle + ", " + f"({self.game_selection.value} Games)"

        if self.set_selection.value != "All":
            subTitle = subTitle + f", ({self.set_selection.value} Sets)"

        self.pdf.cell(0, line_height, subTitle, align="C", ln=True)

        opponent_handedness = {
            0: " Against Right-Handed Players",
            1: " Against Left-Handed Players",
            2: "",
            3: "",
        }
        matches_count = f'{self.sub_titles["noOfMatches"]} Match{"es" if self.sub_titles["noOfMatches"]>1 else""}{opponent_handedness[self.sub_titles["OpponentHandedness"]]}'
        self.pdf.cell(0, line_height, matches_count, align="C")

        # Company logo
        self.pdf.image(IMAGE_LOGO_PATH_BLACK, 67, 100, 85, 85)

        # Footer text
        self.pdf.set_font(family="Din", size=9)
        self.pdf.set_y(-50)
        self.pdf.multi_cell_normal(0, 5.5, HEADER_FOOTER_TEXT, align="C")
