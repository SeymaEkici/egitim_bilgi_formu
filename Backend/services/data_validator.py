from Backend.utils.log_utils import log_message, log_input
from thefuzz import fuzz, process  # Fuzzy string matching için

def check_missing_data(data):
    missing_keys = [key for key, value in data.items() if not value or value == "Veri Yok"]
    if missing_keys:
        log_message(f"Eksik veriler tespit edildi: {', '.join(missing_keys)}")
        return missing_keys
    else:
        log_message("Tüm veriler eksiksiz.")
        return []

def prompt_for_missing_data(data):
    missing_keys = check_missing_data(data)
    
    if missing_keys:
        user_choice = log_input("Eksik verileri elle doldurmak ister misiniz? (E/H): ")
        if user_choice.lower() == 'e':
            for key in missing_keys:
                new_value = log_input(f"{key} için bir değer girin: ")
                data[key] = new_value if new_value else "Veri Yok"
    
    return data
def find_best_match(key, choices, threshold=60):  
    """İsim benzerliği olan keyleri eşleştiriyor"""
    best_match, score = process.extractOne(key, choices, scorer=fuzz.token_sort_ratio)
    return best_match if score >= threshold else None