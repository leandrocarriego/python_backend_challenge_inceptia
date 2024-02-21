from dataclasses import dataclass

import pandas as pd


_PRODUCT_DF = pd.DataFrame({
        "product_name": ["Chocolate", "Granizado", "Limon", "Dulce de Leche"],
         "quantity": [3, 10, 0, 5]
    })

'''
Considero que quedo demasiado compleja esta solución, 
me hubiese gustado que quede mas 'limpia'
pero no me quedaba claro si debía mantener la devolución como booleana o no,
ya que decía "Reformule la función para solucionar este problema."

Tampoco se si la solución elegida seria la mas adecuada o esperada, 
ya que es necesaria logica extra para manejar la respuesta de la función.

Opte por hacer que la función devuelva un objeto Response, que tiene la respuesta booleana 'is_available',
un mensaje según el error de ingreso, 
el atributo 'product_stock' por si se solicita mas cantidad de la disponible (y poder aclararlo en la respuesta)
y el atributo 'products_in_stock', que sirve para listar los productos disponibles
en caso de que el producto ingresado no exista.
'''

@dataclass
class Response:
    is_available: bool = False
    message: str = None
    product_stock: int = None
    products_in_stock: list[dict[str, str | int]] = None


def is_product_available(product_name: str, quantity: float) -> Response | str:

    response = Response()

    try:
        # Valida si el usuario ingresa menos de 1
        if quantity <= 0:
            response.message = 'La cantidad mínima es 1.'
            return response

        for index, row in _PRODUCT_DF.iterrows():
            current_stock: int = row['quantity']

            # Valida si el producto solicitado existe
            if row['product_name'] == product_name:

                # Si hay stock y la cantidad solicitad no es mayor al stock se devuelve True
                if current_stock > 0 and quantity <= current_stock:
                    response.is_available = True
                    return response

                elif current_stock <= 0:
                    response.message = f'No hay stock disponible de {product_name}'
                    response.product_stock = 0
                    return response

                else:
                    response.message = (f'La cantidad ingresada excede el stock actual.\n'
                                        f'Solo hay disponibles {current_stock} del producto "{product_name}".')
                    response.product_stock = current_stock
                    return response

        # Se filtran los productos que tienen stock
        products_in_stock = _PRODUCT_DF[_PRODUCT_DF['quantity'] > 0]

        response.message = 'El producto solicitado no existe.'
        response.products_in_stock = products_in_stock.to_dict(orient='records')

        return response

    except Exception as e:
        return f'Error: {e}'


# Ejemplo de uso
'''
# Producto no existente
product_response = is_product_available(product_name="TEST", quantity=1)

# Producto sin stock
#product_response = is_product_available(product_name="Limon", quantity=1)

# Cantidad solicitada mayor al stock disponible
#product_response = is_product_available(product_name="Chocolate", quantity=4)

# Cantidad ingresada menor a 1
#product_response = is_product_available(product_name="Granizado", quantity=0)

if product_response.is_available:
    print(product_response.is_available)
    pass  # Aca pasaría a pedirle el código de descuento según el diagrama

else:
    print(product_response.message)

    # Si el listado de productos es True es porque el producto no existe y ofrece los que hay
    if product_response.products_in_stock:
        print('Selecciona uno de los siguientes productos:\n')

        for product_info in product_response.products_in_stock:
            name = product_info["product_name"]
            stock = product_info["quantity"]

            print(f'{name} - stock disponible: {stock}')
'''