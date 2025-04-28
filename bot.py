import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Вставьте ваш токен сюда
TOKEN = "7635752557:AAEczMIuW6gd5MM770FUgqoGJHVkx9UYaCM"

# Load data from JSON files
def load_data(filename):
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Load all data
grammar_rules = load_data('grammar_rules')
vocabulary = load_data('vocabulary')
tenses = load_data('tenses')
test_questions = load_data('test_questions')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # Отправляем фото
    photo_url = "1.jpg"  # Замените на реальную ссылку на фото
    await update.message.reply_photo(
        photo=photo_url,
        caption="🌟 Welcome to FluentFox English Learning Bot! 🦊\n\n"
                "📚 Learn English with our comprehensive resources:\n"
                "• Grammar rules and examples\n"
                "• Vocabulary building\n"
                "• Tense practice\n"
                "• Interactive tests\n\n"
                "🌐 Visit our website: https://deni1s-asl.github.io/fluentfox_site/\n"
                "📱 Follow us on Telegram: @fluentfox\n\n"
                "Choose what you want to learn:"
    )

    # Отправляем клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("📚 Grammar", callback_data='grammar'),
            InlineKeyboardButton("📖 Vocabulary", callback_data='vocabulary')
        ],
        [
            InlineKeyboardButton("⏰ Tenses", callback_data='tenses'),
            InlineKeyboardButton("📝 Test", callback_data='test')
        ],
        [
            InlineKeyboardButton("🔗 Resources", callback_data='resources'),
            InlineKeyboardButton("ℹ️ About", callback_data='about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Select an option to start learning:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == 'grammar':
        await show_grammar_rules(query)
    elif query.data == 'vocabulary':
        await show_vocabulary_levels(query)
    elif query.data == 'tenses':
        await show_tense_categories(query)
    elif query.data == 'test':
        await show_test_levels(query)
    elif query.data == 'resources':
        await show_resources(query)
    elif query.data == 'about':
        await show_about(query)
    elif query.data == 'back_to_main':
        await back_to_main(query)
    elif query.data.startswith('grammar_'):
        await show_grammar_rule(query)
    elif query.data.startswith('tense_'):
        await show_tense_level(query)
    elif query.data.startswith('test_'):
        await show_test_questions(query)
    elif query.data.startswith('vocab_'):
        await show_vocabulary_words(query)

async def show_grammar_rules(query) -> None:
    """Show grammar rules with examples."""
    keyboard = []
    for rule in grammar_rules:
        keyboard.append([InlineKeyboardButton(rule['title'], callback_data=f'grammar_{rule["id"]}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📚 Grammar Rules\n\n"
        "Select a rule to learn:",
        reply_markup=reply_markup
    )

async def show_grammar_rule(query) -> None:
    """Show specific grammar rule."""
    rule_id = query.data.split('_')[1]
    rule = next((r for r in grammar_rules if r['id'] == rule_id), None)
    
    if rule:
        text = f"📚 {rule['title']}\n\n"
        text += f"Explanation: {rule['explanation']}\n\n"
        text += "Examples:\n"
        for example in rule['examples']:
            text += f"• {example}\n"
        text += f"\nTranslation: {rule['translation']}"
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Grammar", callback_data='grammar')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

async def show_vocabulary_levels(query) -> None:
    """Show vocabulary difficulty levels."""
    keyboard = [
        [
            InlineKeyboardButton("Easy", callback_data='vocab_easy'),
            InlineKeyboardButton("Medium", callback_data='vocab_medium')
        ],
        [
            InlineKeyboardButton("Hard", callback_data='vocab_hard'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📖 Vocabulary Levels\n\n"
        "Choose your level:",
        reply_markup=reply_markup
    )

async def show_vocabulary_words(query) -> None:
    """Show vocabulary words for selected level."""
    level = query.data.split('_')[1]
    words = vocabulary[level]
    
    text = f"📖 {level.capitalize()} Vocabulary\n\n"
    for word in words:
        text += f"• {word['word']} - {word['translation']}\n"
        text += f"  Example: {word['example']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Vocabulary", callback_data='vocabulary')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_tense_categories(query) -> None:
    """Show tense categories."""
    keyboard = [
        [
            InlineKeyboardButton("Simple", callback_data='tense_simple'),
            InlineKeyboardButton("Continuous", callback_data='tense_continuous')
        ],
        [
            InlineKeyboardButton("Perfect", callback_data='tense_perfect'),
            InlineKeyboardButton("Perfect Continuous", callback_data='tense_perfect_continuous')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⏰ English Tenses\n\n"
        "Select a category:",
        reply_markup=reply_markup
    )

async def show_tense_level(query) -> None:
    """Show tenses for selected category."""
    category = query.data.split('_')[1]
    tense_list = tenses[category]
    
    text = f"⏰ {category.capitalize()} Tenses\n\n"
    for tense in tense_list:
        text += f"📌 {tense['title']}\n"
        text += f"Usage: {tense['explanation']}\n"
        text += f"Form: {tense['form']}\n"
        text += "Examples:\n"
        for example in tense['examples']:
            text += f"• {example}\n"
        text += f"Translation: {tense['translation']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Tenses", callback_data='tenses')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_test_levels(query) -> None:
    """Show test difficulty levels."""
    keyboard = [
        [
            InlineKeyboardButton("Beginner", callback_data='test_beginner'),
            InlineKeyboardButton("Intermediate", callback_data='test_intermediate')
        ],
        [
            InlineKeyboardButton("Advanced", callback_data='test_advanced'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📝 English Test\n\n"
        "Choose your level:",
        reply_markup=reply_markup
    )

async def show_test_questions(query) -> None:
    """Show test questions for selected level."""
    level = query.data.split('_')[1]
    questions = test_questions[level]
    
    text = f"📝 {level.capitalize()} Level Test\n\n"
    for i, question in enumerate(questions, 1):
        text += f"{i}. {question['question']}\n"
        for option in question['options']:
            text += f"   • {option}\n"
        text += f"   Answer: {question['correct']}\n"
        text += f"   Explanation: {question['explanation']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Test", callback_data='test')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_resources(query) -> None:
    """Show learning resources."""
    resources_text = (
        "🔗 Learning Resources\n\n"
        "📚 Grammar Books:\n"
        "- English Grammar in Use\n"
        "- Practical English Usage\n"
        "- Oxford English Grammar\n\n"
        "💻 Online Courses:\n"
        "- Coursera English Courses\n"
        "- Udemy English Classes\n"
        "- BBC Learning English\n\n"
        "📱 Mobile Apps:\n"
        "- Duolingo\n"
        "- Memrise\n"
        "- Busuu\n\n"
        "🎥 YouTube Channels:\n"
        "- English Addict with Mr Steve\n"
        "- BBC Learning English\n"
        "- English with Lucy"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(resources_text, reply_markup=reply_markup)

async def show_about(query) -> None:
    """Show about information."""
    about_text = (
        "ℹ️ About FluentFox\n\n"
        "FluentFox is an English learning platform that helps you master English through:\n"
        "📚 Grammar rules and examples\n"
        "📖 Vocabulary building\n"
        "⏰ Tense practice\n"
        "📝 Tests and exercises\n\n"
        "Contact:\n"
        "📧 Email: den.aslyamov@inbox.ru\n"
        "📱 Telegram: @den1iis\n"
        "🤖 Bot: @helpstudyenglish_bot"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(about_text, reply_markup=reply_markup)

async def back_to_main(query) -> None:
    """Return to main menu."""
    keyboard = [
        [
            InlineKeyboardButton("📚 Grammar", callback_data='grammar'),
            InlineKeyboardButton("📖 Vocabulary", callback_data='vocabulary')
        ],
        [
            InlineKeyboardButton("⏰ Tenses", callback_data='tenses'),
            InlineKeyboardButton("📝 Test", callback_data='test')
        ],
        [
            InlineKeyboardButton("🔗 Resources", callback_data='resources'),
            InlineKeyboardButton("ℹ️ About", callback_data='about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Welcome to FluentFox English Learning Bot! 🦊\n\n"
        "Choose what you want to learn:",
        reply_markup=reply_markup
    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main() 
    