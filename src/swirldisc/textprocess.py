import re
import unicodedata
import dataprocess
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler
from nltk.stem import WordNetLemmatizer

class TextProcessor:
    """
    A class for processing text data by cleaning, vectorizing, and extracting useful features.

    Attributes:
        vector_features (pd.DataFrame): The processed and aggregated text features.
    """

    def __init__(self, path, headers, id_col, max_features=500, target_features=40):
        """
        Initializes the TextProcessor with the specified parameters, processes the data, and extracts features.

        Args:
            path (str): The file path to the CSV data.
            headers (list): A list containing column names for text, labels, and IDs.
            id_col (str): The column name representing unique identifiers for aggregation.
            max_features (int, optional): The maximum number of TF-IDF features. Defaults to 500.
            target_features (int, optional): The number of top features to select. Defaults to 40.
        """
        self.vector_features = None
        
        # Get data
        dp = dataprocess.DataProcess()
        df = dp.csv_to_dataframe(path, headers)
        
        # Clean data
        cleaned = [self.clean_text(text) for text in df[headers[0]]]
        
        # Vectorize
        self.vector_features = self.vectorize_data(cleaned, df[headers[1]], df[headers[2]], max_features, target_features, id=id_col)
            
    def clean_text(self, text):
        """
        Cleans the input text by normalizing, removing unwanted characters, and lemmatizing.

        Args:
            text (str): The raw text input.

        Returns:
            str: The cleaned and normalized text.
        """
        lemma = WordNetLemmatizer()

        text = unicodedata.normalize('NFKC', text)  # Normalize Unicode characters
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove non-alphanumeric characters
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace
        text = text.lower()  # Convert to lowercase
        text = lemma.lemmatize(text)  # Lemmatize the text
        return text
          
    def vectorize_data(self, data, labels, ids, max_features, target_features, id):
        """
        Vectorizes the text data using TF-IDF, selects top features, and aggregates by ID.

        Args:
            data (list): The cleaned text data.
            labels (pd.Series): The target labels corresponding to the text.
            ids (pd.Series): The unique identifiers for grouping.
            max_features (int): The maximum number of TF-IDF features.
            target_features (int): The number of top features to select.
            id (str): The column name for unique identifiers.

        Returns:
            pd.DataFrame: The aggregated text features grouped by the ID column.
        """
        # Tfidf vectorization
        vectorizer = TfidfVectorizer(
            analyzer='word', stop_words='english', max_features=max_features, 
            ngram_range=(1, 3), min_df=2, max_df=0.95
        )
        X = vectorizer.fit_transform(data)
        
        # Feature names from the vectorizer
        feature_names = vectorizer.get_feature_names_out()
                        
        # Select top {target} features
        selector = SelectKBest(chi2, k=target_features)  # Use chi-square for feature selection
        X_selected = selector.fit_transform(X.toarray(), labels)
        
        # Standard scaling
        scaler = StandardScaler(with_mean=False)  # Scale the features
        X_scaled = scaler.fit_transform(X_selected)
                
        # Create DataFrame for text features
        text_features = pd.DataFrame(
            X_scaled, columns=[feature_names[i] for i in selector.get_support(indices=True)]
        )
        text_features[id] = ids
        
        # Aggregate features by ID
        aggregated_text_features = text_features.groupby(id).mean().reset_index()

        return aggregated_text_features

    

# Example usage
# if __name__ == "__main__":
#     ps = TextProcessor("./data/comments.csv")
#     print(ps.vector_features)
