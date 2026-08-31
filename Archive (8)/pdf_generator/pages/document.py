from fpdf import FPDF
from fpdf.enums import (
    Align,
    XPos as XPos,
    YPos as YPos,
)
from pdf_generator.services.constants import CURDIRPATH, FOOTER_TEXT
from abc import ABC, abstractmethod
from enum import Enum


class Header(ABC):
    def __init__(self, page) -> None:
        self.page = page

    @abstractmethod
    def header(self, page):
        pass


class VisualHeader(Header):
    # TODO Clean the previous implementation
    def header(self):
        # Reset text color
        self.page.set_text_color(0, 0, 0)

        # Draw black background
        self.page.set_fill_color(0, 0, 0)
        self.page.rect(0, 0, self.page.w, self.page.h, style="F")

        # Draw White self.page overlapping the black background
        self.page.set_fill_color(255, 255, 255)
        self.page.rect(7, 23.5, self.page.w - 14, self.page.h - 37, style="F")

        # Draw section bar
        if self.page.section_number:
            self.page.image(
                f"{CURDIRPATH}/assets/section_{self.page.section_number}.png",
                7,
                14,
                self.page.w - 14,
            )

        # Page title
        self.page.set_fill_color(217, 217, 217)
        self.page.rect(7, 23.5, self.page.w - 14, 11, style="F")
        # Reset
        self.page.set_fill_color(255, 0, 0)

        # Section title
        self.page.set_font(family="Din Bold", size=14)
        self.page.set_y(17)
        section_x_offset = (
            6 * (self.page.section_number - 1) + (self.page.section_number / 10)
            if self.page.section_number
            else 0
        )
        self.page.set_x(33.5 + section_x_offset)
        self.page.cell(
            105, txt=f"{self.page.section_number}. {self.page.header_title}", align="C"
        )

        # Page title
        self.page.set_font("Din", "", 20)
        self.page.set_y(26)
        # TODO there is margin begin added somewhere
        self.page.cell(0, txt=self.page.header_sub_title, align="C")


class AppendixHeader(Header):
    # TODO
    def header(self):
        pass


class CoverHeader(Header):
    def header(self):
        # Draw black background
        self.page.set_fill_color(0, 0, 0)
        self.page.rect(0, 0, self.page.w, self.page.h, style="F")

        # Draw White page overlapping the black background
        self.page.set_fill_color(255, 255, 255)
        self.page.rect(7, 17, self.page.w - 14, self.page.h - 28, style="F")


class NoHeader(Header):
    def header(self):
        pass


class Footer(ABC):
    def __init__(self, page) -> None:
        self.page = page

    @abstractmethod
    def footer(self, page):
        pass


class VisualFooter(Footer):
    # TODO Clean the previous implementation
    def footer(self):
        # Page numbers in the footer
        self.page.set_font("Din", "", 12)
        self.page.set_text_color(255, 255, 255)
        s = str(self.page.page_number)
        self.page.text(self.page.w - 5, self.page.h - 2, s)

        self.page.set_font("Din Italic", "", 6)
        s = FOOTER_TEXT
        self.page.text(
            ((self.page.w / 2) - self.page.get_string_width(s) / 2) - 15,
            self.page.h - 3,
            s,
        )


class AppendixFooter(Footer):
    # TODO
    def footer(self):
        pass


class NoFooter(Footer):
    def footer(self):
        pass


class Document(FPDF):
    class Preset(Enum):
        DEFAULT = "default"
        VISUAL = "visual"
        APPENDIX = "appendix"
        COVER = "cover"

    def __init__(self):
        super().__init__()
        FPDF.__init__(self, format="Letter")
        self.header_behavior = NoHeader(self)
        self.footer_behavior = NoFooter(self)
        self.section_number = None
        self._page_number = 0
        self.visuals_no = 1
        self.tables_start_num = 1
        self.header_title = ""
        self.header_sub_title = ""
        self.add_fonts()

    def multi_cell(
        self,
        w,
        h=None,
        txt="",
        border=0,
        align=Align.J,
        fill=False,
        split_only=False,
        link="",
        ln="DEPRECATED",
        max_line_height=None,
        markdown=False,
        print_sh=False,
        new_x=XPos.RIGHT,
        new_y=YPos.NEXT,
    ):
        txt = txt.upper()
        return super().multi_cell(
            w,
            h,
            txt,
            border,
            align,
            fill,
            split_only,
            link,
            ln,
            max_line_height,
            markdown,
            print_sh,
            new_x,
            new_y,
        )

    def multi_cell_normal(
        self,
        w,
        h=None,
        txt="",
        border=0,
        align=Align.J,
        fill=False,
        split_only=False,
        link="",
        ln="DEPRECATED",
        max_line_height=None,
        markdown=False,
        print_sh=False,
        new_x=XPos.RIGHT,
        new_y=YPos.NEXT,
    ):
        return super().multi_cell(
            w,
            h,
            txt,
            border,
            align,
            fill,
            split_only,
            link,
            ln,
            max_line_height,
            markdown,
            print_sh,
            new_x,
            new_y,
        )

    def cell(
        self,
        w=None,
        h=None,
        txt: str = "",
        border=0,
        ln="DEPRECATED",
        align=Align.L,
        fill=False,
        link="",
        center="DEPRECATED",
        markdown=False,
        new_x=XPos.RIGHT,
        new_y=YPos.TOP,
    ) -> bool:
        txt = txt.upper()
        return super().cell(
            w, h, txt, border, ln, align, fill, link, center, markdown, new_x, new_y
        )

    def cell_normal(
        self,
        w=None,
        h=None,
        txt: str = "",
        border=0,
        ln="DEPRECATED",
        align=Align.L,
        fill=False,
        link="",
        center="DEPRECATED",
        markdown=False,
        new_x=XPos.RIGHT,
        new_y=YPos.TOP,
    ) -> bool:
        return super().cell(
            w, h, txt, border, ln, align, fill, link, center, markdown, new_x, new_y
        )

    def text(self, x: float, y: float, txt: str = "") -> None:
        txt = txt.upper()
        return super().text(x, y, txt)

    def text_normal(self, x: float, y: float, txt: str = "") -> None:
        return super().text(x, y, txt)

    @property
    def page_number(self):
        self._page_number += 1
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        if value < 0:
            raise ValueError("Invalid value")

        self._page_number = value

    def header(self) -> None:
        self.header_behavior.header()

    def footer(self) -> None:
        self.footer_behavior.footer()

    def set_preset(self, preset: Preset) -> None:
        # Validate the inputted preset
        if preset not in [preset.value for preset in Document.Preset]:
            raise ValueError("Invalid preset")

        # Preset configs
        mapping = {
            Document.Preset.DEFAULT.value: (NoHeader(self), NoFooter(self)),
            Document.Preset.VISUAL.value: (VisualHeader(self), VisualFooter(self)),
            Document.Preset.APPENDIX.value: (
                AppendixHeader(self),
                AppendixFooter(self),
            ),
            Document.Preset.COVER.value: (CoverHeader(self), NoFooter(self)),
        }

        # Set behavior to the desired preset
        self.header_behavior, self.footer_behavior = mapping[preset]

    # TODO Remove both setters
    def set_header_title(self, title: str) -> None:
        self.header_title = title

    def set_header_sub_title(self, sub_title: str) -> None:
        self.header_sub_title = sub_title

    def set_section(self, section_number: int):
        # Validation
        if not isinstance(section_number, int):
            raise TypeError("section must be an integer")
        if not 13 > section_number > 0:
            raise ValueError("section must fall between 1 and 12 inclusive")

        self.section_number = section_number

    # TODO Clean
    def add_fonts(self) -> None:
        self.add_font("Segoe-UI", "", f"{CURDIRPATH}/fonts/SegoeUI.ttf", uni=True)
        self.add_font(
            "Segoe UI Bold", "", f"{CURDIRPATH}/fonts/SegoeUI-Bold.ttf", uni=True
        )
        self.add_font(
            "Segoe-UIL", "", f"{CURDIRPATH}/fonts/SegoeUI-Light.ttf", uni=True
        )
        self.add_font(
            "Segoe UI Italic", "", f"{CURDIRPATH}/fonts/SegoeUI-Italic.ttf", uni=True
        )
        self.add_font(
            "seguisb", "", f"{CURDIRPATH}/fonts/SegoeUI-SemiBold.ttf", uni=True
        )
        self.add_font("Din", "", f"{CURDIRPATH}/fonts/DIN-Thin.ttf", uni=True)
        self.add_font("Din Bold", "", f"{CURDIRPATH}/fonts/DIN-Bold.ttf", uni=True)
        self.add_font("Din Italic", "", f"{CURDIRPATH}/fonts/DIN-Italic.ttf", uni=True)
        self.add_font("Din Medium", "", f"{CURDIRPATH}/fonts/DIN-Medium.ttf", uni=True)

        self.add_font("Calibri", "", f"{CURDIRPATH}/fonts/Calibri.ttf", uni=True)
        self.add_font("Calibrii", "", f"{CURDIRPATH}/fonts/Calibrii.ttf", uni=True)
        self.add_font(
            "Calibri Bold", "", f"{CURDIRPATH}/fonts/Calibri Bold.ttf", uni=True
        )
        self.add_font("ROCK", "", f"{CURDIRPATH}/fonts/ROCK.ttf", uni=True)
        self.add_font("ROCKI", "", f"{CURDIRPATH}/fonts/ROCKI.ttf", uni=True)
        self.add_font("ROCK Bold", "", f"{CURDIRPATH}/fonts/rockb.ttf", uni=True)
        self.add_font(
            "Verdana Bold", "", f"{CURDIRPATH}/fonts/Verdana Bold.ttf", uni=True
        )
