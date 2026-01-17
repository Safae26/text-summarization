# 📰 Text Summarization with T5 & CNN/DailyMail

Ce projet implémente un modèle de **Deep Learning** fine-tunée sur le dataset **CNN/DailyMail** pour le résumé automatique de textes journalistiques.

## 🚀 Fonctionnalités
- **Fine-tuning**
- **Prétraitement** des données (Tokenization, Nettoyage).
- **Visualisation** des données (WordClouds, distribution des longueurs).
- **Évaluation** avec la métrique **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation).
- **Interface** de visualisation des courbes de perte (Training vs Validation).

## 🛠️ Technologies
* **Python 3.10+**
* **Hugging Face Transformers** 
* **PyTorch**
* **Pandas / Matplotlib / Seaborn**

## 📊 Résultats
Le modèle a été entraîné sur GPU (T4 x2) avec les hyperparamètres suivants :
- **Epochs:** 5
- **Batch Size:** 6
- **Optimizer:** AdamW

## 📦 Installation
1. Clonez le dépôt :
```bash
git clone [https://github.com/Safae26/text-summarization.git](https://github.com/Safae26/text-summarization.git)
