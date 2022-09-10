# N_GRAM
Generating texts using the n-gram model The Gram class contains functions for obtaining data from a file, processing them (removing non-alphabetic characters, bringing them into lowercase and dividing the text into words)
Also simulate learning based on text from a file (Search by n grams, n = 1,2)
Prediction based on the prefix of all possible next words and their probabilities.
Generating a text of a given length from a random word of the source text of a given word, during this generation, the next word is randomly selected from everything that will go after this prefix.
There is also a text generation function (probabilistic_generation), where the word with the highest probability is selected next.
There are also two trained models, one of which is based on ATL texts (atl_1 and atl_2), and the other is based on Tolstoy's war and peace (war_and_peace_1).
The numbers in the model name mean which n-gram they are trained on.
The probabilistic_generation function does not work well with large texts, because it loops over stable phrases such as it would be and so on(This function is not in generate).
