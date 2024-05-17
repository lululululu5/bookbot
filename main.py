def main():
    book_path = "books/frankenstein.txt"    
    text = get_book_text(book_path)
    num_words = get_num_words(text)
    letter_count = get_letter_count(text)
    list_dict = convert_dict(letter_count)
    print(f"--- Begin report of {book_path} ---")
    print(f"{num_words} words found in the document")
    print("\n")
    for d in list_dict:
        character = d["character"]
        num = d["num"]
        print(f"The '{character}' character was found {num} times")
    print("--- End report ---")
    
    

def get_book_text(path):
    with open(path) as f:
        return f.read()

def get_num_words(text):
    words = text.split()
    return len(words)

def get_letter_count(text):
    letter_dict = {}
    lower_text = text.lower()
    for s in lower_text:
        if s in letter_dict:
            letter_dict[s] += 1
        elif s.isalpha(): 
            letter_dict[s] = 1
    return letter_dict

def sort_on(dict):
    return dict["num"]

def convert_dict(input_dict):
    list_dict = [{"character": key, "num": value} for key, value in input_dict.items()]
    list_dict.sort(reverse=True, key=sort_on)
    return list_dict

main()
