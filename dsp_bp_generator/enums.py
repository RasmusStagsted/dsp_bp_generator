import enum

class SmeltingRecipe(enum.IntEnum):
    IronIngot = 1
    Magent = 2
    CopperIngot = 3
    StoneBrick = 4
    EnergeticGraphite = 17
    SiliconOre = 34
    CrystalSilicon = 37
    Glass = 57
    HighPuritySilicon = 59
    Diamond = 60
    DiamondAdvanced = 61
    Steel = 63
    TitaniumIngot = 65
    TitaniumAlloy = 66

class AssemblingRecipe(enum.IntEnum):
	OrbitalCollector = 2105 #TODO: Fix number

	Gear = 5
	MagneticCoil = 6
	WindTurbine = 7
	TeslaTower = 8
	MatrixLab = 10
	Prism = 11
	PlasmaExciter = 12
	WirelessPowerTower = 13
	OilExtractor = 14
	OilRefinary = 15
	HydrogenFuelRod = 19
	Thruster = 20
	ReinforcedThruster = 21
	ChemicalPlant = 22
	TitaniumCrystal = 26
	CashmirCrystal = 28
	CashmirCrystalAdvanced = 29
	TitaniumGlass = 30
	ParticleBroadband = 36
	PlaneFilter = 38
	MiniatureParticleCollider = 39
	DeuteronFuelRod = 41
	AnnihilationConstraintSphere = 42
	AntimatterFuelRod = 44
	AssemblingMachineMKI = 45
	AssemblingMachineMKII = 46
	AssemblingMachineMKIII = 47
	MiningMachine = 48
	WaterPump = 49
	CircuitBoard = 50
	Processor = 51
	QuantumChip = 52
	MicrocrystallineComponent = 53
	OrganicCrystal = 54
	ArcSmelter = 56
	CrystalSiliconAdvanced = 62
	ThermalPowerPlant = 64
	SolarPanel = 67
	PhotonCombiner = 68
	PhotonCombinerAdvanced = 69
	SolarSail = 70
	EMRailEjector = 71
	RayReceiver = 72
	SateliteSubstation = 73
	Accumulator = 76
	EnergyExchanger = 77
	SpaceWraper = 78
	SpaceWraperAdvanced = 79
	FrameMaterial = 80
	DysonSphereComponent = 81
	VerticalLaunchingSilo = 82
	DysonSphereRocket = 83
	ConveyorBeltMKI = 84
	SorterMKI = 85
	DepotMKI = 86
	Splitter = 87
	SorterMKII = 88
	ConveyorBeltMKII = 89
	DepotMKII = 91
	ConveyorBeltMKIII = 92
	PlanetaryLogisticsStation = 93
	LogisticDrone = 94
	InterstellarLogisticsStation = 95
	LogisticsVessel = 96
	ElectricMotor = 97
	ParticleContainer = 99
	ParticleContainerAdvanced = 100
	GravitationLens = 101
	SuperMagneticRing = 103
	Engine = 105
	ProlifiratorMKI = 106
	ProlifiratorMKII = 107
	ProlifiratorMKIII = 108
	SprayCoater = 109
	Fractionator = 110
	ObitalCollector = 111
	MiniFusionPowerPlant = 113
	StorageTank = 114
	PlaneSmelter = 116
	ItemMonitor = 117
	GeothermalPowerPlant = 118
	AdvancedMiningMachine = 119
	AutomaticPiler = 120
	LogisticDistributor = 122
	LogisticBot = 123
	QuantumChemicalPlant = 124
	GaussTurrent = 125
	LaserTurret = 126
	ImplosionCanon = 127
	PlasmaTurret = 128
	MissleTurret = 129
	JammerTower = 130
	SignalTower = 131
	PlanetaryShieldGenerator = 132
	CombustibleUnit = 133
	MagnumAmmoBox = 136
	TitaniumAmmoBox = 137
	SuperAlloyAmmoBox = 138
	ShellSet = 139
	HighExplosiveShellSet = 140
	CrystalShellSet = 141
	PlasmaCapsule = 142
	MissleSet = 144
	SuperSonicMissleSet = 145
	Prototype = 147
	PrecisionDrone = 148
	AttackDrone = 149
	Covette = 150
	Destroyer = 151
	BattleFieldAnalysisBase = 152
	SRPlasmaTurret = 157
	JamingCapsule = 158
	StackSorter = 160

class BuildingItem(enum.IntEnum):
    ConveyorBeltMKI = 2001
    ConveyorBeltMKII = 2002
    ConveyorBeltMKIII = 2003
    
    SorterMKI = 2011
    SorterMKII = 2012
    SorterMKIII = 2013
    PileSorter = 2014
    
    Splitter = 2020 # TODO implement
    
    TrafficMonitor = 2030 # TODO implement
    
    DepotMKI = 2101 # TODO implement
    DepotMKII = 2102 # TODO implement
    
    StorageTank = 2106 # TODO implement
    LogisticDistributor = 2107
    
    TeslaTower = 2201
    WirelessPowerTower = 2202
    WindTurbine = 2203 # TODO implement
    ThermalPowerPlant = 2204 # TODO implement
    SolarPanel = 2205 # TODO implement
    Accumulator = 2206 # TODO implement
    
    MiniFusionPowerPlant = 2211 # TODO implement
    SateliteSubstation = 2212
    
    ArcSmelter = 2302
    AssemblingMachineMKI = 2303
    AssemblingMachineMKII = 2304
    AssemblingMachineMKIII = 2305
    
    OilRefinary = 2308 # TODO implement
    ChemicalPlant = 2309 # TODO implement
    MiniatureParticleCollider = 2310 # TODO implement
    
    SprayCoater = 2313 # TODO implement
    Fractionator = 2314 # TODO implement
    
    QuantumChemicalPlant = 2317 # TODO implement

class BuildingModel(enum.IntEnum):
    ConveyorBeltMKI = 35
    ConveyorBeltMKII = 36
    ConveyorBeltMKIII = 37
    SplitterCross = 38
    SplitterTwoLayerStraight = 39
    SplitterTwoLayerCross = 40
    SorterMKI = 41
    SorterMKII = 42
    SorterMKIII = 43
    TeslaTower = 44
    
    Accumulator = 46
    
    DepotMKI = 51
    DepotMKII = 52
    WindTurbine = 53
    ThermalPowerPlant = 54
    SolarPanel = 55
    
    ArcSmelter = 62
    OilRefinary = 63
    ChemicalPlant = 64
    
    SateliteSubstation = 68
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
    LogisticDistributor = 371
    
    QuantumChemicalPlant = 376
    
    PileSorter = 483

class Item(enum.IntEnum):
	Lava = -1
	Water = 1000
	IronOre = 1001
	CopperOre = 1002
	SiliconOre = 1003
	TitaniumOre = 1004
	Stone = 1005
	Coal = 1006
	CrudeOil = 1007
	FireIce = 1011
	KimberliteOre = 1012
	FractalSilicon = 1013
	OpticalGratingCrystal = 1014
	SpiniformStalagmiteCrystal = 1015
	UnipolarMagnet = 1016
	Log = 1030
	PlantFuel = 1031
	IronIngot = 1101
	Magnet = 1102
	Steel = 1103
	CopperIngot = 1104
	HighPuritySilicon = 1105
	TitaniumIngot = 1106
	TitaniumAlloy = 1107
	StoneBrick = 1108
	EnergeticGraphite = 1109
	Glass = 1110
	Prism = 1111
	Diamond = 1112
	CrystalSilicon = 1113
	RefinedOil = 1114
	Plastic = 1115
	SulfuricAcid = 1116
	OrganicCrystal = 1117
	TitaniumCrystal = 1118
	TitaniumGlass = 1119
	Hydrogen = 1120
	Deuterium = 1121
	Antimatter = 1122
	Graphene = 1123
	CarbonNanotube = 1124
	FrameMaterial = 1125
	CasimirCrystal = 1126
	StrangeMatter = 1127
	Foundation = 1131
	AccelerantMkI = 1141
	AccelerantMkII = 1142
	AccelerantMkIII = 1143
	Gear = 1201
	MagneticCoil = 1202
	ElectricMotor = 1203
	ElectromagneticTurbine = 1204
	SuperMagneticRing = 1205
	ParticleContainer = 1206
	CriticalPhoton = 1208
	GravitationLens = 1209
	SpaceWarper = 1210
	CircuitBoard = 1301
	MicrocrystallineComponent = 1302
	Processor = 1303
	PlaneFilter = 1304
	QuantumChip = 1305
	PlasmaExciter = 1401
	ParticleBroadband = 1402
	AnnihilationConstraintSphere = 1403
	PhotonCombiner = 1404
	Thruster = 1405
	ReinforcedThruster = 1406
	SolarSail = 1501
	DysonSphereComponent = 1502
	SmallCarrierRocket = 1503
	HydrogenFuelRod = 1801
	DeuteronFuelRod = 1802
	AntimatterFuelRod = 1803
	ConveyorBeltMKI = 2001
	ConveyorBeltMKII = 2002
	ConveyorBeltMKIII = 2003
	SorterMKI = 2011
	SorterMKII = 2012
	SorterMKIII = 2013
	Splitter = 2020
	DepotMKI = 2101
	DepotMKII = 2102
	PlanetaryLogisticsStation = 2103
	InterstellarLogisticsStation = 2104
	OrbitalCollector = 2105
	StorageTank = 2106
	LogisticDistributor = 2107
	TeslaTower = 2201
	WirelessPowerTower = 2202
	WindTurbine = 2203
	ThermalPowerStation = 2204
	SolarPanel = 2205
	Accumulator = 2206
	AccumulatorFull = 2207
	RayReceiver = 2208
	EnergyExchanger = 2209
	ArtificialStar = 2210
	MiniFusionPowerStation = 2211
	SatelliteSubstation = 2212
	MiningMachine = 2301
	ArcSmelter = 2302
	AssemblingMachineMKI = 2303
	AssemblingMachineMKII = 2304
	AssemblingMachineMKIII = 2305
	WaterPump = 2306
	OilExtractor = 2307
	OilRefinery = 2308
	ChemicalPlant = 2309
	MiniatureParticleCollider = 2310
	EMRailEjector = 2311
	VerticalLaunchingSilo = 2312
	SprayCoater = 2313
	Fractionator = 2314
	PlaneSmelter = 2315
	MatrixLab = 2901
	LogisticsDrone = 5001
	LogisticsVessel = 5002
	ElectromagneticMatrix = 6001
	EnergyMatrix = 6002
	StructureMatrix = 6003
	InformationMatrix = 6004
	GravityMatrix = 6005
	UniverseMatrix = 6006
 
 