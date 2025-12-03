
# 🦅 Arabic NER Professional Platform

**A professional desktop application for Named Entity Recognition (NER) in Arabic texts. This tool allows researchers and developers to extract names, locations, and organizations using state-of-the-art AI models without writing code.**

---

## 📌 Project Definition (نبذة عن المشروع)
The **Arabic NER Platform** is a graphical interface (GUI) built with Python that simplifies the use of complex Artificial Intelligence models for the Arabic language.

Instead of running complex scripts in a command line, this application provides a user-friendly window where you can:
1.  **Input Arabic text** and immediately see extracted entities (Persons, Locations, Organizations).
2.  **Compare different AI models** side-by-side to see which one performs best.
3.  **Download new models** directly from Hugging Face with a single click.
4.  **Export results** to Excel for further analysis.

It is designed for linguists, data scientists, and developers who need a quick and powerful tool for Arabic text analysis.

---

## ✨ Key Features
* **Multi-Model Support:** Comes pre-loaded with top models like **CAMeL Tools**, **mBERT**, **CamelBERT**, and **XLM-RoBERTa**.
* **Dynamic Model Loading:** You can add *any* model from Hugging Face by simply pasting its link.
* **Visual Comparison:** Run multiple models on the same text and see the results aligned side-by-side.
* **Excel Export:** Save your work to an Excel file, including charts and detailed statistics.
* **Color-Coded Visualization:** Entities are highlighted automatically (Blue for Person, Green for Location, etc.).

---

## ⚙️ Installation Requirements (متطلبات التثبيت)

Before running the app, ensure you have the following installed on your computer:

### 1. System Requirements
* **OS:** Windows, macOS, or Linux.
* **Python:** Version 3.8 or higher.
* **Internet:** Required for the first run to download the AI models.

### 2. Python Libraries
You need to install the dependencies listed in `requirements.txt`.

---

## 🚀 Installation Guide (steps)

Follow these steps to set up the project on your machine:

### Step 1: Clone the Repository
Download the project files to your computer.
```bash
git clone [https://github.com/abdo-kao/arabic-ner-platform.git](https://github.com/abdo-kao/arabic-ner-platform.git)
cd arabic-ner-platform
````

### Step 2: Install Dependencies

Install the necessary Python libraries.

```bash
pip install -r requirements.txt
```

### Step 3: Install CAMeL Tools Data

This is a **critical step**. The app uses CAMeL Tools, which requires a specific dataset. Run this command in your terminal:

```bash
camel_data -i ner-arabert
```

*(Note: This download is large \~1GB. Please wait for it to finish).*

-----

## 📖 User Manual (دليل الاستخدام)

### How to Run the App

Open your terminal inside the project folder and type:

```bash
python app.py
```

### How to Use

1.  **Enter Text:** Paste your Arabic text into the input box at the top of the window.
2.  **Select Model:** Choose a model from the dropdown menu (e.g., *CAMeL Tools* or *CamelBERT*).
3.  **Run:** Click the green **Run (+)** button.
      * The app will analyze the text and display the results in a new column.
      * Entities will be colored: **Person (Blue)**, **Location (Green)**, **Organization (Orange)**.
4.  **Compare:** To compare, select a different model from the menu and click **Run (+)** again. A new column will appear next to the first one.
5.  **Save:** Click **Save Excel** to export a report containing all the results and a comparison chart.

### How to Add a New Model

1.  Click the purple **"➕ Add New Model"** button.
2.  Go to [Hugging Face](https://www.google.com/search?q=https://huggingface.co/models%3Fpipeline_tag%3Dtoken-classification%26language%3Dar) and copy the model ID (e.g., `aubmindlab/bert-base-arabertv02`).
3.  Paste the ID into the app and give it a name.
4.  Wait for the download to finish.

-----

## 📂 Project Structure

  * `app.py`: The main application file containing the User Interface (GUI).
  * `ner_model.py`: The backend logic that handles the AI models.
  * `requirements.txt`: List of libraries needed to run the app.
  * `README.md`: This documentation file.

## 📄 License

This project is open-source. Feel free to use, modify, and distribute it.

````

---

### **Don't forget the `requirements.txt` file**
Make sure this file is also in your repository so users know what to install:

**File Name:** `requirements.txt`
```text
torch
transformers
camel-tools
pandas
xlsxwriter
numpy
tqdm
````
