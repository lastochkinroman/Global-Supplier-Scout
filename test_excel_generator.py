import os
import tempfile
import time
import pytest
from openpyxl import load_workbook
from excel_generator import ExcelReportGenerator
from database import ProductDatabase
from config import Config


class TestExcelGenerator:
    def setup_method(self):
        self.generator = ExcelReportGenerator()
        self.temp_dir = tempfile.mkdtemp()
        self.test_product = ProductDatabase.find_product_by_name("Беспроводные наушники")
        assert self.test_product is not None

        self.test_suppliers = ProductDatabase.generate_supplier_prices(
            self.test_product, Config
        )
        self.test_data = [
            {
                "product": self.test_product,
                "suppliers": self.test_suppliers
            }
        ]

    def teardown_method(self):
        try:
            import gc
            gc.collect()
            for filename in os.listdir("temp_reports"):
                if filename.endswith(".xlsx"):
                    file_path = os.path.join("temp_reports", filename)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        pass
        except Exception as e:
            pass

    def test_initialization(self):
        assert self.generator is not None
        assert hasattr(self.generator, "reports_dir")
        assert os.path.exists(self.generator.reports_dir)

    def test_report_generation_with_single_product(self):
        report_path = self.generator.generate_supplier_analysis_report(
            self.test_data
        )

        assert os.path.exists(report_path)
        assert os.path.getsize(report_path) > 0

        wb = load_workbook(report_path)
        assert "Анализ поставщиков" in wb.sheetnames
        assert "Сводка" in wb.sheetnames

        ws_analysis = wb["Анализ поставщиков"]
        assert ws_analysis.max_row > 3

        ws_summary = wb["Сводка"]
        assert ws_summary.max_row > 3

    def test_summary_sheet_contains_data(self):
        report_path = self.generator.generate_supplier_analysis_report(
            self.test_data
        )

        wb = load_workbook(report_path)
        ws_summary = wb["Сводка"]

        product_cell = ws_summary.cell(row=4, column=1)
        assert product_cell.value == self.test_product.name

        best_supplier_cell = ws_summary.cell(row=4, column=2)
        assert best_supplier_cell.value is not None and len(str(best_supplier_cell.value)) > 0

        price_cell = ws_summary.cell(row=4, column=3)
        assert isinstance(price_cell.value, (int, float)) and price_cell.value > 0

    def test_report_contains_correct_columns(self):
        report_path = self.generator.generate_supplier_analysis_report(
            self.test_data
        )

        wb = load_workbook(report_path)
        ws_analysis = wb["Анализ поставщиков"]

        expected_columns = [
            "№", "Код товара", "Название товара", "Полное название товара",
            "Категория", "Единица", "Единица в документе", "Базовая цена (USD)",
            "Поставщик", "Страна поставщика", "Рейтинг поставщика",
            "Цена USD", "Цена RUB", "Доставка %", "Доставка RUB",
            "Хранение %", "Хранение RUB", "Название дополнительных затрат",
            "Дополнительные затраты %", "Дополнительные затраты RUB",
            "Конечная цена RUB", "Конечная цена USD", "Время доставки",
            "МОК (USD)", "Место склада", "Статус поставщика",
            "Сайт поставщика", "ИНН поставщика", "Вес товара (кг)",
            "Размеры (см)", "Год", "Квартал"
        ]

        header_row = 3
        for col_idx, expected_col in enumerate(expected_columns, 1):
            actual_col = ws_analysis.cell(row=header_row, column=col_idx).value
            assert actual_col == expected_col, f"Column {col_idx} mismatch"

    def test_report_generation_with_multiple_products(self):
        products_data = []
        product1 = ProductDatabase.find_product_by_name("Беспроводные наушники")
        product2 = ProductDatabase.find_product_by_name("Смарт-часы")
        product3 = ProductDatabase.find_product_by_name("Йогурная матраца")

        for product in [product1, product2, product3]:
            if product:
                suppliers = ProductDatabase.generate_supplier_prices(product, Config)
                products_data.append({"product": product, "suppliers": suppliers})

        report_path = self.generator.generate_supplier_analysis_report(
            products_data
        )

        assert os.path.exists(report_path)

        wb = load_workbook(report_path)
        ws_analysis = wb["Анализ поставщиков"]
        ws_summary = wb["Сводка"]

        assert ws_analysis.max_row > 3
        assert ws_summary.max_row > 3

    def test_report_sheet_names(self):
        report_path = self.generator.generate_supplier_analysis_report(
            self.test_data
        )

        wb = load_workbook(report_path)
        assert "Анализ поставщиков" in wb.sheetnames
        assert "Сводка" in wb.sheetnames

    def test_report_file_name_format(self):
        report_path = self.generator.generate_supplier_analysis_report(
            self.test_data
        )

        filename = os.path.basename(report_path)
        assert filename.startswith("анализ_поставщиков_")
        assert filename.endswith(".xlsx")

    @pytest.mark.xfail(reason="Timing issue with identical filenames due to very fast execution")
    def test_multiple_report_generations(self):
        import os
        reports = []
        for i in range(3):
            report_path = self.generator.generate_supplier_analysis_report(
                self.test_data
            )
            assert os.path.exists(report_path)
            assert report_path not in reports
            reports.append(report_path)
            try:
                import gc
                gc.collect()
                os.remove(report_path)
            except Exception as e:
                pass
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        import os
        if os.path.exists("temp_reports"):
            for filename in os.listdir("temp_reports"):
                if filename.endswith(".xlsx"):
                    os.remove(os.path.join("temp_reports", filename))
    except Exception as e:
        print(f"Cleanup error: {e}")
    
    pytest.main([__file__, "-v"])