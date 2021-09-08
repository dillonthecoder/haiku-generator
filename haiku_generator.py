import sys
import logging
import random
from collections import defaultdict
from syllable_counter import count_syllables


def load_training_file(file):
    with open(file) as f:
        raw_haiku = f.read()
        return raw_haiku


def prep_training(raw_haiku):
    corpus = raw_haiku.replace('\n', ' ').split()
    return corpus


def map_word_to_word(corpus):
    limit = len(corpus) - 1
    dict1_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            suffix = corpus[index + 1]
            dict1_to_1[word].append(suffix)
    return dict1_to_1


def map_two_words_to_word(corpus):
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word + ' ' + corpus[index + 1]
            suffix = corpus[index + 2]
            dict2_to_1[key].append(suffix)
    logging.debug("map_2_words_to_word results for \"sake jug\" = %s\n", dict2_to_1['sake jug'])
    return dict2_to_1


def random_word(corpus):
    word = random.choice(corpus)
    num_syllables = count_syllables(word)
    if num_syllables > 4:
        random_word(corpus)
    else:
        return word, num_syllables


def word_after_single(prefix, suffix_map_1, current_syllables, target_syllables):
    accepted_words = []
    suffixes = suffix_map_1.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            num_syllables = count_syllables(candidate)
            if current_syllables + num_syllables <= target_syllables:
                accepted_words.append(candidate)
    return accepted_words


def word_after_double(prefix, suffix_map_2, current_syllables, target_syllables):
    accepted_words = []
    suffixes = suffix_map_2.get(prefix)
    if suffixes is not None:
        for candidate in suffixes:
            num_syllables = count_syllables(candidate)
            if current_syllables + num_syllables <= target_syllables:
                accepted_words.append(candidate)
    return accepted_words


def haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line, target_syllables):
    line = '2/3'
    line_syllables = 0
    current_line = []
    if len(end_prev_line) == 0:  # Builds the first line
        line = '1'
        word, num_syllables = random_word(corpus)
        current_line.append(word)
        line_syllables += num_syllables
        word_choices = word_after_single(word, suffix_map_1, line_syllables, target_syllables)

        while len(word_choices) == 0:
            prefix = random.choice(corpus)
            logging.debug("new random prefix = %s", prefix)
            word_choices = word_after_single(prefix, suffix_map_1, line_syllables, target_syllables)

        word = random.choice(word_choices)
        num_syllables = count_syllables(word)
        logging.debug("word and syllables = %s %s", word, num_syllables)
        line_syllables += num_syllables
        current_line.append(word)

        if line_syllables == target_syllables:
            end_prev_line.extend(current_line[-2:])
            return current_line, end_prev_line

    else:  # Build lines 2 and 3
        current_line.extend(end_prev_line)

    while True:
        prefix = current_line[-2] + ' ' + current_line[-1]
        word_choices = word_after_double(prefix, suffix_map_2, line_syllables, target_syllables)

        while len(word_choices) == 0:
            index = random.randint(0, len(corpus) - 2)
            prefix = corpus[index] + ' ' + corpus[index + 1]
            word_choices = word_after_double(prefix, suffix_map_2, line_syllables, target_syllables)

        word = random.choice(word_choices)
        num_syllables = count_syllables(word)

        if line_syllables + num_syllables > target_syllables:
            continue
        elif line_syllables + num_syllables < target_syllables:
            current_line.append(word)
            line_syllables += num_syllables
        elif line_syllables + num_syllables == target_syllables:
            current_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(current_line[-2:])

    if line == '1':
        final_line = current_line[:]
    else:
        final_line = current_line[2:]

    return final_line, end_prev_line


def main():
    raw_haiku = load_training_file('train.txt')
    corpus = prep_training(raw_haiku)
    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_two_words_to_word(corpus)
    final = []

    choice = None
    while choice != '0':

        print(
            """
Haiku Generator

0 - Quit
1 - Generate a Haiku
2 - Regenerate Line 2
3 - Regenerate Line 3
            """
        )

        choice = input('Choice: ')
        print()

        # Exit
        if choice == '0':
            print('Goodbye')
            sys.exit()

        # Generate a Full Haiku
        elif choice == '1':
            final = []
            end_prev_line = []

            first_line, end_prev_line1 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line, 5)
            final.append(first_line)

            line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7)
            final.append(line)

            line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5)
            final.append(line)

        # Regenerate Line 2
        elif choice == '2':
            if not final:
                print('Please generate a full haiku first (Option 1).')
                continue
            else:
                line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7)
                final[1] = line

        # Regenerate Line 3
        elif choice == '3':
            if not final:
                print('Please generate a full haiku first (Option 1).')
                continue
            else:
                line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5)
                final[2] = line

        # Unknown Choice
        else:
            print('\nSorry that is not a valid input.')
            continue

        # Display results
        print(' '.join(final[0]), file=sys.stderr)
        print(' '.join(final[1]), file=sys.stderr)
        print(' '.join(final[2]), file=sys.stderr)

        input('\n\nPress "Enter" key to exit.')


if __name__ == '__main__':
    main()
