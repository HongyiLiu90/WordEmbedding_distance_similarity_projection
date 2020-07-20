# WordEmbedding_distance_similarity_projection

This repository provides the Python code for calculating the distance, similarity, analogy, and projection between wordembeddings based on the three horses, Wor2Vec, fastText, and Glove.


# Training method: Word2Vec, fastText, and Glove

These three learning algorithms are implemented to train 9 different language data, including simplified Chinese, British English, American English, French, German, Hebrew, Italian, Russian, and Spanish. Some feature key words of these languages are also provided in the code as dictionary format.

# Input and Output

Input file is the training model obtained from the learning process on the original data. This 'WordEmbedding' code will output the product of distance between two words, cosine similarity between two words, return value of most similar word from embedding operation (e.g. queen = king + women - men), and the cosine similarity of a feature word embedding projected onto the difference between other two antonyms.
