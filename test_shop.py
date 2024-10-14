"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product_2():
    return Product("pen", 150, "This is a pen", 500)

@pytest.fixture
def empty_cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_available_count(self, product):
        assert product.check_quantity(500) == True

    def test_product_check_quantity_unavailable_count(self, product):
        assert product.check_quantity(1500) == False

    def test_product_buy(self, product):
        product.buy(400)
        assert product.quantity == 600

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError) as error:
            product.buy(1200)
        assert str(error.value) == "Продукта недостаточно"


class TestCart:
    def test_add_product(self, empty_cart, product):
        empty_cart.add_product(product, 1)
        assert empty_cart.products[product] == 1
        empty_cart.add_product(product, 3)
        assert empty_cart.products[product] == 4

    def test_remove_product(self, empty_cart, product):
        empty_cart.add_product(product, 2)
        empty_cart.remove_product(product, 1)
        assert empty_cart.products[product] == 1

    def test_remove_product_all(self, empty_cart, product):
        empty_cart.add_product(product, 2)
        empty_cart.remove_product(product)
        assert empty_cart.products == {}

    def test_remove_different_product(self, empty_cart, product, product_2):
        empty_cart.add_product(product, 2)
        with pytest.raises(ValueError) as error:
            empty_cart.remove_product(product_2)
        assert str(error.value) == "Продукта нет в корзине"

    def test_clear(self, empty_cart, product):
        empty_cart.add_product(product, 2)
        empty_cart.clear(product)
        assert empty_cart.products == {}

    def test_clear_different_product(self, empty_cart, product, product_2):
        empty_cart.add_product(product, 2)
        with pytest.raises(ValueError) as error:
            empty_cart.clear(product_2)
        assert str(error.value) == "Продуктов нет в корзине"

    def test_get_total_price(self, empty_cart, product, product_2):
        empty_cart.add_product(product, 2)
        empty_cart.add_product(product_2, 5)
        total_price = product.price * 2 + product_2.price * 5
        assert empty_cart.get_total_price() == total_price

    def test_buy(self, empty_cart, product):
        empty_cart.add_product(product, 100)
        empty_cart.buy()
        assert product.quantity == 900
        assert empty_cart.products == {}

    def test_buy_more_than_possible(self, empty_cart, product):
        empty_cart.add_product(product, 1100)
        with pytest.raises(ValueError) as error:
            empty_cart.buy()
        assert str(error.value) == "Товара недостаточно"