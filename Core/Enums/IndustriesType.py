from enum import Enum


class TechnologyIndustryType(Enum):
    SoftwareInfrastructure = 1,
    Semiconductors = 2,
    ConsumerElectronics = 3,
    SoftwareApplication = 4,
    InformationTechnologyServices = 5,
    SemiconductorEquipmentAndMaterials = 6,
    CommunicationEquipment = 7,
    ComputerHardware = 8,
    ElectronicComponents = 9,
    ScientificAndTechnicalInstruments = 10,
    Solar = 11,
    ElectronicsAndComputerDistribution = 12


class FinancialServicesIndustryType(Enum):
    BanksDiversified = 1,
    CreditServices = 2,
    AssetManagement = 3,
    InsuranceDiversified = 4,
    BanksRegional = 5,
    CapitalMarkets = 6,
    FinancialDataAndStockExchanges = 7,
    InsurancePropertyAndCasualty = 8,
    InsuranceBrokers = 9,
    InsuranceLife = 10,
    InsuranceSpecialty = 11,
    MortgageFinance = 12,
    InsuranceReinsurance = 13,
    ShellCompanies = 14,
    FinancialConglomerates = 15


class HealthcareIndustryType(Enum):
    DrugManufacturersGeneral = 1,
    HealthcarePlans = 2,
    MedicalDevices = 3,
    Biotechnology = 4,
    DiagnosticsAndResearch = 5,
    MedicalInstrumentsAndSupplies = 6,
    MedicalCareFacilities = 7,
    DrugManufacturersSpecialtyAndGeneric = 8,
    HealthInformationServices = 9,
    MedicalDistribution = 10,
    PharmaceuticalRetailers = 11


class ConsumerCyclicalIndustryType(Enum):
    InternetRetail = 1,
    AutoManufacturers = 2,
    Restaurants = 3,
    HomeImprovementRetail = 4,
    TravelServices = 5,
    SpecialtyRetail = 6,
    ApparelRetail = 8,
    ResidentialConstruction = 9,
    FootwearAndAccessories = 10,
    PackagingAndContainers = 11,
    Lodging = 12,
    AutoParts = 13,
    AutoAndTruckDealerships = 14,
    Gambling = 15,
    ResortsAndCasinos = 16,
    Leisure = 17,
    ApparelManufacturing = 18,
    PersonalServices = 19,
    FurnishingsAndFixturesAndAppliances = 20,
    RecreationalVehicles = 21,
    LuxuryGoods = 22,
    DepartmentStores = 23,
    TextileManufacturing = 24


class IndustrialsIndustryType(Enum):
    AerospaceAndDefense = 1,
    SpecialtyIndustrialMachinery = 2,
    Railroads = 3,
    BuildingProductsAndEquipment = 4,
    FarmAndHeavyConstructionMachinery = 5,
    SpecialtyBusinessServices = 6,
    IntegratedFreightAndLogistics = 7,
    WasteManagement = 8,
    Conglomerates = 9,
    EngineeringAndConstruction = 10,
    IndustrialDistribution = 11,
    RentalAndLeasingServices = 12,
    ConsultingServices = 13,
    ElectricalEquipmentAndParts = 14,
    Trucking = 15,
    Airlines = 16,
    ToolsAndAccessories = 17,
    PollutionAndTreatmentControls = 18,
    SecurityAndProtectionServices = 19,
    MarineShipping = 20,
    MetalFabrication = 21,
    InfrastructureOperations = 22,
    StaffingAndEmploymentServices = 23,
    AirportsAndAirServices = 24,
    BusinessEquipmentAndSupplies = 25


class CommunicationServicesIndustryType(Enum):
    InternetContentAndInformation = 1,
    TelecomServices = 2,
    Entertainment = 3,
    ElectronicGamingAndMultimedia = 4,
    AdvertisingAgencies = 5,
    Publishing = 6,
    Broadcasting = 7


class ConsumerDefensiveIndustryType(Enum):
    DiscountStores = 1,
    BeveragesNonAlcoholic = 2,
    HouseholdAndPersonalProducts = 3,
    PackagedFoods = 4,
    Tobacco = 5,
    Confectioners = 6,
    FarmProducts = 7,
    FoodDistribution = 8,
    GroceryStores = 9,
    BeveragesBrewers = 10,
    EducationAndTrainingServices = 11,
    BeveragesWineriesAndDistilleries = 12


class EnergyIndustryType(Enum):
    OilAndGasIntegrated = 1,
    OilAndGasMidstream = 2,
    OilAndGasEAndP = 3,
    OilAndGasEquipmentAndServices = 4,
    OilAndGasRefiningAndMarketing = 5,
    Uranium = 6,
    OilAndGasDrilling = 7,
    ThermalCoal = 8


class RealEstateIndustryType(Enum):
    REITSpecialty = 1,
    REITIndustrial = 2,
    REITRetail = 3,
    REITResidential = 4,
    REITHealthcareFacilities = 5,
    RealEstateServices = 6,
    REITOffice = 7,
    REITDiversified = 8,
    REITMortgage = 9,
    REITHotelAndMotel = 10,
    RealEstateDevelopment = 11,
    RealEstateDiversified = 12


class BasicMaterialsIndustryType(Enum):
    SpecialtyChemicals = 1,
    Gold = 2,
    BuildingMaterials = 3,
    Copper = 4,
    Steel = 5,
    AgriculturalInputs = 6,
    Chemicals = 7,
    OtherIndustrialMetalsAndMining = 8,
    LumberAndWoodProduction = 9,
    OtherPreciousMetalsAndMining = 10,
    Aluminum = 11,
    CokingCoal = 12,
    PaperAndPaperProducts = 13,
    Silver = 14


class UtilsIndustryType(Enum):
    UtilitiesRegulatedElectric = 1,
    UtilitiesRenewable = 2,
    UtilitiesDiversified = 3,
    UtilitiesRegulatedGas = 4,
    UtilitiesIndependentPowerProducers = 5,
    UtilitiesRegulatedWater = 6
