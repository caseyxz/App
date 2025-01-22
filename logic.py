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
        print(f"[DEBUG] Dataset {dataset_name} loaded successfully: {X.shape}, {len(y)} samples.")
        return X, y, f"Loaded dataset: {dataset_name} ({len(y)} samples)"
    except Exception as e:
        print(f"[ERROR] Failed to load dataset {dataset_name}: {str(e)}")
        return None, None, f"Error loading dataset: {str(e)}"


def run_algorithms_incrementally(X, y, selected_algorithms):
    """
    Uruchamia wybrane algorytmy na podanym zbiorze danych i zwraca wyniki krok po kroku.
    """
    try:
        # Podział danych na treningowe i testowe
        print("[DEBUG] Splitting dataset into training and testing sets.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        print(f"[DEBUG] Training set size: {X_train.shape}, Testing set size: {X_test.shape}")

        for algo_name in selected_algorithms:
            print(f"[INFO] Running algorithm: {algo_name}")
            if algo_name in ALGORITHMS:
                classifier = ALGORITHMS[algo_name]
                try:
                    # Trenowanie modelu
                    classifier.fit(X_train, y_train)
                    print(f"[DEBUG] Model {algo_name} trained successfully.")
                    # Predykcja na zbiorze testowym
                    y_pred = classifier.predict(X_test)
                    print(f"[DEBUG] Predictions for {algo_name} completed.")
                    # Obliczanie dokładności
                    accuracy = accuracy_score(y_test, y_pred)
                    print(f"[INFO] Algorithm {algo_name} achieved accuracy: {accuracy:.4f}")
                    yield algo_name, f"Accuracy: {accuracy:.4f}"  # Zwróć nazwę algorytmu i wynik
                except Exception as e:
                    print(f"[ERROR] Algorithm {algo_name} failed: {str(e)}")
                    yield algo_name, f"Error: {str(e)}"
            else:
                print(f"[WARN] Algorithm {algo_name} is not defined in the ALGORITHMS dictionary.")
                yield algo_name, "Algorithm not found"
    except Exception as e:
        print(f"[ERROR] Error during dataset processing: {str(e)}")
        yield "Error", f"Dataset processing error: {str(e)}"

def run_algorithms_in_thread():
    results = {}
    for algo_name, result in run_algorithms_incrementally(X, y, selected_algorithms):
        results[algo_name] = result
        display_results(results)
