import numpy as np
import re
import joblib


# helper function
def save_model(model, file_name: str) -> None:
    """
    Saving a trained model
    :param model: The model you want to save
    :param file_name: the name under which to save the model
    :return: None
    """
    joblib.dump(model, f'{file_name}.pkl')
    print("The model has been saved successfully")


def load_model(file_name: str):
    """
    Loading the trained model
    :param file_name: the name of the file with the model you want to upload
    :return: None
    """
    print("The model has been loaded successfully")
    return joblib.load(f'{file_name}.pkl')


# Class Description
class NGram:
    def __init__(self, n: int = 1):
        """

        :param n:
        """
        self.n = n
        self.data = None
        self.data_dict = None
        self.dict_train = {}

    def fit(self, text_data):
        """
        :param text_data:
        :return:
        """
        self.data = np.array(text_data)

    @staticmethod
    def get_data(file_name: str) -> list:
        """
        Getting data from a file and writing it to an array

        :param file_name: file name(located in the same directory)
        :return: filtered and word-broken text
        """
        text_data = []
        reg = re.compile('[^а-яёА-ЯЁ 0-9]')
        with open(f"{file_name}", 'r', encoding='utf-8') as data_file:
            while True:
                line = data_file.readline()
                if not line:
                    break
                else:
                    for word in line.lower().split():
                        word_new = reg.sub('', word)
                        if word_new != '':
                            word_new = word_new.split()[0]
                            text_data.append(word_new)
        return text_data

    def convert_data(self) -> dict:
        """
        Creating a dictionary with a prefix key and a value list of words that can go after it

        :return: dictionary with a prefix key and a value list of words that can go after it
        """
        self.data_dict = {}
        if self.n == 1:
            for index in range(len(self.data) - self.n):
                seq = self.data[index:index + self.n]
                if seq[0] not in self.data_dict.keys():
                    self.data_dict[seq[0]] = []
                self.data_dict[seq[0]].append(self.data[index + self.n])
            return self.data_dict
        elif self.n == 2:
            for index in range(len(self.data) - self.n):
                seq = self.data[index:index + self.n]
                if seq[0] + " " + seq[1] not in self.data_dict.keys():
                    self.data_dict[seq[0] + " " + seq[1]] = []
                self.data_dict[seq[0] + " " + seq[1]].append(self.data[index + self.n])
            return self.data_dict

    def convert_frequency(self, new_seq: str) -> list:
        """
        Probability calculation for each word following the prefix

        :param new_seq: the prefix for which to predict the next word
        :return: array of tuples [(next word, probability), (other next word, probability), ...]
            or 'I do not know the given word or phrase' if if this prefix is not in the training sample
        """
        prediction = []
        if new_seq.lower() in self.data_dict.keys():
            for word in self.data_dict[new_seq]:
                prediction.append((word, np.count_nonzero(np.array(self.data_dict[new_seq]) == word) / len(
                    self.data_dict[new_seq])))
            return list(set(prediction))

    def train(self) -> dict:
        """

        :return:
        """
        for new_gram in self.data_dict.keys():
            print("Trained on words:", len(self.dict_train), "/", len(self.data_dict))  # Переименовать
            self.dict_train[new_gram] = self.convert_frequency(new_gram)
        return self.dict_train

    def predict(self, gram: str) -> list or str:
        """

        :param gram:
        :return:
        """
        if gram in self.dict_train.keys():
            return self.dict_train[gram]
        else:
            return 'I do not know the given word or phrase'

    def generating_text(self, length: int = 0, prefix: str = '') -> str:
        """
        Generates a text of a given length based on a training sample (sampling random values from possible prefixes)
        By default, the length of the generated text is equal to the length of the training text

        :param prefix: optional argument. The beginning of a sentence (one or more words). If not specified, select the
        initial word randomly from all the words
        :param length: the length of the generated sequence.
        :return: generated text
        """
        text = []
        if len(prefix) == 0:
            i = np.random.choice(len(self.data) - self.n)
            first_words = " ".join(self.data[i:i + self.n])
        else:
            first_words = prefix
        text.append(first_words)
        if not length:
            length = len(self.data)
        while len(text) < length:
            if self.predict(first_words) != 'I do not know the given word or phrase':
                index = np.random.choice(len(self.predict(first_words)))
                new_word = self.predict(first_words)[index][0]
                text.append(new_word)
                print("Predicted words:", len(text), "/", length)
            else:
                print(f'I do not know this word: "{first_words}"')
                break
            if self.n == 2:
                first_words = " ".join([first_words.split()[-1], new_word])
            elif self.n == 1:
                first_words = new_word
        return " ".join(text)

    @staticmethod
    def max_probability(array):
        """
        Finding the index of the word with the highest probability of following the prefix
        :param array: array of all words that can come after the prefix
        :return: index of the most likely word
        """
        index = 0
        probability = -1
        for i in range(len(array)):
            if array[i][1] > probability:
                probability = array[i][1]
                index = i
        return index

    def probabilistic_generation(self, *prefix: str, length: int = 0) -> str:
        """
        Text generation in which the word following the prefix is chosen not randomly, but the word with the highest
        probability
        :param prefix: optional argument. The beginning of a sentence (one or more words). If not specified, select the
        initial word randomly from all the words
        :param length: the length of the generated sequence.
        :return: generated text
        """
        text = []
        if len(prefix) == 0:
            i = np.random.choice(len(self.data) - self.n)
            first_words = " ".join(self.data[i:i + self.n])
        else:
            first_words = prefix
        text.append(first_words)
        if not length:
            length = len(self.data)
        while len(text) < length:
            if self.predict(first_words) != 'I do not know the given word or phrase':
                index = self.max_probability(self.predict(first_words))
                new_word = self.predict(first_words)[index][0]
                text.append(new_word)
                print("Predicted words:", len(text), "/", length)
            else:
                break
            if self.n == 2:
                first_words = " ".join([first_words.split()[-1], new_word])
            elif self.n == 1:
                first_words = new_word
        return " ".join(text)
