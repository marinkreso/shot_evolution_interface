from pdf_generator.services.constants import RALLY_ENDING_PARAGRAPH, CURDIRPATH


class RallyEnding:
    visual_counter = 6
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 8500

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates
        self.report_metadata = self.data_repo.report_metadata()
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title("Rallies and groundstrokes ")
        self.fpdf.set_header_sub_title("Rally ending shot position")
        self.title = (
            f'Player: {self.player1 if self.duplicates == "1st" else self.player2}'
        )
        self.name = f"Rally Ending {duplicates} page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(12)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_y(38)
        self.fpdf.cell(0, txt=self.title, align="C")

        self.fpdf.set_font(family="Din", size=12)
        self.fpdf.set_y(45)
        self.fpdf.set_x(16)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.multi_cell_normal(175, 5, RALLY_ENDING_PARAGRAPH)
        self.fpdf.ln(10)
        self.fpdf.set_font("Din Medium", size=11)

        for title, y in zip(
            ("Stationary and Running", "Stationary", "Running"), (62, 125, 188)
        ):
            self.fpdf.set_y(y)
            self.fpdf.cell(0, txt=title, align="C")

        visual_keys_mapping = {
            ("1st", False): (80, 81, 82, 83, 84, 85),
            ("1st", True): (81, 80, 83, 82, 85, 84),
            ("2nd", False): (86, 87, 88, 89, 90, 91),
            ("2nd", True): (87, 86, 89, 88, 91, 90),
        }
        is_lefthanded = (
            self.data_repo.is_lefthanded()
            if self.duplicates == "1st"
            else self.data_repo.get_report_inputs()["OpponentHandedness"] == 1
        )
        visual_keys = visual_keys_mapping[(self.duplicates, is_lefthanded)]
        for (
            key,
            x,
            y,
        ) in zip(
            visual_keys,
            (8, 112) * 3,
            (67, 67, 130, 130, 193, 193),
        ):
            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                x,
                y,
                w=96,
            )

            self.fpdf.set_font("Din", size=9)
            self.fpdf.set_y(y + 56)
            self.fpdf.set_x(x + 10)
            self.fpdf.cell(75, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        self.fpdf.set_font(family="Din Italic", size=9)
        # Number of matches included
        self.fpdf.set_y(255)
        # TODO read real data for footer
        self.fpdf.cell_normal(
            0,
            2,
            f"*{self.report_metadata['GS']} matches with rally ending shot position (this page) vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )

        # self.fpdf.image(f"{CURDIRPATH}/assets/rally_pies_legend.png", 8, 252, 30)

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(95, 264, self.title)
