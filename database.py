import random
from typing import List, Dict, Any
import uuid
from datetime import datetime

class SupplierDatabase:
    SUPPLIERS = [
        {
            "id": "SUP001",
            "name": "Global Suppliers Inc.",
            "full_name": "Global Suppliers Incorporated",
            "region": "Global",
            "country": "International",
            "url": "https://globalsuppliers.com",
            "tax_id": "GSI-2024-001",
            "warehouse_location": "Multiple locations worldwide",
            "status": "Verified",
            "rating": 4.8,
            "delivery_time": "7-14 days",
            "min_order_value": 500
        },
        {
            "id": "SUP002",
            "name": "China Direct Trading",
            "full_name": "China Direct Trading Co., Ltd.",
            "region": "Guangdong",
            "country": "China",
            "url": "https://chinadirect.com",
            "tax_id": "CDT-CN-2024",
            "warehouse_location": "Shenzhen, China",
            "status": "Verified",
            "rating": 4.5,
            "delivery_time": "14-21 days",
            "min_order_value": 300
        },
        {
            "id": "SUP003",
            "name": "EuroQuality Goods",
            "full_name": "EuroQuality Goods GmbH",
            "region": "Bavaria",
            "country": "Germany",
            "url": "https://euroquality.de",
            "tax_id": "DE123456789",
            "warehouse_location": "Munich, Germany",
            "status": "Premium",
            "rating": 4.9,
            "delivery_time": "3-5 days",
            "min_order_value": 1000
        },
        {
            "id": "SUP004",
            "name": "US Wholesale Corp",
            "full_name": "US Wholesale Corporation",
            "region": "California",
            "country": "USA",
            "url": "https://uswholesale.com",
            "tax_id": "US-2024-WH",
            "warehouse_location": "Los Angeles, USA",
            "status": "Verified",
            "rating": 4.6,
            "delivery_time": "5-7 days",
            "min_order_value": 750
        },
        {
            "id": "SUP005",
            "name": "India Export Hub",
            "full_name": "India Export Hub Private Limited",
            "region": "Maharashtra",
            "country": "India",
            "url": "https://indiaexporthub.in",
            "tax_id": "IN-MH-2024",
            "warehouse_location": "Mumbai, India",
            "status": "Verified",
            "rating": 4.4,
            "delivery_time": "10-15 days",
            "min_order_value": 200
        },
        {
            "id": "SUP006",
            "name": "Turkey Textile Masters",
            "full_name": "Turkey Textile Masters A.Ş.",
            "region": "Istanbul",
            "country": "Turkey",
            "url": "https://turkeytextile.com",
            "tax_id": "TR-IST-2024",
            "warehouse_location": "Istanbul, Turkey",
            "status": "Premium",
            "rating": 4.7,
            "delivery_time": "7-10 days",
            "min_order_value": 400
        },
        {
            "id": "SUP007",
            "name": "Vietnam Manufacturing",
            "full_name": "Vietnam Manufacturing Joint Stock Company",
            "region": "Ho Chi Minh City",
            "country": "Vietnam",
            "url": "https://vietnammanufacturing.vn",
            "tax_id": "VN-HCM-2024",
            "warehouse_location": "Ho Chi Minh City, Vietnam",
            "status": "Verified",
            "rating": 4.3,
            "delivery_time": "12-18 days",
            "min_order_value": 250
        },
        {
            "id": "SUP008",
            "name": "Mexico Trade Center",
            "full_name": "Mexico Trade Center S.A. de C.V.",
            "region": "Mexico City",
            "country": "Mexico",
            "url": "https://mexicotrade.com.mx",
            "tax_id": "MX-MEX-2024",
            "warehouse_location": "Mexico City, Mexico",
            "status": "Verified",
            "rating": 4.2,
            "delivery_time": "8-12 days",
            "min_order_value": 350
        },
        {
            "id": "SUP009",
            "name": "Dubai Trading Group",
            "full_name": "Dubai Trading Group LLC",
            "region": "Dubai",
            "country": "UAE",
            "url": "https://dubaitrading.ae",
            "tax_id": "AE-DXB-2024",
            "warehouse_location": "Dubai, UAE",
            "status": "Premium",
            "rating": 4.8,
            "delivery_time": "4-7 days",
            "min_order_value": 600
        },
        {
            "id": "SUP010",
            "name": "Brazil Export Solutions",
            "full_name": "Brazil Export Solutions Ltda.",
            "region": "São Paulo",
            "country": "Brazil",
            "url": "https://brazilexport.com.br",
            "tax_id": "BR-SP-2024",
            "warehouse_location": "São Paulo, Brazil",
            "status": "Verified",
            "rating": 4.1,
            "delivery_time": "15-20 days",
            "min_order_value": 450
        }
    ]

class ProductDatabase:
    PRODUCTS = [
        {
            "id": "PROD001",
            "name": "Wireless Earbuds",
            "full_name": "Premium Wireless Bluetooth 5.0 Earbuds with Charging Case",
            "category": "Electronics",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 45.99,
            "weight_kg": 0.05,
            "dimensions_cm": "6x4x3"
        },
        {
            "id": "PROD002",
            "name": "Smart Watch",
            "full_name": "Smart Watch with Heart Rate Monitor and GPS",
            "category": "Electronics",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 89.99,
            "weight_kg": 0.08,
            "dimensions_cm": "4x4x1"
        },
        {
            "id": "PROD003",
            "name": "Yoga Mat",
            "full_name": "Premium Non-Slip Yoga Mat 183x61x0.6 cm",
            "category": "Fitness",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 24.99,
            "weight_kg": 1.2,
            "dimensions_cm": "183x61x6"
        },
        {
            "id": "PROD004",
            "name": "LED Desk Lamp",
            "full_name": "USB LED Desk Lamp with Adjustable Brightness",
            "category": "Home & Office",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 19.99,
            "weight_kg": 0.6,
            "dimensions_cm": "35x15x15"
        },
        {
            "id": "PROD005",
            "name": "Stainless Steel Bottle",
            "full_name": "Insulated Stainless Steel Water Bottle 750ml",
            "category": "Sports",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 29.99,
            "weight_kg": 0.35,
            "dimensions_cm": "25x8x8"
        },
        {
            "id": "PROD006",
            "name": "Portable Power Bank",
            "full_name": "10000mAh Portable Power Bank with Fast Charging",
            "category": "Electronics",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 34.99,
            "weight_kg": 0.22,
            "dimensions_cm": "10x6x2"
        },
        {
            "id": "PROD007",
            "name": "Phone Case",
            "full_name": "Shockproof Phone Case for iPhone 14/15",
            "category": "Accessories",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 12.99,
            "weight_kg": 0.03,
            "dimensions_cm": "16x8x1"
        },
        {
            "id": "PROD008",
            "name": "Bluetooth Speaker",
            "full_name": "Waterproof Portable Bluetooth Speaker",
            "category": "Electronics",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 39.99,
            "weight_kg": 0.45,
            "dimensions_cm": "12x12x6"
        },
        {
            "id": "PROD009",
            "name": "Fitness Tracker",
            "full_name": "Fitness Activity Tracker with Sleep Monitor",
            "category": "Fitness",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 49.99,
            "weight_kg": 0.02,
            "dimensions_cm": "4x2x1"
        },
        {
            "id": "PROD010",
            "name": "Backpack",
            "full_name": "Waterproof Laptop Backpack 15.6 Inch",
            "category": "Travel",
            "unit": "piece",
            "doc_unit": "piece",
            "base_price_usd": 44.99,
            "weight_kg": 0.8,
            "dimensions_cm": "45x30x15"
        }
    ]

    @staticmethod
    def find_product_by_name(product_name: str) -> Dict[str, Any]:
        product_name_lower = product_name.lower()

        for product in ProductDatabase.PRODUCTS:
            if (product_name_lower in product["name"].lower() or
                product_name_lower in product["full_name"].lower()):
                return product.copy()

        return None

    @staticmethod
    def generate_supplier_prices(product: Dict[str, Any], config) -> List[Dict[str, Any]]:
        suppliers_with_prices = []

        for supplier in SupplierDatabase.SUPPLIERS:
            supplier_copy = supplier.copy()

            price_variation = 0.85 + (random.random() * 0.35)

            base_price = product["base_price_usd"]
            supplier_price_usd = round(base_price * price_variation, 2)

            delivery_cost_percent = config.DEFAULT_DELIVERY_PERCENT + random.uniform(-1, 1)
            storage_cost_percent = config.DEFAULT_STORAGE_PERCENT
            additional_costs_percent = config.DEFAULT_ADDITIONAL_COSTS_PERCENT + random.uniform(-0.5, 0.5)

            usd_to_rub = 90
            price_rub = supplier_price_usd * usd_to_rub
            delivery_cost_rub = price_rub * (delivery_cost_percent / 100)
            storage_cost_rub = price_rub * (storage_cost_percent / 100)
            additional_costs_rub = price_rub * (additional_costs_percent / 100)

            final_price_rub = price_rub + delivery_cost_rub + storage_cost_rub + additional_costs_rub

            supplier_copy.update({
                "price_usd": supplier_price_usd,
                "price_rub": round(price_rub, 2),
                "delivery_cost_percent": round(delivery_cost_percent, 2),
                "delivery_cost_rub": round(delivery_cost_rub, 2),
                "storage_cost_percent": storage_cost_percent,
                "storage_cost_rub": round(storage_cost_rub, 2),
                "additional_costs_percent": round(additional_costs_percent, 2),
                "additional_costs_rub": round(additional_costs_rub, 2),
                "final_price_rub": round(final_price_rub, 2),
                "final_price_usd": round(final_price_rub / usd_to_rub, 2),
                "additional_costs_name": random.choice([
                    "Customs clearance",
                    "Insurance",
                    "Packaging",
                    "Documentation"
                ]),
                "moq": supplier["min_order_value"],
                "lead_time": supplier["delivery_time"]
            })

            suppliers_with_prices.append(supplier_copy)

        return suppliers_with_prices

    @staticmethod
    def generate_product_code(product: Dict[str, Any], supplier: Dict[str, Any]) -> str:
        now = datetime.now()
        date_str = now.strftime("%d.%m.%Y")

        region_codes = {
            "Global": "GL",
            "China": "CN",
            "Germany": "DE",
            "USA": "US",
            "India": "IN",
            "Turkey": "TR",
            "Vietnam": "VN",
            "Mexico": "MX",
            "UAE": "AE",
            "Brazil": "BR"
        }

        region_code = region_codes.get(supplier.get("country", ""), "XX")

        return f"MR_{region_code}_{supplier['id']}_{product['id']}_{date_str}"

supplier_db = SupplierDatabase()
product_db = ProductDatabase()
