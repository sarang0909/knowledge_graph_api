"""A Predictor module to load model and get prediction from custom spacy model.

"""


import spacy


class SpacyNerPredictor:
    """A class to load model and get output"""

    model = None

    def get_model(self):
        """A method to load model

        Returns:
            model: trained model
        """

        if self.model is None:
            self.model = spacy.load("src/models/spacy_model")
        return self.model

    def get_model_output(self, input_data):
        """A method to get model output from given text input
        Args:
            input_data (text):input text data

        Returns:
            output: model prediction
        """
        output = []
        doc = self.get_model()(input_data)

        for ent in doc.ents:
            output.append(
                {
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "label": ent.label_,
                }
            )
        return output
