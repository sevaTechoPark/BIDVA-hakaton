import string

class TextPreparetion:

    def __init__(self):
        self.punctuation_translater = str.maketrans('', '', string.punctuation)
        self.part_speech_words = ['а', 'в', 'но', 'и', 'не', 'из', 'под']

    def punctuation_delete(self, iText):
        return iText.translate(self.punctuation_translater)

    def part_speech_delete(self, iText):
        query_words = iText.split()
        result_words  = [word for word in query_words if word.lower() not in self.part_speech_words]
        return ' '.join(result_words)