from pdf_generator.services.constants import ALL_GROUNDSTROKES_PARAGRAPH, CURDIRPATH


class AllGroundstrokesDirection:
    visual_counter = 6
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 3450

    def __init__(self, fpdf, data_repo, variant, visuals_generator):
        self.name = f"All Groundstrokes Direction page"
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.fpdf.set_header_title(f"Rallies and groundstrokes")
        self.fpdf.set_header_sub_title(f"All groundstroke 2-shot directions")

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(12)
        self.fpdf.add_page()
        self.fpdf.ln(9)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.cell(0, line_height, f"All groundstrokes: {self.player1}", align="C")
        self.fpdf.ln(line_height)
        self.fpdf.cell(10)
        self.fpdf.cell(194, line_height, f"Previous shot: {self.player2}", align="C")
        self.fpdf.ln(line_height * 1.5)
        self.fpdf.set_font("Din", style="", size=10)
        self.fpdf.set_y(43.5)
        self.fpdf.set_x(15)
        self.fpdf.multi_cell_normal(175, 4, ALL_GROUNDSTROKES_PARAGRAPH)

        w = 96
        visual_keys = (98, 100, 99, 101, 102, 103)
        is_lefthanded = self.data_repo.is_lefthanded()
        locations = ("Ad", "Ad", "Deuce", "Deuce", "Ad", "Ad")
        if is_lefthanded:
            locations = ("Ad", "Ad", "Deuce", "Deuce", "Deuce", "Deuce")
        for key, x, y, location, shot_type, direction in zip(
            visual_keys,
            (8, 112) * 3,
            (60, 60, 124, 124, 188, 188),
            locations,
            ("FH", "FH", "FH", "FH", "BH", "BH"),
            ("Cross", "DTL") * 3,
        ):
            self.fpdf.set_font("Din Medium", size=10)
            self.fpdf.set_y(y - 3.5)
            self.fpdf.set_x(x)
            self.fpdf.cell(
                w,
                txt=f"{self.player2} {direction}, {location} Side {shot_type} {self.player1}",
                align="C",
            )

            self.fpdf.image(self.visuals_generator.generate_visual(key), x, y, w)

            self.fpdf.set_font("Din", size=9)
            self.fpdf.set_y(y + 55)
            self.fpdf.set_x(x)
            self.fpdf.cell(w, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        # Footer
        # Config
        self.fpdf.set_font(family="Din Italic", size=7)

        # Number of matches included
        self.fpdf.set_y(246)
        self.fpdf.cell_normal(
            0,
            line_height,
            f"*{self.report_metadata['GD']} matches with all groundstrokes shot direction (this page) vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )

        # Gray arrow meaning
        self.fpdf.set_font(family="Din", size=9)
        self.fpdf.image(f"{CURDIRPATH}/assets/last_shot_direction.png", 12, 250, 8)
        self.fpdf.text_normal(20, 257, "Arrow indicating ")
        self.fpdf.text_normal(20, 261, "previous shot direction")

        # Player info
        self.fpdf.set_font("Din Medium", size=9)
        self.fpdf.text_normal(64.5, 257, f"All groundstrokes: {self.player1}")
        self.fpdf.text_normal(74, 261, f"Previous shot: {self.player2}")

        # Pies meaning
        self.fpdf.set_font(family="Din", size=8)
        self.fpdf.image(f"{CURDIRPATH}/assets/pts_lost_pie.png", 125, 254, 3)
        self.fpdf.text_normal(129, 257, "Points lost")
        self.fpdf.image(f"{CURDIRPATH}/assets/pts_won_pie.png", 125, 259, 3)
        self.fpdf.text_normal(129, 261, "Points won")

        # Arrow width meaning (yellow arrow)
        self.fpdf.image(f"{CURDIRPATH}/assets/arrow_width_meaning.png", 151, 250, 7.5)
        self.fpdf.set_font_size(8)
        self.fpdf.text_normal(159, 253, "Arrow width sized")
        self.fpdf.text_normal(159, 257, "according to % of all")
        self.fpdf.text_normal(159, 261, "groundstrokes shot by direction")
        self.fpdf.footer_behavior.footer()
