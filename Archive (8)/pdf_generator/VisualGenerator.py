from PIL import Image
from typing import Any, Callable, Dict, Optional, List
import sys
from pdf_generator.services.ReportMetaDataRepository import ReportMetaDataRepository
from pdf_generator.services.constants import ID
from pdf_generator.models import enums
from pdf_generator.services.dataRepository import DataRepository


class VisualGenerator:
    def __init__(
        self, data: DataRepository, meta_data: ReportMetaDataRepository
    ) -> None:
        self.data = data
        self.meta_data = meta_data
        self.player1, self.player2 = self.data.players_name()

    @staticmethod
    def parse_args(kwargs: Dict) -> Dict[Any, Any]:
        for parameter, value in kwargs.items():
            # Handling Enums
            if isinstance(value, str) and "." in value:
                value = value.split(".")
                enum_class = getattr(enums, value[0])
                enum = getattr(enum_class, value[1])
                kwargs[parameter] = enum

        return kwargs

    def generate_visual(
        self,
        id: int,
        output_path: Optional[str] = None,
        image_name: Optional[str] = None,
    ) -> Image.Image:
        # Fetch visual info from the database
        visual = (
            self.meta_data.get_visual_by_id(id + 200)
            if self.meta_data.get_visual_by_id(id + 200)
            else self.meta_data.get_visual_by_id(id)
        )
        if not visual:
            print("Invalid visual id", file=sys.stderr)
            exit(1)

        try:
            # Get visual data
            data_source: Callable = visual.get_data_source()
            visual_data: dict = data_source(
                self.data, **self.parse_args(visual.data_source_args)
            )
        except:
            print("Data error", file=sys.stderr)
            exit(2)

        # Select the proper template from visual info
        template: Callable = visual.get_template()

        image: Image.Image = template(player_name=self.player1, **visual_data)
        image.format = "JPEG"
        if output_path:
            if not image_name:
                image_name = f"{ID}-visual-{id}"

            image = image.convert("RGB")
            image.save(f"{output_path}/{image_name}.jpg")

            # image.save(f"{output_path}/{image_name}.png")

        return image

    def get_ellipses(
        self, id: int, ellipse_dict: Dict[str, List[int]]
    ) -> List[Dict[str, float]]:
        # Fetch visual info from the database
        visual = (
            self.meta_data.get_visual_by_id(id + 200)
            if self.meta_data.get_visual_by_id(id + 200)
            else self.meta_data.get_visual_by_id(id)
        )
        if not visual:
            print("Invalid visual id", file=sys.stderr)
            exit(1)

        # Select the proper template from visual info
        template: Callable = visual.get_ellipse()

        return template(ellipse_dict)
