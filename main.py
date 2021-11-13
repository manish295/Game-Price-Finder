from stores import Stores
import traceback

prices = {}

game1 = Stores("Assassin's Creed Unity")
try:
    print("Epic Games:", game1.epic_games())
    
    prices["Epic Games"] = game1.epic_games()
except:
    traceback.print_exc()


try:
    print("Steam:", game1.steam())
except:
    traceback.print_exc()


try:
    print("Humble Store:", game1.humble_store())
except:
    traceback.print_exc()

try: 
    print("Ubisoft Store:", game1.ubi_store())
    prices["Ubisoft Store"] = game1.ubi_store()

except:
    traceback.print_exc()

try:
    print("Fanatical: ", game1.fanatical())
    prices["Fanatical"] = game1.fanatical()
except:
    traceback.print_exc()

game1.shut_down()

