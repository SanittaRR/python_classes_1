class CountVectorizer:
    """Convert a collection of text documents to a matrix of token counts"""

    def __init__(self):
        self._vocabulary = {}

    def fit_transform(self, text: list) -> list:
        """Learn the vocabulary dictionary and return document-term matrix"""
        from collections import Counter

        dicts_list = []
        words_list = []
        for sentence in text:
            count = Counter(sentence.lower().split())
            words_list += list(count)
            dicts_list.append(dict(count))

        words_list = sorted(set(list(words_list)), key=list(words_list).index)
        self._vocabulary = words_list

        matrix_list = []
        for sub_dict in dicts_list:
            full_dict = dict.fromkeys(words_list, 0)
            full_dict.update(sub_dict)
            matrix_list.append(list(full_dict.values()))

        return matrix_list

    def tf_transform(self, text: list):
        final = []
        for i in self.fit_transform(text):
            final.append([round((j / sum(i)), 3) for j in i])
        return final

    def idf_transform(self, text: list):
        import math
        total_docs = len(text)
        dict_repeat = dict.fromkeys(list(self._vocabulary), 0)
        for i in text:
            for j in dict_repeat.keys():
                if j in i.lower().split():
                    dict_repeat[j] += 1
        return [round((math.log((total_docs + 1) / (k + 1)) + 1), 1) for k in dict_repeat.values()]

    def get_feature_names(self) -> list:
        """Get output feature names for transformation"""
        return list(self._vocabulary)


class TfidTransformer:
    def fit_transform(self: list):
        vectoriz = CountVectorizer()
        tf_matrix2 = vectoriz.tf_transform(self)
        idf_matrix2 = vectoriz.idf_transform(self)
        new = []
        for i in tf_matrix2:
            sub_l = [round(a * b, 3) for a, b in zip(i, idf_matrix2)]
            new.append(sub_l)
        return new


class TfidfVectorizer2(CountVectorizer, TfidTransformer):
    def __init__(self):
        super().__init__()

    def fit_transform(self, text: list) -> list:
        tfidf_matr = TfidTransformer.fit_transform(text)
        return tfidf_matr


class TfidfVectorizer:

    def __init__(self):
        self._vocabulary = {}

    def fit0_transform(self, text: list) -> list:
        """Learn the vocabulary dictionary and return document-term matrix"""
        from collections import Counter

        dicts_list = []
        words_list = []
        for sentence in text:
            count = Counter(sentence.lower().split())
            words_list += list(count)
            dicts_list.append(dict(count))

        words_list = sorted(set(list(words_list)), key=list(words_list).index)
        self._vocabulary = words_list

        matrix_list = []
        for sub_dict in dicts_list:
            full_dict = dict.fromkeys(words_list, 0)
            full_dict.update(sub_dict)
            matrix_list.append(list(full_dict.values()))

        return matrix_list

    def get_feature_names(self) -> list:
        """Get output feature names for transformation"""
        return list(self._vocabulary)

    def tf_transform(self, text: list):
        transformed_list = []
        for i in self.fit0_transform(text):
            transformed_list.append([round(j / (sum(i)), 3) for j in i])
        return transformed_list

    def idf_transform(self, text: list):
        import math
        total_docs = len(text)
        dict_repeat = dict.fromkeys(list(self._vocabulary), 0)
        for i in text:
            for j in dict_repeat.keys():
                if j in i.lower().split():
                    dict_repeat[j] += 1
        return [round(math.log((total_docs + 1) / (k + 1)) + 1, 1) for k in dict_repeat.values()]

    def fit_transform(self, text: list):
        tf_matrix3 = self.tf_transform(text)
        idf_matrix3 = self.idf_transform(text)
        new = []
        for i in tf_matrix3:
            sub_l = [round(a * b, 3) for a, b in zip(i, idf_matrix3)]
            new.append(sub_l)
        return new


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
                                              'fresh', 'ingredients', 'parmesan', 'to', 'taste']
    tf_matrix = vectorizer.tf_transform(corpus)
    assert tf_matrix == [[0.143, 0.143, 0.286, 0.143, 0.143, 0.143, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0.143, 0, 0, 0, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143]]
    idf_matrix = vectorizer.idf_transform(corpus)
    assert idf_matrix == [1.4, 1.4, 1.0, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    assert vectorizer.get_feature_names() == ['crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
                                              'fresh', 'ingredients', 'parmesan', 'to', 'taste']
    assert tfidf_matrix == [[0.2, 0.2, 0.286, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0.143, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
