import csv
import re
import unicodedata
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler
from nltk.stem import WordNetLemmatizer

class TextProcessor:
    """
    Processes text data from CSV files, cleans it, and extracts TF-IDF features.

    Attributes:
        vector_features (pd.DataFrame): DataFrame containing aggregated TF-IDF features by transaction ID.
        lemma (WordNetLemmatizer): Lemmatizer object for text normalization.
    """

    def __init__(self, path, max_features=500, target_features=30):
        """
        Initializes the TextProcessor by loading, cleaning, and vectorizing data from CSV files.

        Args:
            path (str): file path to CSV file containing text data.
        """
        self.lemma = WordNetLemmatizer()
    
        self.vector_features = None
        
        # get data
        res = self.load_data(path)
        data, labels, txn_ids = res[0], res[1], res[2]
        
        # clean data
        cleaned = [self.clean_text(text) for text in data]
        
        # vectorize
        self.vector_features = self.vectorize_data(cleaned, labels, txn_ids, max_features, target_features)
        
    # load dataset
    def load_data(self, path):
        """
        Loads data from a CSV file.

        Args:
            path (str): Path to the CSV file.

        Returns:
            tuple: A tuple containing lists of data, labels, and transaction IDs.
        """
        data, labels, txn_ids = [], [], []
        
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row['comment'])
                labels.append(row['polar'])
                txn_ids.append(row['txn_id'])
        return (data, labels, txn_ids)
    
    # clean
    def clean_text(self, text):
        """
        Cleans and lemmatizes a given text string.

        Args:
            text (str): The text string to clean.

        Returns:
            str: The cleaned and lemmatized text string.
        """
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = text.lower()
        text = self.lemma.lemmatize(text)
        return text
          
    # vectorize
    def vectorize_data(self, data, labels, txn_ids, max_features, target_features):
        """
        Vectorizes the cleaned text data using TF-IDF and performs feature selection.

        Args:
            data (list): List of cleaned text strings.
            labels (list): List of labels corresponding to the text data.
            txn_ids (list): List of transaction IDs.
            max_features (int, optional): Maximum number of features for TF-IDF. Defaults to 500.
            target_features (int, optional): Number of features to select after feature selection. Defaults to 20.

        Returns:
            pd.DataFrame: DataFrame containing aggregated TF-IDF features by transaction ID.
        """
        # Tfidf vectorization
        vectorizer = TfidfVectorizer(analyzer='word', stop_words='english', max_features=max_features, ngram_range=(1, 3), min_df=2, max_df=0.95)
        X = vectorizer.fit_transform(data)
        
        # Feature names from the vectorizer
        feature_names = vectorizer.get_feature_names_out()
                        
        # Select top {target} features
        selector = SelectKBest(chi2, k=target_features) # chi-square
        X_selected = selector.fit_transform(X.toarray(), labels)
        
        # standard scalar
        scaler = StandardScaler(with_mean=False)
        X_scaled = scaler.fit_transform(X_selected)
                
        # text features
        text_features = pd.DataFrame(X_scaled, columns=[feature_names[i] for i in selector.get_support(indices=True)])
        text_features['txn_id'] = txn_ids
        
        # Aggregate text features by txn_id
        aggregated_text_features = text_features.groupby('txn_id').mean().reset_index()

        return aggregated_text_features
    

# Example usage
# if __name__ == "__main__":
#     ps = TextProcessor("./data/comments.csv")
#     print(ps.vector_features)
