from pdf_generator.services.constants import (
    CURDIRPATH,
    SHOT_AFTER_RETURN_LOCATION_PARAGRAPH,
)


class ShotAfterReturnLocation:
    visual_counter = 6
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 3300

    def __init__(self, fpdf, data_repo, serve_number, visuals_generator):
        """
        serve_number is one of ('1st', '2nd')
        """
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.name = f"Shot after return location {serve_number[0]} page"
        self.serve_number = serve_number
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.fpdf.set_header_title(
            f"{self.player1} 1st shot after {serve_number} serve"
        )
        self.fpdf.set_header_sub_title(f"Serve+1 after {serve_number} serve: direction")

    def build_page_body(self):
        # TODO support the second page, Pies legend
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(10 if self.serve_number == "1st" else 11)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Bold", style="", size=9)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(77, 38, f"Serve, Serve+1 & points won:  {self.player1}")
        self.fpdf.text(111.5, 38 + line_height, f"Return:  {self.player2}")
        self.fpdf.ln(line_height * 2.35)
        self.fpdf.set_font("Din", size=8.7)
        self.fpdf.set_x(14)
        self.fpdf.multi_cell_normal(187, 4.1, SHOT_AFTER_RETURN_LOCATION_PARAGRAPH)

        w = 96
        visual_keys = (
            (65, 66, 67, 68, 69, 70)
            if self.serve_number == "1st"
            else (71, 72, 73, 74, 75, 76)
        )
        for key, x, y, location, direction in zip(
            visual_keys,
            (8, 112) * 3,
            (60, 60, 124, 124, 188, 188),
            ("Deuce", "Ad") * 3,
            ("Cross", "Cross", "Middle", "Middle", "Line", "Line"),
        ):
            self.fpdf.set_font("Din Medium", size=10)
            self.fpdf.set_y(y - 3.75)
            self.fpdf.set_x(x)
            self.fpdf.cell(
                w,
                txt=f"Serve+1 - {self.serve_number} Serve {location}, Return {direction}",
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
        self.fpdf.set_font(family="Din Italic", size=8)

        # Number of matches included
        self.fpdf.set_y(246)
        self.fpdf.cell_normal(
            0,
            line_height,
            f"{self.report_metadata['GS']} matches with Serve+1 data (this page) vs. {self.report_metadata['Basic']} matches with data for other visuals in the report",
            align="C",
        )

        # Gray arrow meaning
        self.fpdf.set_font(family="Din", size=9)
        self.fpdf.image(f"{CURDIRPATH}/assets/last_shot_direction.png", 12, 251, 8)
        self.fpdf.text_normal(21, 257, "Arrow indicating")
        self.fpdf.text_normal(21, 261, "return direction")

        # Player info
        self.fpdf.set_font(family="Din Bold", size=9)
        self.fpdf.text_normal(55, 257, f"Serve, Serve+1 & points won: {self.player1}")
        self.fpdf.text_normal(89.5, 261, f"Return: {self.player2}")

        # Pies meaning
        self.fpdf.set_font(family="Din", size=8)
        self.fpdf.image(f"{CURDIRPATH}/assets/pts_lost_pie.png", 130, 254, 3)
        self.fpdf.text_normal(134, 257, "Points lost")
        self.fpdf.image(f"{CURDIRPATH}/assets/pts_won_pie.png", 130, 259, 3)
        self.fpdf.text_normal(134, 261, "Points won")

        # Arrow width meaning (yellow arrow)
        self.fpdf.image(f"{CURDIRPATH}/assets/arrow_width_meaning.png", 156, 250, 7.5)
        self.fpdf.set_font_size(9)
        self.fpdf.text_normal(165, 253, "Arrow width sized")
        self.fpdf.text_normal(165, 257, "according to % of")
        self.fpdf.text_normal(165, 261, "serve+1s by direction")
