import spacy


def get_ner(text, country_language):
    # nlp = spacy.load(country_language)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lst = []
    for ent in doc.ents:
        lst.append(ent.text)
    # return doc.ents
    return lst


def _test():
    text = ("I want to visit Warsaw. I am going to buy a ticket to the National Museum. "
            "Also, I want to see the Royal Castle. I heard that the Old Town is beautiful. "
            "I really liked Wawel. Elon Musk, the CEO of Tesla, announced a new electric vehicle model ")

    print(get_ner(text, "english"))

# _test()