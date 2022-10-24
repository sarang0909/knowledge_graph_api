"""A module for information extraction
"""

import spacy
from transformers import pipeline
import pandas as pd

from src.inference.entity_linking import perform_wikification

custom_ner_model = spacy.load("src/models/spacy_model")
triplet_extractor = pipeline(
    "text2text-generation",
    model="Babelscape/rebel-large",
    tokenizer="Babelscape/rebel-large",
    device=-1,
)

# https://github.com/Babelscape/rebel
def extract_triplets(text):
    """Function to parse the generated text and extract the triplets from babel


    Args:
        text (str): Input text

    Returns:
        dict: triplets
    """
    triplets = []
    subject, relation, object_ = "", "", ""
    text = text.strip()
    current = "x"
    for token in (
        text.replace("<s>", "")
        .replace("<pad>", "")
        .replace("</s>", "")
        .split()
    ):
        if token == "<triplet>":
            current = "t"
            if relation != "":
                triplets.append(
                    {
                        "subject": subject.strip(),
                        "relation": relation.strip(),
                        "object": object_.strip(),
                    }
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                triplets.append(
                    {
                        "subject": subject.strip(),
                        "relation": relation.strip(),
                        "object": object_.strip(),
                    }
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        triplets.append(
            {
                "subject": subject.strip(),
                "relation": relation.strip(),
                "object": object_.strip(),
            }
        )
    return triplets


def triple_generation(text, only_custom_entities=False):
    """A method to processbabel generated output with wikification and NERstr

    Args:
        text (str): Input text
        only_custom_entities (bool, optional): to extract relationship only for custom entities. Defaults to False.

    Returns:
        Dataframe: triplets dataframe
    """

    df = pd.DataFrame(columns=["subject", "object", "relation"])
    knowledge_base = dict()
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    for sent in doc.sents:
        # We need to use the tokenizer manually since we need special tokens.
        extracted_text = triplet_extractor.tokenizer.batch_decode(
            [
                triplet_extractor(
                    sent.text, return_tensors=True, return_text=False
                )[0]["generated_token_ids"]
            ]
        )
        extracted_triplets = extract_triplets(extracted_text[0])
        for triple in extracted_triplets:
            subject = triple["subject"]
            obj = triple["object"]
            # If we need extract relaions of only custom entities
            if only_custom_entities:
                doc = custom_ner_model(text)
                custom_entities = [i.text for i in doc.ents]
                # If either subject or object not presentin custom entities list then set them as None,ignore them
                if not any(x in [subject, obj] for x in custom_entities):
                    subject = None
                    obj = None

            if None not in [subject, obj]:
                # Get wiki id and add to existing knowledge base
                # If it is already present then use existing id fromknowledge base.
                # This logic will avoid duplication and use first occurance of entity as a reference
                entity_wiki_id = perform_wikification(subject)
                if entity_wiki_id in knowledge_base:
                    subject = knowledge_base[entity_wiki_id]
                else:
                    knowledge_base[entity_wiki_id] = subject

                entity_wiki_id = perform_wikification(obj)
                if entity_wiki_id in knowledge_base:
                    obj = knowledge_base[entity_wiki_id]
                else:
                    knowledge_base[entity_wiki_id] = obj

                df = df.append(
                    {
                        "subject": subject,
                        "object": obj,
                        "relation": triple["relation"],
                    },
                    ignore_index=True,
                )

    return df
