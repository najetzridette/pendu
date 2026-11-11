import datetime
import random
import sys
import unicodedata

MAX_PENALTIES = 12
WRONG_WORD_PENALTY = 5
HIGHSCORE_FILE = "highscore.txt"


def normalize(text):
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def load_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: file not found:", filename)
        sys.exit(1)
    if not words:
        print("Error: the file is empty:", filename)
        sys.exit(1)
    return words


def show(secret, found):
    return " ".join(c if normalize(c) in found else "_" for c in secret)


def read_record():
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None
    records = []
    for line in lines:
        tries, date = line.split(";")
        records.append((int(tries), date))
    return min(records) if records else None


def save_record(tries):
    with open(HIGHSCORE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{tries};{datetime.date.today()}\n")


def play(secret):
    target = normalize(secret)
    found = set()
    penalties = 0
    tries = 0

    print(show(secret, found))
    while True:
        guess = normalize(input("Propose une lettre ou un mot : ").strip())
        if not guess:
            continue
        if len(guess) == 1 and guess in found:
            print("Tu as déjà proposé cette lettre.")
            continue

        tries += 1
        if len(guess) == 1:
            found.add(guess)
            if guess not in target:
                penalties += 1
        elif guess == target:
            return True, tries
        else:
            penalties += WRONG_WORD_PENALTY

        if all(c in found for c in target):
            return True, tries
        if penalties >= MAX_PENALTIES:
            return False, tries
        print(show(secret, found), "/ pénalités restantes :", MAX_PENALTIES - penalties)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pendu.py mots.txt")
        sys.exit(1)

    secret = random.choice(load_words(sys.argv[1]))
    print("Bienvenue dans le jeu du pendu ! Propose une lettre ou un mot à chaque tour.")
    print(f"Lettre fausse : 1 pénalité. Mot faux : {WRONG_WORD_PENALTY} pénalités. "
          f"Au bout de {MAX_PENALTIES} pénalités, tu as perdu.")

    won, tries = play(secret)
    if not won:
        print("Perdu ! Le mot était :", secret)
        return

    print(f"Bravo, tu as trouvé le mot {secret} en {tries} tentatives !")
    record = read_record()
    if record is None or tries < record[0]:
        save_record(tries)
        print("C'est le nouveau record !")
    else:
        print(f"Le record est de {record[0]} tentatives, établi le {record[1]}.")


if __name__ == "__main__":
    main()
