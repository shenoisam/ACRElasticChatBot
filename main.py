# Author: Sam Shenoi
# Description: This is a dumb version that uses basic NLP to extract information and then retrieve
#  the correct ACR criteria

from textblob import TextBlob
import spacy
import re
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
from classes import Elastic
from NER import ImagingNER

if __name__ == "__main__":
    e = Elastic()
    i = ImagingNER()


    parser = argparse.ArgumentParser(prog='ElasticACR',description='This program reads in a clinical case and then searches ACR appropriateness criteria to output ACR recommendations for imaging. ',epilog='')

    parser.add_argument('-p', '--prompt')
    parser.add_argument('-l', '--load_data')

    args = parser.parse_args()
    prompt = "A 27-year-old female presents to clinic with a firm tender right sided breast mass."
    if args.load_data is not None:
        e.index(args.load_data)
        i.train_ner().save()

    elif args.prompt is not None:
        prompt = args.prompt

    doc_results = e.query(prompt)["_source"]["text"]
    print(doc_results)
    final_recs = i.load_model().returnImaging(doc_results)
    print(final_recs)


    #"/Users/samshenoi/Desktop/projects/chatgptrads/data/acrguidelines/txt"