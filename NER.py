import spacy
import random
from spacy.util import minibatch, compounding
from pathlib import Path
from spacy.training.example import Example

# Adapted from: https://www.machinelearningplus.com/nlp/training-custom-ner-model-in-spacy/

TRAIN_DATA = [
    ("CT imaging is used to assess the patient.", {"entities": [(0, 2, "IMAGING")]}),
    ("Ultrasound imaging is used to assess the patient.", {"entities": [(0, 18, "IMAGING")]}),
    ("My sister went to get a US breast due to a mass.", {"entities": [(24, 33, "IMAGING")]}),
    ("Nobody likes to get a MRI", {"entities": [(22, 25, "IMAGING")]}),
    ("Jonny had a head injury so he got a Computed Tomography scan", {"entities": [(36, 60, "IMAGING")]}),
]
class ImagingNER:
    def __init__(self):
        # Load the pretrained model.
        self.nlp=spacy.load('en_core_web_sm')

    def train_ner(self):
        # Getting the pipeline component. We will be training the NER model to pick up on imaging types
        ner=self.nlp.get_pipe("ner")

        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # Disable pipeline components you dont need to change
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        unaffected_pipes = [pipe for pipe in self.nlp.pipe_names if pipe not in pipe_exceptions]
        with self.nlp.disable_pipes(*unaffected_pipes):
            # Training for 30 iterations
            for iteration in range(30):

                # shuufling examples  before every iteration
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    for text, annotations in batch:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        # Update the model
                        self.nlp.update([example], losses=losses, drop=0.3)
                        print("Losses", losses)
        return self

    def save(self,output='./ner'):
        output_dir = Path(output)
        self.nlp.to_disk(output_dir)
        return self

    def load_model(self,output_dir='./ner'):
        # Load the saved model and predict
        self.nlp = spacy.load(output_dir)
        return self

    def returnImaging(self,txt):
        imaging_recs = []
        doc=self.nlp(txt)
        for ent in doc.ents:
            if ent.label_ == "IMAGING":
                imaging_recs.append(ent.text)
        return imaging_recs


    def testModel(self,article):
        doc=self.nlp(article)

        for ent in doc.ents:
            print(ent.text,ent.label_)

if __name__ == "__main__":
    ImagingNER().train_ner().save().testModel("A MRI is the recommended type of imaging in this case.")