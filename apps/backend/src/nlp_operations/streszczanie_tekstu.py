from transformers import BartTokenizer, BartForConditionalGeneration


def summarize_text():
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    text = """The US has "passed the peak" on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month.
    The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world.
    At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors.
    "We'll be the comeback kids, all of us," he said. "We want to get our country back."
    The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.
    """

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    print(summary)
    return summary
