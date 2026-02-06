import os
import asyncio
import logging
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from config import Config
from database import product_db, Product
from excel_generator import report_generator
from groq_analyzer import groq_analyzer

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
📊 **Бот Анализа Рынка Поставщиков**

Я помогаю анализировать поставщиков товаров для e-commerce.

**Как это работает:**
1. Отправьте мне названия товаров (через запятую)
2. Я проанализирую 10+ международных поставщиков для каждого
3. Сгенерирую подробный отчет Excel с ценами
4. Предоставлю AI рекомендации по поставщикам

**Примеры:**
`беспроводные наушники, смарт-часы, йогурная матраца`
`чехол для телефона, портативный аккумулятор, настольная лампа led`
`рюкзак, нержавеющая стальная бутылка, фитнес-трекер`

**Я анализирую:**
• Цены от разных стран
• Время доставки и МОК
• Рейтинги поставщиков и надежность
• Полные расчеты стоимости
• Оценка рисков

**Отправьте названия товаров, чтобы начать!**
    """

    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📋 **Использование Бота Анализа Рынка**

**Основные команды:**
/start - Приветственное сообщение и инструкции
/help - Это справочное сообщение
/examples - Примеры продуктов

**Как искать:**
• Отправьте названия товаров, разделенные запятыми
• Используйте распространенные названия товаров
• Будьте конкретны, когда нужно
• Максимум 5 продуктов за запрос

**Примеры поиска:**
• `беспроводные наушники, смарт-часы`
• `йогурная матраца, фитнес-трекер`
• `настольная лампа led, usb зарядное устройство`
• `рюкзак, нержавеющая стальная бутылка, чехол для телефона`

**Что вы получите:**
1. **Отчет Excel** с подробным анализом поставщиков
2. **AI Анализ** лучших поставщиков
3. **Сравнение цен** по странам
4. **Оценка рисков** для каждого поставщика
5. **Рекомендации** по переговорам

**Нужна помощь?** Просто отправьте названия товаров и я проведу исследование!
    """

    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def examples_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    examples_text = """
🎯 **Примеры продуктов для анализа:**

**Электроника:**
• Беспроводные наушники
• Смарт-часы
• Bluetooth колонка
• Портативный аккумулятор
• Настольная лампа LED

**Фитнес и спорт:**
• Йогурная матраца
• Фитнес-трекер
• Нержавеющая стальная бутылка
• Упругие резинки
• Смарт-весы

**Дом и офис:**
• Органайзер для письменного стола
• USB-хаб
• Беспроводной зарядный станция
• Настольный вентилятор
• Подставка для монитора

**Мода и аксессуары:**
• Рюкзак
• Чехол для телефона
• Солнечные очки
• Кошелек
• Ремень для часов

**Просто скопируйте и вставьте любой из них, чтобы начать анализ!**
    """

    await update.message.reply_text(examples_text, parse_mode=ParseMode.MARKDOWN)


async def handle_product_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    search_text = update.message.text.strip()

    if len(search_text) < Config.MIN_SEARCH_TEXT_LENGTH:
        await update.message.reply_text(
            "🔍 Пожалуйста, введите не менее 3 символов для поиска.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await update.message.reply_text(
        f"🔎 Поиск поставщиков для: *{search_text}*",
        parse_mode=ParseMode.MARKDOWN
    )

    product_names = [name.strip() for name in search_text.split(',')]
    product_names = [name for name in product_names if len(name) > 0][:Config.MAX_PRODUCTS_PER_REQUEST]

    if not product_names:
        await update.message.reply_text(
            "❌ Не найдены допустимые названия продуктов. Попробуйте еще раз.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    found_products, not_found_products = _search_products(product_names)

    if not found_products:
        await update.message.reply_text(
            "❌ Продукты не найдены. Попробуйте другие поисковые термины.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    status_text = _format_search_status(found_products, not_found_products)
    status_msg = await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)

    try:
        products_data = await _process_products(found_products)

        await status_msg.edit_text("📊 Генерация отчета Excel...")
        report_path = report_generator.generate_supplier_analysis_report(products_data)

        await status_msg.edit_text("🤖 Анализ поставщиков с помощью AI...")
        analyses = await groq_analyzer.analyze_multiple_products(products_data)

        await send_analysis_results(update, analyses, report_path)
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Error processing search: {e}")
        await status_msg.edit_text(
            "❌ Ошибка обработки вашего запроса. Попробуйте еще раз позже.",
            parse_mode=ParseMode.MARKDOWN
        )


def _search_products(product_names: list) -> tuple:
    found_products = []
    not_found_products = []

    for name in product_names:
        product = product_db.find_product_by_name(name)
        if product:
            found_products.append(product)
        else:
            not_found_products.append(name)

    return found_products, not_found_products


def _format_search_status(found_products: list, not_found_products: list) -> str:
    status_text = (
        f"\n📊 **Результаты поиска:**\n"
        f"• Найдено: {len(found_products)} продукт(ов)\n"
        f"• Не найдено: {len(not_found_products)} продукт(ов)\n\n"
        "Анализируем международных поставщиков...\n"
        "Это может занять некоторое время ⏳"
    )

    if not_found_products:
        status_text += f"\n❌ Не найдено: {', '.join(not_found_products)}"

    return status_text


async def _process_products(found_products: list) -> list:
    products_data = []

    for product in found_products:
        suppliers = product_db.generate_supplier_prices(product, Config)
        sorted_suppliers = sorted(suppliers, key=lambda x: x["final_price_usd"])
        products_data.append({
            "product": product,
            "suppliers": sorted_suppliers
        })

    return products_data


async def send_analysis_results(update: Update, analyses: list, report_path: str):
    try:
        analysis_header = """
📈 **РЕЗУЛЬТАТЫ АНАЛИЗА ПОСТАВЩИКОВ**
────────────────────────────
        """

        await update.message.reply_text(analysis_header, parse_mode=ParseMode.MARKDOWN)

        for analysis in analyses:
            formatted_analysis = groq_analyzer.format_analysis_for_telegram(analysis)

            if len(formatted_analysis) > 4000:
                parts = [formatted_analysis[i:i+4000] for i in range(0, len(formatted_analysis), 4000)]
                for part in parts:
                    await update.message.reply_text(part, parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(0.3)
            else:
                await update.message.reply_text(formatted_analysis, parse_mode=ParseMode.MARKDOWN)

            await asyncio.sleep(0.5)

        await update.message.reply_text(
            "📊 **Генерация подробного отчета Excel...**",
            parse_mode=ParseMode.MARKDOWN
        )

        with open(report_path, 'rb') as report_file:
            await update.message.reply_document(
                document=report_file,
                filename=f"анализ_поставщиков.xlsx",
                caption="📈 Полный отчет анализа поставщиков"
            )

        final_text = """
✅ **Анализ завершен!**

**Следующие шаги:**
1. Просмотрите отчет Excel для подробного ценообразования
2. Свяжитесь с топ 3 поставщиками из анализа
3. Запросите образцы перед оптовым заказом
4. Обсудите лучшие условия на основе данных

**Нужно проанализировать больше продуктов?**
Просто отправьте названия товаров!
        """

        await update.message.reply_text(final_text, parse_mode=ParseMode.MARKDOWN)

        try:
            os.remove(report_path)
        except:
            pass

    except Exception as e:
        logger.error(f"Error sending results: {e}")
        await update.message.reply_text(
            "✅ Анализ завершен! Проверьте свои файлы.",
            parse_mode=ParseMode.MARKDOWN
        )


def main():
    config_errors = Config.validate()
    if config_errors:
        logger.error("❌ Configuration errors: %s", ", ".join(config_errors))
        return

    Path(Config.TEMP_DIR).mkdir(exist_ok=True)

    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("examples", examples_command))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_product_search
    ))

    logger.info("🤖 Бот Анализа Рынка Поставщиков запущен...")
    logger.info("Готов анализировать поставщиков!")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()