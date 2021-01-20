import os

from flair.data import Dictionary
from flair.embeddings import WordEmbeddings, FlairEmbeddings, \
    StackedEmbeddings
from flair.trainers.language_model_trainer import LanguageModelTrainer, TextCorpus
from flair.visual.training_curves import Plotter


class FineTuneLM:

    def __init__(self, params) -> None:
        """Please carefully read the compatible associations between model and model type.
        """
        self.model = params.get('model', 'flair')
        self.model_type = params.get('model_type', 'news_forward')
        self.seq_len = params.get('seq_len', 250)
        self.batch_size = params.get('batch_size', 100)
        self.lr = params.get('lr', 0.1)
        self.patience = params.get('patience', 0.1)
        self.checkpoint = params.get('checkpoint', True)

        if self.model == 'flair':
            self.model = FlairEmbeddings(self.model_type)  # forward-news, backward-news
        elif self.model == 'word':
            self.model = WordEmbeddings(self.model_type)  # glove, de-crawl, etc.
        elif self.model == 'stacked':
            self.model = StackedEmbeddings(self.model_type)

        self.corpus_dir = params.get('corpus_dir', './')
        if not os.path.exists(self.corpus_dir):
            raise ValueError('Expected a corpus to train a language model.')

        # define corpus, dictionary and instantiate LM
        self.dictionary = Dictionary.load('chars')
        self.corpus = self._define_corpus()
        self.lm = self.model.lm

        self.save_dir = params.get('save_dir', './')

    def _define_corpus(self) -> TextCorpus:
        return TextCorpus(self.corpus_dir,
                          self.dictionary,
                          self.lm.is_forward_lm,
                          character_level=True)

    def train(self):
        trainer = LanguageModelTrainer(self.lm, self.corpus)
        trainer.train(self.save_dir,
                      sequence_length=self.seq_len,
                      mini_batch_size=self.batch_size,
                      learning_rate=self.lr,
                      patience=self.patience,
                      checkpoint=self.checkpoint,
                      write_weights=True,
                      use_tensorboard=True)

    @staticmethod
    def visualize(path: str):
        plotter = Plotter()
        plotter.plot_training_curves(path + 'loss.tsv')
        plotter.plot_weights(path + 'weights.txt')
