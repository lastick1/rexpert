"""Форматы MCU в исходниках миссий"""


decorations_format = """Decoration
{{
  Name = {0};
  Desc = {1};
  XPos = {2};
  YPos = {3};
  ZPos = {4};
  OY = {5};
  Length = {6:.0f};
  Width = {7:.0f};{8}
  Dogfight = {9};
  Transport = {10};
  Train = {11};
  Tank = {12};
  Artillery = {13};
  AAAPosition = {14};
  Ship = {15};
  Balloon = {16};
  Windsock = {17};
  CityFire = {18};
  Spotter = {19};
  Bridge = {20};
  AtArtPosition = {21};
  FiringPoint = {22};
  Siren = {23};
  Parking = {24};
}}"""

ground_objective_format = """GroundObjective
{{
  Name = {0};
  Desc = {1};
  XPos = {2};
  YPos = {3};
  ZPos = {4};
  OY = {5};
  Length = {6};
  Width = {7};{8}
  Transport = {9};
  Armoured = {10};
  Tank = {11};
  AAAPosition = {12};
  Artillery = {13};
  Building = {14};
  Ship = {15};
  Train = {16};
  RailwayStation = {17};
  SupplyDump = {18};
  Factory = {19};
  Airfield = {20};
  Port = {21};
  ReconArea = {22};
}}"""
airfields_format = """Airfield
{{
  Name = "Airfield";
  Desc = "";
  XPos = {0:.3f};
  YPos = {1:.3f};
  ZPos = {2:.3f};
  OY = 0.000;
  Length = 10;
  Width = 10;{3}
  GrassField = 0;
  WaterField = 0;
}}"""
air_objectives_format = """AirObjective
{{
  Name = "AirObjective";
  Desc = "";
  XPos = {0:.3f};
  YPos = 75.515;
  ZPos = {1:.3f};
  OY = 0.000;
  Length = 1000;
  Width = 1000;
  Country = {2};
  ReconFlight = 0;
  BomberFlight = 0;
  FighterPatrolFlight = 0;
  Dogfight = 0;
  DuelOpponent = 0;
  Balloon = 1;
}}"""

division_format = """AirObjective
{{
  Name = "AirObjective";
  Desc = "";
  XPos = {0:.3f};
  YPos = 75.515;
  ZPos = {1:.3f};
  OY = {2:.3f};
  Length = {3:.3f};
  Width = {4:.3f};
  ReconFlight = 0;
  BomberFlight = 0;
  FighterPatrolFlight = 0;
  Dogfight = 0;
  DuelOpponent = 1;
  Balloon = 0;
}}"""

influence_text = """MCU_TR_InfluenceArea
{{
  Index = {};
  Name = "Translator Influence Area";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = {:.3f};
  YPos = 17.795;
  ZPos = {:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Enabled = 1;
  Country = {};
  Boundary
  {{
{}  }}
}}

"""  # не двигать кавычки!

icon_text = """MCU_Icon
{{
  Index = {0};
  Targets = [{1}];
  Objects = [];
  XPos = {2:.3f};
  YPos = 200.000;
  ZPos = {3:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Enabled = 1;
  LCName = {4};
  LCDesc = {5};
  IconId = 0;
  RColor = 255;
  GColor = 255;
  BColor = 255;
  LineType = 13;
  Coalitions = [1, 2, 0];
}}

"""  # не двигать кавычки!

ref_point_helper_format = """MCU_H_ReferencePoint
{{
  Index = {0};
  Name = "";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = {1:.3f};
  YPos = 0.000;
  ZPos = {2:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Forward = 1;
  Backward = 1;
  Left = 1;
  Right = 1;
}}

"""  # не двигать кавычки!
