import pytest

from ..main.building import *

class TestBuilding:
    
    # Building tests ==================================================
    @pytest.yield_fixture(autouse=True)    
    def new_building(self):
        newBuilding = Building("colvin-1-floor", ["colvin", "colvin apartment"], 6, 6)
        return newBuilding
         
    def test_ID(self, new_building):
        assert new_building.buildingId == "colvin-1-floor"
    
    def test_nameList(self, new_building):
        names = ["colvin", "colvin apartment"]
        for i in range(len(names)):
            assert names[i] in new_building.nameList
    
    def test_numWashers(self, new_building):
        assert new_building.numWashers == 6
    
    def test_numDryers(self, new_building):
        assert new_building.numDryers == 6
    
    # ValueError tests ==================================================
    def test_noneBuilding(self):
        with pytest.raises(ValueError):
            noneBuilding = Building(None, None, None, None)
    
    def test_noneBuildingId(self):
        with pytest.raises(ValueError):
            noneBuilding = Building(None, ["colvin", "colvin apartments"], 6, 6)
            
    def test_noneBuildingNames(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", None, 6, 6)
            
    def test_noneBuildingWasher(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], None, 6)
            
    def test_noneBuildingDryer(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], 6, None)
    
    def test_negWashers(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], -1, 6)
             
    def test_negDryers(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], 6, -6)
    
    def test_nonIntWashers(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], '1', 6)
        
    def test_nonIntDryers(self):
        with pytest.raises(ValueError):
            noneBuilding = Building("colvin-1-floor", ["colvin", "colvin apartments"], 6, '6')
