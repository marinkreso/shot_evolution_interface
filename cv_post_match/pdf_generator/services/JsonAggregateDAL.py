import os
import json
from typing import Dict, Optional

from pdf_generator.models.enums import (
    CourtSide,
    MovementType,
    PointType,
    ServeStat,
    StatType,
    Distribution,
)


class JsonAggregateDAL:
    def __init__(self, report_path):
        f = open(report_path)
        self.data = json.load(f)
        f.close()
        self.player1_name = ""
        self.player2_name = ""

        try:
            self.game_selection = self.data["Report"]["ReportInputs"]["GamesFilter"][
                "ResultSelection"
            ]
            self.serve_selection = self.data["Report"]["ReportInputs"]["GamesFilter"][
                "ServeSelection"
            ]
            self.set_selection = self.data["Report"]["ReportInputs"]["GamesFilter"][
                "SetsResultSelection"
            ]
        except KeyError:
            self.game_selection = 2
            self.result_selection = 2
            self.set_selection = 2

        self.is_left_handed = (
            self.data["Report"]["ReportInputs"]["TargetHandedness"] == 1
        )
        self.is_matchup = (
            not self.data["Report"]["ReportInputs"]["Opponent"].split()[0].isnumeric()
        )
        self.players_name()

    @property
    def target_hand(self) -> int:
        return self.data["Report"]["ReportInputs"]["TargetHandedness"]

    @property
    def opponent_hand(self) -> int:
        return self.data["Report"]["ReportInputs"]["OpponentHandedness"]

    @property
    def category(self) -> int:
        return self.data["Report"]["ReportInputs"]["Category"]

    @property
    def gs_matches_count(self) -> int:
        return self.data["Report"]["NumberOfFilesGS"]

    def is_lefthanded(self):
        return self.is_left_handed

    def get_player_id(self, key: str) -> int:
        """
        Gets the LocalPlayerId based on the key

        :param key: can be either Target or Opponent
        :returns: the id of the player as an integer
        """
        if key != "Opponent":
            return self.data["Target"]["LocalFilePlayerId"]
        if key == "Opponent" and self.data["Report"]["ReportInputs"]["ReportType"] in (
            0,
            2,
        ):
            return self.data["Opponent"]["LocalFilePlayerId"]
        return None

    def get_surface_id(self) -> int:
        return self.data["Report"]["ReportInputs"]["Surface"]

    def players_name(self):
        parsed_names = []
        for player in ("PlayerName1", "PlayerName2"):
            if "Multiple" in self.data[player]:
                name = self.data[player].split("(")[1][:-1]
                name = name if name[0].isdigit() else f"{len(name)} Players"

            else:
                name = self.data[player]
            parsed_names.append(name)
        self.player1_name, self.player2_name = parsed_names
        return self.player1_name, self.player2_name

    def get_player_handedness(self, key) -> str:
        if key not in ("Target", "Opponent"):
            key = "Target"
        handedness = self.data["Report"]["ReportInputs"][f"{key}Handedness"]
        if handedness == 1:
            return "left"
        return "right"

    def divide(self, n1, n2):
        try:
            return n1 / n2
        except:
            return 0

    def nan_to_zero(self, value):
        if type(value) != int and type(value) != float:
            return 0
        return value

    def cover_page_sub_titles(self):
        subTitlesDic = {
            "years": self.data["Report"]["ReportInputs"]["AggregateSubTitle"],
            "noOfMatches": self.data["Report"]["NumberOfFilesBasic"],
            "OpponentHandedness": self.data["Report"]["ReportInputs"][
                "OpponentHandedness"
            ]
            if not self.is_matchup
            else 2,
            "TargetHandedness": self.data["Report"]["ReportInputs"]["TargetHandedness"],
            "subTitle": self.data["Report"]["ReportInputs"]["SubTitle"],
        }

        return subTitlesDic

    def get_report_inputs(self):
        target = self.data["Report"]["ReportInputs"]["Target"]
        targetHandedness = self.data["Report"]["ReportInputs"]["TargetHandedness"]
        OpponentHandedness = self.data["Report"]["ReportInputs"]["OpponentHandedness"]
        subtitle = self.data["Report"]["ReportInputs"]["AggregateSubTitle"]

        reportInputs = {
            "target": target,
            "targetHandedness": targetHandedness,
            "subtitle": subtitle,
            "OpponentHandedness": OpponentHandedness,
        }

        return reportInputs

    def core_stats_table_data(self):
        coreStatsDic = {
            "Player1": {"Name": self.player1_name, "Value": {}},
            "Player2": {"Name": self.player2_name, "Value": {}},
        }

        for i in range(1, 3):
            core = self.data[f"PlayerStats{i}"]["StatsSections"]["Basic"]["CoreStats"][
                "CoreStatsValues"
            ]["Default"]
            games_core = self.data[f"PlayerStats{i}"]["StatsSections"]["Basic"][
                "BasicGameStats"
            ]

            coreStatsDic[f"Player{i}"]["Value"]["1st serve in %"] = self.divide(
                core["FirstServeIn"], core["ServesTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["2nd serve in %"] = self.divide(
                core["SecondServeIn"], core["SecondServesTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["1st serve win %"] = self.divide(
                core["FirstServeWinner"], core["FirstServeIn"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["2nd serve win %"] = self.divide(
                core["SecondServeWinner"], core["SecondServesTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["1st return win %"] = self.divide(
                core["Return1StServeWinner"], core["Return1StServeTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["2nd return win %"] = self.divide(
                core["Return2NdServeWinner"], core["Return2NdServeTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["Serve Win %"] = self.divide(
                core["ServeWinner"], core["ServesTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["Return Win %"] = self.divide(
                core["ReturnWinner"], core["ReturnTotal"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["Break pt faced win %"] = self.divide(
                core["BreakPointFacedWin"], core["BreakPointFaced"]
            )
            coreStatsDic[f"Player{i}"]["Value"][
                "Break pt opportunity win %"
            ] = self.divide(
                core["BreakPointOpportunityWin"], core["BreakPointOpportunity"]
            )
            coreStatsDic[f"Player{i}"]["Value"][
                "Pressure Pt faced win %"
            ] = self.divide(core["PressurePointFacedWin"], core["PressurePointFaced"])
            coreStatsDic[f"Player{i}"]["Value"][
                "Pressure pt opportunity win %"
            ] = self.divide(
                core["PressurePointOpportunityWin"], core["PressurePointOpportunity"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["Total serve Games"] = self.nan_to_zero(
                games_core["GameServer"]
            )
            coreStatsDic[f"Player{i}"]["Value"][
                "Total serve Games Won"
            ] = self.nan_to_zero(games_core["WonGameServer"])
            coreStatsDic[f"Player{i}"]["Value"]["Serve Game Win %"] = self.nan_to_zero(
                games_core["ServiceGameWinPercentage"]
            )
            coreStatsDic[f"Player{i}"]["Value"]["Total Tiebreakers"] = self.nan_to_zero(
                games_core["TieBreakGame"]
            )
            coreStatsDic[f"Player{i}"]["Value"][
                "Total Tiebreakers Won"
            ] = self.nan_to_zero(games_core["WonTieBreakGame"])
            coreStatsDic[f"Player{i}"]["Value"][
                "Total Tiebreakers Win %"
            ] = self.nan_to_zero(games_core["TieGameWinPercentage"])

        return coreStatsDic

    def serve_stats_table_data(self):
        serveStatsDic = {
            "Player1": {"Name": self.player1_name, "Value": {}},
            "Player2": {"Name": self.player2_name, "Value": {}},
        }

        for i in range(1, 3):
            serve = self.data[f"PlayerStats{i}"]["StatsSections"]["Basic"][
                "ServeBasicStats"
            ]

            serveStatsDic[f"Player{i}"]["Value"]["Aces"] = self.nan_to_zero(
                serve["Aces"]
            )
            serveStatsDic[f"Player{i}"]["Value"]["Aces/game"] = self.nan_to_zero(
                serve["AcesPerGames"]
            )
            serveStatsDic[f"Player{i}"]["Value"][
                "Unreturned serves (incl. aces)"
            ] = self.nan_to_zero(serve["UnReturnedServes"])
            serveStatsDic[f"Player{i}"]["Value"][
                "Unreturned serves/game"
            ] = self.nan_to_zero(serve["UnReturnedServesPerGames"])
            serveStatsDic[f"Player{i}"]["Value"][
                "Serves with poor returns/game"
            ] = self.nan_to_zero(serve["ServesWithPoorReturns"])
            serveStatsDic[f"Player{i}"]["Value"][
                "Serves with aggressive return/game"
            ] = self.nan_to_zero(serve["ServesWithAggressiveReturns"])
            serveStatsDic[f"Player{i}"]["Value"][
                "Serves with killer returns/game"
            ] = self.nan_to_zero(serve["ServesWithKillerReturns"])
            serveStatsDic[f"Player{i}"]["Value"]["Double Faults"] = self.nan_to_zero(
                serve["DoubleFaults"]
            )
            serveStatsDic[f"Player{i}"]["Value"][
                "Double Faults/game"
            ] = self.nan_to_zero(serve["DoubleFaultsPerGames"])

        return serveStatsDic

    def read_serve_table(self, table_dict, total_key="All"):
        playerServeStatsDic = {"Wide": {}, "Body": {}, "T": {}, "Total": {}}

        for key in playerServeStatsDic.keys():
            if "Total" in key:
                jsonkey = total_key
            else:
                jsonkey = key
            playerServeStatsDic[key]["1st - Deuce"] = table_dict[f"FirstDeuce{jsonkey}"]
            playerServeStatsDic[key]["2nd - Deuce"] = table_dict[
                f"SecondDeuce{jsonkey}"
            ]
            playerServeStatsDic[key]["1st - Ad"] = table_dict[f"FirstAd{jsonkey}"]
            playerServeStatsDic[key]["2nd - Ad"] = table_dict[f"SecondAd{jsonkey}"]

        return playerServeStatsDic

    def rally_ending_table_data(self):
        rallyEndingDic = {
            "Player1": {
                "Name": self.player1_name,
                "Winner": {"Value": {}},
                "Forcing": {"Value": {}},
                "Unforced": {"Value": {}},
            },
            "Player2": {
                "Name": self.player2_name,
                "Winner": {"Value": {}},
                "Forcing": {"Value": {}},
                "Unforced": {"Value": {}},
            },
        }

        target1_table = self.data[f"PlayerStats1"]["StatsSections"]["GS"][
            "RallyEndingStats"
        ]["RallyEndingStatsValues"]["All"]
        target2_table = self.data[f"PlayerStats2"]["StatsSections"]["GS"][
            "RallyEndingStats"
        ]["RallyEndingStatsValues"]["All"]
        for i in target1_table[0]:
            if i == "CourtPositionHorizontal" or i == "EndingStroke":
                continue
            if i == "Length3ShotsOrLess":
                break
            rallyEndingDic["Player1"]["Winner"]["Value"][i] = target1_table[0][i]
            rallyEndingDic["Player1"]["Forcing"]["Value"][i] = target1_table[1][i]
            rallyEndingDic["Player1"]["Unforced"]["Value"][i] = target1_table[2][i]

            rallyEndingDic["Player2"]["Winner"]["Value"][i] = target2_table[0][i]
            rallyEndingDic["Player2"]["Forcing"]["Value"][i] = target2_table[1][i]
            rallyEndingDic["Player2"]["Unforced"]["Value"][i] = target2_table[2][i]

        return rallyEndingDic

    def match_list_table(self):
        matches = self.data["MatchesTable"]
        gs = {"Match": [], "Winner": [], "Score": []}
        non_gs = {"Match": [], "Winner": [], "Score": []}

        for match in matches:
            file_name = match["File Name"]
            match_name = os.path.splitext(file_name)[0]
            if "--GS" in match["File Name"]:
                gs["Match"].append("* " + match_name)
                gs["Winner"].append(match["Winner"])
                gs["Score"].append(match["Result"])
            else:
                non_gs["Match"].append(match_name)
                non_gs["Winner"].append(match["Winner"])
                non_gs["Score"].append(match["Result"])

        return {
            "Match": gs["Match"] + non_gs["Match"],
            "Winner": gs["Winner"] + non_gs["Winner"],
            "Score": gs["Score"] + non_gs["Score"],
        }

    def get_match_list(self):
        return self.data["MatchesTable"]

    def avg_return_speed(self, player_no):
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["Speed"][
            "AllReturnSpeedStats"
        ]["Values"]["Average"]
        cleaned_data = {
            "1st - Deuce-- Wide": [data["FirstDeuceWide"]],
            "1st - Deuce -- Body": [data["FirstDeuceBody"]],
            "1st - Deuce -- T": [data["FirstDeuceT"]],
            "2nd - Deuce-- Wide": [data["SecondDeuceWide"]],
            "2nd - Deuce -- Body": [data["SecondDeuceBody"]],
            "2nd - Deuce -- T": [data["SecondDeuceT"]],
            "1st -- Ad -- Wide": [data["FirstAdWide"]],
            "1st -- Ad -- Body": [data["FirstAdBody"]],
            "1st -- Ad -- T": [data["FirstAdT"]],
            "2nd -- Ad -- Wide": [data["SecondAdWide"]],
            "2nd -- Ad -- Body": [data["SecondAdBody"]],
            "2nd -- Ad -- T": [data["SecondAdT"]],
        }
        for key in cleaned_data:
            cleaned_data[key] = [round(datum) for datum in cleaned_data[key]]

        return cleaned_data

    def return_v_serve_speed(self, position, player_no):
        # position is one of (Deuce, Ad)
        keys = (
            "<90 mph",
            "90-99 mph",
            "100-109 mph",
            "110-119 mph",
            "120-129 mph",
            "130+ mph",
        )

        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["Speed"][
            "ReturnStats"
        ]["Values"][position]["ServeLocationValues"]
        cleaned_data = {"Wide": {}, "Body": {}, "T": {}}
        for type in cleaned_data:
            for i, speed in enumerate(
                (
                    "LessThan90",
                    "MoreThan89AndLessThan100",
                    "MoreThan99AndLessThan110",
                    "MoreThan109AndLessThan120",
                    "MoreThan119AndLessThan130",
                )
            ):
                row = []
                for stat in ("In", "Good", "Win", "Total"):
                    row.append(data[type][stat + speed])
                for stat in ("In", "Good", "Win"):
                    total = data[type]["Total" + speed]
                    precentage = data[type][stat + speed] / total * 100 if total else 0
                    row.append(f"{round(precentage)}%" if precentage else "")
                cleaned_data[type][keys[i]] = row

        return cleaned_data

    def GS_stats(self, mode, player_no):
        # Mode is one of : (Stationary, Running)
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "LastGroundStrokeShotStats"
        ]["Values"]
        cleaned_data = {"C": {}, "P": {}}

        # Fetch each row
        for dir in ("Line", "Middle", "Cross"):
            row = []
            for pos in ("Deuce", "Middle", "Ad"):
                for type in ("FH", "BH"):
                    row.append(data[mode + pos][type + dir])

            cleaned_data["C"][dir] = row

        # Calculate total row
        total_row = []
        total_precent_row = []
        for i in range(6):
            total = 0
            for dir in ("Line", "Middle", "Cross"):
                total += cleaned_data["C"][dir][i]
            total_row.append(total)
            total_precent_row.append(100 if total else "")

        cleaned_data["C"]["Total"] = total_row

        # Calculate the precentage data
        for dir in ("Line", "Middle", "Cross"):
            row = []
            for i, value in enumerate(cleaned_data["C"][dir]):
                current_total = cleaned_data["C"]["Total"][i]
                datum = round(value / current_total * 100) if current_total else ""
                row.append(datum)
            cleaned_data["P"][dir] = row
        cleaned_data["P"]["Total"] = total_precent_row

        return cleaned_data

    def GS_pair(self, pos, player_no):
        # pos is one of: Deuce, Ad
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "GSRallyPairsStats"
        ]["LastRallyPairStatsValues"][pos]
        cleaned_data = {"C": {}, "P": {}}

        # Fetch each row
        for dir in ("Line", "Middle", "Cross"):
            row = []
            for type in ("FH", "BH"):
                for sub_dir in ("Line", "Middle", "Cross"):
                    row.append(data[dir + type + sub_dir])

            cleaned_data["C"][dir] = row

        # Calculate the precentage
        for dir in ("Line", "Middle", "Cross"):
            FH_values = cleaned_data["C"][dir][:3]
            BH_values = cleaned_data["C"][dir][3:]
            FH_sum = sum(FH_values)
            BH_sum = sum(BH_values)

            row = []
            for values, total in ((FH_values, FH_sum), (BH_values, BH_sum)):
                for value in values:
                    row.append(round(value / total * 100) if total else "")
            cleaned_data["P"][dir] = row

        return cleaned_data

    def GS_all_shots(self, pos, player_no):
        # pos is one of: Deuce, Ad
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "LastGroundStrokeShotStats"
        ]["AllShotsValues"][pos]
        cleaned_data = {}
        for category in ("Won", "Total Pts Lost"):
            row = []
            for type in ("FH", "BH"):
                for dir in ("Line", "Middle", "Cross"):
                    if category == "Won":
                        datum = data[type + dir]
                    else:
                        datum = data["Lost" + type + dir]

                    row.append(datum)
            cleaned_data[category] = row

        row = []
        for i in range(6):
            won = cleaned_data["Won"][i]
            lost = cleaned_data["Total Pts Lost"][i]
            total = won + lost
            row.append(round(won / total * 100) if total else "")

        cleaned_data["Pts Won %"] = row

        return cleaned_data

    def report_metadata(self):
        data = self.data["Report"]
        return {
            "Basic": data["NumberOfFilesBasic"],
            "GS": data["NumberOfFilesGS"],
            "MT": data["NumberOfFilesMT"],
            "SM": data["NumberOfFilesSM"],
            "GD": data["NumberOfFilesGD"],
        }

    def serve_rally_points(self, serve_no, is_pressure):
        """
        serve_no is one of (1st, 2nd)
        is_pressure is a boolean (True | False)
        """
        point_type = (
            "PressureRallyLengthStats" if is_pressure else "NonPressureRallyLengthStats"
        )
        serve = "FirstServe" if serve_no == "1st" else "SecondServe"
        opponent_name = (
            f"{self.player2_name.split()[0]} OPP"
            if self.player2_name.split()[0].isnumeric()
            else self.player2_name
        )

        keys = (
            f"{self.player1_name} serving (2-4 shots)",
            f"{self.player1_name} serving (5-8 shots)",
            f"{self.player1_name} serving (9+ shots)",
            f"{opponent_name} serving (2-4 shots)",
            f"{opponent_name} serving (5-8 shots)",
            f"{opponent_name} serving (9+ shots)",
            "2-4 shots",
            "4-8 shots",
            "5-8 shots",
            "5-10 shots",
            "2+ shots",
            "4+ shots",
            "6+ shots",
            "9+ shots",
            "11+ shots",
            "13+ shots",
        )

        data = self.data["PlayerStats1"]["StatsSections"]["Basic"][point_type][
            "Values"
        ][serve]
        cleaned_data = {}

        for key, type in zip(
            keys,
            (
                "TargetServing2To4Shots",
                "TargetServing5To8Shots",
                "TargetServing9PlusShots",
                "OpponentServing2To4Shots",
                "OpponentServing5To8Shots",
                "OpponentServing9PlusShots",
                "Len2To4Shots",
                "Len4To8Shots",
                "Len5To8Shots",
                "Len5To10Shots",
                "Len2PlusShots",
                "Len4PlusShots",
                "Len6PlusShots",
                "Len9PlusShots",
                "Len11PlusShots",
                "Len13PlusShots",
            ),
        ):
            row = []

            for stat in ("Won", "Loss", "Total"):
                row.append(data[stat + type])

            for stat in ("Won", "Loss"):
                total = data["Total" + type]
                precentage = data[stat + type] / total * 100 if total else None
                row.append(f"{round(precentage)}%" if precentage else "")

            cleaned_data[key] = row

        return cleaned_data

    def MT_tables(self):
        return self.data["MTDetailedTable"]

    def stats_section(
        self, stat_type: StatType, point_type: Optional[PointType] = PointType.NORMAL
    ) -> Dict:
        return self.data["PlayerStats1"]["StatsSections"][stat_type.value][
            point_type.value
        ]["ServeStatsValues"]

    def stats_section_2(
        self, stat_type: StatType, point_type: Optional[PointType] = PointType.NORMAL
    ) -> Dict:
        return self.data["PlayerStats2"]["StatsSections"][stat_type.value][
            point_type.value
        ]["ServeStatsValues"]

    def stats_section_generic(
        self,
        stat_type: StatType,
        point_type: Optional[PointType] = PointType.NORMAL,
        player_no: Optional[int] = 1,
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"][stat_type.value][
            point_type.value
        ]["ServeStatsValues"]
        return data

    def serve_stats_values(
        self,
        stat_type: StatType,
        serve_stat: ServeStat,
        point_type: Optional[PointType] = PointType.NORMAL,
        player_no: Optional[int] = 1,
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"][stat_type.value][
            point_type.value
        ]["ServeStatsValues"][serve_stat.value]
        return data

    def shot_after_return_values(self, player_no: Optional[int] = 1) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "ShotAfterReturnStats"
        ]["Values"]
        return data

    def rally_ending_direction_values(
        self, court_side: CourtSide, player_no: Optional[int] = 1
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "GSRallyPairsStats"
        ]["LastRallyPairStatsValues"][court_side.value]
        return data

    def all_ground_strokes_direction_values(
        self, court_side: CourtSide, player_no: Optional[int] = 1
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GD"][
            "GDPairsStats"
        ]["AllRallyPairsValues"][court_side.value]
        return data

    def rally_ending_shot_values(self, player_no: int) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "RallyEndingStats"
        ]["RallyEndingStatsValues"]
        return data

    def rally_ending_non_pressure_values(self, player_no: int) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "NonPressureRallyEndingStats"
        ]["RallyEndingStatsValues"]
        return data

    def rally_ending_pressure_values(self, player_no: int) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "PressureRallyEndingStats"
        ]["RallyEndingStatsValues"]
        return data

    def last_ground_strokes_shot_values(
        self, court_side: CourtSide, player_no: int
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "LastGroundStrokeShotStats"
        ]["AllShotsValues"][court_side.value]
        return data

    def last_ground_strokes_movement_values(
        self, movement_type: MovementType, court_side: CourtSide, player_no: int
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["GS"][
            "LastGroundStrokeShotStats"
        ]["Values"][f"{movement_type.value}{court_side.value}"]
        return data

    def rally_length_values(self, player_no: Optional[int] = 1):
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["Basic"][
            "RallyLengthStats"
        ]["Values"]
        return data

    def serve_speed_values(
        self,
        distribution: Distribution,
        point_type: Optional[PointType] = PointType.SPEED_ALL,
        player_no: Optional[int] = 1,
    ) -> Dict:
        data = self.data[f"PlayerStats{player_no}"]["StatsSections"]["Speed"][
            point_type.value
        ]["Values"][distribution.value]
        return data

    def get_target_player_details(self):
        return self.data["Target"]["LocalFilePlayer"]

    def get_return_speed(self, player_no: int):
        return self.data[f"PlayerStats{player_no}"]["StatsSections"]["Speed"][
            "AllReturnSpeedStats"
        ]["Values"]["Average"]
