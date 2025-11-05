from typing import List

import spacy

from src.nlp_operations._absa import get_sentiment_data
from src.nlp_operations.gensim_similarity import get_similarity3, get_subcategories
from src.nlp_operations.ner import get_ner
from src.nlp_operations.pipelines import pipelines_ner
from src.nlp_operations.translation import detect_language, translate
from src.nlp_operations.utils import divide_text_to_sentences, process_sentiment_data
from src.twitter_tweepy.twitter_scraper import get_twitter_posts


def _ner(text):
    lang = detect_language(text)
    ne = get_ner(text, pipelines_ner[lang[0]["label"]])
    return ne


class AspectBasedSentimentAnalyzer:
    """Class for Aspect Based Sentiment Analysis."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # self.gensim_model = KeyedVectors.load_word2vec_format(
        #     # '../new_models/word2vec-google-news-300.model'
        #     "../../new_models/GoogleNews-vectors-negative300.bin",
        #     binary=True,
        #     # '../../fasttext-wiki-news-subwords-300'
        # )  # TODO: to działa?

    def get_preferences_from_text_data(self, text):
        """
        1. wyciagniecie aspektow z tekstu
        2. obliczenie podobienstwa do kategorii
        3. zwrocenie listy kategorii
        """
        lang = detect_language(text)  # detect language
        text = translate(text, lang[0]["label"])  # translate to english
        sentences = divide_text_to_sentences(text, self.nlp)
        sentiment_data = get_sentiment_data(sentences)
        list_of_aspects = process_sentiment_data(sentiment_data)
        return get_similarity3(list_of_aspects, self.gensim_model)

    async def get_preferences_from_twitter(self):
        """
        1. wyciagniecie aspektow z postow
        2. obliczenie podobienstwa do kategorii
        3. zwrocenie listy kategorii
        :return:
        """
        twitter_posts = await get_twitter_posts()
        subcategories = {}
        for post in twitter_posts:
            lang = detect_language(post)  # detect language
            post = translate(post, lang[0]["label"])  # translate to english
            sentences = divide_text_to_sentences(post, self.nlp)
            sentiment_data = get_sentiment_data(sentences)
            list_of_aspects = process_sentiment_data(sentiment_data)
            subcategories.update(get_subcategories(list_of_aspects, self.gensim_model))

        return subcategories

    def get_preferences_from_reviews(self, reviews: List[str]):
        """
        1. wyciagniecie aspektow z recenzji
        2. obliczenie podobienstwa do podkategorii
        3. zwrocenie listy podkategorii
        :param reviews:
        :return:
        """
        subcategories = {}  # set()
        for review in reviews:
            sentences = divide_text_to_sentences(review, self.nlp)
            sentiment_data = get_sentiment_data(sentences)
            list_of_aspects = process_sentiment_data(sentiment_data)
            subcategories.update(get_subcategories(list_of_aspects, self.gensim_model))

        return subcategories


if __name__ == "__main__":
    text = "Lubię jedzenie, ale obsługa była okropna."
    absa = AspectBasedSentimentAnalyzer()
    print(absa.get_preferences_from_text_data(text))
    # print(absa.get_preferences_from_reviews(["I love the food, but the service was terrible."]))
    # print(absa.get_preferences_from_twitter())
    # print(_ner(text))
