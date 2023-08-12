# Author: Sam Shenoi
# Description: This file
from textblob import TextBlob
import spacy
import re
import json
import os
from elasticsearch import Elasticsearch
import ssl
class Elastic:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200",  basic_auth=("elastic", "AutoBCT2022!"))

    def genMultiMatchObj(self,query,fields,type,boost):
        obj = {
            "multi_match":{
                            "query":query,
                            "fields":fields,
                            "tie_breaker":.4,
                            "type":type,
                            "boost":boost
            }
        }
        return obj
    def index(self,filename="out.txt"):
        f = open(filename)
        data = json.loads(f.read())
        f.close()
        counter = 1
        errcounter = 0
        docs = data["docs"]
        err = open("err.csv",'w')
        err.write("Number,Error Message,Document\n")
        for doc in docs:
            try:
                resp = self.es.index(index="test-index", id=counter, document=doc)
            except Exception as e:
                err.write(f"{errcounter},{e},{doc}\n")
                errcounter = errcounter + 1
            counter = counter + 1
        err.close()

    def query(self,query):
        de = DumbExtraction()
        cc = de.extract_chief_complaint(query)

        cc_u = cc[1:]
        print(cc)
        query_obj = {

                "query_string": {
                "query": cc_u[1],
                "default_field": "text"
                }
        }

        resp = self.es.search(index="test-index", query=query_obj)
        print("Got %d Hits:" % resp['hits']['total']['value'])
        print(resp['hits']["hits"][0])





class DumbExtraction:
    def extract_age(self,phrase):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(phrase)
        dates = []
        max_age = 200
        min_age = -1

        for ent in doc.ents: # for every entity, print text, start index, end index, label (what type of entity it is)
            if "DATE" in str(ent.label_):
                min_age = ent.text

        # Check to see if there are restrictions on child/adult
        if len(re.findall("child",phrase.lower())) > 0:
            max_age = 18

        return max_age,min_age
    def extract_chief_complaint(self,phrase):
        return TextBlob(phrase).noun_phrases

    def extract_name(self,name):
        return re.findall('[A-Z][^A-Z]*', name)

    def buildDocuments(self,directory,outfile="out.txt"):
        res = []
        counter = 0
        total = os.listdir(directory)
        for filename in total:
            fpath = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(fpath):
                print(filename)
                f = open(fpath)
                phrases = f.read()
                f.close()

                p = phrases.split('\n')
                name = self.extract_name(filename.split('.txt')[0])
                for phrase in p:
                    if phrase != "":
                        max_age,min_age = self.extract_age(phrase)
                        cc = self.extract_chief_complaint(phrase)

                        doc = {
                            'docname': " ".join(name),
                            'text': phrase,
                            'max_age': max_age,
                            "min_age": min_age
                        }
                        res.append(doc)

            counter = counter + 1
            print(f"Completed {(counter/len(total) * 100)}")


        f = open(outfile,'w')
        f.write(json.dumps({"docs":res}) +"\n")
        f.close()

