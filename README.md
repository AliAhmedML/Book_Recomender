# 📖 Book Recommender

**An LLM-powered system for analyzing book metadata and reader preferences to generate personalized reading recommendations.**  

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)

## 📌 Overview  

This project is an LLM-powered Book Recommender App that leverages Large Language Models (LLMs) to analyze book metadata, descriptions, and user preferences. Unlike traditional recommenders that rely only on ratings or collaborative filtering, this system uses semantic understanding of text to provide smarter and more personalized recommendations.

---

## 🛠️ Requirements  

- **Python 3.11 or later**  
- Recommended: **MiniConda** for environment management  

---

## ⚙️ Setup  

### Install Python via MiniConda  

1. Download and install [MiniConda](https://docs.anaconda.com/free/miniconda/#quick-command-line-install).  
2. Create a dedicated environment:  

   ```bash  
   conda create -p venv_Book python==3.11 

## 🛠️ Environment Setup

### Activate the Conda Environment

```bash
conda activate ./venv_Book
```

## 🛠️ Installation

### Install Required Packages

Ensure all dependencies are installed by running:

```bash
pip install -r Requirements.txt
```

## 🔍 Data Preprocessing Guide

### Essential Preprocessing Steps

1. **Dataset Loading**
   - Load your dataset using appropriate methods
   - Verify the dataset structure and contents

2. **Missing Value Handling**
   - Identify and document missing values
   - Apply either removal or imputation strategies
   - Maintain records of all modifications

3. **Missing Values Analysis**
   - Visualize the distribution of missing data across columns  
   - Identify patterns of missingness
   - Explore relationships between missing values and other features to check if missingness itself is informative
   - Use visual tools to better understand data quality

4. **Feature Engineering**
   - Create new features from existing data
   - Transform categorical and textual data into numerical representations suitable for modeling
   - Generate missing value indicators (flags) where useful  
   - Document all feature engineering steps clearly to ensure reproducibility

5. **Data Preparation**
   - To prepare the dataset for downstream NLP tasks, we export the tagged book descriptions into a plain text file
   - Load the text file and split it into smaller chunks for better handling by embedding models
   - Generate semantic embeddings using a transformer model and store them in a Chroma vector database for efficient similarity search
   - Simplify detailed book categories into broader groups for easier analysis and modeling

6. **Emotion Classification in Book Descriptions**
   - Initialize a Hugging Face `pipeline` with the model `j-hartmann/emotion-english-distilroberta-base`
   - Define the target emotion labels: `anger`, `disgust`, `fear`, `joy`, `sadness`, `surprise`, `neutral`
   - Create helper function `calculate_max_emotion_scores` to compute the maximum score for each emotion across sentences
   - Split each book description into sentences and classify emotions per sentence
   - Aggregate predictions by taking the maximum score per emotion
   - Store results for each book (`isbn13`) and its corresponding emotion scores

## 📁 Project Structure

1. **Main Application**
   - `main.py`: Entry point to launch the Gradio dashboard.

2. **Core Logic**
   - `recommender.py`: Contains the `BookRecommender` class with methods for retrieving and formatting recommendations.
   - `ui.py`: Defines the Gradio Blocks interface (query input, category/tone dropdowns, gallery output).
   - `config.py`: Central configuration (paths, model name, fallback cover).

3. **Data & Models**
   - `assets/`: Contains static resources like images and dataset.
     - `books_with_emotions.csv`: Dataset with book metadata and emotion scores.
     - `cover-not-found.jpg`: Default fallback cover image.
   - `chroma_db/`: Persisted Chroma vector database.

## 🚀 Run the App

### Start the Gardio Application

1. Make sure your virtual environment is activated:

   ```bash
   conda activate ./venv_Book
2. Run the Gardio app:

   ```bash
   python main.py
