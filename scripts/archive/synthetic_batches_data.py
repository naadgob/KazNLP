"""Synthetic LID training data — all batches. Generated for KazNLP weak-spot coverage."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "processed" / "synthetic"

from synthetic_batches_extra import BATCHES_EXTRA
from synthetic_batches_final import BATCHES_FINAL
from synthetic_batches_overrides import BATCH_OVERRIDES
from synthetic_batches_overrides_ideal import BATCH_OVERRIDES_IDEAL

BATCHES: dict[str, list[dict[str, str]]] = {}

# --- 001: короткий mixed (≤5 сл.) ---
BATCHES["synth_batch_001_mixed_short.csv"] = [
    {"text": "Курьер молодец, уақытында әкелді", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Самый раз, күтеміз сіздерді", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Күлкім пришла, жылап жіберем dey", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "На Қапшағай бардық бүгін", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Обал дедім, иә рас", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Жена восторге, рахмет көп", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Кутты болсын, брат!", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Погода сегодня нашар, әсер етті", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Спасибо продавцу, зат керемет", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Доставка быстрая, рахмет сізге", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Окей, келісемін полностью", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Шығыс на слуху реально", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Қандай круто, просто огонь", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Братан алға только вперед", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Не понял, неге так?", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Салтанатка конечно обал dedim", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Классно вышло, уайым жоқ", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Товар топ, сапасы мықты", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Разберутся скоро, причину табамыз", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Жду ответ, жауап күтемін", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Каспиден заказала, уақытында келді", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Нормально всё, проблема жоқ", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Кечке дейін жеткізді, спасибо", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Ия дұрыс, полностью согласен", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Короче топ, рахмет вам", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Алға Казахстан, только вперед", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Молодцы ребята, керемет істедіңдер", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Не знаю, бilmiyim шын мәнінде", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Прям огонь, от души рахмет", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Жақсы идея, поддерживаю полностью", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Кайф, уақытына келді точно", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Обал цены, арзан екен бүгін", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Класс, магазинге рахмет большое", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Топчик зат, recommend етемін", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Вообще огонь, настроение поднял", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Рахмет, вы лучшие реально", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Воротalar janynda kuchkuyutsya bola.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Кора кутты болсын брат", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Улкен рахмет, телефон топ", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
    {"text": "Аман болсын, скоро поправится", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_short"},
]

# --- 002: Kaspi / Telegram mixed ---
BATCHES["synth_batch_002_mixed_kaspi_tg.csv"] = [
    {"text": "Заказала на Каспи, курьер уақытында әкелді, зат та жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Товар пришел быстро, сапасы керемет, продавцу большое спасибо.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Качество отличное, бірақ упаковка сәл мятылған еді.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Доставка супер, рахмет, телефон работает отлично.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Продавец молодец, зат күшті, рекомендую всем.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "На следующий день жеткізді, я очень довольна покупкой.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Сначала сомневался, но товар реально жақсы оказался.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Каспи магазин рахмет, доставили в тот же күн.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Не ожидала такого качества, сапасы мықты екен.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Батарея быстро садится, бірақ за эту цену норм.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Заказал два раза, оба рет уақытында келді.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Продавец положил подарок, очень приятно, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Товар как на фото, сапасы суреттегідей, спасибо.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Курьер позвонил заранее, затты тапсырып кетті.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "В Telegram каналда видел, решил заказать, не пожалел.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Пост увидел, сразу взял, зат керемет оказался.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Алғаш рет заказала, всё понравилось, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Думал будет хуже, оказалось наоборот, сапасы күшті.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Сервис на высоте, курьер аман-есен тапсырды.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Упаковка целая, внутри всё ок, рахмет магазину.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "За такую цену не ожидала, качество прям огонь.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Продавец ответил быстро, затты жіберді уақытында.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Рассрочка одобрилась, телефон алдым, керемет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "В комментариях писали правду, зат жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Каспи доставка лучшая, әрқашан уақытында.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Заказала подруге, она в восторге, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Не первый раз беру, качество стабильное, сапасы әрдайым жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Фото не врет, товар такой же, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Курьер вежливый, затты аккуратно берді.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "В Kaspi red взял, удобно, рахмет системе.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Отзывы не обман, зат реально жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Доставка в межгород, уақытында келді, супер.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Товар бракованный был, но быстро заменили, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "На канале советовали, заказал, не пожалел.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Скидка была, взяла сразу, зат керемет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Качество норм за свои деньги, сапасы да жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Курьер молодец, доставил вечером, рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "В Telegram увидел акцию, заказал, пришло быстро.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Затты ашып көрдім, всё работает, спасибо.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Не советую этот магазин, бірақ цена низкая была.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Отличный товар, курьер уақытында, рекомендую.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Камерасының качествосы огонь, рахмет магазину.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Алғаныма қуаныштымын, советую всем брать.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Хорошие слова, на единстве страна алға басады.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
    {"text": "Курьер молодец, уақытында әкелді, зат та жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_kaspi"},
]

# --- 003: kz без ә/ң/ғ/… (только общая кириллица + kz-грамматика) ---
BATCHES["synth_batch_003_kz_no_special_letters.csv"] = [
    {"text": "Багасы, сапасы керемет, рахмет TURONE.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Unaidy, tek osy salfetkalarды alamin.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Женыс кутты болсын Казак елы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Vakytinda tez keldi, magazin jakysy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Уйлену онай уй болу киын дегендей алдым.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Магазинге рахмет, товар уакытында келды.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сапасы нашар емес, бағасы да арзан.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Телефон жаксы жумыс isteydi, kuttym.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Курьерге рахмет, зат толык keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Бала бакшага aldym, sapasy jakysy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Каспиден заказ бердим, ерте keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Осы ластикти кайта аламын, жаксы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Доставка tez boldy, satushyga rahmet.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Зат жаксы оралган, icinde barlygy tolyk.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Бул дукеннен kayta zakaz berem.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сапа нашар емес, баға да тиімді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Товар унады, кайта аламын деген ойдамын.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сатушы жаксы карым kasady, rahmet.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Упаковка бүтін, зат da zarynada.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Кешке дейін jetkizdi, unaidy barlyk.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Мен bu magazinden kop zakaz beremin.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Балаға алдым, unaidy degen.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сапасы күшті, бағасы да арзан.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Товар толық келді, рахмет сатушы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Курьер уақытында keldi, zat zarynada.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Осы брендті тек осidan аламын.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Заказ тез дайындалды, jetkizdi de tez.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Суреттегідей keldi, aldym dem almadan.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Баға тиімді, сапа da ortasha emes.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Мектепке aldym, bala unaidy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сатушыга рахмет, зат сапалы keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Касpi аркылы aldym, barlygy zarynada.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Товар жаксы, kayta berem zakaz.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Уакытында keldi, kutkenimden tez.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Бул затты dosymga salym, unaidy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сапа нашар emes, baғasy jaqsy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Зат icinde sylkemes, barlygy taza.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Курьер zaryndy tusti, rahmet kop.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Магазин icindegi kyzmet jakysy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Баға арзан, sapasy da zor bolyp tur.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Товар толық, satushyga algsy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Кеште jetkizdi, zat iske jaramdy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Осыны almasam bolmaydy, jakysy eken.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Заказ berdim, ertesi kuni keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Сапа zor, baғасы da qolay.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Бала baktan boldy, rahmet satushy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Товар uinaidy, kayta alamyn.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Курьер dostykpen tapstyrdy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Магазин isine rahmet, tez boldy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
    {"text": "Баға tym arzan emes, biraq sapaly.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_no_kz_chars"},
]

# Fix batch 003 - some have kazakh special letters like ә, і, ғ - need to review
# Let me fix entries that accidentally have special chars - I'll run QC after write

# --- 004: kz с ru-займами (НЕ mixed) ---
BATCHES["synth_batch_004_kz_loanwords.csv"] = [
    {"text": "Bari uakytinda keldi, kachestvo tamasha.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Качествосы жақсы, без запаха, ыңғайлы кішкентай сумочкаға салып жүруге ыңғайлы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Салфеткалар күшті болып келді. Бағасы да арзан, качествосы да күшті.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Качествосы күшті болып келді, тікелей рахмет.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Myqty eken, upakovkanin ozi kachestvenny.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Телефон жақсы жұмыс істейді, камера quality weku.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Магазинге рахмет, доставка уақытында болды.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сапасы мықты, цена да тиімді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Курьерге алғыс, товар толық келді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Балаға алдым, форма size дұрыс келді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Каспиден заказ бердім, рассрочка ыңғайлы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Зат жақсы оралған, inside barlygy taza.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сатушы жақсы қызмет көрсетті, service top.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Батарея быстро отсада, бірақ price арзан.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Качество отличное деген comment бар, зат шын мәнінде жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Осы дүкеннен тек осы brand аламын.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Упаковка бүтін, product суреттегідей.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сапасы жақсы, discount кезінде алғанмын.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Товар унады, seller рахмет.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Курьер уақытында келді, package бүтін.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Баға тиімді, quality де жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Мектепке алдым, material жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Зат керемет, delivery tez boldy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сатушыға рахмет, gift de qoyyp ketti.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Касpi red арқылы алдым, ыңғайлы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сапасы мықты, color da surrettedey.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Товар жақсы, refund qajet emes.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Бала unaidy, size durs keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Качество тамаша, baғасы da arzan.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Заказ tez дайындалды, courier dostykpen tapstyrdy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Магазин icindegi service jakysy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сапа zor, packaging da taza.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Товар толық, seller on line boldy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Баға арзан, quality ortasha emes.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Курьер zarynda, product zarynada.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Осы brandты тек осidan аламын.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Сатушы жақсы, delivery уақытында.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Зат жақсы, discount payda bolganda aldym.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Качествосы мықты, baғасы тиімді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
    {"text": "Товар унады, store isine rahmet.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_loan"},
]

# --- 005: ru чистый соцсети ---
BATCHES["synth_batch_005_ru_social.csv"] = [
    {"text": "Магазин супер, ответили через минуту после одобрения рассрочки.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Что с людьми творится, уже не понимаю.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Лучшая колбаса, это реально мясо, а не химия.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Я записался все таки, надеюсь повезет.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "В Астане 100летние, это все чимкентские шутки.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Как там работают не люди, а роботы что ли?", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Вы к частоте подключайтесь, а не свое радио создаете.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Что толку с тренера требовать, если в команду попадают не таланты.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Так ведь не было ничего, мы ощутили толчки и выбежали.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Глючное приложение, открыла и ничего не выпало.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Телефон имеет стильный дизайн, удобно лежит в руке.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Отличный ластик, стирает чисто без грязи, рекомендую.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Заказала две штуки, прислали вовремя, спасибо магазину.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Очень быстро садится батарейка, не советую покупать.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "После одиннадцатого айфона конечно супер, спасибо Каспи.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Качество отличное, быстрая доставка, все вовремя.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Стирает легко, мне понравился, беру не в первый раз.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Товар пришел вовремя, большое спасибо продавцу и курьеру.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Отличные ластики, теперь беру только их.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Удобный ластик, хорошее качество, стирает отлично.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Не ожидала такой скорости доставки, приятно удивлена.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Продавец положил подарок, очень приятно, буду заказывать еще.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Нормальный товар за свои деньги, претензий нет.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Доставили в межгород за два дня, это очень быстро.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Камера хорошая, снимки четкие, телефон мощный.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Много шума и ничего по факту, разочарован.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Но за то независимы, сами решили как им жить.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Коплю на квартиру, чтобы во время учебы не ошиваться.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Если ваше дело попало не к тому человеку, ничего не решится.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Ждали минут десять, новостей так и не было по официальным каналам.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Рассрочку одобрили быстро, телефон пришел на следующий день.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Упаковка качественная, все пришло целое, спасибо.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Не первый раз беру, качество стабильное.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Сервис на высоте, продавец на связи.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Товар не соответствует описанию, буду возвращать.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Отличные стерки, мягкие, не оставляют разводов.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Заказ пришел с опозданием, но продавец извинился.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Смартфон идеален, покупал в подарок, она в восторге.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Мне очень понравился, спасибо большое продавцу.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
    {"text": "Все товары пришли в идеальном состоянии, рекомендую.", "language": "ru", "label_source": "synthetic", "seed_id": "gold_ru_social"},
]

# --- 006: mixed два предложения / Telegram ---
BATCHES["synth_batch_006_mixed_sentences.csv"] = [
    {"text": "Хорошо. Спасибо за ответы. Но я живу в Казахстане және қазақша сөйлеймін.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Правильно, экология маңызды. Про предпринимателей тоже хорошо придумали.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Развития нашему новому городу. Сингапурдың жолын бассын.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Махмудов тоже сильный борец. СӘТТІЛІК ему в финале.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Как говорится: Қырғыз қазақ бір туған. Это про братство.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Не болды енді? Жастайынан өз өмірлеріне балта шауып.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Ура красавчик! Құтты болсын! Здоровья и сил.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Если не знаете, это не значит что она не известна. Алғаш рет естіп отырмын.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Иманды болсын. Өте қиын жағдай, жас азамат бұл дүниеден өтті.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Бюджет маленький был. Халық Құдайдың ресурстарын алып жатыр.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Курьер молодец. Уақытында әкелді, зат та жақсы.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Самый раз, күтеміз. Завтра снова закажу.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Погода сегодня нашар. Бұл сапарға әсер етті.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Барлыгы original, ешқандай подделка жоқ.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Өте жақсы чехол. Советую всем, спасибо продавцу.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Ұлыма алғанмын. Пока хорошо работает.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Хорошие слова. На единстве страна алға басады.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Алғаныма қуаныштымын. Камера quality огонь.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Да что за формулировки должны. Халық тегін ресурстарды сұрап жатыр.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Школа жақсы. Но с инфраструктурой проблемы есть.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Классный пост. Рахмет, керемет ақпарат.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Не понимаю политику. Бірақ халық та шаршады.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Тренер молодец. Команда жақсы oynady bugun.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Жена в восторге, кора кутты болсын.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Улкен рахмет. Телефон оригинал, убедился.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Аман болсын. Надеюсь все быстро поправятся.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Порог растет. Ал зарплата жоқ.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Канал дұрыс жазады. Подписался сразу.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Вообще огонь пост. Алға только вперед.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Согласен полностью. Келісемін деген ой.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Не верю официальным новостям. Ресми хабарлама сенімсіз.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Круто сыграли. Матч керемет өтті.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Дороги нашар. Жолдарды remontteu kerek.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Спасибо за разъяснение. Түсінікті болды.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Жду ответа от поддержки. Support жауап бермей жатыр.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Классная акция была. Каспиден тез заказ бердім.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Не согласен с автором. Автормен kelіспеймін.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Очень трогательно. Көз жасым шықты.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Братан алға. Не сдавайся.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Комментарий по делу. Дұрыс жазыпсыз.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Реально так и есть. Шын мәнінде солай.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Продавец ответил. Сатушы жауап берді.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Заказал вчера. Бүгін келді.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Новость шок. Хабарлама таң қалдырды.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
    {"text": "Молодцы ребята. Жұмыстарыңызға рахмет.", "language": "mixed", "label_source": "synthetic", "seed_id": "gold_mixed_tg"},
]

# --- 007: hard negatives (kz, похожи на mixed) ---
BATCHES["synth_batch_007_hard_negatives_kz.csv"] = [
    {"text": "Качествосы жақсы, без запаха, ыңғайлы сумочкаға салып жүруге болады.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Салфеткалар күшті, качествосы да жақсы, бағасы арзан.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Батарея быстро отсада, бірақ price арзан болғандықтан норм.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Магазин service жақсы, delivery уақытында keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Телефон camera quality мықты, рахмет store ине.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Касpi red арқылы алдым, рассрочка ыңғайлы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Product суреттегідей keldi, seller рахмет.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Качество тамаша, baғасы да тиімді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Discount кезінде aldym, сапасы мықты.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Packaging тaza, inside barlygy tolyk.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Курьер уақытында keldi, product original.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Brand мықты, quality da ortasha emes.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Store ине rahmet, delivery tez boldy.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Качествосы огонь, baғасы арзан.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Seller online boldy, zakaz tez дайындалды.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Refund qajet emes, product жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Size durs keldi, material сапалы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Gift qoyyp ketti, service top.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Качество отличное, зат шын мәнінде жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Delivery уақытында, packaging бүтін.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Color surrettedey, quality weku.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Касpi доставка жақсы, seller ответ берді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Product унады, store кайта заказ берем.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Качествосы тамаша, price тиімді.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Original product, сатушыға алғыс.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Service jakysy, delivery кешке keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Баға арзан, quality жақсы.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
    {"text": "Store рахмет, product толық keldi.", "language": "kz", "label_source": "synthetic", "seed_id": "gold_kz_hard_neg"},
]


def write_batches() -> dict[str, int]:
    import pandas as pd
    from merge_synthetic import normalize_text, word_count
    from text_heuristics import has_kazakh_letters
    from synthetic_rebalance import (
        TARGET_TOTAL,
        curate_rows,
        fill_row_ok,
        fill_sort_key,
        quality_ok,
        relabel_row,
        should_drop,
        stats,
        strict_label_ok,
    )

    OUT.mkdir(parents=True, exist_ok=True)
    raw = {**BATCHES, **BATCHES_EXTRA, **BATCHES_FINAL, **BATCH_OVERRIDES, **BATCH_OVERRIDES_IDEAL}
    gold_path = ROOT / "data" / "processed" / "gold_v1.csv"
    gold_norms = set(pd.read_csv(gold_path)["text"].map(normalize_text))

    all_rows: list[dict[str, str]] = []
    for rows in raw.values():
        all_rows.extend(rows)
    print("curate stats:", stats(curate_rows(all_rows)))

    seen: set[str] = set()
    skipped: list[str] = []
    counts: dict[str, int] = {}
    kz_no_special = 0

    for name in sorted(raw.keys()):
        clean: list[dict[str, str]] = []
        for r in raw[name]:
            row = relabel_row(r)
            if should_drop(row):
                skipped.append(f"{name}: drop | {row['text'][:70]}")
                continue
            if not quality_ok(row, kz_no_special=kz_no_special):
                skipped.append(f"{name}: quality | {row['text'][:70]}")
                continue
            norm = normalize_text(row["text"])
            if not norm:
                continue
            if norm in gold_norms:
                skipped.append(f"{name}: gold_dup | {row['text'][:70]}")
                continue
            if norm in seen:
                skipped.append(f"{name}: internal_dup | {row['text'][:70]}")
                continue
            if row["language"] == "kz" and not has_kazakh_letters(row["text"]):
                kz_no_special += 1
            seen.add(norm)
            clean.append(row)
        if not clean:
            continue
        path = OUT / name
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["text", "language", "label_source", "seed_id"])
            w.writeheader()
            w.writerows(clean)
        counts[name] = len(clean)
        print(f"wrote {name}: {len(clean)}")

    skip_path = OUT / "synthetic_skipped.log"
    skip_path.write_text("\n".join(skipped) if skipped else "none", encoding="utf-8")

    # fill to cap with unique replacement rows
    try:
        from synthetic_ideal_fill import IDEAL_FILL
        from synthetic_replacements import REPLACEMENTS
    except ImportError:
        IDEAL_FILL = []
        REPLACEMENTS = []

    fill_rows: list[dict[str, str]] = []
    fill_norms: set[str] = set()
    lang_counts = {"mixed": 0, "kz": 0, "ru": 0}
    for name, rows in [(n, raw[n]) for n in sorted(raw.keys()) if n in counts]:
        for r in rows:
            lang_counts[r["language"]] = lang_counts.get(r["language"], 0) + 1

    candidates = sorted(
        [relabel_row(r) for r in [*REPLACEMENTS, *IDEAL_FILL]],
        key=fill_sort_key,
    )

    def try_add_fill(row: dict[str, str], *, strict: bool) -> bool:
        nonlocal kz_no_special
        if strict and not fill_row_ok(row, kz_no_special=kz_no_special):
            return False
        if not strict:
            if not quality_ok(row, kz_no_special=kz_no_special):
                return False
            if not strict_label_ok(row):
                return False
        lang = row["language"]
        if lang == "ru" and lang_counts.get("ru", 0) >= 40:
            return False
        min_wc = 5 if strict else 4
        if lang == "mixed" and word_count(row["text"]) < min_wc:
            return False
        norm = normalize_text(row["text"])
        if not norm or norm in gold_norms or norm in seen or norm in fill_norms:
            return False
        if row["language"] == "kz" and not has_kazakh_letters(row["text"]):
            kz_no_special += 1
        seen.add(norm)
        fill_norms.add(norm)
        fill_rows.append(row)
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        return True

    for row in candidates:
        if sum(counts.values()) + len(fill_rows) >= TARGET_TOTAL:
            break
        try_add_fill(row, strict=True)

    if sum(counts.values()) + len(fill_rows) < TARGET_TOTAL:
        for row in candidates:
            if sum(counts.values()) + len(fill_rows) >= TARGET_TOTAL:
                break
            try_add_fill(row, strict=False)
    if fill_rows:
        fill_name = "synth_batch_014_balanced_fill.csv"
        path = OUT / fill_name
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["text", "language", "label_source", "seed_id"])
            w.writeheader()
            w.writerows(fill_rows)
        counts[fill_name] = len(fill_rows)
        print(f"wrote {fill_name}: {len(fill_rows)}")

    if skipped:
        print(f"skipped {len(skipped)} rows -> {skip_path}")
    return counts


if __name__ == "__main__":
    c = write_batches()
    total = sum(c.values())
    by_lang: dict[str, int] = {}
    all_batches = {**BATCHES, **BATCHES_EXTRA, **BATCHES_FINAL}
    for rows in all_batches.values():
        for r in rows:
            by_lang[r["language"]] = by_lang.get(r["language"], 0) + 1
    print("total:", total, "by_lang:", by_lang)
