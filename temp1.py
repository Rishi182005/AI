from collections import Counter

def get_most_common_word(file_path):
    with open(file_path, 'r') as file:
        text = file.read().lower().split()
        word_counts = Counter(text)
        most_common_word, _ = word_counts.most_common(1)[0]
        return most_common_word

# Example usage
file_path = r'C:\Users\rishi\OneDrive\Desktop\college\fall_sem_24-25\ai\j_comp\d_english.txt'
most_common_word = get_most_common_word(file_path)
print(f"The most common word in the file is: {most_common_word}")
