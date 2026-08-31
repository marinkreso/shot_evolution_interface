from pdf_generator.services.constants import RALLY_ENDING_TABLE_PARAGRAPH


class RallyEndingTable:
    visual_counter = 0
    table_counter = 0
    execution_cost = 13

    def __init__(self, fpdf, data_repo, variant):
        super().__init__()
        self.fpdf = fpdf
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.fpdf.set_header_title("Rallies and groundstrokes ")
        self.fpdf.set_header_sub_title("Rally ending shot summary table")
        self.title = f"Player: {self.player1}"
        self.name = f"Rally Ending table page"

    def divide(self, n1, n2, default=0):
        try:
            return n1 / n2
        except:
            return default

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(12)

        self.fpdf.add_page()
        self.fpdf.ln(7)

        self.fpdf.set_font(family="Din", size=12)
        self.fpdf.set_y(38)
        self.fpdf.set_x(16)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.multi_cell_normal(175, 5, RALLY_ENDING_TABLE_PARAGRAPH)

        self.fpdf.ln(10)

        rally_ending_dic = self.data_repo.rally_ending_table_data()

        # draw table

        self.fpdf.set_font("Din Bold", style="", size=11)
        th = self.fpdf.font_size
        self.fpdf.set_left_margin(24)
        self.fpdf.set_line_width(0.4)
        self.fpdf.set_fill_color(217, 217, 217)

        # draw table header
        self.fpdf.set_font("Din Bold", style="", size=7)
        prev_y = self.fpdf.get_y()
        self.fpdf.cell(60, 4.5 * th, "All Rallies", border=1, align="C", fill=True)
        prev_x1 = self.fpdf.get_x()
        self.fpdf.cell(
            40.5, 2.25 * th, f"{self.player1}", border=1, align="C", fill=True
        )
        prev_x2 = self.fpdf.get_x()
        self.fpdf.cell(
            40.5, 2.25 * th, f"{self.player2}", border=1, align="C", fill=True
        )
        prev_x3 = self.fpdf.get_x()
        self.fpdf.set_y(66.7)
        self.fpdf.set_x(prev_x1)
        self.fpdf.cell(
            40.5, 2.25 * th, " Winner     Forcing   Unforced", border=1, fill=True
        )
        self.fpdf.set_x(prev_x2)
        self.fpdf.cell(
            40.5, 2.25 * th, " Winner     Forcing   Unforced", border=1, fill=True
        )
        self.fpdf.set_y(prev_y)
        self.fpdf.set_x(prev_x3)
        self.fpdf.cell(13.5, 4.5 * th, "", border=1, fill=True)
        self.fpdf.cell(13.5, 4.5 * th, "", border=1, fill=True)

        # place last two positioned text cell
        player1_name = ""
        for i in range(len(self.player1)):
            if i == 7:
                break
            player1_name += self.player1[i]
        # self.fpdf.text(prev_x3 + 0.5, prev_y + 8, player1_name)
        # self.fpdf.text(prev_x3 + 3.5, prev_y + 12, 'Effic.')
        self.fpdf.set_y(prev_y + 5)
        self.fpdf.set_x(prev_x3)
        self.fpdf.multi_cell(13.5, 4, f"{self.player1}\nEffic.", align="C")
        self.fpdf.set_y(prev_y + 2)
        self.fpdf.set_x(prev_x3 + 12.75)
        self.fpdf.multi_cell(15, 4, f"{self.player2} Effic", align="C")
        self.fpdf.set_y(prev_y + 17.5)

        # self.fpdf.ln(4.5 * th)
        keys = [
            "Stationary FH behind baseline (no slice)",
            "Running FH behind baseline (no slice)",
            "Stationary FH back court (no slice)",
            "Running FH back court (no slice)",
            "Stationary FH fore court (no slice)",
            "Running FH fore court (no slice)",
            "Stationary FH volley",
            "Running FH volley",
            "Stationary BH behind baseline (no slice)",
            "Running BH behind baseline (no slice)",
            "" "Stationary BH back court (no slice)",
            "Running BH back court (no slice)",
            "Stationary BH fore court (no slice)",
            "Running BH fore court (no slice)",
            "Stationary BH volley",
            "Running BH volley",
            "FH overhead",
            "FH lob",
            "FH dropshot",
            "FH Passing (Non-lob)",
            "FH Slice (deep)",
            "BH overhead",
            "BH lob",
            "BH dropshot",
            "BH Passing (Non-lob)",
            "BH Slice (deep)",
            "Total ( \u203A 3 shots)",
        ]

        for i, key in zip(rally_ending_dic["Player1"]["Winner"]["Value"], keys):
            self.fpdf.set_font("Din", style="", size=7.5)
            self.fpdf.set_text_color(0, 0, 0)
            self.fpdf.cell(60, 1.5 * th, key, border=1)
            self.fpdf.set_font("ROCK", style="", size=9)
            self.fpdf.set_text_color(21, 71, 52)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player1"]["Winner"]["Value"][i])),
                border=1,
                align="C",
            )
            self.fpdf.set_text_color(144, 238, 144)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player1"]["Forcing"]["Value"][i])),
                border=1,
                align="C",
            )
            self.fpdf.set_text_color(255, 0, 0)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player1"]["Unforced"]["Value"][i])),
                border=1,
                align="C",
            )
            self.fpdf.set_text_color(21, 71, 52)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player2"]["Winner"]["Value"][i])),
                border=1,
                align="C",
            )
            self.fpdf.set_text_color(144, 238, 144)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player2"]["Forcing"]["Value"][i])),
                border=1,
                align="C",
            )
            self.fpdf.set_text_color(255, 0, 0)
            self.fpdf.cell(
                13.5,
                1.5 * th,
                str(int(rally_ending_dic["Player2"]["Unforced"]["Value"][i])),
                border=1,
                align="C",
            )

            # calculate eff
            # check if it divisible by 0
            if (
                int(rally_ending_dic["Player1"]["Winner"]["Value"][i])
                + int(rally_ending_dic["Player1"]["Forcing"]["Value"][i])
                + int(rally_ending_dic["Player1"]["Unforced"]["Value"][i])
                == 0
            ):
                self.fpdf.cell(13.5, 1.5 * th, " ", border=1, align="C")
            else:
                tally = (
                    int(rally_ending_dic["Player1"]["Winner"]["Value"][i])
                    + int(rally_ending_dic["Player1"]["Forcing"]["Value"][i])
                    - int(rally_ending_dic["Player1"]["Unforced"]["Value"][i])
                )
                sum = (
                    int(rally_ending_dic["Player1"]["Winner"]["Value"][i])
                    + int(rally_ending_dic["Player1"]["Forcing"]["Value"][i])
                    + int(rally_ending_dic["Player1"]["Unforced"]["Value"][i])
                )

                player1Eff = self.divide(n1=tally, n2=sum, default=0)
                if player1Eff > 0:
                    self.fpdf.set_text_color(21, 71, 52)
                    self.fpdf.cell(
                        13.5, 1.5 * th, "{:.0%}".format(player1Eff), border=1, align="C"
                    )
                else:
                    self.fpdf.set_text_color(255, 0, 0)
                    self.fpdf.cell(
                        13.5, 1.5 * th, "{:.0%}".format(player1Eff), border=1, align="C"
                    )
            if (
                int(rally_ending_dic["Player2"]["Winner"]["Value"][i])
                + int(rally_ending_dic["Player2"]["Forcing"]["Value"][i])
                + int(rally_ending_dic["Player2"]["Unforced"]["Value"][i])
                == 0
            ):
                self.fpdf.cell(13.5, 1.5 * th, " ", border=1, align="C")
            else:
                tally = (
                    int(rally_ending_dic["Player2"]["Winner"]["Value"][i])
                    + int(rally_ending_dic["Player2"]["Forcing"]["Value"][i])
                    - int(rally_ending_dic["Player2"]["Unforced"]["Value"][i])
                )
                sum = (
                    int(rally_ending_dic["Player2"]["Winner"]["Value"][i])
                    + int(rally_ending_dic["Player2"]["Forcing"]["Value"][i])
                    + int(rally_ending_dic["Player2"]["Unforced"]["Value"][i])
                )
                player2Eff = self.divide(n1=tally, n2=sum, default=0)
                if player2Eff > 0:
                    self.fpdf.set_text_color(21, 71, 52)
                    self.fpdf.cell(
                        13.5, 1.5 * th, "{:.0%}".format(player2Eff), border=1, align="C"
                    )
                else:
                    self.fpdf.set_text_color(255, 0, 0)
                    self.fpdf.cell(
                        13.5, 1.5 * th, "{:.0%}".format(player2Eff), border=1, align="C"
                    )
            self.fpdf.ln(1.5 * th)

        self.fpdf.set_font("Din", style="", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        s = "Table 3"
        self.fpdf.text((self.fpdf.w / 2) - self.fpdf.get_string_width(s) / 2, 238, s)

        self.fpdf.set_text_color(0, 0, 0)
        if self.report_metadata["GS"] != self.report_metadata["Basic"]:
            self.fpdf.set_font(family="Din Italic", size=8)
            self.fpdf.set_y(250)
            self.fpdf.cell(
                0,
                4,
                f"* {self.report_metadata['GS']} matches with rally ending shot data (this page) vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
                align="C",
            )
