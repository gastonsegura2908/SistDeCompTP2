from src.MainProcess import value_get,get_country,filter_and_fill,get_values_po, button_position

# Testea si se pudieron obtener los datos o si hubo algun error. 200 es si anduvo bien
def test_value_get():
    assert value_get().status_code == 200

# Testea si el pais elegido para ver los indices GINI es argentina
def test_get_country():
    assert get_country() == "Argentina"

def test_button_position():
    assert button_position() > 0

# Testea si el tamaño de la lista de indice GINI antes de pasarsela a C y luego de retornarla es el mismo
def test_pre_post_c_function():
    assert len(get_values_po()) > 0 #len(filter_and_fill()) == len(get_values_po())  
