#import pandas as pd
#import numpy as np
import argparse
#import json
#import random
#from random import shuffle
#import multiprocessing
#import copy
from os import listdir
from os.path import isfile, join
#import math
#import csv
#from sklearn.metrics import roc_auc_score
#from sklearn.ensemble import RandomForestClassifier
#from sklearn import tree
#import bz2
#import pickle
#import _pickle as cPickle
#import matplotlib.pyplot as plt
#import joblib
#import xlrd


def read_pirche(pirche):
    data = {}
    interesting_cols = [1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 122]
    files = []
    if isfile(pirche):
        files = [pirche]
    else:
        files = [join(args.pirche, f) for f in listdir(args.pirche) if isfile(join(args.pirche, f))]

    for file in files:
        print("Read file " + file)
        with open(file, "r") as input:
            for row in input:
                cols = row.split(",")
                if len(cols) > max(interesting_cols):
                    data[cols[0]] = [cols[q] for q in interesting_cols]
    return data


def write_pirche(writer, id, max_patient, max_donor):
    writer.write("patient_" + id + "," + ",".join(max_patient) + "," + "donor_" + id + "," + ",".join(max_donor) + "\n")
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="verbose operation", action="store_true")
    parser.add_argument("-p", "--pirche", help="PIRCHE raw result file", required=True, type=str)
    parser.add_argument("-o", "--output", help="output file", required=True, type=str)
    args = parser.parse_args()

    pirche = read_pirche(args.pirche)

    with open(args.output, "w") as output:
        datasets = list(pirche.keys())
        for patient_id in [d for d in datasets if "patient_" in d and not "#" in d]:
            hr_patient_ids = [d for d in datasets if patient_id in d and "#" in d]
            id = patient_id.split("_")[1]
            max_weight = 0.
            max_patient = None
            for hr_patient_id in hr_patient_ids:
                curr_weight = float(pirche[hr_patient_id][-1])
                if max_weight < curr_weight:
                    max_weight = curr_weight
                    max_patient = pirche[hr_patient_id]
            if len(hr_patient_ids) > 0:
                hr_donor_ids = [d for d in datasets if "donor_" + id in d and "#" in d]
                print("Patient: " + patient_id + " with " + str(len(hr_patient_ids)) + " HR options, donor options: " + str(len(hr_donor_ids)/len(hr_patient_ids)))

                donor_weight = {}
                donor_mapping = {}
                for hr_donor_id in hr_donor_ids:
                    donor_id = hr_donor_id.split("#")[2]
                    if donor_id not in donor_weight:
                        donor_weight[donor_id] = 0.
                    donor_weight[donor_id] += float(pirche[hr_donor_id][-1])
                    donor_mapping[donor_id] = hr_donor_id

                max_weight = 0.
                max_donor = None
                for donor_id in donor_weight:
                    curr_weight = donor_weight[donor_id]
                    if curr_weight > max_weight:
                        max_donor = pirche[donor_mapping[donor_id]]
                        max_weight = curr_weight
                max_donor[-1] = str(max_weight)

                if max_patient is not None and max_donor is not None:
                    write_pirche(output, id, max_patient, max_donor)
