> **English version:** [README.md](README.md)

# Pretrained tone models (RU / KZ)

Две open-source модели для monolingual routing. Mixed tone — отдельно (`models/xlm-roberta/tone_v1.pt`, дубликат в `tone/tone_v1.pt`).

| Папка | Модель | Классы |
|-------|--------|--------|
| `ru_rubert_rureviews/` | [sismetanin/rubert_conversational-ru-sentiment-rureviews](https://huggingface.co/sismetanin/rubert_conversational-ru-sentiment-rureviews) | neutral · negative · positive |
| `kz_kazakh_sentiment_bert/` | [R3iwan/kazakh-sentiment-bert](https://huggingface.co/R3iwan/kazakh-sentiment-bert) | negative · neutral · positive |

**RU labels:** `LABEL_0` neutral · `LABEL_1` negative · `LABEL_2` positive  

**KZ labels:** `negative` · `neutral` · `positive`

Для бинарного API: pos/neg напрямую; neutral — argmax(pos, neg) или отдельный статус.

```bash
python scripts/download_tone_pretrained.py
python scripts/verify_tone_pretrained.py
```
