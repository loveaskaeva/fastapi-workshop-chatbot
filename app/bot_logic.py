from typing import Dict


KEYWORDS: Dict[str, str] = {
    "привет": "Здравствуйте! Чем помочь?",
    "помощь": "Опишите проблему, я постараюсь помочь.",
    "поддержка": "Служба поддержки на связи.",
    "оплата": "Информация по оплате доступна в личном кабинете.",
}


def reply(text: str) -> str:
    lower = text.lower()
    for k, v in KEYWORDS.items():
        if k in lower:
            return v
    return "Я не понял запрос. Могу помочь с общими вопросами."
