from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess_number', methods=['GET', 'POST'])
def guess_number():
    if 'number_to_guess' not in session:
        session['number_to_guess'] = random.randint(1, 100)
    
    message = ''
    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
            if guess < session['number_to_guess']:
                message = 'Your guess is low!'
            elif guess > session['number_to_guess']:
                message = 'Your guess is high!'
            else:
                message = 'Congratulations! You guessed the number.'
                session.pop('number_to_guess', None)
        except ValueError:
            message = 'Please enter a valid number.'
            
    return render_template('game.html', game_title='Guess the Number', message=message)

@app.route('/roll_dice', methods=['GET', 'POST'])
def roll_dice():
    result = None
    if request.method == 'POST':
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        result = f"({die1}, {die2})"
    return render_template('game.html', game_title='Roll Two Dice', result=result)

@app.route('/coin_flip', methods=['GET', 'POST'])
def coin_flip():
    if 'heads' not in session:
        session['heads'] = 0
        session['tails'] = 0
        
    result = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'flip':
            result = random.choice(["Heads", "Tails"])
            if result == "Heads":
                session['heads'] += 1
            else:
                session['tails'] += 1
        elif action == 'reset':
            session['heads'] = 0
            session['tails'] = 0
            
    stats = f"Heads: {session['heads']} | Tails: {session['tails']}"
    return render_template('game.html', game_title='Coin Flip', result=result, stats=stats)

@app.route('/rps', methods=['GET', 'POST'])
def rock_paper_scissors():
    if 'user_wins' not in session:
        session['user_wins'] = 0
        session['computer_wins'] = 0
        
    message = ''
    options = {"r": "rock", "p": "paper", "s": "scissors"}
    
    if request.method == 'POST':
        user_input = request.form.get('choice')
        if user_input in options:
            user_pick = options[user_input]
            computer_pick = random.choice(list(options.values()))
            
            if (user_pick, computer_pick) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
                message = f"Computer picked {computer_pick}. You won!"
                session['user_wins'] += 1
            elif user_pick == computer_pick:
                message = f"Computer picked {computer_pick}. It's a tie!"
            else:
                message = f"Computer picked {computer_pick}. You lost!"
                session['computer_wins'] += 1
                
    stats = f"Score - You: {session['user_wins']} | Computer: {session['computer_wins']}"
    return render_template('game.html', game_title='Rock Paper Scissors', message=message, stats=stats, rps=True)

@app.route('/guess_word', methods=['GET', 'POST'])
def guess_word():
    word_hints = {
        "python": "A popular programming language named after a snake",
        "banana": "A long curved yellow fruit",
        "guitar": "A musical instrument with strings",
        "planet": "A large celestial body orbiting a star",
        "window": "An opening in a wall to let in light and air",
        "rocket": "A spacecraft designed to travel into space"
    }
    
    if 'secret_word' not in session or 'word_hint' not in session:
        word = random.choice(list(word_hints.keys()))
        session['secret_word'] = word
        session['word_hint'] = word_hints[word]
        session['guessed_letters'] = []
        session['lives'] = 6

    message = ''
    word = session['secret_word']
    hint = session.get('word_hint', 'A mystery word')
    guessed = session.get('guessed_letters', [])
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'reset':
            session.pop('secret_word', None)
            session.pop('word_hint', None)
            session.pop('guessed_letters', None)
            session.pop('lives', None)
            return redirect(url_for('guess_word'))
            
        guess = request.form.get('letter', '').lower()
        if len(guess) != 1 or not guess.isalpha():
            message = "Please enter a single letter."
        elif guess in guessed:
            message = "You already guessed that!"
        else:
            guessed.append(guess)
            session['guessed_letters'] = guessed
            if guess in word:
                message = "Good guess!"
            else:
                session['lives'] -= 1
                message = "Wrong guess!"

    display = "".join([l + " " if l in guessed else "_ " for l in word])
    game_over = session.get('lives', 6) <= 0 or "_" not in display
    
    return render_template('game.html', game_title='Guess the Word', display=display, lives=session.get('lives', 6), message=message, game_over=game_over, word=word, hint=hint)

if __name__ == '__main__':
    app.run(debug=True)