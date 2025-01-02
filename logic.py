from aeon.datasets import load_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier, ElasticEnsemble
from aeon.classification.convolution_based import RocketClassifier
from aeon.classification.feature_based import Catch22Classifier
from aeon.classification.interval_based import TimeSeriesForestClassifier, DrCIFClassifier
from aeon.classification.dictionary_based import ContractableBOSS, WEASEL
from aeon.classification.deep_learning import InceptionTimeClassifier
from aeon.classification.hybrid import HIVECOTEV1

# Lista algorytmów
ALGORITHMS = {
    "KNN": KNeighborsTimeSeriesClassifier(),
    "ROCKET": RocketClassifier(),
    "Catch22": Catch22Classifier(),
    "TimeSeriesForest": TimeSeriesForestClassifier(),
    "ContractableBOSS": ContractableBOSS(),
    "WEASEL": WEASEL(),
    "InceptionTime": InceptionTimeClassifier(),
    "HIVECOTEV1": HIVECOTEV1(),
    "DrCIF": DrCIFClassifier(),
    "ElasticEnsemble": ElasticEnsemble(),
}


def load_dataset(dataset_name):
    """
    Ładuje zestaw danych z AEON.
    """
    try:
        X, y = load_classification(dataset_name)
        return X, y, f"Loaded dataset: {dataset_name} ({len(y)} samples)"
    except Exception as e:
        return None, None, f"Error loading dataset: {str(e)}"


def run_algorithms_incrementally(X, y, selected_algorithms):
    """
    Uruchamia wybrane algorytmy na podanym zbiorze danych i zwraca wyniki krok po kroku.
    """
    try:
        # Podział danych na treningowe i testowe
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        for algo_name in selected_algorithms:
            if algo_name in ALGORITHMS:
                classifier = ALGORITHMS[algo_name]
                try:
                    # Trenowanie modelu
                    classifier.fit(X_train, y_train)
                    # Predykcja na zbiorze testowym
                    y_pred = classifier.predict(X_test)
                    # Obliczanie dokładności
                    accuracy = accuracy_score(y_test, y_pred)
                    yield algo_name, f"Accuracy: {accuracy:.4f}"  # Zwróć nazwę algorytmu i wynik
                except Exception as e:
                    yield algo_name, "Not compatible"
    except Exception as e:
        yield "Error", f"Dataset processing error: {str(e)}"
