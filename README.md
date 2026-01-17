# 📰 Text Summarization with T5 & CNN/DailyMail

Ce projet implémente un modèle de **Deep Learning** pour le résumé automatique de textes journalistiques. Il utilise l'architecture **T5 (Text-To-Text Transfer Transformer)** fine-tunée sur le dataset **CNN/DailyMail**.

## 🚀 Fonctionnalités
- **Fine-tuning** du modèle `t5-small` sur des articles de presse.
- **Prétraitement** des données (Tokenization, Nettoyage).
- **Visualisation** des données (WordClouds, distribution des longueurs).
- **Évaluation** avec la métrique **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation).
- **Interface** de visualisation des courbes de perte (Training vs Validation).

## 🛠️ Technologies
* **Python 3.10+**
* **Hugging Face Transformers** (T5, Seq2SeqTrainer)
* **PyTorch**
* **Pandas / Matplotlib / Seaborn**

## 📊 Résultats
Le modèle a été entraîné sur GPU (T4 x2) avec les hyperparamètres suivants :
- **Epochs:** 3
- **Batch Size:** 32
- **Optimizer:** AdamW

## 📦 Installation
1. Clonez le dépôt :
```bash
git clone [https://github.com/Safae26/text-summarization.git](https://github.com/Safae26/text-summarization.git)
