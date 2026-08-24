from abc import ABC, abstractmethod
from pdf_generator.services.constants import (
    APPENDIX_AVG_SPEED_HEADER_COL_1,
    APPENDIX_AVG_SPEED_HEADER_COL_2,
)

# TODO needs refactor (knows too much about table data)


class Table(ABC):
    def __init__(
        self,
        pdf,
        data,
        x_offset=None,
        y_offset=0,
        line_height_scaler=1.25,
        widths=None,
        fill_header=False,
        footer_data=None,
    ):
        self.pdf = pdf
        self.data = data
        self.x_offset = x_offset if x_offset else pdf.x
        self.y_offset = pdf.y + y_offset
        self.line_height = pdf.font_size * line_height_scaler
        self.fill_header = fill_header
        self.footer_data = footer_data
        self.widths = widths

    def multi_cell_row(self, headers):
        # Make a copy of x_offset
        header_offset = self.x_offset

        # Building the row using multi cell
        for datum, width in zip(headers, self.widths):
            # Set coordinates
            self.pdf.set_y(self.y_offset)
            self.pdf.set_x(header_offset)

            self.pdf.multi_cell(
                width,
                self.line_height,
                datum,
                border=True,
                align="C",
                fill=self.fill_header,
            )
            # Update coordinates to the next position
            header_offset += width

            # Cancel multi cell line break then Drop one line
            self.pdf.set_y(self.y_offset)
            self.pdf.ln(self.line_height)

    def cell_row(self, key):
        # Set coordinates
        self.pdf.set_y(self.y_offset)
        self.pdf.set_x(self.x_offset)

        # Building the row
        self.pdf.cell(self.widths[0], self.line_height, key, border=True, align="C")
        for datum, width in zip(self.data[key], self.widths[1:]):
            datum = str(datum)
            self.pdf.cell(width, self.line_height, datum, border=True, align="C")
        self.pdf.ln(self.line_height)

    def footer(self, category, num):
        if not all([category, num]):
            return

        # Config
        self.pdf.set_font("ROCKI", "", 10)

        # Normal footer
        if not self.footer_data:
            self.pdf.cell(
                0, self.line_height, f"Table {category}.{num}", align="C", ln=True
            )
            return

        # Building the footer
        self.pdf.cell(0, self.line_height, self.footer_data, align="C")
        self.pdf.set_x(self.x_offset)
        self.pdf.cell(30, self.line_height, f"Table {category}.{num}", ln=True)

    @abstractmethod
    def header(self):
        pass

    @abstractmethod
    def body(self):
        pass

    def draw(self, category=None, num=None):
        self.pdf.set_font(family="ROCK", size=11)

        # Building the table
        self.header()
        self.body()

        self.footer(category, num)
        self.pdf.ln(self.line_height * 0.5)


class AvgSpeedTable(Table):
    def header(self):
        self.widths = [80, 65] if not self.widths else self.widths
        headers = (APPENDIX_AVG_SPEED_HEADER_COL_1, APPENDIX_AVG_SPEED_HEADER_COL_2)
        self.multi_cell_row(headers)
        self.pdf.ln(self.line_height)
        self.y_offset = self.pdf.y

    def body(self):
        for key in self.data:
            self.cell_row(key)
            self.y_offset = self.pdf.y

    def footer(self, category, num):
        self.pdf.set_x(self.x_offset)
        self.pdf.set_font("ROCKI", "", 10)
        self.pdf.cell(
            self.widths[0], self.line_height, f"Table {category}.{num}", align="C"
        )
        self.pdf.cell(
            self.widths[1], self.line_height, self.footer_data, align="C", ln=True
        )


class ServeSpeedTable(Table):
    def __init__(
        self,
        pdf,
        data,
        type,
        x_offset=None,
        y_offset=0,
        line_height_scaler=1.25,
        widths=None,
        fill_header=True,
        footer_data=None,
    ):
        super().__init__(
            pdf,
            data,
            x_offset,
            y_offset,
            line_height_scaler,
            widths,
            fill_header,
            footer_data,
        )
        if type not in ("Wide", "Body", "T", None):
            raise ValueError("Invalid type")
        self.type = type

    def header(self):
        headers = (
            f"Returns v. Serve Speed\nOppnt Serving ({self.type})",
            "\nIn",
            "\nGood",
            "Win\nPoint",
            "\nTotal",
            "%\nIn",
            "%\nGood",
            "% Pts\nWon",
        )
        self.widths = [50] + [(155 - 50) / 7] * 7 if not self.widths else self.widths

        self.multi_cell_row(headers)
        self.pdf.ln(self.line_height)
        self.y_offset = self.pdf.y

    def body(self):
        for key in self.data:
            self.cell_row(key)
            self.y_offset = self.pdf.y


class RallyPointsTable(Table):
    def __init__(
        self,
        pdf,
        data,
        player_name,
        opponent_name,
        is_pressure_pts,
        x_offset=None,
        y_offset=0,
        line_height_scaler=1.25,
        widths=None,
        fill_header=True,
        footer_data=None,
    ):
        super().__init__(
            pdf,
            data,
            x_offset,
            y_offset,
            line_height_scaler,
            widths,
            fill_header,
            footer_data,
        )
        if is_pressure_pts not in (True, False):
            raise ValueError("Invalid value")
        self.is_pressure_pts = is_pressure_pts
        self.player_name = player_name
        self.opponent_name = (
            f"{opponent_name.split()[0]} OPP"
            if opponent_name.split()[0].isnumeric()
            else opponent_name
        )

    def header(self):
        pts_sub_header = (
            "(Pressure Points)" if self.is_pressure_pts else "(Non Pressure Points)"
        )
        headers = (
            f"Rally Pts Won\n{pts_sub_header}",
            f"Win Total\n{self.player_name}",
            f"Win Total\n{self.opponent_name}",
            "\nTotal",
            f"Win %\n{self.player_name}",
            f"Win %\n{self.opponent_name}",
        )
        self.widths = (
            [60] + [25, 25] + [(170 - 60) / 5] * 3 if not self.widths else self.widths
        )

        self.multi_cell_row(headers)
        self.pdf.ln(self.line_height)
        self.y_offset = self.pdf.y

    def body(self):
        for key in self.data:
            self.cell_row(key)
            self.y_offset = self.pdf.y


class DirectionTable(Table):
    def __init__(
        self,
        pdf,
        data,
        rally_ending_no,
        data_type,
        x_offset=None,
        y_offset=0,
        line_height_scaler=1.25,
        widths=None,
        fill_header=False,
        footer_data=None,
    ):
        super().__init__(
            pdf,
            data,
            x_offset,
            y_offset,
            line_height_scaler,
            widths,
            fill_header,
            footer_data,
        )
        if rally_ending_no not in (1, 2):
            raise ValueError("Invalid rally_ending_no")
        self.rally_ending_no = rally_ending_no
        if data_type.upper() not in ("C", "P"):
            raise ValueError("Invalid data_type")
        self.data_type = "Count" if data_type.upper() == "C" else "%"

    def header(self):
        if self.rally_ending_no == 1:
            headers = (self.main_header, self.sub_header, self.shot_type_header)
        else:
            headers = (self.main_header, self.shot_type_header)

        for header in headers:
            header()
            self.pdf.ln(self.line_height)

    def body(self):
        # Config
        self.pdf.set_fill_color(220, 230, 241)

        for pos in self.data:
            # Temporary
            if pos == "Total":
                continue

            self.pdf.set_x(self.x_offset)
            self.pdf.cell(30, self.line_height, pos, border="LR", fill=True)

            break_at = 2 if self.rally_ending_no == 1 else 3
            for j, datum in enumerate(map(str, self.data[pos])):
                if datum and self.data_type == "%":
                    datum += "%"

                if (j + 1) % break_at == 0:
                    self.pdf.cell(
                        125 / 6, self.line_height, datum, align="C", border="R"
                    )
                else:
                    self.pdf.cell(125 / 6, self.line_height, datum, align="C")
            self.pdf.ln(self.line_height)

        if self.rally_ending_no == 1:
            self.total(self.data["Total"])
            self.pdf.ln(self.line_height)
        else:
            self.pdf.line(self.x_offset, self.pdf.y, self.x_offset + 155, self.pdf.y)

    def main_header(self):
        # Set coordinates
        self.pdf.set_y(self.y_offset)
        self.pdf.set_x(self.x_offset)

        # Config
        self.pdf.set_draw_color(128, 128, 128)
        self.pdf.set_fill_color(242, 242, 242)
        self.pdf.set_line_width(0.4)

        # Header
        # Title & Type
        self.pdf.set_font("ROCKI", "", 10)
        self.pdf.cell(30, self.line_height, self.data_type, border=True)
        style = "U" if self.rally_ending_no == 1 else ""
        self.pdf.set_font("ROCK Bold", style, 10)

        title = "position" if self.rally_ending_no == 1 else "direction"
        self.pdf.cell(
            125,
            self.line_height,
            f"Last shot {title}",
            border="TRL",
            align="C",
            fill=True,
        )

    def sub_header(self):
        # Positions
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.set_x(self.x_offset)
        self.pdf.cell(30, self.line_height, "", border=True)
        for pos in ("Deuce", "Middle", "Ad"):
            self.pdf.cell(
                125 / 3,
                self.line_height,
                f"{pos} court",
                border="LR",
                align="C",
                fill=True,
            )

    def shot_type_header(self):
        self.pdf.set_font("ROCK Bold", "U", 10)
        self.pdf.set_x(self.x_offset)
        self.pdf.set_fill_color(220, 230, 241)

        title = "Direction" if self.rally_ending_no == 1 else "2nd to last"
        self.pdf.cell(30, self.line_height, title, border="LTR", fill=True)
        self.pdf.set_font(family="ROCK", size=10)
        self.pdf.set_fill_color(242, 242, 242)

        # Shot type
        if self.rally_ending_no == 1:
            for _ in range(3):
                for type in ("FH", "BH"):
                    if type == "FH":
                        self.pdf.cell(
                            125 / 6,
                            self.line_height,
                            type,
                            align="C",
                            border="BL",
                            fill=True,
                        )
                    else:
                        self.pdf.cell(
                            125 / 6,
                            self.line_height,
                            type,
                            align="C",
                            border="BR",
                            fill=True,
                        )

        else:
            for type in ("FH", "BH"):
                for pos in ("Line", "Middle", "Cross"):
                    border = "B"
                    if pos == "Line":
                        border += "L"
                    elif pos == "Cross":
                        border += "R"

                    self.pdf.cell(
                        125 / 6,
                        self.line_height,
                        f"{type} {pos}",
                        align="C",
                        border=border,
                        fill=True,
                    )

    def total(self, data):
        self.pdf.set_x(self.x_offset)
        self.pdf.set_font("ROCK Bold", "", 10)
        self.pdf.set_line_width(0.5)
        self.pdf.cell(30, self.line_height, "Total", border=True, fill=True)

        for i, datum in enumerate(map(str, data)):
            if datum and self.data_type == "%":
                datum += "%"

            if i % 2 == 0:
                self.pdf.cell(125 / 6, self.line_height, datum, align="C", border="TB")
            else:
                self.pdf.cell(125 / 6, self.line_height, datum, border="TRB", align="C")


class DirectionSuccessTable(Table):
    def header(self):
        # Set coordinates
        self.pdf.set_y(self.y_offset)
        self.pdf.set_x(self.x_offset)

        # Config
        self.pdf.set_draw_color(128, 128, 128)
        self.pdf.set_fill_color(242, 242, 242)
        self.pdf.set_line_width(0.3)
        self.pdf.set_font(family="ROCK", size=10)

        # Shot type
        self.pdf.cell(30, self.line_height, "", border="LTR", fill=True)
        for type in ("FH", "BH"):
            for pos in ("Line", "Middle", "Cross"):
                border = "T"
                if pos == "Line":
                    border += "L"
                elif pos == "Cross":
                    border += "R"

                self.pdf.cell(
                    125 / 6,
                    self.line_height,
                    f"{type} {pos}",
                    align="C",
                    border=border,
                    fill=True,
                )
        self.pdf.ln(self.line_height)

    def body(self):
        data_length = len(self.data)

        for i, pos in enumerate(self.data):
            self.pdf.set_x(self.x_offset)
            self.pdf.cell(30, self.line_height, pos, border="LR")

            for j, datum in enumerate(map(str, self.data[pos])):
                if datum and i == data_length - 1:
                    datum += "%"

                if (j + 1) % 3 == 0:
                    self.pdf.cell(
                        125 / 6, self.line_height, datum, align="C", border="R"
                    )
                else:
                    self.pdf.cell(125 / 6, self.line_height, datum, align="C")
            self.pdf.ln(self.line_height)

        self.pdf.line(self.x_offset, self.pdf.y, self.x_offset + 155, self.pdf.y)
