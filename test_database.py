import pytest
from database import ProductDatabase, SupplierDatabase, Product, Supplier
from config import Config


class TestProductDatabase:
    def test_find_product_by_name(self):
        product = ProductDatabase.find_product_by_name("Беспроводные наушники")
        assert product is not None
        assert isinstance(product, Product)
        assert product.name == "Беспроводные наушники"

        product = ProductDatabase.find_product_by_name("Смарт-часы")
        assert product is not None
        assert isinstance(product, Product)
        assert product.name == "Смарт-часы"

        product = ProductDatabase.find_product_by_name("наушники")
        assert product is not None

        product = ProductDatabase.find_product_by_name("БЕСПРОВОДНЫЕ НАУШНИКИ")
        assert product is not None

        product = ProductDatabase.find_product_by_name("Некоторый несуществующий продукт")
        assert product is None

    def test_generate_supplier_prices(self):
        product = ProductDatabase.find_product_by_name("Беспроводные наушники")
        assert product is not None

        suppliers = ProductDatabase.generate_supplier_prices(product, Config)
        assert len(suppliers) > 0

        for supplier in suppliers:
            assert "id" in supplier
            assert "name" in supplier
            assert "country" in supplier

            assert isinstance(supplier["price_usd"], float)
            assert isinstance(supplier["price_rub"], float)
            assert isinstance(supplier["final_price_usd"], float)
            assert isinstance(supplier["final_price_rub"], float)

            assert supplier["price_usd"] > 0
            assert supplier["price_rub"] > 0
            assert supplier["final_price_usd"] > 0
            assert supplier["final_price_rub"] > 0

            assert supplier["delivery_cost_percent"] >= 0
            assert supplier["delivery_cost_rub"] >= 0
            assert supplier["storage_cost_percent"] >= 0
            assert supplier["storage_cost_rub"] >= 0
            assert supplier["additional_costs_percent"] >= 0
            assert supplier["additional_costs_rub"] >= 0

    def test_generate_product_code(self):
        product = ProductDatabase.find_product_by_name("Беспроводные наушники")
        assert product is not None

        suppliers = ProductDatabase.generate_supplier_prices(product, Config)
        assert len(suppliers) > 0

        product_code = ProductDatabase.generate_product_code(product, suppliers[0])
        assert isinstance(product_code, str)
        assert len(product_code) > 0


class TestSupplierDatabase:
    def test_get_all_suppliers(self):
        suppliers = SupplierDatabase.get_all_suppliers()
        assert len(suppliers) > 0

        for supplier in suppliers:
            assert isinstance(supplier, Supplier)
            assert supplier.id is not None
            assert supplier.name is not None
            assert supplier.country is not None

    def test_supplier_attributes(self):
        suppliers = SupplierDatabase.get_all_suppliers()
        assert len(suppliers) > 0

        first_supplier = suppliers[0]
        assert hasattr(first_supplier, "id")
        assert hasattr(first_supplier, "name")
        assert hasattr(first_supplier, "full_name")
        assert hasattr(first_supplier, "region")
        assert hasattr(first_supplier, "country")
        assert hasattr(first_supplier, "url")
        assert hasattr(first_supplier, "tax_id")
        assert hasattr(first_supplier, "warehouse_location")
        assert hasattr(first_supplier, "status")
        assert hasattr(first_supplier, "rating")
        assert hasattr(first_supplier, "delivery_time")
        assert hasattr(first_supplier, "min_order_value")


class TestConfig:
    def test_config_validation(self):
        errors = Config.validate()

        if len(errors) > 0:
            print(f"Configuration errors: {errors}")

    def test_config_is_valid(self):
        is_valid = Config.is_valid()
        assert isinstance(is_valid, bool)

    def test_config_constants(self):
        assert Config.MAX_PRODUCTS_PER_REQUEST > 0
        assert Config.MIN_SEARCH_TEXT_LENGTH > 0
        assert Config.MAX_SUPPLIERS_PER_PRODUCT > 0
        assert Config.USD_TO_RUB_EXCHANGE_RATE > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])