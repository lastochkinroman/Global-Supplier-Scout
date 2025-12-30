import asyncio
from typing import List, Dict, Any
from groq import Groq
from config import Config

class GroqAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL
        self.temperature = Config.GROQ_TEMPERATURE

    async def analyze_product_suppliers(self, product: Dict[str, Any], suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            sorted_suppliers = sorted(suppliers, key=lambda x: x["final_price_usd"])

            supplier_info = []
            for i, supplier in enumerate(sorted_suppliers[:5], 1):
                supplier_info.append(
                    f"{i}. {supplier['name']} ({supplier['country']}): "
                    f"${supplier['final_price_usd']:.2f}, "
                    f"Rating: {supplier['rating']}/5, "
                    f"Lead Time: {supplier['lead_time']}, "
                    f"MOQ: ${supplier['moq']}"
                )

            system_prompt = """Вы эксперт в международной торговле и анализе поставщиков.
            Ваша задача - анализировать поставщиков товаров для e-commerce и предоставлять действенные insights.

            Анализируйте каждого поставщика по:
            1. Конкурентоспособность цены
            2. Время доставки и надежность
            3. Репутация поставщика (рейтинг)
            4. Минимальные требования к заказу
            5. Географические преимущества/недостатки
            6. Общая оценка рисков

            Предоставляйте рекомендации в структурированном формате."""

            user_prompt = f"""Пожалуйста, проанализируйте поставщиков для следующего товара:

            ТОВАР: {product['name']}
            КАТЕГОРИЯ: {product['category']}
            БАЗОВЫЙ ДИАПАЗОН ЦЕН: ${product['base_price_usd']:.2f}

            ТОП ПОСТАВЩИКИ:
            {' | '.join(supplier_info)}

            Пожалуйста, предоставьте:
            1. ЛУЧШИЙ ВЫБОР: Какой поставщик предлагает лучшую ценность?
            2. БЮДЖЕТНЫЙ ВАРИАНТ: Лучший вариант для низкого бюджета?
            3. ПРЕМИУМ ВАРИАНТ: Лучший для качества/надежности?
            4. ОЦЕНКА РИСКОВ: Есть ли красные флаги?
            5. РЕКОМЕНДАЦИЯ: Общая рекомендация с обоснованием.

            Форматируйте ответ четко с маркерами и эмодзи."""

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

            stats = {
                "total_suppliers_analyzed": len(sorted_suppliers),
                "price_range_usd": f"${sorted_suppliers[0]['final_price_usd']:.2f} - ${sorted_suppliers[-1]['final_price_usd']:.2f}",
                "average_rating": sum(s['rating'] for s in sorted_suppliers[:5]) / 5,
                "best_supplier": sorted_suppliers[0]['name'],
                "best_price_usd": sorted_suppliers[0]['final_price_usd'],
                "worst_supplier": sorted_suppliers[-1]['name'],
                "worst_price_usd": sorted_suppliers[-1]['final_price_usd']
            }

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

    async def analyze_multiple_products(self, products_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

        formatted = f"""
📦 **{product_name.upper()} - АНАЛИЗ ПОСТАВЩИКОВ**

{analysis_text}

📊 **БЫСТРАЯ СТАТИСТИКА:**
• Поставщики проанализированы: {stats.get('total_suppliers_analyzed', 'N/A')}
• Диапазон цен: {stats.get('price_range_usd', 'N/A')}
• Средний рейтинг: {stats.get('average_rating', 'N/A'):.1f}/5
• Лучшая цена: ${stats.get('best_price_usd', 'N/A'):.2f} ({stats.get('best_supplier', 'N/A')})

💡 **СЛЕДУЮЩИЕ ШАГИ:**
1. Свяжитесь с топ 3 поставщиками для образцов
2. Обсудите лучшие условия MOQ
3. Запросите сертификаты продукта
4. Проверьте стоимость доставки
        """

        return formatted

groq_analyzer = GroqAnalyzer()
