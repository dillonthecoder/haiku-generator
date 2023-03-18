# haiku-generator

This program generates potentially original haiku by using Markov chain analysis, a large set of haiku, nltk, and python. 

Haiku is a form of Japanese poetry, usually about nature, where the first line consists of five syllables, the second line consists of seven syllables, and the third and final line consists of five syllables. 

This program uses Markov chain analysis to start with a random word and then determine what a “good” next set of words might be based on the large set of haiku included with the “train.txt” file. The nltk module is used to help count the amount of syllables per line so that the poem generated can stay true to the haiku form of five, seven, and five syllables.

It doesn't always form coherent poems, and sometimes even produces an entire poem that was included with the training set. However, I’ve been happily surprised at how often it produces completely original and interesting haiku on its own.

There are still a few bugs I’m trying to work out but it’s definitely up and running and is capable of producing original haiku. Here's an example of one it created:


Forest in winter

Winds howl in rage and fury

Underneath the falls
