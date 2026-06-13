# Mental Health Sentiment Detection Project

A free college project for detecting mental health sentiment from user-entered text.

## What’s new
- Manual text analysis for mental health sentiment
- Local model prediction from natural-language input
- Improved preprocessing with stopwords and lemmatization
- Better model training with evaluation metrics
- History logging of analyzed text and tweets

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- The current workflow only needs local text input and model prediction.
- Twitter search is planned as a future improvement and does not require a paid API key for the current version.

## NLTK Setup
Run once in Python:
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Train or Retrain the Model
```bash
python src/models/train_model.py
```
This will train on `data/raw/dataset.csv` and save the pipeline to `models/model_pipeline.pkl`.

## Run the App
```bash
python -m streamlit run app.py
```
Open the browser URL shown by Streamlit. Enter a natural-language sentence in the app and click analyze.

### Future improvement
- Twitter or social-media fetching can be added later if needed.
- No Twitter API key is required for the current text-only workflow.

## Project Structure
- `app.py`: Main Streamlit interface
- `src/config/config.py`: Configuration constants
- `src/data/twitter_fetcher.py`: Public tweet extraction
- `src/preprocessing/preprocessor.py`: Text cleaning and token normalization
- `src/models/train_model.py`: Model training and evaluation
- `src/models/predict_model.py`: Model loading and prediction
- `src/storage/storage_manager.py`: Results logging
- `data/raw/dataset.csv`: Training dataset
- `models/model_pipeline.pkl`: Saved pipeline

## Notes
- This project is educational and not a medical diagnostic tool.
