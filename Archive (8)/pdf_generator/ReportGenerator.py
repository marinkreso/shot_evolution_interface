import os
import uuid
from enum import Enum
from time import sleep
from pathlib import Path
from threading import Thread
from typing import List, Tuple
from multiprocessing import Process

from PyPDF2 import PageObject
from PyPDF2 import PdfMerger, PdfReader, PdfWriter, Transformation
from pdf_generator.pages.document import Document
from pdf_generator.pages.scatter_plot import RallyScatterPlotPage
from pdf_generator.services.constants import TEMPFOLDER

from pdf_generator.pages import (
    corestatsPage,
    serveLocationAPage,
    serveLocationBPage,
    headerPage,
    matchListPage,
    finalPage,
    goodRetrunsAPage,
    goodReturnsBPage,
    firstShotOffReturnPage,
    returnLocationPage,
    returnLocationCPage,
    returnLocationCInvPage,
    serveLocationCPage,
    serveLocationCInvPage,
    rallyEndingPage,
    rallyEndingTablePage,
    secondToLastPage,
    secondToLast2Page,
    serveLocationAInvPage,
    newRallyLengthPage,
)

from pdf_generator.pages.rallyEndingDirection import RallyEndingDirection
from pdf_generator.pages.AllGroundstrokesDirection import AllGroundstrokesDirection
from pdf_generator.pages.shotAfterReturnLocation import ShotAfterReturnLocation
from pdf_generator.pages.appendixPage import Appendix
from pdf_generator.pages.appendixPage2 import AppendixPage2
from pdf_generator.pages.appendixPage3 import AppendixPage3
from pdf_generator.pages.serveRallyPointsPage import AppendixPage4
from pdf_generator.pages.lastShotPage import LastShot


class ReportGenerator:
    class Category(Enum):
        SCOUTING = "scouting"
        MATCHUP = "matchup"

    class Type(Enum):
        COMPLETE_PLUS = "complete+"
        COMPLETE = "complete"
        SHORT = "short"
        TC = "TCv1.0"

    class Variant(Enum):
        COMBINED = "with_gs"
        NONCOMBINED = "no_gs"

    def __init__(self, data, visuals_generator, report_params) -> None:
        self.data = data
        self.visuals_generator = visuals_generator
        self.game_selection = data.get_game_selection()
        self.set_selection = data.get_set_selection()
        self.serve_selection = data.get_serve_selection()
        self.category = ReportGenerator.Category(report_params.category)
        self.type = ReportGenerator.Type(report_params.type)
        self.variant = ReportGenerator.Variant(report_params.mode)
        self.is_new = report_params.new
        self.output_path = report_params.output
        self.name = self.generate_report_file_name()
        self.id = str(uuid.uuid4())

    def generate_report_file_name(self):
        report_inputs = self.data.get_report_inputs()
        name = f"{report_inputs['target']} {report_inputs['subtitle']}{' TCv1.0 ' if self.type == ReportGenerator.Type.TC else ' '}{self.report_title()}"
        if self.game_selection.value == "All":
            if self.serve_selection.value != "All":
                name = (
                    name
                    + ", "
                    + f"({self.game_selection.value} Games as {self.serve_selection.value})"
                )
        else:
            if self.serve_selection.value != "All":
                name = (
                    name
                    + ", "
                    + f"({self.game_selection.value} Games as {self.serve_selection.value})"
                )
            else:
                name = name + ", " + f"({self.game_selection.value} Games)"
        
        if self.set_selection.value != "All":
            name = name + ", " + f"({self.set_selection.value} Sets)"
        return name

    def get_output_path(self):
        return f"{self.output_path}/{self.name}.pdf"

    def report_title(self):
        title = ""
        title += "Short " if self.type == ReportGenerator.Type.SHORT else ""
        title += (
            "Scouting "
            if self.category == ReportGenerator.Category.SCOUTING
            else "Match-Up "
        )
        title += "Report"
        title += " With Groundstrokes" if self.variant == self.variant.COMBINED else ""
        title += " (New)" if self.is_new else ""
        return title

    def get_report_pages(self):
        report_selection = {
            ReportGenerator.Category.SCOUTING: 0,
            ReportGenerator.Category.MATCHUP: 1,
        }

        index = report_selection[self.category]
        is_tc = True if self.type == ReportGenerator.Type.TC else False
        is_complete = (
            True
            if self.type
            in (ReportGenerator.Type.COMPLETE, ReportGenerator.Type.COMPLETE_PLUS)
            else False
        )
        is_combined = (
            True
            if self.variant == ReportGenerator.Variant.COMBINED
            and self.data.report_metadata()["GS"]
            else False
        )
        has_mt_data = (
            True if self.data.report_metadata()["MT"] and is_complete else False
        )
        has_GD_data = (
            True if self.data.report_metadata()["GD"] and is_complete else False
        )
        is_complete_plus = (
            True
            if self.type == ReportGenerator.Type.COMPLETE_PLUS and is_combined
            else False
        )

        # TODO fix ServeLocationCPage & INV naming
        page_selection = {
            (headerPage.Header, self.report_title()): [True, True],
            (matchListPage.MatchList, None): [True, True],
            (corestatsPage.CoreStats, None): [True, True],
            (serveLocationAPage.ServeLocationA, "1st"): [True, True],
            (serveLocationBPage.ServeLocationB, "1st"): [not is_tc, not is_tc],
            (serveLocationCPage.ServeLocationCPage, "1st"): [has_mt_data, has_mt_data],
            (firstShotOffReturnPage.FirstShotOffReturnPage, "First"): [
                is_complete,
                is_complete,
            ],
            (returnLocationCPage.ReturnLocationCPage, "1st"): [
                has_mt_data,
                has_mt_data,
            ],
            (serveLocationAPage.ServeLocationA, "2nd"): [True, True],
            (serveLocationBPage.ServeLocationB, "2nd"): [not is_tc, not is_tc],
            (serveLocationCPage.ServeLocationCPage, "2nd"): [has_mt_data, has_mt_data],
            (firstShotOffReturnPage.FirstShotOffReturnPage, "Second"): [
                is_complete,
                is_complete,
            ],
            (returnLocationCPage.ReturnLocationCPage, "2nd"): [
                has_mt_data,
                has_mt_data,
            ],
            (serveLocationAInvPage.ServeLocationAINV, "1st"): [False, not is_tc],
            (serveLocationCInvPage.ServeLocationCInvPage, "1st"): [
                has_mt_data,
                has_mt_data,
            ],
            # (ReturnSpeedPage.ReturnSpeed, "1st"): [is_complete, is_complete],
            (goodRetrunsAPage.GoodReturnsA, "1st"): [not is_tc, not is_tc],
            (goodReturnsBPage.GoodReturnsB, "1st"): [not is_tc, not is_tc],
            (returnLocationPage.ReturnLocationPage, "First"): [
                is_complete,
                is_complete,
            ],
            (returnLocationCInvPage.ReturnLocationCInvPage, "1st"): [
                has_mt_data,
                has_mt_data,
            ],
            (serveLocationAInvPage.ServeLocationAINV, "2nd"): [False, not is_tc],
            (serveLocationCInvPage.ServeLocationCInvPage, "2nd"): [
                has_mt_data,
                has_mt_data,
            ],
            # (ReturnSpeedPage.ReturnSpeed, "2nd"): [is_complete, is_complete],
            (goodRetrunsAPage.GoodReturnsA, "2nd"): [not is_tc, not is_tc],
            (goodReturnsBPage.GoodReturnsB, "2nd"): [not is_tc, not is_tc],
            (returnLocationPage.ReturnLocationPage, "Second"): [
                is_complete,
                is_complete,
            ],
            (returnLocationCInvPage.ReturnLocationCInvPage, "2nd"): [
                has_mt_data,
                has_mt_data,
            ],
            (ShotAfterReturnLocation, "1st"): [
                is_combined and is_complete,
                is_combined and is_complete,
            ],
            (ShotAfterReturnLocation, "2nd"): [
                is_combined and is_complete,
                is_combined and is_complete,
            ],
            (newRallyLengthPage.RallyLengthPage, None): [is_complete, is_complete],
            (rallyEndingPage.RallyEnding, "1st"): [
                is_combined and not is_tc,
                is_combined and not is_tc,
            ],
            (rallyEndingPage.RallyEnding, "2nd"): [
                is_combined and not is_tc,
                is_combined and not is_tc,
            ],
            (rallyEndingTablePage.RallyEndingTable, None): [
                is_combined and not is_tc,
                is_combined and not is_tc,
            ],
            (RallyEndingDirection, None): [
                is_complete and is_combined,
                is_complete and is_combined,
            ],
            (AllGroundstrokesDirection, None): [
                has_GD_data and is_combined,
                has_GD_data and is_combined,
            ],
            (RallyScatterPlotPage, 9): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (RallyScatterPlotPage, 10): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (RallyScatterPlotPage, 11): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (RallyScatterPlotPage, 12): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (RallyScatterPlotPage, 13): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (RallyScatterPlotPage, 14): [
                has_mt_data and is_complete_plus,
                has_mt_data and is_complete_plus,
            ],
            (Appendix, self.report_title()): [is_complete, is_complete],
            (AppendixPage2, 1): [is_complete, is_complete],
            (AppendixPage3, 1): [is_complete, is_complete],
            (AppendixPage2, 2): [is_complete and is_combined, is_complete],
            (AppendixPage3, 2): [is_complete and is_combined, is_complete],
            (AppendixPage4, "1st"): [is_complete, is_complete],
            (AppendixPage4, "2nd"): [is_complete, is_complete],
            (LastShot, 1): [is_complete and is_combined, is_complete and is_combined],
            (LastShot, 2): [is_complete and is_combined, is_complete and is_combined],
            (secondToLastPage.SecondToLast, 1): [
                is_complete and is_combined,
                is_complete and is_combined,
            ],
            (secondToLast2Page.SecondToLast, 1): [
                is_complete and is_combined,
                is_complete and is_combined,
            ],
            (secondToLastPage.SecondToLast, 2): [
                is_complete and is_combined,
                is_complete and is_combined,
            ],
            (secondToLast2Page.SecondToLast, 2): [
                is_complete and is_combined,
                is_complete and is_combined,
            ],
            (finalPage.Final, None): [True, True],
        }

        return [page for page, option in page_selection.items() if option[index]]

    def generate_page(self, document, page, variant):
        # Handle new serve location page
        if page == serveLocationAPage.ServeLocationA:
            variant = (variant, self.is_new)
        page = (
            page(document, self.data, variant, self.visuals_generator)
            if getattr(page, "requires_visual_generator", None)
            else page(document, self.data, variant)
        )
        page.build_page_body()
        print(f"{page.name} generated")

    def generate_batch(
        self, batch_pages, start_page_number, visuals_start_no, tables_start_no, file_no
    ):
        from pdf_generator.services.constants import ID

        # Document config
        document = Document()
        document.page_number = start_page_number
        document.visuals_no = visuals_start_no
        document.tables_start_num = tables_start_no

        for page, variant in batch_pages:
            self.generate_page(document, page, variant)

        document.output(f"{TEMPFOLDER}/PdfGeneratorTemp/{self.id}-{file_no}.pdf", "F")

        # Clean temporary files
        temp_dir = Path(f"{TEMPFOLDER}/PdfGeneratorTemp/")
        for file_path in temp_dir.glob(f"{ID}*"):
            os.unlink(file_path)

    def generate_report(self):
        pages = self.get_report_pages()
        output_file_path = self.get_output_path()
        total_cost = sum([page.execution_cost for page, _ in pages])

        def generate_using_single_thread():
            document = Document()
            for page, variant in pages:
                self.generate_page(document, page, variant)
            document.output(f"{self.output_path}/report.pdf", "F")

        def generate_using_balanced_batches():
            visuals_start_no = 1
            tables_start_no = 1

            processes = []

            no_batches = 3
            no_pages = len(pages)
            batch_cost = total_cost / no_batches
            page_number_tracker = 0
            start = 0
            end = 1
            for batch_no in range(no_batches):
                is_last_batch = batch_no == no_batches - 1

                if not is_last_batch:
                    while True:
                        current_cost = sum(
                            [page.execution_cost for page, _ in pages[start:end]]
                        )
                        if current_cost > batch_cost or end > no_pages:
                            break
                        else:
                            end += 1

                    batch = pages[start:end]
                    start = end
                    end += 1
                else:
                    batch = pages[start:]
                process = Process(
                    target=self.generate_batch,
                    args=(
                        batch,
                        page_number_tracker,
                        visuals_start_no,
                        tables_start_no,
                        batch_no,
                    ),
                )
                page_number_tracker += len(batch)
                processes.append(process)
                process.start()

                visuals_start_no += sum([page.visual_counter for page, _ in batch])
                tables_start_no += sum([page.table_counter for page, _ in batch])

            for process in processes:
                process.join()

            merger = PdfMerger()

            for file in range(no_batches):
                merger.append(f"{TEMPFOLDER}/PdfGeneratorTemp/{self.id}-{file}.pdf")

            merger.write(output_file_path)

            merger.close()

            # Clean temporary files
            temp_dir = Path(f"{TEMPFOLDER}/PdfGeneratorTemp/")
            for file_path in temp_dir.glob(f"{self.id}*"):
                os.unlink(file_path)

            print("Generated report name:")
            print(f"{self.name}.pdf")

        # generate_using_balanced_batches()
        generate_using_single_thread()

        return (Path(output_file_path), pages)

    # TODO: This is just a blueprint, refactor required

    def merge_reports(
        self,
        pdf1_path: Path,
        pdf2_path: Path,
        report1_pages: List[Tuple],
        report2_pages: List[Tuple],
    ) -> None:
        pdf1_file = open(pdf1_path, "rb")
        pdf2_file = open(pdf2_path, "rb")

        pdf1_reader = PdfReader(pdf1_file)
        pdf2_reader = PdfReader(pdf2_file)

        if len(pdf1_reader.pages) < len(pdf2_reader.pages):
            pdf1_reader, pdf2_reader = pdf2_reader, pdf1_reader
            report1_pages, report2_pages = report2_pages, report1_pages

        pages_no = len(pdf1_reader.pages)

        pdf_writer = PdfWriter()

        i = j = 0
        while i < pages_no:
            pdf1_page = pdf1_reader.pages[i]
            pdf2_page = pdf2_reader.pages[j]

            width = pdf1_page.mediabox.width
            height = pdf1_page.mediabox.height

            report1_page = report1_pages[i]
            report2_page = report2_pages[j]

            blank_page = PageObject.create_blank_page(
                pdf=None, width=width * 2, height=height
            )
            transformation = Transformation().translate(width, 0)

            if report1_page == report2_page:
                # Merge the two pages side by side
                pdf2_page.add_transformation(transformation, expand=True)
                blank_page.merge_page(pdf1_page, expand=True)
                blank_page.merge_page(pdf2_page, expand=True)
                pdf_writer.add_page(blank_page)

                # Increment the short PDF pointer
                j += 1

            else:
                # Write only the page of the longer PDF
                blank_page.merge_page(pdf1_page, expand=True)
                pdf_writer.add_page(blank_page)

            # Increment the long PDF pointer
            i += 1

        with open(f"{self.output_path}/merged-{self.name}.pdf", "wb") as f:
            print(f"merged-{self.name}.pdf")
            pdf_writer.write(f)

        pdf1_file.close()
        pdf2_file.close()
