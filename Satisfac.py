import numpy as np
import pygame
import re

"""
Okay so. The idea is:
- Global maximum conveyor/miner tier set at top
    - Used to inform several things
        - Miner outputs and caps to these by conveyor speeds
        - Whether number of buildings for a recipe must be increased due to input/output limit by conveyor speeds
        - Number of conveyor lines that will be needed on inputs to recipes
        - Whether to suggest a sub-maximum miner tier for some input nodes
- Sources as boxes with outputs (right)
    - Can be configured with number of source nodes, of what kind (gives limits for construction)
        - When calculations resolved, can show how many nodes need be used at what tier miner (prioritise use of purer)
    - Maybe can also be configured with whether to allow overclocking or not
    - Separate type for water extractor sources
        - Default set to limitless
        - Calculates number of extractors needed
    - Separate type for pressurised wells (work out details on these later)
- Products box on right with inputs (left)
    - Can set intended proportions that should be produced
        - Defaults to equality
    - Maybe can fix output rates if wanted
- Recipes added as boxes with inputs (left) and outputs (right)
    - Unfulfilled inputs/outputs highlighted
        - Inputs must be connected to something
        - Outputs must be connected to something or manually set to "ignore" (i.e. AWESOME sunk)
            - Liquid outputs cannot be ignored (TODO: Can they?)
    - BIG ONE: How many buildings of each recipe to be calculated automatically and displayed
        - Balances usage of each recipe to maximise output rate within limits set by input rates
        - Seems like this will be simple where all inputs/outputs are one-to-one mappings
            - Complicated by having multiple final products
            - Complicated by having multiple recipe outputs combined into same input (competing alternate recipes)
                - May require Combiner nodes so as not to have a cats cradle issue with many-to-many mappings
            - Complicated by multi-output recipes (e.g. packagers, refineries, blenders)
            - Complicated by loopbacks (e.g. aluminium production water)
- Inputs and outputs of source nodes, recipes, outputs linked manually
    - Multiple inputs can be sourced from one output and vice versa
    - Would be nice if everything laid itself out neatly (or could be moved around to do so by hand)
- Displays some handy info
"""


class BadRecipeException(Exception):
    pass


# Recipes found downwards from Supercomputer, working through all recipes producing first part input to last recipe of
# previous part, working upwards through recipe list to find new parts for which recipes not listed
recipeSheet = """
Supercomputer: 2 computer, 2 ai limiter, 3 high-speed connector, 28 plastic: 1 supercomputer: 1.875: manufacturer
Computer: 10 circuit board, 9 cable, 18 plastic, 52 screw: 1 computer: 2.5: manufacturer
Computer (Crystal Computer): 8 circuit board, 3 crystal oscillator: 3 computer: 2.8125: assembler
Computer (Caterium Computer): 7 circuit board, 28 quickwire, 12 rubber: 1 computer: 3.75: manufacturer
Circuit Board: 2 copper sheet, 4 plastic: 1 circuit board: 7.5: assembler
Circuit Board (Electrode Circuit Board): 6 rubber, 9 petroleum coke: 1 circuit board: 5: assembler
Circuit Board (Silicon Circuit Board): 11 copper sheet, 11 silica: 5 circuit board: 12.5: assembler
Circuit Board (Caterium Circuit Board): 10 plastic, 30 quickwire: 7 circuit board: 8.75: assembler
Plastic: 3 crude oil: 2 plastic, 1 heavy oil residue: 20: refinery
Plastic (Residual Plastic): 6 polymer resin, 2 water: 2 plastic: 20: refinery
Plastic (Recycled Plastic): 6 rubber, 6 fuel: 12 plastic: 60: refinery
Rubber: 3 crude oil: 2 rubber, 2 heavy oil residue: 20: refinery
Rubber (Residual Rubber): 4 polymer resin, 4 water: 2 rubber: 20: refinery
Rubber (Recycled Rubber): 6 plastic, 6 fuel: 12 rubber: 60: refinery
Fuel: 6 crude oil: 4 fuel, 3 polymer resin: 40: refinery
Fuel (Residual Fuel): 6 heavy oil residue: 4 fuel: 40: refinery
Unpackage Fuel: 2 packaged fuel: 2 fuel, 2 empty canister: 60: packager
Fuel (Diluted Fuel): 5 heavy oil residue, 10 water: 10 fuel: 100: blender
Heavy Oil Residue: 3 crude oil: 4 heavy oil residue, 2 polymer resin: 40: refinery
Polymer Resin: 6 crude oil: 13 polymer resin, 2 heavy oil residue: 130: refinery
Empty Canister: 2 plastic: 4 empty canister: 60: constructor
Empty Canister (Steel Canister): 3 steel ingot: 2 empty canister: 40: constructor
Empty Canister (Coated Iron Canister): 2 iron plate, 1 copper sheet: 4 empty canister: 60: assembler
Unpackage Turbofuel: 2 packaged turbofuel: 2 turbofuel, 2 empty canister: 20: packager
Packaged Water: 2 water, 2 empty canister: 2 packaged water: 120: packager
Aluminium Scrap: 4 alumina solution, 2 coal: 6 aluminium scrap, 2 water: 360: refinery
Aluminium Scrap (Electrode Aluminium Scrap): 12 alumina solution, 4 petroleum coke: 20 aluminium scrap, 7 water: 300: refinery
Aluminium Scrap (Instant Scrap): 15 bauxite, 10 coal, 5 sulphuric acid, 6 water: 30 aluminium scrap, 5 water: 300: blender
Battery: 2.5 sulphuric acid, 2 alumina solution, 1 aluminium casing: 1 battery, 1.5 water: 20: blender
Non-fissile Uranium: 15 uranium waste, 10 silica, 6 nitric acid, 6 sulphuric acid: 20 non-fissile uranium, 6 water: 50: blender
Non-fissile Uranium (Fertile Uranium): 5 uranium, 5 uranium waste, 3 nitric acid, 5 sulphuric acid: 20 non-fissile uranium, 8 water: 100: blender
Uranium Waste: 1 uranium fuel rod, 1500 water: 50 uranium waste: 10: nuclear power plant
Uranium Fuel Rod: 50 encased uranium cell, 3 encased industrial beam, 5 electromagnetic control rod: 1 uranium fuel rod: 0.4: manufacturer
Uranium Fuel Rod (Uranium Fuel Unit): 100 encased uranium cell, 10 electromagnetic control rod, 3 crystal oscillator, 6 beacon: 3 uranium fuel rod: 0.6: manufacturer
Encased Uranium Cell: 10 uranium, 3 concrete, 8 sulphuric acid: 5 encased uranium cell, 2 sulphuric acid: 25: blender
Encased Uranium Cell (Infused Uranium Cell): 5 uranium, 3 silica, 5 sulphur, 15 quickwire: 4 encased uranium cell: 20: manufacturer
Silica: 3 raw quartz: 5 silica: 37.5: constructor
Silica (Cheap Silica): 3 raw quartz, 5 limestone: 7 silica: 26.25: assembler
Alumina Solution: 12 bauxite, 18 water: 12 alumina solution, 5 silica: 120: refinery
Quickwire: 1 caterium ingot: 5 quickwire: 60: constructor
Quickwire (Fused Quickwire): 1 caterium ingot, 5 copper ingot: 12 quickwire: 90: assembler
Caterium Ingot: 3 caterium ore: 1 caterium ingot: 15: smelter
Caterium Ingot (Pure Caterium Ingot): 2 caterium ore, 2 water: 1 caterium ingot: 12: refinery
Copper Ingot: 1 copper ore: 1 copper ingot: 30: smelter
Copper Ingot (Copper Alloy Ingot): 10 copper ore, 5 iron ore: 20 copper ingot: 100: foundry
Copper Ingot (Pure Copper Ingot): 6 copper ore, 4 water: 15 copper ingot: 37.5: refinery
Sulphuric Acid: 5 sulphur, 5 water: 5 sulphuric acid: 50: refinery
Concrete: 3 limestone: 1 concrete: 15: constructor
Concrete (Rubber Concrete): 10 limestone, 2 rubber: 9 concrete: 45: assembler
Concrete (Wet Concrete): 6 limestone, 5 water: 4 concrete: 80: refinery
Concrete (Fine Concrete): 3 silica, 12 limestone: 10 concrete: 25: assembler
Electromagnetic Control Rod: 3 stator, 2 ai limiter: 2 electromagnetic control rod: 4: assembler
Electromagnetic Control Rod (Electromagnetic Connection Rod): 2 stator, 1 high-speed connector: 2 electromagnetic control rod: 8: assembler
Stator: 3 steel pipe, 8 wire: 1 stator: 5: assembler
Stator (Quickwire Stator): 4 steel pipe, 15 quickwire: 2 stator: 8: assembler
Steel Pipe: 3 steel ingot: 2 steel pipe: 20: constructor
Steel Ingot: 3 iron ore, 3 coal: 3 steel ingot: 45: foundry
Steel Ingot (Coke Steel Ingot): 15 iron ore, 15 petroleum coke: 20 steel ingot: 100: foundry
Steel Ingot (Compacted Steel Ingot): 6 iron ore, 3 compacted coal: 10 steel ingot: 37.5: foundry
Steel Ingot (Solid Steel Ingot): 2 iron ingot, 2 coal: 3 steel ingot: 60: foundry
Iron Ingot: 1 iron ore: 1 iron ingot: 30: smelter
Iron Ingot (Pure Iron Ingot): 7 iron ore, 4 water: 13 iron ingot: 65: refinery
Iron Ingot (Iron Alloy Ingot): 2 iron ore, 2 copper ore: 5 iron ingot: 50: foundry
Compacted Coal: 5 coal, 5 sulphur: 5 compacted coal: 25: assembler
Petroleum Coke: 4 heavy oil residue: 12 petroleum coke: 120: refinery
Wire: 1 copper ingot: 2 wire: 30: constructor
Wire (Fused Wire): 4 copper ingot, 1 caterium ingot: 30 wire: 90: assembler
Wire (Iron Wire): 5 iron ingot: 9 wire: 22.5: constructor
Wire (Caterium Wire): 1 caterium ingot: 8 wire: 120: constructor
High-Speed Connector: 56 quickwire, 10 cable, 1 circuit board: 1 high-speed connector: 3.75: manufacturer
High-Speed Connector (Silicon High-Speed Connector): 60 quickwire, 25 silica, 2 circuit board: 2 high-speed connector: 3: manufacturer
Cable: 2 wire: 1 cable: 30: constructor
Cable (Coated Cable): 5 wire, 2 heavy oil residue: 9 cable: 67.5: refinery
Cable (Insulated Cable): 9 wire, 6 rubber: 20 cable: 100: assembler
Cable (Quickwire Cable): 3 quickwire, 2 rubber: 11 cable: 27.5: assembler
AI Limiter: 5 copper sheet, 20 quickwire: 1 ai limiter: 5: assembler
Copper Sheet: 2 copper ingot: 1 copper sheet: 10: constructor
Copper Sheet (Steamed Copper Sheet): 3 copper ingot, 3 water: 3 copper sheet: 22.5: refinery
Crystal Oscillator: 36 quartz crystal, 28 cable, 5 reinforced iron plate: 2 crystal oscillator: 1: manufacturer
Crystal Oscillator (Insulated Crystal Oscillator): 10 quartz crystal, 7 rubber, 1 ai limiter: 1 crystal oscillator: 1.875: manufacturer
Quartz Crystal: 5 raw quartz: 3 quartz crystal: 22.5: constructor
Quartz Crystal (Pure Quartz Crystal): 9 raw quartz, 5 water: 7 quartz crystal: 52.5: refinery
Reinforced Iron Plate: 6 iron plate, 12 screw: 1 reinforced iron plate: 5: assembler
Reinforced Iron Plate (Adhered Iron Plate): 3 iron plate, 1 rubber: 1 reinforced iron plate: 3.75: assembler
Reinforced Iron Plate (Bolted Iron Plate): 18 iron plate, 50 screw: 3 reinforced iron plate: 15: assembler
Reinforced Iron Plate (Stitched Iron Plate): 10 iron plate, 20 wire: 3 reinforced iron plate: 5.625: assembler
Iron Plate: 3 iron ingot: 2 iron plate: 20: constructor
Iron Plate (Coated Iron Plate): 10 iron ingot, 2 plastic: 15 iron plate: 75: assembler
Iron Plate (Steel Coated Iron Plate): 3 steel ingot, 2 plastic: 18 iron plate: 45: assembler
Screw: 1 iron rod: 4 screw: 40: constructor
Screw (Cast Screw): 5 iron ingot: 20 screw: 50: constructor
Screw (Steel Screw): 1 steel beam: 52 screw: 260: constructor
Steel Beam: 4 steel ingot: 1 steel beam: 15: constructor
Iron Rod: 1 iron ingot: 1 iron rod: 15: constructor
Iron Rod (Steel Rod): 1 steel ingot: 4 iron rod: 48: constructor
Beacon: 3 iron plate, 1 iron rod, 15 wire, 2 cable: 1 beacon: 7.5: manufacturer
Beacon (Crystal Beacon): 4 steel beam, 16 steel pipe, 1 crystal oscillator: 20 beacon: 10: manufacturer
Encased Industrial Beam: 4 steel beam, 5 concrete: 1 encased industrial beam: 6: assembler
Encased Industrial Beam (Encased Industrial Pipe): 7 steel pipe, 5 concrete: 1 encased industrial beam: 4: assembler
Nitric Acid: 12 nitrogen gas, 3 water, 1 iron plate: 3 nitric acid: 30: blender
Empty Fluid Tank: 1 aluminium ingot: 1 empty fluid tank: 60: constructor
Aluminium Ingot: 6 aluminium scrap, 5 silica: 4 aluminium ingot: 60: foundry
Aluminium Ingot (Pure Aluminium Ingot): 2 aluminium scrap: 1 aluminium ingot: 30: smelter
Alumina Solution (Sloppy Alumina): 10 bauxite, 10 water: 12 alumina solution: 240: refinery
Aluminium Casing: 3 aluminium ingot: 2 aluminium casing: 60: constructor
Aluminium Casing (Alclad Casing): 20 aluminium ingot, 10 copper ingot: 15 aluminium casing: 112.5: assembler
Packaged Turbofuel: 2 turbofuel, 2 empty canister: 2 packaged turbofuel: 20: packager
Turbofuel: 6 fuel, 4 compacted coal: 5 turbofuel: 18.75: refinery
Turbofuel (Turbo Heavy Fuel): 5 heavy oil residue, 4 compacted coal: 4 turbofuel: 30: refinery
Turbofuel (Turbo Blend Fuel): 2 fuel, 4 heavy oil residue, 3 sulphur, 3 petroleum coke: 6 turbofuel: 45: blender
Packaged Fuel: 2 fuel, 2 empty canister: 2 packaged fuel: 40: packager
Packaged Fuel (Diluted Packaged Fuel): 1 heavy oil residue, 2 packaged water: 2 packaged fuel: 60: refinery
Supercomputer (OC Supercomputer): 3 radio control unit, 3 cooling system: 1 supercomputer: 3: assembler
Supercomputer (Super-State Computer): 3 computer, 2 electromagnetic control rod, 20 battery, 45 wire: 2 supercomputer: 2.4: manufacturer
Battery (Classic Battery): 6 sulphur, 7 alclad aluminium sheet, 8 plastic, 12 wire: 4 battery: 30: manufacturer
Alclad Aluminium Sheet: 3 aluminium ingot, 1 copper ingot: 3 alclad aluminium sheet: 30: assembler
Radio Control Unit: 32 aluminium casing, 1 crystal oscillator, 1 computer: 2 radio control unit: 2.5: manufacturer
Radio Control Unit (Radio Control System): 1 crystal oscillator, 10 circuit board, 60 aluminium casing, 30 rubber: 3 radio control unit: 4.5: manufacturer
Radio Control Unit (Radio Connection Unit): 4 heat sink, 2 high-speed connector, 12 quartz crystal: 1 radio control unit: 3.75: manufacturer
Heat Sink: 5 alclad aluminium sheet, 3 copper sheet: 1 heat sink: 7.5: assembler
Heat Sink (Heat Exchanger): 3 aluminium casing, 3 rubber: 1 heat sink: 10: assembler
Cooling System: 2 heat sink, 2 rubber, 5 water, 25 nitrogen gas: 1 cooling system: 6: blender
Cooling System (Cooling Device): 5 heat sink, 1 motor, 24 nitrogen gas: 2 cooling system: 3.75: blender
Motor: 2 rotor, 2 stator: 1 motor: 5: assembler
Motor (Rigour Motor): 3 rotor, 3 stator, 1 crystal oscillator: 6 motor: 7.5: manufacturer
Motor (Electric Motor): 1 electromagnetic control rod, 2 rotor: 2 motor: 7.5: assembler
Rotor: 5 iron rod, 25 screw: 1 rotor: 4: assembler
Rotor (Copper Rotor): 6 copper sheet, 52 screw: 3 rotor: 11.25: assembler
Rotor (Steel Rotor): 2 steel pipe, 6 wire: 1 rotor: 5: assembler
Assembly Director System: 2 adaptive control unit, 1 supercomputer: 1 assembly director system: 0.75: assembler
Adaptive Control Unit: 15 automated wiring, 10 circuit board, 2 heavy modular frame, 2 computer: 2 adaptive control unit: 1: manufacturer
Automated Wiring: 1 stator, 20 cable: 1 automated wiring: 2.5: assembler
Automated Wiring (Automated Speed Wiring): 2 stator, 40 wire, 1 high-speed connector: 4 automated wiring: 7.5: manufacturer
Heavy Modular Frame: 5 modular frame, 15 steel pipe, 5 encased industrial beam, 100 screw: 1 heavy modular frame: 2: manufacturer
Heavy Modular Frame (Heavy Flexible Frame): 5 modular frame, 3 encased industrial beam, 20 rubber, 104 screw: 1 heavy modular frame: 3.75: manufacturer
Heavy Modular Frame (Heavy Encased Frame): 8 modular frame, 10 encased industrial beam, 36 steel pipe, 22 concrete: 3 heavy modular frame: 2.8125: manufacturer
Modular Frame: 3 reinforced iron plate, 12 iron rod: 2 modular frame: 2: assembler
Modular Frame (Bolted Frame): 3 reinforced iron plate, 56 screw: 2 modular frame: 5: assembler
Modular Frame (Steeled Frame): 2 reinforced iron plate, 10 steel pipe: 3 modular frame: 3: assembler
Magnetic Field Generator: 5 versatile framework, 2 electromagnetic control rod, 10 battery: 2 magnetic field generator: 1: manufacturer
Versatile Framework: 1 modular frame, 12 steel beam: 2 versatile framework: 5: assembler
Versatile Framework (Flexible Framework): 1 modular frame, 6 steel beam, 8 rubber: 2 versatile framework: 7.5: manufacturer
Nuclear Pasta: 200 copper powder, 1 pressure conversion cube: 1 nuclear pasta: 0.5: particle accelerator
Copper Powder: 30 copper ingot: 5 copper powder: 50: constructor
Pressure Conversion Cube: 1 fused modular frame, 2 radio control unit: 1 pressure conversion cube: 1: assembler
Fused Modular Frame: 1 heavy modular frame, 50 aluminium casing, 25 nitrogen gas: 1 fused modular frame: 1.5: blender
Fused Modular Frame (Heat-Fused Frame): 1 heavy modular frame, 50 aluminium ingot, 8 nitric acid, 10 fuel: 1 fused modular frame: 3: blender
Thermal Propulsion Rocket: 5 modular engine, 2 turbo motor, 6 cooling system, 2 fused modular frame: 2 thermal propulsion rocket: 1: manufacturer
Modular Engine: 2 motor, 15 rubber, 2 smart plating: 1 modular engine: 1: manufacturer
Smart Plating: 1 reinforced iron plate, 1 rotor: 1 smart plating: 2: assembler
Smart Plating (Plastic Smart Plating): 1 reinforced iron plate, 1 rotor, 3 plastic: 2 smart plating: 5: manufacturer
Turbo Motor: 4 cooling system, 2 radio control unit, 4 motor, 24 rubber: 1 turbo motor: 1.875: manufacturer
Turbo Motor (Turbo Electric Motor): 7 motor, 9 radio control unit, 5 electromagnetic control rod, 7 rotor: 3 turbo motor: 2.8125: manufacturer
Turbo Motor (Turbo Pressure Motor): 4 motor, 1 pressure conversion cube, 24 packaged nitrogen gas, 8 stator: 2 turbo motor: 3.75: manufacturer
Packaged Nitrogen Gas: 4 nitrogen gas, 1 empty fluid tank: 1 packaged nitrogen gas: 60: packager
Cluster Nobelisk: 3 nobelisk, 4 smokeless powder: 1 cluster nobelisk: 2.5: assembler
Nobelisk: 2 steel pipe, 2 black powder: 1 nobelisk: 10: assembler
Nobelisk (Seismic Nobelisk): 8 black powder, 8 steel pipe, 1 crystal oscillator: 4 nobelisk: 6: manufacturer
Smokeless Powder: 2 black powder, 1 heavy oil residue: 2 smokeless powder: 20: refinery
Black Powder: 1 coal, 1 sulphur: 2 black powder: 30: assembler
Black Powder (Fine Black Powder): 2 sulphur, 1 compacted coal: 4 black powder: 15: assembler
Nuke Nobelisk: 5 nobelisk, 20 encased uranium cell, 10 smokeless powder, 6 ai limiter: 1 nuke nobelisk: 0.5: manufacturer
Pulse Nobelisk: 5 nobelisk, 1 crystal oscillator: 5 pulse nobelisk: 5: assembler
Explosive Rebar: 2 iron rebar, 2 smokeless powder, 2 steel pipe: 1 explosive rebar: 5: manufacturer
Iron Rebar: 1 iron rod: 1 iron rebar: 15: constructor
Shatter Rebar: 2 iron rebar, 3 quartz crystal: 1 shatter rebar: 5: assembler
Stun Rebar: 1 iron rebar, 5 quickwire: 1 stun rebar: 10: assembler
Homing Rifle Ammo: 20 rifle ammo, 1 high-speed connector: 10 homing rifle ammo: 25: assembler
Rifle Ammo: 3 copper sheet, 2 smokeless powder: 15 rifle ammo: 75: assembler
Turbo Rifle Ammo (Packaged Turbofuel): 25 rifle ammo, 3 aluminium casing, 3 packaged turbofuel: 50 turbo rifle ammo: 250: manufacturer
Turbo Rifle Ammo (Liquid Turbofuel): 25 rifle ammo, 3 aluminium casing, 3 turbofuel: 50 turbo rifle ammo: 250: blender
Plutonium Waste: 1 plutonium fuel rod, 3000 water: 10 plutonium waste: 1: nuclear power plant
Plutonium Fuel Rod: 30 encased plutonium cell, 18 steel beam, 6 electromagnetic control rod, 10 heat sink: 1 plutonium fuel rod: 0.25: manufacturer
Plutonium Fuel Rod (Plutonium Fuel Unit): 20 encased plutonium cell, 1 pressure conversion cube: 1 plutonium fuel rod: 0.5: assembler
Encased Plutonium Cell: 2 plutonium pellet, 4 concrete: 1 encased plutonium cell: 5: assembler
Encased Plutonium Cell (Instant Plutonium Cell): 150 non-fissile uranium, 20 aluminium casing: 20 encased uranium cell: 10: particle accelerator
Plutonium Pellet: 100 non-fissile uranium, 25 uranium waste: 30 plutonium pellet: 30: particle accelerator
Iodine Infused Filter: 1 gas filter, 8 quickwire, 1 aluminium casing: 1 iodine infused filter: 3.75: manufacturer
Gas Filter: 5 coal, 2 rubber, 2 fabric: 1 gas filter: 7.5: manufacturer
Fabric (Polyester Fabric): 1 polymer resin, 1 water: 1 fabric: 30: refinery
Portable Miner (Automated Miner): 1 motor, 4 steel pipe, 4 iron rod, 2 iron plate: 1 portable miner: 1: manufacturer
"""

# Recipes removed as they are not used in any further recipes and are only for convenience
forbiddenRecipeSheet = """
Unpackage Heavy Oil Residue: 2 packaged heavy oil residue: 2 heavy oil residue, 2 empty canister: 20: packager
Packaged Heavy Oil Residue: 2 heavy oil residue, 2 empty canister: 2 packaged heavy oil residue: 20: packager
Unpackage Alumina Solution: 2 packaged alumina solution: 2 alumina solution, 2 empty canister: 120: packager
Packaged Alumina Solution: 2 alumina solution, 2 empty canister: 2 packaged alumina solution: 120: packager
Unpackage Oil: 2 packaged oil: 2 crude oil, 2 empty canister: 60: packager
Packaged Oil: 2 crude oil, 2 empty canister: 2 packaged oil: 30: packager
Unpackage Sulphuric Acid: 1 packaged sulphuric acid: 1 sulphuric acid, 1 empty canister: 60: packager
Packaged Sulphuric Acid: 2 sulphuric acid, 2 empty canister: 2 packaged sulphuric acid: 40: packager
Unpackage Water: 2 packaged water: 2 water, 2 empty canister: 120: packager
Unpackage Nitric Acid: 1 packaged nitric acid: 1 nitric acid, 1 empty fluid tank: 20: packager
Packaged Nitric Acid: 1 nitric acid, 1 empty fluid tank: 1 packaged nitric acid: 30: packager
Unpackage Nitrogen Gas: 1 packaged nitrogen gas: 4 nitrogen gas, 1 empty fluid tank: 240: packager
"""

# Some handy parts lists (some items appear in more than one)
basicResourceParts = {"bauxite", "cateriumore", "coal", "copperore", "crudeoil", "ironore", "limestone", "nitrogengas",
                      "rawquartz", "sulphur", "uranium", "water"}
spaceElevatorParts = {"adaptivecontrolunit", "assemblydirectorsystem", "automatedwiring", "magneticfieldgenerator",
                      "modularengine", "nuclearpasta", "smartplating", "thermalpropulsionrocket", "versatileframework"}
fluidParts = {"aluminasolution", "crudeoil", "fuel", "heavyoilresidue", "nitrogengas", "nitricacid", "sulphuricacid",
              "turbofuel", "water"}
equipmentParts = {"clusternobelisk", "explosiverebar", "gasfilter", "homingrifleammo", "iodineinfusedfilter",
                  "ironrebar", "nobelisk", "nukenobelisk", "portableminer", "pulsenobelisk", "rifleammo",
                  "shatterrebar", "stunrebar", "turborifleammo"}
radioactiveParts = {"encasedplutoniumcell", "encaseduraniumcell", "non-fissileuranium", "plutoniumfuelrod",
                    "plutoniumpellet", "plutoniumwaste", "uranium", "uraniumfuelrod", "uraniumwaste"}
miscParts = {"ailimiter", "alcladaluminiumsheet", "aluminiumcasing", "aluminiumingot",
             "aluminiumscrap", "battery", "beacon", "blackpowder", "cable", "cateriumingot", "circuitboard",
             "compactedcoal", "computer", "concrete", "coolingsystem", "copperingot", "copperpowder", "coppersheet",
             "crystaloscillator", "electromagneticcontrolrod", "emptycanister", "emptyfluidtank",
             "encasedindustrialbeam", "fabric", "fusedmodularframe", "heatsink",
             "heavymodularframe", "high-speedconnector", "ironingot", "ironplate", "ironrod", "modularframe", "motor",
             "packagedaluminasolution", "packagedfuel", "packagedheavyoilresidue",
             "packagedliquidbiofuel", "packagednitricacid", "packagednitrogengas", "packagedoil",
             "packagedsulphuricacid", "packagedturbofuel", "packagedwater", "petroleumcoke", "plastic",
             "polymerresin", "pressureconversioncube",
             "quantumcomputer", "quartzcrystal", "quickwire", "radiocontrolunit", "reinforcedironplate", "rotor",
             "rubber", "screw", "silica", "smokelesspowder", "stator", "steelbeam", "steelingot", "steelpipe",
             "supercomputer", "turbomotor", "wire"}
allParts = basicResourceParts | spaceElevatorParts | fluidParts | equipmentParts | radioactiveParts | miscParts
allPartsList = sorted(allParts)
print(len(allParts), "parts available")

makeableParts = spaceElevatorParts | equipmentParts | fluidParts | (radioactiveParts ^ {"uranium"}) | miscParts
unsinkableParts = fluidParts | (radioactiveParts ^ {"plutoniumfuelrod", "uranium"})
sinkableParts = allParts ^ unsinkableParts

buildingTypes = {"assembler", "blender", "constructor", "foundry", "manufacturer", "nuclearpowerplant", "packager",
                 "particleaccelerator", "refinery", "smelter"}
recipeBook = set()
recipeOutputDict = {}

recipeFormatRegex = (r"[a-zA-Z\d\s()-]+\s?:\s?"
                     r"(?:[\d.]+[a-zA-Z\s-]+\s?[,+]?\s?){1,4}\s?:\s?"
                     r"(?:[\d.]+[a-zA-Z-\s]+\s?[,+]?\s?){1,2}\s?:\s?"
                     r"[\d.]+\s?:\s?"
                     r"[a-zA-Z\s-]+")


class Recipe:
    def __init__(self, recipeString, recipeHeritage=None):
        self.recipeString = recipeString
        # Pretty loosely defined recipe input; just has to be:
        # "[RecipeName]:[N1][ingredient1][N2][ingredient2]...:[N3][Output3][N4][Output4]...:[OutputRate]:[BuildingType]"
        # Output rate is for the first listed part in the outputs, since all should be proportional
        # Can have ","s or "+"s between items in input/output and whitespace around ":"s, ","s and "+"s
        if not re.fullmatch(recipeFormatRegex, self.recipeString):
            raise BadRecipeException("Recipe string - \"%s\" - not formatted correctly" % recipeString)
        self.name = re.search(r"^\s*(.+?)\s*:", recipeString).group(1)
        # print(self.name)
        # Lower-case, remove ","s, "+"s and whitespace
        self.recipeStringSanitised = re.sub(r"[,+\s]", "", recipeString.lower())
        # print(self.recipeStringSanitised)
        recipeSections = self.recipeStringSanitised.split(":")[1:]

        # Parse Input Parts
        self.inputPartsDict = {i[1]: float(i[0]) for i in re.findall(r"([\d.]+)([a-z-]+)", recipeSections[0])}
        if not set(self.inputPartsDict).issubset(allParts):
            raise BadRecipeException("Stated input parts - \"%s\" - not in accepted list of parts"
                                     % set(self.inputPartsDict).difference(allParts))
        self.inputPartsArray = np.zeros(len(allParts), "float64")
        for part in self.inputPartsDict:
            self.inputPartsArray[allPartsList.index(part)] = self.inputPartsDict[part]

        # Parse Output Parts
        self.outputPartsDict = {i[1]: float(i[0]) for i in re.findall(r"([\d.]+)([a-z-]+)", recipeSections[1])}
        if not set(self.outputPartsDict).issubset(makeableParts | {"dummy"}):
            if not set(self.outputPartsDict).issubset(allParts):
                raise BadRecipeException("Stated output parts - \"%s\" - not in accepted list of parts"
                                         % set(self.outputPartsDict).difference(allParts))
            raise BadRecipeException("Stated output parts - \"%s\" - not in accepted list of makeable parts"
                                     % set(self.outputPartsDict).difference(makeableParts))
        for part in self.outputPartsDict:
            try:
                recipeOutputDict[part].append(self)
            except KeyError:
                recipeOutputDict[part] = [self]
        self.outputPartsArray = np.zeros(len(allParts), "float64")
        for part in self.outputPartsDict:
            if part != "dummy":
                self.outputPartsArray[allPartsList.index(part)] = self.outputPartsDict[part]

        # print(self.recipeInputs, self.recipeOutputs)
        self.outputRate = float(recipeSections[2])
        self.building = recipeSections[3]
        if self.building not in (buildingTypes | {"dummy"}):
            raise BadRecipeException("Stated building type - \"%s\" - is not in accepted list of building types"
                                     % self.recipeString.split(":")[4])
        self.inputRecipes = None
        self.inputResources = None
        self.recipeHeritage = recipeHeritage
        recipeBook.add(self)

    def __lt__(self, other):
        return self.name < other.name

    def findDependencies(self, recipesFound=None, resourcesFound=None, decisionPointsFound=None, deadEndsFound=None,
                         availableResources=None, availableBuildings=None, level=0):
        print(("| " * level) + self.name)
        if availableBuildings is None:
            availableBuildings = buildingTypes
        if availableResources is None:
            availableResources = basicResourceParts
        if recipesFound is None:
            recipesFound = set()
        self.inputRecipes = set()
        self.inputResources = set()
        if resourcesFound is None:
            resourcesFound = set()
        if decisionPointsFound is None:
            decisionPointsFound = set()
        if deadEndsFound is None:
            deadEndsFound = set()
        for part in sorted(self.inputPartsDict):
            print(("| " * (level + 1)) + "needs " + part)
            if part in deadEndsFound:
                print(("| " * (level + 2)) + "part known to be unobtainable")
                return "UNMAKEABLE", None, None, None
            if part in basicResourceParts:
                if part in availableResources:
                    self.inputResources.add(part)
                    resourcesFound.add(part)
                else:
                    print(("| " * (level + 2)) + "resource is unavailable")
                    print(("| " * (level + 1)) + "cannot make recipe due to unavailability of", part)
                    return "UNMAKEABLE", None, None, None
            else:
                waysToMakePart = 0
                for recipe in recipeOutputDict[part]:
                    if recipe.building in (availableBuildings | {"dummy"}):
                        if recipe in recipesFound:
                            waysToMakePart += 1
                            print(("| " * (level + 2)) + "already got recipe:", recipe.name)
                        else:
                            newRecipesFound, newResourcesFound, newDecisionPointsFound, newDeadendsFound \
                                = recipe.findDependencies(recipesFound | {self}, resourcesFound,
                                                          decisionPointsFound, deadEndsFound,
                                                          availableResources, availableBuildings, level + 2)
                            if newRecipesFound != "UNMAKEABLE":
                                self.inputRecipes.add(recipe)
                                waysToMakePart += 1
                                recipesFound |= newRecipesFound.difference({self})
                                resourcesFound |= newResourcesFound
                                decisionPointsFound |= newDecisionPointsFound
                                deadEndsFound |= newDeadendsFound
                    else:
                        print(("| " * (level + 2)) + recipe.name, "not makeable as", recipe.building,
                              "unavailable")
                if waysToMakePart > 1:
                    if part not in decisionPointsFound:
                        decisionPointsFound.add(part)
                        print(("| " * (level + 2)) + "DECISION POINT %s: %s recipes for %s"
                              % (len(decisionPointsFound), len(recipeOutputDict[part]), part))
                elif waysToMakePart == 0:
                    print(("| " * (level + 1)) + "recipe not makeable as no recipes for", part, "are makeable")
                    deadEndsFound.add(part)
                    return "UNMAKEABLE", None, None, None
        # Add recipe to found list if it's definitely useful
        recipesFound.add(self)
        return recipesFound, resourcesFound, decisionPointsFound, deadEndsFound


for line in recipeSheet.split("\n")[1:-1]:
    Recipe(line)
print(len(recipeBook), "recipes available")


basicResourceMask = np.zeros(len(allParts), "bool")
for part in basicResourceParts:
    basicResourceMask[allPartsList.index(part)] = 1


def optimise(outputParts, availableResources=None, availableBuildings=None, silence=False):
    if type(outputParts) == str:
        outputParts = [outputParts]
    outputParts = [part.lower().replace(" ", "") for part in outputParts]
    dummyRecipe = Recipe("RECIPE TO OPTIMISE:"
                         + "".join(["1"+part for part in outputParts]) + ":"
                         + "1dummy:1:dummy")
    recipesFound, resourcesFound, decisionPointsFound, deadEndsFound \
        = dummyRecipe.findDependencies(availableResources=availableResources, availableBuildings=availableBuildings)
    recipesFound.remove(dummyRecipe)
    print(len(recipesFound), "recipes discovered for use:", sorted([recipe.name for recipe in recipesFound]))
    print(len(resourcesFound), "resource requirements discovered:", ", ".join(resourcesFound))
    print(len(decisionPointsFound), "decision points discovered:", ", ".join(decisionPointsFound))
    # Dict of recipes used in this tree, listed by outputs
    currentRecipeOutputDict = {}
    for recipe in recipesFound:
        for part in recipe.outputPartsDict:
            try:
                currentRecipeOutputDict[part].append(recipe)
            except KeyError:
                currentRecipeOutputDict[part] = [recipe]
    # Ordered list of said recipes, for use with...
    recipesFoundList = sorted(recipesFound)
    # ... The usage rates of said recipes (effectively number of buildings running that recipe at 100%)
    recipeUsageArray = np.zeros(len(recipesFoundList), "float64")
    # Dict of relative production rates used by competing recipes (1:1:1 means each recipe contributes 1/3) by part
    decisionPointLevels = {part: np.ones(len(currentRecipeOutputDict[part]), "float64") for part in decisionPointsFound}
    # Working array of values representing part input numbers needed by recipes added to the chain thus far
    requirements = np.zeros(len(allPartsList), "float64")
    for part in outputParts:
        requirements[allPartsList.index(part)] += 1
    lowestMaxResourceRequirement = 1e100
    while np.any((requirements > 0) * ~basicResourceMask):
        partIndex = np.argmax(requirements * (requirements > 0) * ~basicResourceMask)
        part = allPartsList[partIndex]
        amountNeeded = requirements[partIndex]
        print(amountNeeded, part, "needed >>")
        # Gotta stop somewhere...
        if amountNeeded < 1e-100:
            print("Actually, close enough.")
            break
        if part in decisionPointsFound:
            for i, recipe in enumerate(currentRecipeOutputDict[part]):
                moreRecipeUsage = (amountNeeded
                                   * (decisionPointLevels[part][i] / sum(decisionPointLevels[part]))
                                   / recipe.outputPartsArray[partIndex])
                recipeUsageArray[recipesFoundList.index(recipe)] += moreRecipeUsage
                requirements += (recipe.inputPartsArray - recipe.outputPartsArray) * moreRecipeUsage
        else:
            recipe = currentRecipeOutputDict[part][0]
            moreRecipeUsage = amountNeeded / recipe.outputPartsArray[partIndex]
            recipeUsageArray[recipesFoundList.index(recipe)] += moreRecipeUsage
            requirements += (recipe.inputPartsArray - recipe.outputPartsArray) * moreRecipeUsage
        print(requirements[partIndex], part)
    print("\nFinal Buildings List:")
    for usage, recipe in zip(recipeUsageArray, recipesFoundList):
        print(usage, recipe.building, "buildings for", recipe.name)
    print("\nRequires (per unit production per minute):")
    for i in np.nonzero((requirements > 0) * basicResourceMask)[0]:
        print(requirements[i], allPartsList[i])
    if np.any(requirements < 0):
        print("\nByproducts:")
        for i in np.nonzero(requirements < 0)[0]:
            print(-requirements[i], allPartsList[i])


optimise({"supercomputer"},
         #availableResources={"copperore", "ironore", "coal", "sulphur"},
         availableBuildings={"smelter", "foundry", "constructor", "assembler", "manufacturer", "refinery", "packager"}
         )
