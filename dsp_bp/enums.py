import enum

class Recipe(enum.IntEnum):
    Gear = 5

class BuildingItem(enum.IntEnum):
    ConveyorBeltMKI = 2001
    ConveyorBeltMKII = 2002
    ConveyorBeltMKIII = 2003
    
    SorterMKI = 2011
    SorterMKII = 2012
    SorterMKIII = 2013
    PileSorter = 2014
    
    Splitter = 2020
    
    TrafficMonitor = 2030
    
    DepotMK1 = 2101
    DepotMK2 = 2102
    
    StorageTank = 2106
    
    TeslaTower = 2201
    WirelessPowerTower = 2202
    WindTurbine = 2203
    ThermalPowerPlant = 2204
    SolarPanel = 2205
    Accumulator = 2206
    
    MiniFusionPowerPlant = 2211
    SateliteSubStation = 2212
    
    ArcSmelter = 2302
    AssemblingMachineMKI = 2303
    AssemblingMachineMKII = 2304
    AssemblingMachineMKIII = 2305
    
    OilRefinary = 2308
    ChemicalPlant = 2309
    MiniatureParticleCollider = 2310
    
    SprayCoater = 2313
    Fractionator = 2314
    
    QuantumChemicalPlant = 2317

class BuildingModel(enum.IntEnum):
    ConveyorBeltMKI = 35
    ConveyorBeltMKII = 36
    ConveyorBeltMKIII = 37
    SplitterX = 38
    SplitterK = 39
    SplitterI = 40
    SorterMKI = 41
    SorterMKII = 42
    SorterMKIII = 43
    TeslaTower = 44
    
    Accumulator = 46
    
    DepotMK1 = 51
    DepotMK2 = 52
    WindTurbine = 53
    ThermalPowerPlant = 54
    SolarPanel = 55
    
    ArcSmelter = 62
    OilRefinary = 63
    ChemicalPlant = 64
    
    SateliteSubStation = 68
    MiniatureParticleCollider = 69
    
    WirelessPowerTower = 71
    
    AssemblingMachineMKI = 65
    AssemblingMachineMKII = 66
    AssemblingMachineMKIII = 67
    
    MiniFusionPowerPlant = 118
    Fractionator = 119
    SprayCoater = 120
    StorageTank = 121
    
    TrafficMonitor = 208
    
    QuantumChemicalPlant = 376
    
    PileSorter = 483

class Item(enum.IntEnum):
	Lava = -1
	IronOre = 1001
	CopperOre = 1002
	SiliconOre = 1003
	TitaniumOre = 1004
	Stone = 1005
	Coal = 1006
	Log = 1030
	PlantFuel = 1031
	FireIce = 1011
	KimberliteOre = 1012
	FractalSilicon = 1013
	OpticalGratingCrystal = 1014
	SpiniformStalagmiteCrystal = 1015
	UnipolarMagnet = 1016
	IronIngot = 1101
	CopperIngot = 1104
	HighPuritySilicon = 1105
	TitaniumIngot = 1106
	StoneBrick = 1108
	EnergeticGraphite = 1109
	Steel = 1103
	TitaniumAlloy = 1107
	Glass = 1110
	TitaniumGlass = 1119
	Prism = 1111
	Diamond = 1112
	CrystalSilicon = 1113
	Gear = 1201
	Magnet = 1102
	MagneticCoil = 1202
	ElectricMotor = 1203
	ElectromagneticTurbine = 1204
	SuperMagneticRing = 1205
	ParticleContainer = 1206
	StrangeMatter = 1127
	CircuitBoard = 1301
	Processor = 1303
	QuantumChip = 1305
	MicrocrystallineComponent = 1302
	PlaneFilter = 1304
	ParticleBroadband = 1402
	PlasmaExciter = 1401
	PhotonCombiner = 1404
	SolarSail = 1501
	Water = 1000
	CrudeOil = 1007
	RefinedOil = 1114
	SulfuricAcid = 1116
	Hydrogen = 1120
	Deuterium = 1121
	Antimatter = 1122
	CriticalPhoton = 1208
	HydrogenFuelRod = 1801
	DeuteronFuelRod = 1802
	AntimatterFuelRod = 1803
	Plastic = 1115
	Graphene = 1123
	CarbonNanotube = 1124
	OrganicCrystal = 1117
	TitaniumCrystal = 1118
	CasimirCrystal = 1126
	GravitationLens = 1209
	SpaceWarper = 1210
	AnnihilationConstraintSphere = 1403
	Thruster = 1405
	ReinforcedThruster = 1406
	LogisticsDrone = 5001
	LogisticsVessel = 5002
	FrameMaterial = 1125
	DysonSphereComponent = 1502
	SmallCarrierRocket = 1503
	Foundation = 1131
	AccelerantMkI = 1141
	AccelerantMkII = 1142
	AccelerantMkIII = 1143
	ConveyorBeltMKI = 2001
	ConveyorBeltMKII = 2002
	ConveyorBeltMKIII = 2003
	SorterMKI = 2011
	SorterMKII = 2012
	SorterMKIII = 2013
	Splitter = 2020
	StorageMKI = 2101
	StorageMKII = 2102
	StorageTank = 2106
	AssemblingMachineMKI = 2303
	AssemblingMachineMKII = 2304
	AssemblingMachineMKIII = 2305
	PlaneSmelter = 2315
	TeslaTower = 2201
	WirelessPowerTower = 2202
	SatelliteSubstation = 2212
	WindTurbine = 2203
	ThermalPowerStation = 2204
	MiniFusionPowerStation = 2211
	MiningMachine = 2301
	ArcSmelter = 2302
	OilExtractor = 2307
	OilRefinery = 2308
	WaterPump = 2306
	ChemicalPlant = 2309
	Fractionator = 2314
	SprayCoater = 2313
	SolarPanel = 2205
	Accumulator = 2206
	AccumulatorFull = 2207
	EMRailEjector = 2311
	RayReceiver = 2208
	VerticalLaunchingSilo = 2312
	EnergyExchanger = 2209
	MiniatureParticleCollider = 2310
	ArtificialStar = 2210
	PlanetaryLogisticsStation = 2103
	InterstellarLogisticsStation = 2104
	OrbitalCollector = 2105
	MatrixLab = 2901
	ElectromagneticMatrix = 6001
	EnergyMatrix = 6002
	StructureMatrix = 6003
	InformationMatrix = 6004
	GravityMatrix = 6005
	UniverseMatrix = 6006