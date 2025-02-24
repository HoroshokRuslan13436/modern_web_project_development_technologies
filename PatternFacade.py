class Product:
    def __init__(self, name, price):
        if not name:
            raise ValueError("Некоректне ім'я товару!")
        if price <= 0:
            raise ValueError("Некоректна ціна товару!")
        self.name = name
        self.price = price


class Customer:
    def __init__(self, name, email):
        if not name:
            raise ValueError("Некоректне ім'я клієнта!")
        if not email:
            raise ValueError("Некоректний email клієнта!")
        self.name = name
        self.email = email


class PaymentProcessor:
    def process_payment(self, product, customer, amount, payment_method):
        print(f"Платіж у розмірі {amount} успішно оброблений за товар {product.name} від клієнта {customer.name}")


class Shipping:
    def ship_product(self, product, customer):
        print(f"Товар {product.name} успішно доставлений клієнту {customer.name}")


class OnlineStoreFacade:
    def __init__(self):
        self.payment_processor = PaymentProcessor()
        self.shipping = Shipping()

    def purchase_product(self, product, customer, payment_method):
        self.payment_processor.process_payment(product, customer, product.price, payment_method)
        self.shipping.ship_product(product, customer)


if __name__ == '__main__':
    product = Product("Телефон", 19000)
    customer = Customer("Іван", "ivan@gmail.com")
    payment_method = "Кредитна карта"

    facade = OnlineStoreFacade()
    facade.purchase_product(product, customer, payment_method)
