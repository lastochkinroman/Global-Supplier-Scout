import asyncio
from typing import List, Dict, Any
from groq import Groq
from config import Config


class GroqAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL
        self.temperature = Config.GROQ_TEMPERATURE

    async def analyze_product_suppliers(
        self,
        product: Dict[str, Any],
        suppliers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            sorted_suppliers = sorted(suppliers, key=lambda x: x["final_price_usd"])
            supplier_info = self._format_supplier_info(sorted_suppliers)

            system_prompt = self._get_system_prompt()
            user_prompt = self._get_user_prompt(product, supplier_info)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=600
            )

            analysis = response.choices[0].message.content.strip()
            stats = self._calculate_statistics(sorted_suppliers)

            return {
                "product_name": product["name"],
                "analysis": analysis,
                "statistics": stats,
                "top_suppliers": sorted_suppliers[:3]
            }

        except Exception as e:
            print(f"Groq analysis error: {e}")
            return {
                "product_name": product["name"],
                "analysis": "Не удалось сгенерировать анализ в данный момент.",
                "statistics": {},
                "top_suppliers": []
            }

    async def analyze_multiple_products(
        self,
        products_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        analyses = []

        for product_data in products_data:
            try:
                analysis = await self.analyze_product_suppliers(
                    product_data["product"],
                    product_data["suppliers"]
                )
                analyses.append(analysis)

                await asyncio.sleep(0.5)

            except Exception as e:
                print(f"Error analyzing product {product_data['product']['name']}: {e}")
                analyses.append({
                    "product_name": product_data["product"]["name"],
                    "analysis": "Анализ не удался.",
                    "statistics": {},
                    "top_suppliers": []
                })

        return analyses

    def format_analysis_for_telegram(self, analysis: Dict[str, Any]) -> str:
        product_name = analysis["product_name"]
        analysis_text = analysis["analysis"]
        stats = analysis["statistics"]

        formatted = (
            f"\n📦 **{product_name.upper()} - АНАЛИЗ ПОСТАВЩИКОВ**\n\n"
            f"{analysis_text}\n\n"
            "📊 **БЫСТРАЯ СТАТИСТИКА:**\n"
            f"• Поставщики проанализированы: {stats.get('total_suppliers_analyzed', 'N/A')}\n"
            f"• Диапазон цен: {stats.get('price_range_usd', 'N/A')}\n"
            f"• Средний рейтинг: {stats.get('average_rating', 'N/A'):.1f}/5\n"
            f"• Лучшая цена: ${stats.get('best_price_usd', 'N/A'):.2f} "
            f"({stats.get('best_supplier', 'N/A')})\n\n"
            "💡 **СЛЕДУЮЩИЕ ШАГИ:**\n"
            "1. Свяжитесь с топ 3 поставщиками для образцов\n"
            "2. Обсудите лучшие условия MOQ\n"
            "3. Запросите сертификаты продукта\n"
            "4. Проверьте стоимость доставки"
        )

        return formatted

    def _format_supplier_info(self, suppliers: List[Dict[str, Any]]) -> List[str]:
        supplier_info = []
        for i, supplier in enumerate(suppliers[:5], 1):
            supplier_info.append(
                f"{i}. {supplier['name']} ({supplier['country']}): "
                f"${supplier['final_price_usd']:.2f}, "
                f"Rating: {supplier['rating']}/5, "
                f"Lead Time: {supplier['lead_time']}, "
                f"MOQ: ${supplier['moq']}"
            )
        return supplier_info

    def _get_system_prompt(self) -> str:
        return """Вы эксперт в международной торговле и анализе поставщиков.
        Ваша задача - анализировать поставщиков товаров для e-commerce и предоставлять действенные insights.

        Анализируйте каждого поставщика по:
        1. Конкурентоспособность цены
        2. Время доставки и надежность
        3. Репутация поставщика (рейтинг)
        4. Минимальные требования к заказу
        5. Географические преимущества/недостатки
        6. Общая оценка рисков

        Предоставляйте рекомендации в структурированном формате."""

    def _get_user_prompt(
        self,
        product: Dict[str, Any],
        supplier_info: List[str]
    ) -> str:
        return (
            f"Пожалуйста, проанализируйте поставщиков для следующего товара:\n\n"
            f"ТОВАР: {product['name']}\n"
            f"КАТЕГОРИЯ: {product['category']}\n"
            f"БАЗОВЫЙ ДИАПАЗОН ЦЕН: ${product['base_price_usd']:.2f}\n\n"
            f"ТОП ПОСТАВЩИКИ:\n{' | '.join(supplier_info)}\n\n"
            "Пожалуйста, предоставьте:\n"
            "1. ЛУЧШИЙ ВЫБОР: Какой поставщик предлагает лучшую ценность?\n"
            "2. БЮДЖЕТНЫЙ ВАРИАНТ: Лучший вариант для низкого бюджета?\n"
            "3. ПРЕМИУМ ВАРИАНТ: Лучший для качества/надежности?\n"
            "4. ОЦЕНКА РИСКОВ: Есть ли красные флаги?\n"
            "5. РЕКОМЕНДАЦИЯ: Общая рекомендация с обоснованием.\n\n"
            "Форматируйте ответ четко с маркерами и эмодзи."
        )

    def _calculate_statistics(self, suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        top_5_suppliers = suppliers[:5]
        return {
            "total_suppliers_analyzed": len(suppliers),
            "price_range_usd": (
                f"${suppliers[0]['final_price_usd']:.2f} - "
                f"${suppliers[-1]['final_price_usd']:.2f}"
            ),
            "average_rating": sum(s['rating'] for s in top_5_suppliers) / 5,
            "best_supplier": suppliers[0]['name'],
            "best_price_usd": suppliers[0]['final_price_usd'],
            "worst_supplier": suppliers[-1]['name'],
            "worst_price_usd": suppliers[-1]['final_price_usd']
        }


groq_analyzer = GroqAnalyzer()