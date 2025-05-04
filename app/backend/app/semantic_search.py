import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from text_preparetion import TextPreparetion

class SemanticSearch:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("deepvk/USER-bge-m3")
        self.model = AutoModel.from_pretrained("deepvk/USER-bge-m3")
        self.textPreparetion = TextPreparetion()
    
    #Метод поиска
    def search(self, iDocument, iWord):
        #Инициализируем словарь результата функции
        result = {
            'probability': 0.0,
            'startIndex': 0,
            'endIndex': 0
        }
        
        #Делим текст на пары
        segmentation_document = self.__prepare_document__(iDocument)
        #Собираем словарь сровнения пар с таргетом
        segment_probabilities = self.__compare_list_embeddings_(iWord, segmentation_document)
        #Получаем сегмент с наилучшим сходством
        best_similar_segment = self.__get_key_max_similar__(segment_probabilities)
        
        #Если лучшее решение меньше 67% точности, то считаем что ничего не нашли
        if segment_probabilities[best_similar_segment] <= 0.67:
            return result

        #В паре слов проверим каждое слово
        word_probabilities = self.__compare_list_embeddings_(iWord, best_similar_segment.split(' '))
        #Получаем слово с наилучшим сходством
        best_similar_word = self.__get_key_max_similar__(word_probabilities)

        #Проверяем что лучше сегмент или слово
        if segment_probabilities[best_similar_segment] > word_probabilities[best_similar_word]:
            result['probability'] = float(segment_probabilities[best_similar_segment])
            text_for_position =  best_similar_segment
        else:
            result['probability'] = float(word_probabilities[best_similar_word])
            text_for_position =  best_similar_word

        #Определим позицию в тексте
        start_index, end_index = self.__get_position_in_text__(iDocument, text_for_position)
        result['startIndex'] = start_index
        result['endIndex'] = end_index

        return result


    #Метод сегментации документа на пары слов
    def __prepare_document__(self, iDocument):
        #Удалим знаки препинания
        document = self.textPreparetion.punctuation_delete(iDocument)
        #Удалим служебные части речи
        document = self.textPreparetion.part_speech_delete(document)

        words_list = document.split(' ')
        segmentation_document = list()

        for index in range(len(words_list)):
            #Добавляем пару слов
            if index != len(words_list) - 1:
                segmentation_document.append(
                    words_list[index] + ' ' + words_list[index + 1]
                )
                
        if len(segmentation_document) == 0:
            segmentation_document.append(words_list[0])
            
        return(segmentation_document)

    #Метод получения векторного представления текста 
    def __get_bert_embedding__(self, iText):
        inputs = self.tokenizer(iText, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()
    
    def __compare_list_embeddings_(self, iTarget_text, iTexsts_list):
        probabilities = dict()
        
        #Переврдим в векторное представление целевой текст
        target_embedding = self.__get_bert_embedding__(iTarget_text)

        #Составляем словарь с вероятностями совпадений
        for segmrnt_text in iTexsts_list:
            segment_embedding = self.__get_bert_embedding__(segmrnt_text)
            similarity = cosine_similarity(target_embedding, segment_embedding)[0][0]
            probabilities[segmrnt_text] = similarity

        return probabilities
    
    #Метод для получения индекса слова максимального совпадения
    def __get_key_max_similar__(self, iProbabilities):

        if len(iProbabilities) == 1:
            return list(iProbabilities.keys())[0]
        else:
            return max(iProbabilities, key=iProbabilities.get)
    
    #Метод поиска позиции части текста в исходном документе
    def __get_position_in_text__(self, iMain_text, iFragment):
        strar_position = iMain_text.find(iFragment)
        end_position = strar_position + len(iFragment) - 1
        return strar_position, end_position