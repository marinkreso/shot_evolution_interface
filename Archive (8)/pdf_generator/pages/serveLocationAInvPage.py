from pdf_generator.models.enums import Serve, Distribution
from pdf_generator.services.constants import (
    ARROW_DETAIL1,
    ARROW_DETAIL2,
    ARROW_DETAIL3,
    CURDIRPATH,
    SERVER_LOCATION_1A_INV_PARGRAPH,
)


class ServeLocationAINV:
    visual_counter = 2
    table_counter = 0
    requires_visual_generator = True
    execution_cost = 700

    def __init__(self, fpdf, data_repo, duplicates, visuals_generator):
        self.fpdf = fpdf
        self.data_repo = data_repo
        self.visuals_generator = visuals_generator
        self.duplicates = duplicates
        self.player1, self.player2 = self.data_repo.players_name()
        self.report_metadata = self.data_repo.report_metadata()
        self.fpdf.set_header_title(f"Where to serve to {self.player1} on {duplicates}")
        self.fpdf.set_header_sub_title(f"{duplicates} serve: in % and speed")
        self.title = f"Serve & in %: {self.player2}"
        self.subTitle = f"Return: {self.player1}"
        self.name = f"Serve Location A {duplicates} Inv Page"

    def build_page_body(self):
        self.fpdf.set_preset("visual")
        self.fpdf.set_section(6 if self.duplicates == "1st" else 8)
        self.fpdf.set_text_color(0, 0, 0)

        self.fpdf.add_page()
        self.fpdf.ln(7)

        # Page header
        self.fpdf.set_font("Din Medium", size=10)
        line_height = self.fpdf.font_size * 1.25
        self.fpdf.text(81, 38, self.title)
        self.fpdf.text(89.5, 38 + line_height, self.subTitle)
        self.fpdf.ln(line_height * 2.5)

        self.fpdf.set_font("Din", size=9)
        self.fpdf.set_x(16)
        self.fpdf.multi_cell_normal(175, 5, SERVER_LOCATION_1A_INV_PARGRAPH)

        self.fpdf.ln(7)

        # image url
        visuals_keys = (31, 32) if self.duplicates == "1st" else (48, 49)
        for key, y, title in zip(
            visuals_keys, (68, 163), ("serve direction and in %", "serve speed")
        ):
            self.fpdf.set_font("Din Medium", size=11)
            self.fpdf.set_y(y - 5)
            self.fpdf.set_x(55)
            self.fpdf.cell(105, txt=f"{self.duplicates} {title}", align="C")

            self.fpdf.image(
                self.visuals_generator.generate_visual(key),
                35,
                y,
                w=145,
            )
            self.fpdf.set_font("Din", size=11)
            self.fpdf.set_y(y + 83)
            self.fpdf.set_x(55)
            self.fpdf.cell(105, txt=f"Visual {self.fpdf.visuals_no}", align="C")
            self.fpdf.visuals_no += 1

        speed_data = self.data_repo.json_aggregate.serve_speed_values(
            Distribution.AVG, player_no=2
        )
        speed_data_filtered = []
        for court in ("Deuce", "Ad"):
            directions = ["Wide", "Body", "T"]
            for direction in directions:
                speed_data_filtered.append(
                    speed_data[
                        f"{'First' if self.duplicates == '1st' else 'Second'}{court}{direction}"
                    ]
                )
        if sum(speed_data_filtered) == 0:
            self.fpdf.image(
                f"{CURDIRPATH}/assets/speed_data_unavailable.png",
                80,
                170,
                w=120,
            )

        self.fpdf.set_font("Din Medium", size=10)
        self.fpdf.set_text_color(0, 0, 0)
        self.fpdf.text(81, 260, self.title)
        self.fpdf.text(89.5, 264, self.subTitle)

        self.fpdf.image(
            f"{CURDIRPATH}/assets/arrow_detail_GR.jpg", 155, 252, 7.5, 13, type="jpg"
        )

        self.fpdf.set_font(family="Din", size=10)
        self.fpdf.set_text_color(0)
        self.fpdf.text_normal(164, 255, ARROW_DETAIL1)
        self.fpdf.text_normal(164, 259.5, ARROW_DETAIL2)
        self.fpdf.text_normal(164, 264, ARROW_DETAIL3.format("serves"))

        # Check for speed data
        # serve_no = Serve.FIRST if self.duplicates == "1st" else Serve.SECOND
        # stats = self.data_repo.serve_location_a_inv(serve_no, serve_speed=True)
        # speed_stats = [int(stat) for stat in stats["arrows_numbers"]]
        # if not sum(speed_stats):
        #     speed_text = "data\nunavailable in our dataset"
        # else:
        #     speed_text = "\n(MPH) by direction"

        # Reset font color
        self.fpdf.set_text_color(0, 0, 0)

        # Reset to original margin
        self.fpdf.set_right_margin(8)
