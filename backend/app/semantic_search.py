import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearch:

    def __init__(self):
        self.sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    #Метод поиска
    def search(self, iDocument, iWord):
        segmentation_document = self.__prepare_document__(iDocument)
        probabilities_index = dict()

        #Переводим в векторное представление подготовленный документ
        sentence_embeddings_doc = self.sbert_model.encode(segmentation_document)
        #Переврдим в векторное представление строку поиска
        sentence_embeddings_search = self.sbert_model.encode(iWord)

        #Составляем словарь с вероятностями совпадений
        for index in range(len(segmentation_document)):
            probabilities_index[index] = cosine_similarity(
                sentence_embeddings_search.reshape(1, -1),
                sentence_embeddings_doc[index].reshape(1, -1)
            )[0, 0]

        index_best_similar = self.__get_index_max_similar__(probabilities_index)
        start_index, end_index = self.__get_position_in_text__(iDocument, segmentation_document[index_best_similar])

        return {
            'probability': float(probabilities_index[index_best_similar]),
            'startIndex': start_index,
            'endIndex': end_index
        }


    #Метод сегментации документа на отдельные тексты
    def __prepare_document__(self, iDocument):
        words_list = iDocument.split(' ')
        segmentation_document = list()

        for index in range(len(words_list)):
            #Добавляем единичное слово
            segmentation_document.append(words_list[index])

            #Добавляем пару слов
            if index != len(words_list) - 1:
                segmentation_document.append(
                    words_list[index] + ' ' + words_list[index + 1]
                )
        
        return(segmentation_document)
    
    #Метод для получения индекса слова максимального совпадения
    def __get_index_max_similar__(self, iProbabilities):
        return max(iProbabilities, key=iProbabilities.get)
    
    #Метод поиска позиции части текста в исходном документе
    def __get_position_in_text__(self, iMain_text, iFragment):
        strar_position = iMain_text.find(iFragment)
        end_position = strar_position + len(iFragment) - 1
        return strar_position, end_position