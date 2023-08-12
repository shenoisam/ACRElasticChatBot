# Author: Sam Shenoi
# Description: This is a dumb version that uses basic NLP to extract information and then retrieve
#  the correct ACR criteria

from textblob import TextBlob
import spacy
import re
import json
import os
import argparse

from classes import Elastic

if __name__ == "__main__":
    e = Elastic()


    parser = argparse.ArgumentParser(prog='ElasticACR',description='This program reads in a clinical case and then searches ACR appropriateness criteria to output ACR recommendations for imaging. ',epilog='')

    parser.add_argument('-p', '--prompt')
    parser.add_argument('-l', '--load_data')

    args = parser.parse_args()
    prompt = "A 27-year-old female presents to clinic with a firm tender right sided breast mass."
    if args.load_data is not None:
        e.index(args.load_data)
    elif args.prompt is not None:
        prompt = args.prompt

    e.query(prompt)

    #"/Users/samshenoi/Desktop/projects/chatgptrads/data/acrguidelines/txt"