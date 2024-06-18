# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JmAIenZKg8-gm-wkmO_De_GYzwBBTeXz
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from nltk.tokenize import word_tokenize
import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
import matplotlib.pyplot as plt



# Загрузка и вывод данных
df = pd.read_excel('VA.xlsx')
#df.head(17)
#df.info(17)

df = df.rename(columns={'На первый взгляд, насколько вам нравится дизайн этого прототипа?': 'design',
                        'Как вы оцениваете удобство навигации по прототипу?': 'navigation',
                        'На что вы сразу обратили внимание при первом просмотре прототипа?': 'first_view',
                        'Нашли ли вы всю необходимую информацию без помощи других?': 'necessary_info',
                        'Были ли какие-либо элементы интерфейса, которые вы нашли особенно трудными для понимания или использования?': 'difficult_elements',
                        'После тестирования прототипа, насколько вероятно, что вы бы рекомендовали этот продукт другим?': 'prototype',
                        'Как бы вы в целом предпочли взаимодействовать с виртуальным помощником в банке: через голосовые команды, чат-интерфейс, или возможно, другие методы?' : 'interaction'
})


#Медиана оценки дизайна
df['design'] = df['design']
print('Медиана оценки дизайна', df['design'].median().astype(int))

#Медиана удобства навигации по прототипу
df['navigation'] = df['navigation']
print('Медиана удобства навигации по прототипу', df['navigation'].median().astype(int))

#Медиана рекомендации продукта
df['prototype'] = df['prototype']
print('Медиана рекомендации продукта', df['prototype'].median().astype(int))



#Создаем экземпляры токенизатора и модели для классификации последовательностей
tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment', return_dict=True)

#
def predict(text):
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted

#Случайные ответы
sample = pd.DataFrame()
sample = df[['first_view']].sample(17)
sample['prediction'] = sample['first_view'].apply(predict)

sample1 = pd.DataFrame()
sample1 = df[['difficult_elements']].sample(17)
sample1['prediction'] = sample1['difficult_elements'].apply(predict)
print(sample)
print(sample1)

#Визуализация данных первого вопроса в опроснике
design_counts = df['design'].value_counts()
plt.hist(df['design'], bins=len(design_counts), align='left', rwidth=0.7, color='lightblue')
plt.title('На первый взгляд, насколько вам нравится дизайн этого прототипа?', fontsize=10, color='green')
plt.xticks(range(len(df['design'])), df['design'].index)
plt.xlabel('Оценка дизайна')
plt.ylabel('Количество')
plt.legend(['Количество оценок'])
plt.show()

#Визуализация данных второго вопроса в опроснике
navigation_counts = df['navigation']
plt.hist(df['navigation'], bins=len(design_counts), align='left', rwidth=0.5, color='blue')
plt.title('Как вы оцениваете удобство навигации по прототипу?', fontsize=10, color='green')
plt.xticks(range(1, 8), range(1, 8))
plt.xlabel('Оценка навигации')
plt.ylabel('Количество')
plt.legend(['Количество оценок'])
plt.show()

#Визуализация данных третьего вопроса в опроснике(На что вы сразу обратили внимание при первом просмотре прототипа?)
data = {
    'first_view': ['Простота дизайна', 'Возможность голосового запроса', 'На расположение элементов', 'Возможность создания чека/автоплатежа/шаблона'],
    'count': [25, 35, 20, 30]
}
plt.pie(data['count'], labels=data['first_view'], colors=['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue'], autopct='%1.1f%%')
plt.title('На что вы сразу обратили внимание при первом просмотре прототипа?', fontsize=10, color='green')
plt.show()

#Визуализация данных четвертого вопроса в опроснике 0 - нет, 1 - да
necessary_counts = df['necessary_info']
plt.hist(df['necessary_info'], bins=len(necessary_counts), align='left', rwidth=0.5, color='lightblue')
plt.title('Нашли ли вы всю необходимую информацию без помощи других?', fontsize=10, color='green')
plt.xticks(range(1, 3), range(1, 3))
plt.xlabel('Вся ли отображается необходимая информация в прототипе')
plt.ylabel('Количество')
plt.legend(['Количество оценок'])
plt.show()

#Визуализация данных шестого вопроса в опроснике
prototype_counts = df['prototype']
plt.hist(df['prototype'], bins=len(design_counts), align='left', rwidth=0.5, color='blue')
plt.title('После тестирования прототипа, насколько вероятно, что вы бы рекомендовали этот продукт другим?', fontsize=10, color='green')
plt.xticks(range(1, 8), range(1, 8))
plt.xlabel('Насколько рекомендовали ли бы респонденты данный прототип')
plt.ylabel('Количество')
plt.legend(['Количество оценок'])
plt.show()

#Визуализация данных седьмого вопроса в опроснике
data = {
    'interaction': ['Чат-интерфейс', 'Через голосовые команды'],
    'count': [78, 22]
}
colors = ['lightblue', 'lightgreen', 'lightcoral']
plt.pie(data['count'], labels=data['interaction'], colors=colors, autopct='%1.1f%%')
plt.title('Как бы вы в целом предпочли взаимодействовать с виртуальным помощником в банке: через голосовые команды, чат-интерфейс, или возможно, другие методы?', fontsize=10, color='green')
plt.show()


# Лингвистический анализ с помощью библиотеки NLTK
reviews_tokenized = [word_tokenize(row) for row in df['difficult_elements'].astype(str)]
#nltk.download('punkt')
print(reviews_tokenized)


# Загружаем лемматизатор и список стоп-слов для русского языка:
mystem = Mystem()
russian_stopwords = stopwords.words('russian')

stop_words = set(stopwords.words('russian'))

def preprocess_text(review):
    # Лемматизируем токены, приводим их к нижнему регистру
    tokens = mystem.lemmatize(review.lower())
    # Пропускаем токен, если он пустой или находится в списке стоп-слов
    clean_tokens = []
    for token in tokens:
        if token not in russian_stopwords and token != " " and token.strip() not in punctuation:
            clean_tokens.append(token)
    # Объединяем токены назад в текст
    review = " ".join(clean_tokens)
    return review
russian_stopwords.append('ещё одно стоп-слово')