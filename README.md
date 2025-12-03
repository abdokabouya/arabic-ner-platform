# 🦅 Arabic NER Professional Platform

**A comprehensive desktop application for Named Entity Recognition (NER) in Arabic texts, supporting multiple Transformer models and dynamic model loading.**

## 📌 Project Definition
The **Arabic NER Platform** is a Python-based GUI application designed to simplify the process of extracting entities (Persons, Locations, Organizations, etc.) from Arabic text.

Unlike standard command-line scripts, this tool provides a visual interface that allows researchers, linguists, and developers to:
1.  **Visualize** NER results with color-coded tags.
2.  **Compare** different state-of-the-art models (CAMeL Tools, mBERT, XLM-R, etc.) side-by-side.
3.  **Analyze** performance speed and entity counts.
4.  **Download** new models directly from Hugging Face without writing code.

## ✨ Key Features
* **Multi-Model Support:** Comes pre-loaded with top Arabic NER models:
    * CAMeL Tools (Standard)
    * CamelBERT (MSA & Mix/Dialect)
    * mBERT & DistilBERT (Multilingual)
    * XLM-RoBERTa
* **Dynamic Model Loading:** Add *any* Hugging Face NER model simply by pasting the repository link (e.g., `marefa-nlp/marefa-ner`).
* **Side-by-Side Comparison:** Run multiple models on the same text and see the results aligned horizontally to compare accuracy.
* **Excel Export:** Save your analysis to an Excel file, including a detailed breakdown of entities and a summary chart.
* **Visual Interface:** Built with `Tkinter`, offering a clean, native desktop experience with a "CMD-style" download window for transparency.

## 🛠️ Installation

### Prerequisites
* Python 3.8+
* Internet connection (for downloading models)

### 1. Clone the Repository
```bash
git clone [https://github.com/abdo-kao/arabic-ner-platform.git](https://github.com/abdo-kao/arabic-ner-platform.git)
cd arabic-ner-platform