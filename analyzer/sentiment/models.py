import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# from fasttext import load_model as load_fasttext_model
import fasttext


from analyzer.sentiment.data import DATA_BASE_PATH
from analyzer.sentiment.tokenization import BaseTokenizer

fasttext.FastText.eprint = lambda x: None

class BaseModel(ABC):
    def __init__(
        self,
        tokenizer: BaseTokenizer,
        lemmatize: bool = True,
        model_path: Optional[str] = None,
        # corpus: Optional[BaseCorpus] = None,
    ):
        self.model_path = model_path
        self.tokenizer = tokenizer
        self.lemmatize = lemmatize
        # self.corpus = corpus
        self.model = self.get_compiled_model() if self.model_path else self.get_raw_model()

    @abstractmethod
    def get_compiled_model(self):
        raise NotImplementedError

    def preprocess_input(self, sentences: List[str]):
        raise NotImplementedError

    @abstractmethod
    def predict(self, sentences: List[str], **kwargs) -> List[Dict[str, float]]:
        raise NotImplementedError

    def get_raw_model(self):
        raise NotImplementedError


class FastTextSocialNetworkModel(BaseModel):
    """
    FastText model trained on RuSentiment dataset.
    """

    SENTENCE_LENGTH: Optional[int] = None

    MODEL_PATH: str = os.path.join(DATA_BASE_PATH, 'models/model.bin')

    def __init__(
        self,
        tokenizer: BaseTokenizer,
        lemmatize: bool = False,
    ):
        # super(FastTextSocialNetworkModel, self).__init__(
        #     tokenizer=tokenizer, lemmatize=lemmatize, model_path=self.MODEL_PATH, corpus=None
        # )
        super(FastTextSocialNetworkModel, self).__init__(
            tokenizer=tokenizer, lemmatize=lemmatize, model_path=self.MODEL_PATH
        )

    def get_compiled_model(self):
        return fasttext.load_model(self.MODEL_PATH)

    def preprocess_input(self, sentences: List[str]) -> List[str]:
        return [
            ' '.join(token for token, _ in self.tokenizer.split(sentence, lemmatize=self.lemmatize))
            for sentence in sentences
        ]

    def convert_to_points(self, points: list):
        labels = {
            'negative': 0,
            'neutral': 33,
            'positive': 66
        }

        return float("{0:.2f}".format(labels[points[0]] + 33 * float(points[1])))

    def predict(self, sentences: List[str], **kwargs) -> float:
        k = kwargs.get('k', -1)
        X = self.preprocess_input(sentences)
        Y = (self.model.predict(sentence, k=k) for sentence in X)
        for labels, scores in Y:
            return self.convert_to_points([
                labels[0].replace('__label__', ''),
                scores
            ])
        # return self.convert_to_points(
        #     points=[, scores for labels, scores in Y]
        # )


class FastTextToxicModel(FastTextSocialNetworkModel):
    """
    FastText model trained on russian toxic comments dataset.
    """

    SENTENCE_LENGTH: Optional[int] = None

    MODEL_PATH: str = os.path.join(DATA_BASE_PATH, 'models/fasttext-toxic-model.bin')
