import random

# Lists of words for each line of the haiku
line1 = ["Autumn leaves rustle", "Cherry blossom petals fall", "A summer downpour"]
line2 = ["Softly to the ground below", "Whispers in the wind", "Glistening in the sun"]
line3 = ["Nature's way of letting go", "Beauty beyond measure", "A moment of peace"]

# Function to generate the haiku
def generate_haiku():
    haiku = ""
    haiku += random.choice(line1) + "\n"
    haiku += random.choice(line2) + "\n"
    haiku += random.choice(line3) + "\n"
    return haiku

# Example usage
print(generate_haiku())
