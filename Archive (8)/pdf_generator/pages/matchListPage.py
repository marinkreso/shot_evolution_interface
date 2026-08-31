import os


class MatchList:
    visual_counter = 0
    table_counter = 0
    execution_cost = 3

    def __init__(self, fpdf, data_repo, variant):
        super().__init__()
        self.fpdf = fpdf
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.width = self.fpdf.w
        self.name = "Match List Page"
        self.fpdf.set_header_sub_title(f"Match list")

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.add_page()

        self.fpdf.set_fill_color(0, 0, 0)
        self.fpdf.rect(0, 14, self.fpdf.w, 9, style="F")

        self.fpdf.ln(15)

        match_list_table = self.data_repo.match_list_table()
        # draw header
        self.fpdf.set_font("Din Bold", style="", size=9)
        th = self.fpdf.font_size
        self.fpdf.set_left_margin(23)
        self.fpdf.set_line_width(0.4)
        self.fpdf.cell(7, 1.5 * th, "#", border=1, align="C")
        self.fpdf.cell(97, 1.5 * th, "Match ", border=1)
        self.fpdf.cell(21, 1.5 * th, "Winner ", border=1, align="C")
        self.fpdf.cell(45, 1.5 * th, "Score ", border=1, align="C")
        self.fpdf.ln(1.5 * th)

        self.fpdf.set_font("Din", style="", size=8)

        # Draw table
        for i in range(0, 40):
            if i < len(match_list_table["Winner"]):
                x = match_list_table["Match"][i].split("--")[0:4]
                # TODO Cleaning
                z = x[0].replace("_R", "").replace("_L", "").split("-")
                y = " - ".join(z) + ", " + ", ".join(x[1:])
                y = os.path.splitext(y)[0]
                self.fpdf.cell(7, 1.5 * th, str(i + 1), border=1, align="C")
                self.fpdf.cell(97, 1.5 * th, y, border=1)
                winner = ""
                for j in range(0, len(str(match_list_table["Winner"][i]))):
                    if j == 12:
                        break
                    winner += str(match_list_table["Winner"][i][j])
                self.fpdf.cell(21, 1.5 * th, winner, border=1)
                self.fpdf.cell(
                    45, 1.5 * th, str(match_list_table["Score"][i]), border=1, align="C"
                )
                self.fpdf.ln(1.5 * th)
            else:
                self.fpdf.cell(7, 1.5 * th, "", border=1, align="C")
                self.fpdf.cell(97, 1.5 * th, "", border=1)
                self.fpdf.cell(21, 1.5 * th, "", border=1, align="C")
                self.fpdf.cell(45, 1.5 * th, "", border=1, align="C")
                self.fpdf.ln(1.5 * th)

        self.fpdf.set_font(family="Din Italic", size=8)
        # Number of matches included
        self.fpdf.set_y(244)
        self.fpdf.cell(
            0,
            10,
            f"*{self.report_metadata['GS']} matches with groundstrokes vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )
