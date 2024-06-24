import password_guesser

# Create a new password guesser object
guesser = password_guesser.PasswordGuesser()

# Set the target password to guess
target = "sekret"

# Start guessing the password
guesses = guesser.guess(target)

# Print the guessed password
print(guesses[0])
