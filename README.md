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
cd arabic-ner-platform
📖 User Manual
1. The Interface
The application is divided into three main sections:

Top Section: Input area for your Arabic text.

Control Bar: Dropdown menu to select models, buttons to run analysis, add models, or export data.

Bottom Canvas: A scrollable area where results appear side-by-side.

2. Analyzing Text
Paste your Arabic text into the input box at the top.

Select a model from the dropdown menu (Default: CAMeL Tools).

Click the green "تشغيل (+)" (Run) button.

The result will appear in a new column below, showing the processing time and extracted entities colored by type:

🟦 Blue: Person (PER)

🟩 Green: Location (LOC)

🟧 Orange: Organization (ORG)

🟨 Yellow: Miscellaneous (MISC)

3. Comparing Models
To compare models, simply change the selection in the dropdown (e.g., switch to CamelBERT) and click Run (+) again. A new column will appear next to the previous one, allowing you to see how different models handle the same text.

4. Adding a New Model (Hugging Face)
Click the purple "➕ إضافة نموذج جديد" button.

Enter the Hugging Face model path (e.g., aubmindlab/bert-base-arabertv02).

Enter a display name (e.g., AraBERT v02).

A terminal window will open showing the download progress. Once finished, the model is automatically added to your dropdown menu.

5. Exporting Results
Click the blue "📊 حفظ Excel" button to save a report. The Excel file contains:

Data Sheet: Detailed list of tokens and labels for every model run.

Analysis Sheet: Summary of entity counts and execution time with a bar chart.

📂 Project Structure
app.py: The main entry point containing the Tkinter GUI logic and threading.

ner_model.py: The backend logic handling transformers, camel-tools, and PyTorch operations.

📜 License
This project is open-source. Feel free to modify and distribute.


### 1. Clone the Repository
```bash
git clone [https://github.com/abdo-kao/arabic-ner-platform.git](https://github.com/abdo-kao/arabic-ner-platform.git)

