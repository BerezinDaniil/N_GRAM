# N_GRAM
Generating texts using the n-gram model
The Gram class contains functions for getting data from a file, processing it (removing non-alphabetic characters, bringing it to lowercase and splitting text into words)
Also model training based on text from a file (Search for n grams , n = 1,2 )
Prediction based on the prefix of all possible next words and their probability.
Generating a text of a given length from the random word of the source text\ a given word, with this generation, the next word is selected randomly from all that will go after this prefix.
There is also a generation, where the word with the highest probability is chosen next.
There are also two trained models, one based on ATL texts and the other on Dostoevsky's "crime and punishment".
