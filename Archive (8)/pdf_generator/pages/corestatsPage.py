class CoreStats:
    visual_counter = 0
    table_counter = 0
    execution_cost = 20

    def __init__(self, fpdf, data_repo, variant):
        super().__init__()
        self.fpdf = fpdf
        self.fpdf.set_header_title("Summary")
        self.fpdf.set_header_sub_title("Summary statistics")
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.name = "Core Stats Page"

    def divide(self, n1, n2, default=0):
        try:
            return n1 / n2
        except:
            return default

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(1)
        self.fpdf.add_page()
        self.fpdf.ln(20)
        core_stats_dic = self.data_repo.core_stats_table_data()
        serve_stats_dic = self.data_repo.serve_stats_table_data()

        self.fpdf.set_line_width(0.4)
        self.fpdf.set_left_margin(97)

        # Draw table header
        self.fpdf.set_fill_color(217, 217, 217)
        self.fpdf.set_font("Din Bold", style="", size=10)
        th = self.fpdf.font_size

        self.fpdf.cell(47, 1.5 * th, self.player1, border=1, align="C", fill=True)
        self.fpdf.set_fill_color(191, 191, 191)
        self.fpdf.cell(47, 1.5 * th, self.player2, border=1, align="C", fill=True)

        self.fpdf.set_font("Din", style="", size=11)
        self.fpdf.set_fill_color(255, 255, 255)
        self.fpdf.set_left_margin(25)
        self.fpdf.ln(1.5 * th)

        # Draw coreStatsTable
        for i in core_stats_dic["Player1"]["Value"]:
            height = 1.5
            if i == "Total Tiebreakers":
                break
            if i == "Pressure Pt faced win %":
                self.fpdf.set_font("Din Bold", style="", size=10)
                self.fpdf.cell(72, 2.5 * th, "", border=1, align="C")
                self.fpdf.set_font("Din", style="", size=11)
                height = 2.5
            else:
                self.fpdf.set_font("Din Bold", style="", size=10)
                self.fpdf.cell(72, height * th, i, border=1, align="C")
                self.fpdf.set_font("Din", style="", size=11)
            if i == "Total serve Games" or i == "Total serve Games Won":
                self.fpdf.set_fill_color(255, 255, 255)
                self.fpdf.cell(
                    47,
                    height * th,
                    str(core_stats_dic["Player1"]["Value"][i]),
                    border=1,
                    align="C",
                )
                self.fpdf.set_fill_color(242, 242, 242)
                self.fpdf.cell(
                    47,
                    height * th,
                    str(core_stats_dic["Player2"]["Value"][i]),
                    border=1,
                    align="C",
                    fill=True,
                )
            else:
                self.fpdf.set_fill_color(255, 255, 255)

                self.fpdf.cell(
                    47,
                    height * th,
                    "{:.0%}".format(float(core_stats_dic["Player1"]["Value"][i])),
                    border=1,
                    align="C",
                )
                self.fpdf.set_fill_color(242, 242, 242)
                self.fpdf.cell(
                    47,
                    height * th,
                    "{:.0%}".format(float(core_stats_dic["Player2"]["Value"][i])),
                    border=1,
                    align="C",
                    fill=True,
                )
            self.fpdf.ln(height * th)

        self.fpdf.ln(2)
        self.fpdf.set_x((self.fpdf.w / 2) - 10)
        self.fpdf.cell(50, 1.5 * th, "Table 1")

        self.fpdf.ln(15)

        self.fpdf.set_left_margin(97)
        self.fpdf.set_fill_color(217, 217, 217)
        self.fpdf.set_font("Din Bold", style="", size=10)
        self.fpdf.cell(47, 1.5 * th, self.player1, border=1, align="C", fill=True)
        self.fpdf.set_fill_color(191, 191, 191)
        self.fpdf.cell(47, 1.5 * th, self.player2, border=1, align="C", fill=True)
        self.fpdf.set_font("Din", style="", size=11)
        self.fpdf.set_fill_color(255, 255, 255)
        self.fpdf.set_left_margin(25)
        self.fpdf.ln(1.5 * th)

        # Draw serveStatsTable
        for i in serve_stats_dic["Player1"]["Value"]:
            height = 1.5
            if (
                i == "Serves with poor returns/game"
                or i == "Serves with aggressive return/game"
                or i == "Serves with killer returns/game"
            ):
                self.fpdf.set_font("Din Bold", style="", size=10)
                self.fpdf.cell(72, 2.5 * th, "", border=1, align="C")
                self.fpdf.set_font("Din", style="", size=11)
                height = 2.5
            else:
                self.fpdf.set_font("Din Bold", style="", size=10)
                self.fpdf.cell(72, height * th, i, border=1, align="C")
                self.fpdf.set_font("Din", style="", size=11)
            if (
                i == "Serves with poor returns/game"
                or i == "Serves with aggressive return/game"
                or i == "Serves with killer returns/game"
            ):
                value1 = self.divide(
                    n1=int(serve_stats_dic["Player1"]["Value"][i]),
                    n2=int(core_stats_dic["Player1"]["Value"]["Total serve Games"])
                    + int(core_stats_dic["Player1"]["Value"]["Total Tiebreakers"]),
                )

                value2 = self.divide(
                    n1=int(serve_stats_dic["Player2"]["Value"][i]),
                    n2=int(core_stats_dic["Player2"]["Value"]["Total serve Games"])
                    + int(core_stats_dic["Player2"]["Value"]["Total Tiebreakers"]),
                )

                self.fpdf.set_fill_color(255, 255, 255)
                self.fpdf.cell(
                    47, height * th, str(round(value1, 2)), border=1, align="C"
                )
                self.fpdf.set_fill_color(242, 242, 242)
                self.fpdf.cell(
                    47,
                    height * th,
                    str(round(value2, 2)),
                    border=1,
                    align="C",
                    fill=True,
                )
            else:
                self.fpdf.set_fill_color(255, 255, 255)
                self.fpdf.cell(
                    47,
                    height * th,
                    str(round(serve_stats_dic["Player1"]["Value"][i], 2)),
                    border=1,
                    align="C",
                )
                self.fpdf.set_fill_color(242, 242, 242)
                self.fpdf.cell(
                    47,
                    height * th,
                    str(round(serve_stats_dic["Player2"]["Value"][i], 2)),
                    border=1,
                    align="C",
                    fill=True,
                )
            self.fpdf.ln(height * th)

        self.fpdf.ln(2)
        self.fpdf.set_x((self.fpdf.w / 2) - 10)
        self.fpdf.cell(50, 1.5 * th, "Table 2")

        # draw hardcoded positioned text
        self.fpdf.set_font("Din Bold", style="", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(39, 108, "Pressure Pt faced win %")
        self.fpdf.text(30, 181, "Serves with poor returns/game")
        self.fpdf.text(27, 190, "Serves with aggressive return/game")
        self.fpdf.text(32, 199, "Serves with killer returns/game")

        self.fpdf.set_font("Din", style="", size=7)
        self.fpdf.text(30, 112, "Pressure: 0-30, 15-30, 30-30 & all (tie) break points")
        self.fpdf.text(34, 185, "Poor return = server wins in 5 shots or less")
        self.fpdf.text(33, 194, "Aggressive return = returner wins in 2-5 shots")
        self.fpdf.text(37, 203, "Killer return = returner wins in 2-3 shots")
