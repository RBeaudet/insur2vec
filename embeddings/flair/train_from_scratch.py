import os
from typing import Dict

from flair.data import Dictionary
from flair.models import LanguageModel
from flair.trainers.language_model_trainer import LanguageModelTrainer, TextCorpus
from flair.visual.training_curves import Plotter


class Trainer:

    def __init__(self, params: Dict) -> None:
        """Train a Language Model from scratch. This model can then be used as Flair embeddings.

        Args:
            params (dict): training config.
        """
        self.checkpoint = params.get('checkpoint', True)
        self.sequence_length = params.get('seq_len', 250)
        self.mini_batch_size = params.get('batch_size', 100)
        self.learning_rate = params.get('lr', 20)
        self.patience = params.get('patience', 25)

        # forward LM predicts the next word, backward LM reads the sentence backwards and predicts the previous word.
        self.is_forward_lm = params.get('forward', True)

        self.corpus_dir = params.get('corpus_dir', '../')
        if not os.path.exists(self.corpus_dir):
            raise ValueError('Expected a corpus to train a language model.')

        # define corpus, dictionary and instantiate LM
        self.dictionary = Dictionary.load('chars')
        self.corpus = self._define_corpus()
        self.lm = self._define_model()

        self.save_dir = params.get('save_dir', '../')

    def train(self) -> None:
        trainer = LanguageModelTrainer(self.lm, self.corpus)
        trainer.train(self.save_dir,
                      sequence_length=self.sequence_length,
                      mini_batch_size=self.mini_batch_size,
                      learning_rate=self.learning_rate,
                      patience=self.patience,
                      checkpoint=self.checkpoint,
                      write_weights=True,
                      use_tensorboard=True)

    def _define_model(self) -> LanguageModel:
        return LanguageModel(self.dictionary,
                             self.is_forward_lm,
                             hidden_size=1024,
                             nlayers=1)

    def _define_corpus(self) -> TextCorpus:
        return TextCorpus(self.corpus_dir,  # '/path/to/your/corpus'
                          self.dictionary,
                          self.is_forward_lm,
                          character_level=True)

    @staticmethod
    def visualize(path: str):
        plotter = Plotter()
        plotter.plot_training_curves(path + 'loss.tsv')
        plotter.plot_weights(path + 'weights.txt')
