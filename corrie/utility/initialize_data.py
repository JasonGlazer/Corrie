from corrie.utility.building_specifications import BuildingSpecification

class InitializeData(object):

    def __init__(self):
        self.buildings = self.populate_buildings()

    def populate_buildings(self):
        common_standards = ['90.1-2004', '90.1-2007', '90.1-2010', '90.1-2013']
        buildings = []
        buildings.append(BuildingSpecification('SecondarySchool', 'Secondary School', [], common_standards))
        buildings.append(BuildingSpecification('PrimarySchool', 'Primary School', [], common_standards))
        buildings.append(BuildingSpecification('SmallOffice', 'Small Office', [], common_standards))
        buildings.append(BuildingSpecification('MediumOffice', 'Medium Office', ['Retail Standalone','Warehouse'], common_standards))
        buildings.append(BuildingSpecification('LargeOffice', 'Large Office', ['Retail Standalone','Warehouse',], common_standards))
        buildings.append(BuildingSpecification('SmallHotel', 'Small Hotel', [], common_standards))
        buildings.append(BuildingSpecification('LargeHotel', 'Large Hotel', ['Retail Standalone',], common_standards))
        buildings.append(BuildingSpecification('Warehouse', 'Warehouse', [], common_standards))
        buildings.append(BuildingSpecification('RetailStandalone', 'Retail Standalone', [], common_standards))
        buildings.append(BuildingSpecification('RetailStripmall', 'Retail Stripmall', [], common_standards))
        buildings.append(BuildingSpecification('QuickServiceRestaurant', 'Quick Service Restaurant', ['Retail Standalone',], common_standards))
        buildings.append(BuildingSpecification('FullServiceRestaurant', 'Full Service Restaurant', ['Retail Standalone',], common_standards))
        buildings.append(BuildingSpecification('MidriseApartment', 'Midrise Apartment', [], common_standards))
        buildings.append(BuildingSpecification('HighriseApartment', 'Highrise Apartment', ['Retail Standalone',], common_standards))
        buildings.append(BuildingSpecification('Hospital', 'Hospital', [], common_standards))
        buildings.append(BuildingSpecification('Outpatient', 'Outpatient', [], common_standards))
        buildings.append(BuildingSpecification('SuperMarket', 'Supermarket', ['Quick Service Restaurant',], common_standards))
        # create a dictionary
        dict = {}
        for building in buildings:
            dict[building.display_string] = building
        return dict


