"""A core module to get knoweldge graph output
"""


from src.inference.coreference_resolution import get_coref_resolution
from src.inference.information_extraction import triple_generation


def generate_output(text):
    """A method to generate output

    Args:
        text (str): Input text

    Returns:
        Dataframe: Information Extraction dataframe
    """

    resolved_output = get_coref_resolution(text)
    output_df = triple_generation(resolved_output)
    return output_df
