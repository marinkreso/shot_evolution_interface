from functools import partial
import re
from typing import List, Tuple, Optional
from .JsonAggregateDAL import JsonAggregateDAL
from pdf_generator.visuals.templates import ColorPreset
from pdf_generator.models.enums import (
    Serve,
    Surface,
    ShotType,
    StatType,
    Category,
    ServeStat,
    PointType,
    CourtSide,
    MovementType,
    Distribution,
    GameSelection,
    SetSelection,
    ServeSelection,
    ServeDirection,
    ReturnDirection,
    SurfaceCode,
)


class DataRepository:
    def __init__(self, json_aggregate: JsonAggregateDAL):
        self.json_aggregate = json_aggregate

    @property
    def target_hand_id(self) -> int:
        return self.json_aggregate.target_hand

    @property
    def opponent_hand_id(self) -> int:
        return self.json_aggregate.opponent_hand

    @property
    def category(self) -> Category:
        if self.json_aggregate.category == 1:
            return Category.ATP
        elif self.json_aggregate.category == 2:
            return Category.WTA
        elif self.json_aggregate.category == 3:
            return Category.ITF

    @property
    def gs_matches_count(self) -> int:
        return self.json_aggregate.gs_matches_count

    @property
    def surface(self) -> Surface:
        surface_id = self.json_aggregate.get_surface_id()
        if surface_id == 2:
            return Surface.HARD
        if surface_id == 4:
            return Surface.GRASS
        if surface_id == 8:
            return Surface.CLAY
        if surface_id == 16:
            return Surface.CARPET
        if surface_id == 32:
            return Surface.ALL
        if surface_id == 64:
            return Surface.ACRYLIC

    def get_opponents_names(self):
        """
        Retrieves the names of opponents for a given target player.

        Returns:
            A dictionary containing the names of opponents as keys and their hand (R or L) as values.
        """
        target, _ = self.json_aggregate.players_name()

        if target[0].isdigit():
            return {}

        target = target.replace("-", " ")
        opponents = {}
        matches = self.json_aggregate.get_match_list()

        # Matches are in the format:
        # Van de Zandschulp_R-Nadal_L--Wimbledon--2022--R16--SM.xlsx
        # Nadal_L-Tiafoe_R--US Open--2022--R16--SM.xlsx
        # Auger-Aliassime_R-Nadal_L--Turin--2022--RR--SM.xlsx

        pattern = re.compile(r"([A-Za-z\-]+)_([RL])")

        for match in matches:
            players = pattern.findall(match["File Name"])[:2]

            for player, hand in players:
                player_name = player.replace("-", " ").strip()
                if player_name != target:
                    opponents[player_name] = hand

        return opponents

    def get_game_selection(self):
        if self.json_aggregate.game_selection == 0:
            return GameSelection.WON
        elif self.json_aggregate.game_selection == 1:
            return GameSelection.LOST
        else:
            return GameSelection.ALL
        
    def get_set_selection(self):
        if self.json_aggregate.set_selection == 0:
            return SetSelection.WON
        elif self.json_aggregate.set_selection == 1:
            return SetSelection.LOST
        else:
            return SetSelection.ALL

    def get_serve_selection(self):
        if self.json_aggregate.serve_selection == 0:
            return ServeSelection.SERVER
        elif self.json_aggregate.serve_selection == 1:
            return ServeSelection.RETURNER
        else:
            return ServeSelection.ALL

    def get_player_handedness(self, key: str) -> str:
        self.json_aggregate.get_player_handedness(key)

    def get_player_id(self, key: str) -> int:
        return self.json_aggregate.get_player_id(key)

    def get_surface_id(self) -> int:
        return self.json_aggregate.get_surface_id()

    def get_surface(self) -> SurfaceCode:
        surface_id = self.json_aggregate.get_surface_id()
        surface_id = (
            surface_id
            if surface_id in (surface.value for surface in SurfaceCode)
            else 0
        )
        return SurfaceCode(surface_id)

    def is_lefthanded(self):
        return self.json_aggregate.is_lefthanded()

    def cover_page_sub_titles(self):
        return self.json_aggregate.cover_page_sub_titles()

    def core_stats_table_data(self):
        return self.json_aggregate.core_stats_table_data()

    def serve_stats_table_data(self):
        return self.json_aggregate.serve_stats_table_data()

    def scatter_plot_data(
        self,
        table_no: int,
        inv: Optional[bool] = False,
        half_court: Optional[bool] = False,
    ):
        data = self.json_aggregate.MT_tables()[f"Table{table_no}"]
        cleaned_data = {
            "points_x_coordinates": [],
            "points_y_coordinates": [],
            "inv": inv,
            "surface": self.get_surface(),
        }
        if half_court:
            cleaned_data["half_court"] = half_court

        for point in data:
            cleaned_data["points_x_coordinates"].append(point["X"])
            cleaned_data["points_y_coordinates"].append(point["Y"])

        return cleaned_data

    def rally_ending_table_data(self):
        return self.json_aggregate.rally_ending_table_data()

    def match_list_table(self):
        return self.json_aggregate.match_list_table()

    def players_name(self):
        return self.json_aggregate.players_name()

    def get_report_inputs(self):
        return self.json_aggregate.get_report_inputs()

    def avg_return_speed(self, player_no):
        return self.json_aggregate.avg_return_speed(player_no)

    def return_v_serve_speed(self, position, player_no):
        return self.json_aggregate.return_v_serve_speed(
            position=position, player_no=player_no
        )

    def GS_stats(self, mode, player_no):
        return self.json_aggregate.GS_stats(mode=mode, player_no=player_no)

    def GS_pair(self, pos, player_no):
        return self.json_aggregate.GS_pair(pos=pos, player_no=player_no)

    def GS_all_shots(self, pos, player_no):
        return self.json_aggregate.GS_all_shots(pos=pos, player_no=player_no)

    def report_metadata(self):
        return self.json_aggregate.report_metadata()

    def serve_rally_points(self, serve_no, is_pressure):
        return self.json_aggregate.serve_rally_points(serve_no, is_pressure)

    def serve_location_a(
        self,
        serve_no: Serve,
        is_new: Optional[bool] = False,
        all_serves: Optional[bool] = False,
        serve_speed: Optional[bool] = False,
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
            "is_new": is_new,
            "all_serves": all_serves,
            "serve_speed": serve_speed,
            "serve_speed_values": [],
        }

        in_serves_data = self.json_aggregate.serve_stats_values(
            StatType.SMHC, ServeStat.IN
        )
        missed_serves = self.json_aggregate.serve_stats_values(
            StatType.SMHC, ServeStat.MISS
        )

        if serve_speed:
            serves_speed_data = self.json_aggregate.serve_speed_values(Distribution.AVG)

        for court in ("Ad", "Deuce"):
            directions = ["Wide", "Body", "T"]
            if court == "Deuce":
                directions.reverse()

            if all_serves:
                totals = []
                for direction in directions:
                    hit = in_serves_data[f"{serve_no.value}{court}{direction}"]
                    missed = missed_serves[f"{serve_no.value}{court}{direction}"]
                    totals.append(hit + missed)

            for direction in directions:
                percent = round(
                    in_serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = in_serves_data[f"{serve_no.value}{court}{direction}"]
                miss_serves = missed_serves[f"{serve_no.value}{court}{direction}"]
                total = hit_serves + miss_serves
                if all_serves:
                    percent = round(total / sum(totals) * 100 if sum(totals) else 0)

                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(
                    str(round(serves_speed_data[f"{serve_no.value}{court}{direction}"]))
                    if serve_speed and not is_new
                    else f"{percent}%"
                )
                if serve_speed:
                    cleaned_data["serve_speed_values"].append(
                        round(serves_speed_data[f"{serve_no.value}{court}{direction}"])
                    )
                cleaned_data["numbers"].append(hit_serves if not all_serves else total)

                if not serve_speed:
                    cleaned_data["pies_percentages"].append(
                        round(hit_serves / total * 100) if total else -1
                    )
        return cleaned_data

    def serve_location_b(
        self,
        serve_no: Serve,
        point_type: PointType,
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "preset": ColorPreset.ORANGE,
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
        }

        in_serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC, ServeStat.IN, point_type
        )
        wining_serves = self.json_aggregate.serve_stats_values(
            StatType.BASIC, ServeStat.WON, point_type
        )
        for court in ("Ad", "Deuce"):
            directions = ["Wide", "Body", "T"]
            if court == "Deuce":
                directions.reverse()

            for direction in directions:
                percent = round(
                    in_serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = in_serves_data[f"{serve_no.value}{court}{direction}"]
                won_serves = wining_serves[f"{serve_no.value}{court}{direction}"]

                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(f"{percent}%")
                cleaned_data["numbers"].append(hit_serves)
                cleaned_data["pies_percentages"].append(
                    round(won_serves / hit_serves * 100 if hit_serves else -1)
                )
        return cleaned_data

    def serve_location_c(
        self,
        serve_no: Serve,
        point_type: PointType,
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "preset": ColorPreset.ORANGE,
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
        }

        in_serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC, ServeStat.IN, point_type
        )
        unreturned_serves = self.json_aggregate.serve_stats_values(
            StatType.BASIC, ServeStat.ACES, point_type
        )
        for court in ("Ad", "Deuce"):
            directions = ["Wide", "Body", "T"]
            if court == "Deuce":
                directions.reverse()

            for direction in directions:
                percent = round(
                    in_serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = in_serves_data[f"{serve_no.value}{court}{direction}"]
                won_serves = unreturned_serves[f"{serve_no.value}{court}{direction}"]

                percent = round(
                    won_serves / hit_serves
                )

                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(f"{percent}%")
                cleaned_data["numbers"].append(hit_serves)
                cleaned_data["pies_percentages"].append(
                    round(won_serves / hit_serves * 100 if hit_serves else -1)
                )
        return cleaned_data
    
    def first_shot_off_return(
        self, serve_no: Serve, court_side: CourtSide, serve_direction: ServeDirection
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "court_side": court_side,
            "serve_direction": serve_direction,
            "arrows_widths": [],
            "numbers": [],
            "pies_percentages": [],
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
        }
        serve_stat = [
            {
                "won": ServeStat.WON_CROSS,
                "total": ServeStat.TOTAL_CROSS,
            },
            {
                "won": ServeStat.WON_MIDDLE,
                "total": ServeStat.TOTAL_MIDDLE,
            },
            {
                "won": ServeStat.WON_LINE,
                "total": ServeStat.TOTAL_LINE,
            },
        ]

        if court_side == CourtSide.AD:
            serve_stat.reverse()

        data = self.json_aggregate.stats_section(StatType.BASIC)
        key = f"{serve_no.value}{court_side.value}{serve_direction.value}"

        for direction in serve_stat:
            total = data[direction["total"].value][key]
            won = data[direction["won"].value][key]
            percent = won / total * 100 if total else -1

            cleaned_data["numbers"].append(total)
            cleaned_data["pies_percentages"].append(round(percent))

        total_sum = sum(cleaned_data["numbers"])
        for number in cleaned_data["numbers"]:
            cleaned_data["arrows_widths"].append(
                round(number / total_sum * 100) if total_sum else 0
            )

        return cleaned_data

    def serve_location_a_inv(
        self,
        serve_no: Serve,
        speed: Optional[bool] = False,
        won: Optional[bool] = False,
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "preset": ColorPreset.ORANGE if won else ColorPreset.RED,
            "clear": True,
            "surface": self.get_surface(),
        }
        stats_type = StatType.BASIC if won else StatType.SMHC
        serve_stat = ServeStat.WON if won else ServeStat.MISS

        serves_data = self.json_aggregate.serve_stats_values(
            stats_type,
            ServeStat.IN,
            player_no=2,
        )
        missed_serves_data = self.json_aggregate.serve_stats_values(
            stats_type,
            serve_stat,
            player_no=2,
        )

        if speed:
            serves_speed_data = self.json_aggregate.serve_speed_values(
                Distribution.AVG, player_no=2
            )

        for court in ("Deuce", "Ad"):
            directions = ["Wide", "Body", "T"]
            if court == "Ad":
                directions.reverse()

            for direction in directions:
                percent = round(
                    serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = serves_data[f"{serve_no.value}{court}{direction}"]
                missed_serves = missed_serves_data[
                    f"{serve_no.value}{court}{direction}"
                ]
                total = hit_serves + missed_serves

                # pie in/return  arrows return / total
                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(
                    f"{percent}%"
                    if not speed
                    else str(
                        round(serves_speed_data[f"{serve_no.value}{court}{direction}"])
                    )
                )
                if not speed:
                    cleaned_data["numbers"].append(hit_serves)
                    if won:
                        pie_percent = (
                            round((hit_serves - missed_serves) / hit_serves * 100)
                            if hit_serves
                            else -1
                        )
                    else:
                        pie_percent = round(hit_serves / total * 100) if total else -1

                    cleaned_data["pies_percentages"].append(pie_percent)
        return cleaned_data

    def good_returns_a(
        self,
        serve_no: Serve,
        won: Optional[bool] = False,
        by_direction: Optional[bool] = False,
        player_no: Optional[int] = 0,
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "preset": ColorPreset.ORANGE if won else ColorPreset.RED,
            "clear": True if by_direction else False,
            "surface": self.get_surface(),
        }

        serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC,
            ServeStat.RETURN,
            PointType.RETURN_NORMAL,
        )
        in_serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC,
            ServeStat.IN_RETURN if not won else ServeStat.WON_RETURN,
            PointType.RETURN_NORMAL,
        )
        if player_no:
            return_speed_data = self.json_aggregate.get_return_speed(player_no)
            cleaned_data["speed"] = []

        for court in ("Deuce", "Ad"):
            directions = ["Wide", "Body", "T"]
            if court == "Ad":
                directions.reverse()

            for direction in directions:
                percent = round(
                    serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = serves_data[f"{serve_no.value}{court}{direction}"]
                in_serves = in_serves_data[f"{serve_no.value}{court}{direction}"]
                total = serves_data[f"{serve_no.value}{court}All"]

                # (pie) in/return | (arrows) return / total
                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(f"{percent}%")
                cleaned_data["numbers"].append(hit_serves)
                cleaned_data["pies_percentages"].append(
                    round(in_serves / hit_serves * 100)
                    if hit_serves
                    else (
                        -1
                        if not by_direction
                        else round(hit_serves / total * 100) if total else -1
                    )
                )
                if player_no:
                    cleaned_data["speed"].append(
                        round(return_speed_data[f"{serve_no.value}{court}{direction}"])
                    )
        if player_no:
            cleaned_data["pies_percentages"] = []
        return cleaned_data

    def good_returns_b(self, serve_no: Serve, point_type: PointType):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "arrows_widths": [],
            "arrows_numbers": [],
            "numbers": [],
            "pies_percentages": [],
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "preset": ColorPreset.ORANGE,
            "surface": self.get_surface(),
        }

        serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC,
            ServeStat.RETURN,
            point_type,
        )
        in_serves_data = self.json_aggregate.serve_stats_values(
            StatType.BASIC,
            ServeStat.WON_RETURN,
            point_type,
        )
        for court in ("Deuce", "Ad"):
            directions = ["Wide", "Body", "T"]
            if court == "Ad":
                directions.reverse()

            for direction in directions:
                percent = round(
                    serves_data[f"{serve_no.value}{court}{direction}Avg"] * 100
                )
                hit_serves = serves_data[f"{serve_no.value}{court}{direction}"]
                in_serves = in_serves_data[f"{serve_no.value}{court}{direction}"]

                cleaned_data["arrows_widths"].append(percent)
                cleaned_data["arrows_numbers"].append(f"{percent}%")
                cleaned_data["numbers"].append(hit_serves)
                cleaned_data["pies_percentages"].append(
                    round(in_serves / hit_serves * 100) if hit_serves else -1
                )
        return cleaned_data

    def return_location(
        self,
        serve_no: Serve,
        court_side: CourtSide,
        serve_direction: ServeDirection,
    ):
        cleaned_data = {
            "return_percentages": [],
            "return_numbers": [],
            "pies_percentages": [],
            "court_side": court_side,
            "serve_direction": serve_direction,
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
        }

        arrow_selector = self.json_aggregate.stats_section(
            StatType.BASIC, PointType.RETURN_NORMAL
        )
        pie_selector = self.json_aggregate.stats_section_2(
            StatType.BASIC, PointType.NORMAL
        )

        total_points = arrow_selector["InReturn"][
            f"{serve_no.value}{court_side.value}{serve_direction.value}"
        ]
        directions = (
            ("Cross", "Middle", "Line")
            if court_side == CourtSide.AD
            else ("Line", "Middle", "Cross")
        )
        for direction in directions:
            return_points = arrow_selector[f"{direction}ReturnsTotal"][
                f"{serve_no.value}{court_side.value}{serve_direction.value}"
            ]
            cleaned_data["return_percentages"].append(
                round(return_points / total_points * 100 if total_points else 0)
            )
            cleaned_data["return_numbers"].append(return_points)

            won_points = pie_selector[f"Won{direction}OpponentReturns"][
                f"{serve_no.value}{court_side.value}{serve_direction.value}"
            ]
            cleaned_data["pies_percentages"].append(
                round((return_points - won_points) / return_points * 100)
                if return_points
                else -1
            )

        return cleaned_data

    def shot_after_return(
        self,
        serve_no: Serve,
        court_side: CourtSide,
        return_direction: ReturnDirection,
    ):
        cleaned_data = {
            "return_percentages": [],
            "return_numbers": [],
            "pies_percentages": [],
            "court_side": court_side,
            "return_direction": return_direction,
            "serve_no": "1st" if serve_no == Serve.FIRST else "2nd",
            "surface": self.get_surface(),
        }

        selector = self.json_aggregate.shot_after_return_values()
        won_data = selector[f"Won{serve_no.value}{court_side.value}"][
            "ShotAfterReturnCounts"
        ][return_direction.value]

        directions = ("Line", "Middle", "Cross")
        if (court_side == CourtSide.AD) ^ (return_direction == ReturnDirection.LINE):
            directions = ("Cross", "Middle", "Line")

        adder = selector[f"{serve_no.value}{court_side.value}"][
            "ShotAfterReturnCounts"
        ][return_direction.value]
        total_points = adder["Cross"] + adder["Middle"] + adder["Line"]

        for direction in directions:
            return_points = selector[f"{serve_no.value}{court_side.value}"][
                "ShotAfterReturnCounts"
            ][return_direction.value][direction]

            cleaned_data["return_percentages"].append(
                round(return_points / total_points * 100 if total_points else 0)
            )
            cleaned_data["return_numbers"].append(return_points)

            won_percentage = (
                round(won_data[direction] / return_points * 100)
                if return_points
                else -1
            )
            cleaned_data["pies_percentages"].append(won_percentage)

        return cleaned_data

    def rally_ending_direction(
        self,
        court_side: CourtSide,
        return_direction: ReturnDirection,
        shot_type: ShotType,
    ):
        cleaned_data = {
            "return_percentages": [],
            "return_numbers": [],
            "pies_percentages": [],
            "court_side": court_side,
            "return_direction": return_direction,
            "shot_type": shot_type,
            "is_left_handed": self.is_lefthanded(),
            "surface": self.get_surface(),
        }

        if self.is_lefthanded() and shot_type == ShotType.BH:
            court_side = CourtSide.DEUCE

        if return_direction == ReturnDirection.LINE:
            court_side = (
                court_side.AD if court_side == CourtSide.DEUCE else CourtSide.DEUCE
            )

        # Get json data for rally ending
        data = self.json_aggregate.rally_ending_direction_values(court_side)

        # Yello arrows direction
        directions = ["Line", "Middle", "Cross"]
        if (court_side == CourtSide.AD) ^ (return_direction == ReturnDirection.LINE):
            directions = ["Cross", "Middle", "Line"]

        # Calculate total points
        total_points = 0
        for direction in directions:
            total_points += data[
                f"{return_direction.value}{shot_type.value}{direction}"
            ]

        for direction in directions:
            template = f"{return_direction.value}{shot_type.value}{direction}"
            points = data[template]
            points_percentage = (
                round(points / total_points * 100) if total_points else 0
            )
            win_percentage = (
                round(data[f"Won{template}"] / points * 100) if points else -1
            )

            cleaned_data["return_numbers"].append(points)
            cleaned_data["return_percentages"].append(points_percentage)
            cleaned_data["pies_percentages"].append(win_percentage)

        return cleaned_data

    def all_ground_strokes_direction(
        self,
        court_side: CourtSide,
        return_direction: ReturnDirection,
        shot_type: ShotType,
    ):
        cleaned_data = {
            "return_percentages": [],
            "return_numbers": [],
            "pies_percentages": [],
            "court_side": court_side,
            "return_direction": return_direction,
            "shot_type": shot_type,
            "is_left_handed": self.is_lefthanded(),
            "gd": True,
            "surface": self.get_surface(),
        }

        if return_direction == ReturnDirection.LINE:
            court_side = (
                CourtSide.AD if court_side == CourtSide.DEUCE else CourtSide.DEUCE
            )
        # Get json data for rally ending
        data = self.json_aggregate.all_ground_strokes_direction_values(court_side)

        # Yellow arrows direction
        directions = ["Line", "Middle", "Cross"]
        if (court_side == CourtSide.AD) ^ (return_direction == ReturnDirection.LINE):
            directions = ["Cross", "Middle", "Line"]

        if self.is_lefthanded():
            directions = directions[::-1]

        # Calculate total points
        total_points = 0
        for direction in directions:
            total_points += data[
                f"{return_direction.value}{shot_type.value}{direction}"
            ]

        for direction in directions:
            template = f"{return_direction.value}{shot_type.value}{direction}"
            points = data[template]
            points_percentage = (
                round(points / total_points * 100) if total_points else 0
            )
            win_percentage = (
                round(data[f"Won{template}"] / points * 100) if points else -1
            )

            cleaned_data["return_numbers"].append(points)
            cleaned_data["return_percentages"].append(points_percentage)
            cleaned_data["pies_percentages"].append(win_percentage)

        return cleaned_data

    def rally_ending_shot_new(
        self,
        player_no: int,
        shot_type: ShotType,
        movement_type: Optional[MovementType] = None,
    ):
        cleaned_data = {
            "pies_percentages": [],
            "shot_type": shot_type,
            "is_left_handed": self.is_lefthanded(),
            "surface": self.get_surface(),
        }

        if player_no == 2:
            cleaned_data["is_left_handed"] = (
                self.json_aggregate.get_report_inputs()["OpponentHandedness"] == 1
            )

        # Get json data for rally ending shot
        data = self.json_aggregate.rally_ending_shot_values(player_no)

        sides = ("Deuce", "Middle", "Ad")
        locations = ("BehindBaseline", "BackCourt", "ForeCourt", "Volley")
        for location in locations:
            for side in sides:
                percentages = {}
                side_data = data[side]
                for d in side_data:
                    if movement_type is None:
                        value = (
                            d[f"Stationary{shot_type.value}{location}"]
                            + d[f"Running{shot_type.value}{location}"]
                        )
                    else:
                        value = d[f"{movement_type.value}{shot_type.value}{location}"]

                    percentages[d["EndingStroke"]] = value

                cleaned_data["pies_percentages"].append(percentages)
        return cleaned_data

    def rally_ending_shot(
        self,
        player_no: int,
        shot_type: ShotType,
        movement_type: Optional[MovementType] = None,
    ):
        cleaned_data = {
            "pies_percentages": [],
            "shot_type": shot_type,
            "is_left_handed": self.is_lefthanded(),
            "surface": self.get_surface(),
        }

        if player_no == 2:
            cleaned_data["is_left_handed"] = (
                self.json_aggregate.get_report_inputs()["OpponentHandedness"] == 1
            )

        # Get json data for rally ending shot
        data = self.json_aggregate.rally_ending_shot_values(player_no)

        sides = ("Deuce", "Middle", "Ad")
        locations = ("BehindBaseline", "BackCourt", "ForeCourt", "Volley")
        for location in locations:
            for side in sides:
                percentages = []
                side_data = data[side]
                for d in side_data:
                    if movement_type is None:
                        value = (
                            d[f"Stationary{shot_type.value}{location}"]
                            + d[f"Running{shot_type.value}{location}"]
                        )
                    else:
                        value = d[f"{movement_type.value}{shot_type.value}{location}"]
                    percentages.append(value)
                cleaned_data["pies_percentages"].append(percentages)
        return cleaned_data

    def rally_length(
        self, serve_no: Optional[Serve] = None, player_no: Optional[int] = None
    ):
        cleaned_data = {
            "opponent_name": self.json_aggregate.player2_name,
            "serve_no": "",
            "labels": [],
            "points": [],
            "surface": self.get_surface(),
            "player_no": player_no,
        }

        shot_dict = {
            "2To4": "2-4 shots",
            "5To8": "5-8 shots",
            "9Plus": "9+ shots",
        }

        if serve_no is None:
            cleaned_data["serve_no"] = serve = "All"
        elif serve_no == Serve.FIRST:
            serve = serve_no.value + "Serve"
            cleaned_data["serve_no"] = "1st"
        else:
            serve = serve_no.value + "Serve"
            cleaned_data["serve_no"] = "2nd"

        # Get json data for rally length
        data = self.json_aggregate.rally_length_values()[serve]

        players = (
            ["Target", "Opponent"]
            if player_no is None
            else ["Target"] if player_no == 1 else ["Opponent"]
        )

        shots_no = ("2To4", "5To8", "9Plus")

        for player in players:
            for shot in shots_no:
                won = data[f"Won{player}Serving{shot}Shots"]
                loss = data[f"Loss{player}Serving{shot}Shots"]

                cleaned_data["points"].append((won, loss))
                cleaned_data["labels"].append(shot_dict[shot])

        return cleaned_data

    def rally_ending_table_page(self):
        from pdf_generator.pages.document import Document
        from pdf_generator.pages.rallyEndingTablePage import RallyEndingTable

        cleaned_data = {
            "pdf_buffer": None,
            "left": 42,
            "top": 245,
            "right": 1232,
            "bottom": 1415,
        }

        pdf = Document()
        RallyEndingTable(pdf, self, None).build_page_body()
        cleaned_data["pdf_buffer"] = pdf.output()

        return cleaned_data

    def get_target_player_details(self):
        return self.json_aggregate.get_target_player_details()

    def serve_bullets(
        self,
        stat_type: StatType,
        serve_stat: ServeStat,
        point_type: PointType,
        player_no: int,
        variance: Optional[bool] = False,
    ) -> List:
        serve_stats = self.json_aggregate.serve_stats_values(
            stat_type, serve_stat, point_type, player_no
        )
        rows = (
            (Serve.FIRST, CourtSide.DEUCE),
            (Serve.SECOND, CourtSide.DEUCE),
            (Serve.FIRST, CourtSide.AD),
            (Serve.SECOND, CourtSide.AD),
        )
        cols = (ServeDirection.WIDE, ServeDirection.BODY, ServeDirection.T)
        all_stats = []
        for row in rows:
            current_stats = []
            serve_no, court_side = row
            for serve_direction in cols:
                key = f"{serve_no.value}{court_side.value}{serve_direction.value}"
                if variance:
                    key += "Variance"
                current_stats.append(serve_stats[key])
            all_stats.append(current_stats)
        return all_stats

    def where_to_return_bullets(
        self,
        point_type: PointType,
        serve_no: Serve,
        court_side: CourtSide,
        serve_direction: ServeDirection,
        stat_type: Optional[StatType] = StatType.BASIC,
    ) -> None:
        return_stats = self.json_aggregate.stats_section(stat_type, point_type)
        columns = (
            ServeStat.WON_CROSS,
            ServeStat.TOTAL_CROSS,
            ServeStat.WON_MIDDLE,
            ServeStat.TOTAL_MIDDLE,
            ServeStat.WON_LINE,
            ServeStat.TOTAL_LINE,
        )
        all_stats = []
        for col in columns:
            all_stats.append(
                return_stats[f"{col.value}"][
                    f"{serve_no.value}{court_side.value}{serve_direction.value}"
                ]
            )
        return all_stats

    def where_to_serve_bullets(
        self,
        stat_type: StatType,
        point_type: PointType,
        player_no: int,
    ):
        return_stats = self.json_aggregate.stats_section_generic(
            stat_type, point_type, player_no
        )
        rows = (
            (Serve.FIRST, CourtSide.DEUCE),
            (Serve.SECOND, CourtSide.DEUCE),
            (Serve.FIRST, CourtSide.AD),
            (Serve.SECOND, CourtSide.AD),
        )
        columns = (
            ("WonReturn", ServeDirection.WIDE),
            ("ReturnsTotal", ServeDirection.WIDE),
            ("WonReturn", ServeDirection.BODY),
            ("ReturnsTotal", ServeDirection.BODY),
            ("WonReturn", ServeDirection.T),
            ("ReturnsTotal", ServeDirection.T),
        )
        all_stats = []
        for row in rows:
            current_stats = []
            serve_no, court_side = row
            for col in columns:
                stat_type, serve_direction = col
                current_stats.append(
                    return_stats[stat_type][
                        f"{serve_no.value}{court_side.value}{serve_direction.value}"
                    ]
                )
            all_stats.append(current_stats)
        return all_stats

    def return_direction_bullets(
        self,
        stat_type: StatType,
        point_type: PointType,
        player_no: int,
        return_direction_rows: Tuple,
    ):
        return_stats = self.json_aggregate.stats_section_generic(
            stat_type, point_type, player_no
        )
        columns = (
            "CrossReturnsTotal",
            "MiddleReturnsTotal",
            "LineReturnsTotal",
            "UnReturnsTotal",
            "ReturnsTotal",
        )
        all_stats = []
        for row in return_direction_rows:
            current_stats = []
            serve_no, court_side, serve_direction = row
            for col in columns:
                current_stats.append(
                    return_stats[col][
                        f"{serve_no.value}{court_side.value}{serve_direction.value}"
                    ]
                )
            all_stats.append(current_stats)
        return all_stats

    def shot_off_return_bullets(
        self,
        stat_type: StatType,
        point_type: PointType,
        player_no: int,
        return_direction_rows: Tuple,
    ) -> None:
        return_stats = self.json_aggregate.stats_section_generic(
            stat_type, point_type, player_no
        )
        columns = (
            ServeStat.WON_CROSS,
            ServeStat.TOTAL_CROSS,
            ServeStat.WON_MIDDLE,
            ServeStat.TOTAL_MIDDLE,
            ServeStat.WON_LINE,
            ServeStat.TOTAL_LINE,
        )
        all_stats = []
        for row in return_direction_rows:
            current_stats = []
            serve_no, court_side, serve_direction = row
            for col in columns:
                current_stats.append(
                    return_stats[f"{col.value}"][
                        f"{serve_no.value}{court_side.value}{serve_direction.value}"
                    ]
                )
            all_stats.append(current_stats)
        return all_stats

    def gs_pressure_bullets(self, non_pressure: bool):
        if non_pressure:
            target_data = self.json_aggregate.rally_ending_non_pressure_values(
                player_no=1
            )["All"]
            opponent_data = self.json_aggregate.rally_ending_non_pressure_values(
                player_no=2
            )["All"]
        else:
            target_data = self.json_aggregate.rally_ending_pressure_values(player_no=1)[
                "All"
            ]
            opponent_data = self.json_aggregate.rally_ending_pressure_values(
                player_no=2
            )["All"]

        all_stats = []
        # Insert aggregate rows (first 4 rows in excel)
        for row in ("StationaryFH", "RunningFH", "StationaryBH", "RunningBH"):
            current_stats = []
            total = 0
            for i in range(6):
                vals = target_data[i] if i < 3 else opponent_data[i % 3]
                val = sum(
                    (
                        vals[f"{row}BehindBaseline"],
                        vals[f"{row}BackCourt"],
                        vals[f"{row}ForeCourt"],
                    )
                )
                if "Stationary" in row:
                    hand = row[-2:]
                    val += sum(
                        (
                            vals[f"{hand}DropShot"],
                            vals[f"{hand}PassingNonLob"],
                            vals[f"{hand}SliceDeep"],
                        )
                    )
                current_stats.append(val)
                total += val if i < 3 else 0
            tally = current_stats[0] + current_stats[1] - current_stats[2]
            current_stats.append(total)
            current_stats.append(tally / total if total else 0)
            all_stats.append(current_stats)
        return all_stats

    def gs_basic_bullets(self):
        target_data = self.json_aggregate.rally_ending_shot_values(player_no=1)["All"]
        opponent_data = self.json_aggregate.rally_ending_shot_values(player_no=2)["All"]
        all_stats = []
        for key in list(target_data[0].keys())[2:28]:
            current_stats = []
            total = 0
            for i in range(3):
                value = target_data[i][key]
                current_stats.append(value)
                total += value
            for j in range(3):
                current_stats.append(opponent_data[j][key])
            current_stats.append(current_stats[0] + current_stats[1] - current_stats[2])
            current_stats.append(current_stats[3] + current_stats[4] - current_stats[5])
            current_stats.append(total)
            current_stats.append(current_stats[6] / total if total else 0)
            all_stats.append(current_stats)
        return all_stats

    def gs_last_shots_bullets(self, court_side: CourtSide, player_no: int):
        gs_stats = self.json_aggregate.last_ground_strokes_shot_values(
            court_side, player_no
        )
        all_stats = []
        for row in ("", "Lost"):
            current_stats = []
            for hand in (ShotType.FH, ShotType.BH):
                for direction in (
                    ReturnDirection.LINE,
                    ReturnDirection.MIDDLE,
                    ReturnDirection.CROSS,
                ):
                    current_stats.append(
                        gs_stats[f"{row}{hand.value}{direction.value}"]
                    )
            all_stats.append(current_stats)
        return all_stats

    def gs_movement_shots_bullets(
        self,
        movement_type: MovementType,
        court_side: CourtSide,
        player_no: int,
    ):
        gs_stats = self.json_aggregate.last_ground_strokes_movement_values(
            movement_type, court_side, player_no
        )
        all_stats = []
        for direction in (
            ReturnDirection.LINE,
            ReturnDirection.MIDDLE,
            ReturnDirection.CROSS,
        ):
            current_stats = []
            for hand in (ShotType.FH, ShotType.BH):
                current_stats.append(gs_stats[f"{hand.value}{direction.value}"])
            all_stats.append(current_stats)
        return all_stats

    def gs_intermediate_bullets(self):
        target_data = self.json_aggregate.rally_ending_shot_values(player_no=1)["All"]

        all_stats = []
        # Insert aggregate rows (first 4 rows in excel)
        for row in ("StationaryFH", "RunningFH", "StationaryBH", "RunningBH"):
            current_stats = []
            total = 0
            for i in range(3):
                vals = target_data[i]
                val = sum(
                    (
                        vals[f"{row}BehindBaseline"],
                        vals[f"{row}BackCourt"],
                        vals[f"{row}ForeCourt"],
                    )
                )
                if "Stationary" in row:
                    hand = row[-2:]
                    val += sum(
                        (
                            vals[f"{hand}DropShot"],
                            vals[f"{hand}PassingNonLob"],
                            vals[f"{hand}SliceDeep"],
                        )
                    )
                current_stats.append(val)
                total += val if i < 3 else 0
            tally = current_stats[0] + current_stats[1] - current_stats[2]
            current_stats.append(total)
            current_stats.append(tally / total if total else 0)
            all_stats.append(current_stats)
        return all_stats

    def gs_cross_bullets(self, court_side: CourtSide, player_no: int):
        gs_stats = self.json_aggregate.rally_ending_direction_values(
            court_side, player_no
        )
        all_stats = []
        for row in ("Line", "Middle", "Cross"):
            current_stats = []
            for shot in ("FH", "BH"):
                for return_direction in ("Line", "Middle", "Cross"):
                    current_stats.append(gs_stats[f"{row}{shot}{return_direction}"])
            all_stats.append(current_stats)
        return all_stats

    def is_matchup_report(self):
        return self.json_aggregate.is_matchup

    def get_matches_details(self):
        matches = self.json_aggregate.get_match_list()
        parsed_matches = []
        for match in matches:
            players, tournament, year = match["File Name"].split("--")[:3]
            player1_name, player2_name = players.split("-")

            parsed_matches.append(
                {
                    "p1": player1_name.split("_")[0],
                    "p2": player2_name.split("_")[0],
                    "tournament": tournament,
                    "year": year,
                }
            )
        return parsed_matches
