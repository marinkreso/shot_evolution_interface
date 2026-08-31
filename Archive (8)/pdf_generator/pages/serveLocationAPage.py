from pdf_generator.models.enums import Serve
from pdf_generator.services.constants import (
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
    CURDIRPATH,
    SERVER_LOCATION_PARAGRAPH,
)


class ServeLocationA:
    visual_counter = 2
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 1195

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.visuals_generator = visuals_generator
        self.data_repo = data_repo
        self.duplicates = duplicates[0]
        self.is_new = duplicates[1]
        self.player1, self.player2 = self.data_repo.players_name()
        self.fpdf.set_header_title(f"Where {self.player1} serves on {self.duplicates}")
        self.fpdf.set_header_sub_title(
            f"{self.duplicates} serve: all serves, in % and speed"
            if self.is_new
            else f"{self.duplicates} serve: in % and speed"
        )
        self.title = (
            f"{self.duplicates} serves direction & in %:  {self.player1}"
            if self.is_new
            else f"Serve & in %: {self.player1}"
        )
        self.sub_title = f"Return:  {self.player2}"
        self.image_title = (
            f"All {self.duplicates} serves by direction & in %"
            if self.is_new
            else f"{self.duplicates} serve direction & in %"
        )
        self.width = self.fpdf.w
        self.name = f"Serve Location A {self.duplicates} Page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(2 if self.duplicates == "1st" else 4)
        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(90, 39, self.title)
        self.fpdf.text(98.5, 39 + line_height, self.sub_title)
        self.fpdf.ln(line_height * 2.75)

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, SERVER_LOCATION_PARAGRAPH)

        self.fpdf.ln(5.5)
        self.fpdf.set_font(family="Din Medium", size=11)
        self.fpdf.set_x(
            ((self.width / 2) - self.fpdf.get_string_width(self.image_title) / 2) - 7
        )
        self.fpdf.write(1, self.image_title.upper())

        visual_id = 1 if self.duplicates == "1st" else 16
        visual_id += 200 if self.is_new else 0
        self.fpdf.image(
            self.visuals_generator.generate_visual(visual_id), 35, 68, w=145
        )

        self.fpdf.set_font("Din", size=11)
        self.fpdf.set_text_color(0, 0, 0)
        s = f"Visual {self.fpdf.visuals_no}"
        self.fpdf.text((self.fpdf.w / 2) - self.fpdf.get_string_width(s) / 2, 154, s)
        self.fpdf.visuals_no += 1
        self.fpdf.set_font("Din Medium", size=11)
        self.fpdf.set_text_color(0, 0, 0)
        s = (
            f"{self.duplicates} serves in by direction and speed"
            if self.is_new
            else f"{self.duplicates} serve speed"
        )
        self.fpdf.text(
            ((self.fpdf.w / 2) - self.fpdf.get_string_width(s) / 2) - 7, 161, s
        )

        # 2nd visual
        visual_id = 2 if self.duplicates == "1st" else 17
        visual_id += 200 if self.is_new else 0
        self.fpdf.image(
            self.visuals_generator.generate_visual(visual_id), 35, 163, w=145
        )
        self.fpdf.set_font("Din", size=11)
        self.fpdf.set_text_color(0, 0, 0)
        s = f"Visual {self.fpdf.visuals_no}"
        self.fpdf.text((self.fpdf.w / 2) - self.fpdf.get_string_width(s) / 2, 250, s)
        self.fpdf.visuals_no += 1

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)

        self.fpdf.text(90, 260, self.title)
        self.fpdf.text(98.5, 260 + line_height, self.sub_title)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_A.jpg", 155, 252, 7.5, 13, type="jpg"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("serves"))

        # Check for speed data
        # serve_no = Serve.FIRST if self.duplicates == "1st" else Serve.SECOND
        # stats = self.data_repo.serve_location_a(serve_no, serve_speed=True)
        # speed_stats = [int(stat) for stat in stats["arrows_numbers"]]
        # if not sum(speed_stats):
        #     speed_text = "data\nunavailable in our dataset"
        # else:
        #     speed_text = "\n(MPH) by direction"

        # Reset font color
        self.fpdf.set_text_color(0, 0, 0)

        # Reset to original margin
        self.fpdf.set_right_margin(8)
