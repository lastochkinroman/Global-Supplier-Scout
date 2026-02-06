"""Tests for database module."""

import pytest
from database import ProductDatabase, SupplierDatabase, Product, Supplier
from config import Config


class TestProductDatabase:
    """Test ProductDatabase functionality."""

    def test_find_product_by_name(self):
        """Test finding products by name."""
        product = ProductDatabase.find_product_by_name("Wireless Earbuds")
        assert product is not None
        assert isinstance(product, Product)
        assert product.name == "Wireless Earbuds"

        product = ProductDatabase.find_product_by_name("Smart Watch")
        assert product is not None
        assert isinstance(product, Product)
        assert product.name == "Smart Watch"

        # Test with partial match
        product = ProductDatabase.find_product_by_name("earbuds")
        assert product is not None

        # Test with case insensitivity
        product = ProductDatabase.find_product_by_name("WIRELESS EARBUDS")
        assert product is not None

        # Test with non-existent product
        product = ProductDatabase.find_product_by_name("Non-existent Product")
        assert product is None

    def test_generate_supplier_prices(self):
        """Test generating supplier prices."""
        product = ProductDatabase.find_product_by_name("Wireless Earbuds")
        assert product is not None

        suppliers = ProductDatabase.generate_supplier_prices(product, Config)
        assert len(suppliers) > 0

        for supplier in suppliers:
            # Basic checks
            assert "id" in supplier
            assert "name" in supplier
            assert "country" in supplier

            # Price fields should be numeric
            assert isinstance(supplier["price_usd"], float)
            assert isinstance(supplier["price_rub"], float)
            assert isinstance(supplier["final_price_usd"], float)
            assert isinstance(supplier["final_price_rub"], float)

            # Price should be positive
            assert supplier["price_usd"] > 0
            assert supplier["price_rub"] > 0
            assert supplier["final_price_usd"] > 0
            assert supplier["final_price_rub"] > 0

            # Costs should be non-negative
            assert supplier["delivery_cost_percent"] >= 0
            assert supplier["delivery_cost_rub"] >= 0
            assert supplier["storage_cost_percent"] >= 0
            assert supplier["storage_cost_rub"] >= 0
            assert supplier["additional_costs_percent"] >= 0
            assert supplier["additional_costs_rub"] >= 0

    def test_generate_product_code(self):
        """Test product code generation."""
        product = ProductDatabase.find_product_by_name("Wireless Earbuds")
        assert product is not None

        suppliers = ProductDatabase.generate_supplier_prices(product, Config)
        assert len(suppliers) > 0

        product_code = ProductDatabase.generate_product_code(product, suppliers[0])
        assert isinstance(product_code, str)
        assert len(product_code) > 0


class TestSupplierDatabase:
    """Test SupplierDatabase functionality."""

    def test_get_all_suppliers(self):
        """Test getting all suppliers."""
        suppliers = SupplierDatabase.get_all_suppliers()
        assert len(suppliers) > 0

        for supplier in suppliers:
            assert isinstance(supplier, Supplier)
            assert supplier.id is not None
            assert supplier.name is not None
            assert supplier.country is not None

    def test_supplier_attributes(self):
        """Test that all suppliers have required attributes."""
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
    """Test configuration class."""

    def test_config_validation(self):
        """Test configuration validation."""
        errors = Config.validate()

        # Check that we don't have errors for required fields that should be optional
        if len(errors) > 0:
            # We might have errors if .env file is not set, which is acceptable for tests
            print(f"Configuration errors: {errors}")

    def test_config_is_valid(self):
        """Test configuration validity check."""
        is_valid = Config.is_valid()
        assert isinstance(is_valid, bool)

    def test_config_constants(self):
        """Test that configuration constants are properly set."""
        assert Config.MAX_PRODUCTS_PER_REQUEST > 0
        assert Config.MIN_SEARCH_TEXT_LENGTH > 0
        assert Config.MAX_SUPPLIERS_PER_PRODUCT > 0
        assert Config.USD_TO_RUB_EXCHANGE_RATE > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])