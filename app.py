from flask import Flask, render_template, request, redirect, url_for
import random
app = Flask(__name__)

words = ['excelsior', 'adamantium', 'web shooters', 'gamma radiation', 'mjolnir', "x-men", "laser vision", "fantastic"]

hidden_word = ''
guessed_letters = []
attempts = 0

@app.route('/')
def home():
    return redirect(url_for('hangman_game'))

@app.route('/hangman_game')
def hangman_game():
    global hidden_word, guessed_letters, attempts
    hidden_word = random.choice(words)
    guessed_letters = []
    attempts = 0
    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts, guessed_letters = guessed_letters)

# TODO TASK 1
#  Implement logic that correctly processes the hidden_word and guessed_letters and
#  returns a string with letters revealed or hidden based on user guesses.
def get_display_word():
    global hidden_word, guessed_letters
    result = ""
    for c in hidden_word:
        if c in guessed_letters:
            result+=c
        elif c == " ":
            result+=" "
        else:
            result += "_"
    return result
# TODO TASK 2
#  Ensure that guesses are only added if they haven’t already been guessed.
#  Ensure that the function returns True for correct guesses and False for incorrect guesses.
def check_correct_guess(input_letter):
    global guessed_letters
    input_letter = input_letter.lower()
    if input_letter == " ":
        return None
    if input_letter in guessed_letters:
        return None
    guessed_letters.append(input_letter)
    if input_letter in hidden_word:
        return True
    else:
        return False
# TODO TASK 3
#  Implement the logic that tracks the number of attempts and determines if
#  the player has lost (attempts ≥ 6).
def check_lose():
    global attempts
    return attempts >=6
# TODO TASK 4
#  Ensure that the function correctly checks if all letters in hidden_word are
#  in the guessed_letters.
def check_win():
    global hidden_word, guessed_letters
    for letter in hidden_word:
        if letter !=" " and letter not in guessed_letters:
            return False
    return True
@app.route('/guess', methods=['POST'])
def guess():
    global hidden_word, attempts

    guessed_letter = request.form['letter']

    if not check_correct_guess(guessed_letter):
        attempts += 1

    if check_lose():
        return render_template('lose.html', word=hidden_word)

    if check_win():
        return render_template('win.html', word=hidden_word)

    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts, guessed_letters = guessed_letters)

if __name__ == '__main__':
    app.run(debug=True)
