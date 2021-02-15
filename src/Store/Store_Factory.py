from Store.Pccom import Pccomponentes
from Store.Corteingles import Elcorteingles
from Store.Mediamarkt import Mediamarkt 

def get_store(store, driver, logger):
    if store == 'pccomponentes':
        return Pccomponentes(driver, logger)
    elif store == 'elcorteingles':
        return Elcorteingles(driver, logger)
    elif store == 'mediamarkt':
        return Mediamarkt(driver, logger)
    else:
        raise Exception("Store not supported yet!")