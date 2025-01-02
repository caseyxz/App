# Importy modułów klasyfikatorów
import aeon.classification.distance_based as distance
import aeon.classification.convolution_based as convolution
import aeon.classification.feature_based as feature
import aeon.classification.interval_based as interval
import aeon.classification.dictionary_based as dictionary
import aeon.classification.deep_learning as deep
import aeon.classification.hybrid as hybrid

# Funkcja pomocnicza do wypisania dostępnych klas
def list_classes(module, module_name):
    print(f"Classes in {module_name}:")
    print([cls for cls in dir(module) if not cls.startswith("_")])
    print()

# Sprawdzanie wszystkich modułów klasyfikatorów
list_classes(distance, "distance_based")
list_classes(convolution, "convolution_based")
list_classes(feature, "feature_based")
list_classes(interval, "interval_based")
list_classes(dictionary, "dictionary_based")
list_classes(deep, "deep_learning")
list_classes(hybrid, "hybrid")


