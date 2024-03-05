import pytest

from models import Product
from models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(500)
        assert product.quantity == 500
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    def test_add_product(self, cart, product):
        assert len(cart.products) == 0
        cart.add_product(product)
        assert len(cart.products) == 1
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=20)
        assert cart.products[product] == 21

    def test_remove_product(self, cart, product):
        cart.add_product(product, buy_count=3)
        assert cart.products[product] == 3

        cart.remove_product(product, remove_count=1)
        assert cart.products[product] == 2

        cart.remove_product(product, remove_count=3)
        assert product not in cart.products

        cart.add_product(product)
        cart.remove_product(product, remove_count=1)
        assert product not in cart.products

        cart.add_product(product, buy_count=2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        assert product not in cart.products
        cart.clear()
        assert product not in cart.products

        cart.add_product(product)
        assert product in cart.products
        cart.clear()
        assert product not in cart.products

    def test_total_price(self, cart, product):
        assert product not in cart.products
        assert cart.get_total_price() is None

        cart.add_product(product, buy_count=10)
        assert cart.get_total_price() == product.price * 10

    def test_buy(self, cart, product):
        assert product not in cart.products
        cart.buy()
        assert product.quantity == 1000

        cart.add_product(product)
        cart.buy()
        assert product.quantity == 999

        cart.add_product(product, buy_count=1000)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 999
