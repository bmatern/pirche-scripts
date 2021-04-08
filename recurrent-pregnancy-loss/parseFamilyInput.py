import argparse
from os.path import isdir, join
from os import makedirs

'''


import sys
import re
from os.path import isfile, join
from os import listdir

def hlaListFromString(input):
    ags = input.split(" ")
    asList = []
    for ag in ags:
        asList.append(ag.strip())
    return asList

def removeBroads(bsMap, input):
    output = []
    for ag in input:
        output.append(ag)
    for ag in input:
        if ag in bsMap.keys():
            if bsMap[ag] in output:
                output.remove(bsMap[ag])
    return output

def pircheAgString(input, separator):
    if(input is None):
        return ''

    output = ""
    for ag in input:
        match = re.match(r"([A-Za-z]+)([0-9]+)", ag, re.I)
        if match:
            items = match.groups()
            locus = items[0]
            allele = items[1]
            print('found locus ' + str(locus))
            if(locus == 'DRB'):
                output = output + ag + separator
            elif not locus == "Bw" and not locus == "BW" and not (locus == "DR" and (allele == "51" or allele == "52" or allele == "53")):
                if locus == "Cw":
                    locus = "C"
                if locus == "CW":
                    locus = "C"
                if locus == "DQ":
                    locus = "DQB1"
                if locus == "DR":
                    locus = "DRB1"
                output = output + locus + "*" + allele + separator

    print('returning output ' + str(output))

    return output
def removeMolecular(input):
    output = []
    for ag in input:
        if not "*" in ag and not ":" in ag and not ag == "DQB1":
            output.append(ag)
    return output


def extrapolateDrb1Typings(id, patientTypings, extrapolatedDrb1Typings):
    #print('patient ' + str(id) + ' typing before:' + str(patientTypings))
    typingsWithExtrapolatedDrb1 = []

    # If there is an extrapolated typing for this patient
    if(id in extrapolatedDrb1Typings.keys()):
        #print('patient ' + str(id) + ' is in the list of patients with extrapolated typings.')
        for ag in patientTypings:
            #print('ag:' + str(ag))
            if not str(ag).startswith('DR'):
                typingsWithExtrapolatedDrb1.append(ag)
        extrapolatedDr1, extrapolatedDr2 = extrapolatedDrb1Typings[id].split(';')
        typingsWithExtrapolatedDrb1.append(extrapolatedDr1)
        typingsWithExtrapolatedDrb1.append(extrapolatedDr2)

        #print('patient ' + str(id) + ' typing after:' + str(typingsWithExtrapolatedDrb1))
        return typingsWithExtrapolatedDrb1

    # otherwise this patient probably didn't reach the cutoff for confidence in the extrapolated typing
    else:
        #print('patient ' + str(id) + ' is NOT in the list of patients with extrapolated typings.')
        return None


    #return typingsWithExtrapolatedDrb1
    return patientTypings
'''


def parseExcelForFamilyData(excelFile=None):
    print('Parsing Excel File:' + str(excelFile))



def writePircheOutputFile(outputFileName=None, familyData=None):
    print('Writing output file:' + str(outputFileName))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="verbose operation", action="store_true")
    parser.add_argument("-o", "--output", help="output directory", required=True)
    parser.add_argument("-x", "--excel", help="input excel file", required=True)

    args = parser.parse_args()

    verbose = args.verbose
    if verbose:
        print("verbose mode active")

    if (verbose):
        print("Excel:" + args.excel)
        print("Output:" + args.output)

    familyData = parseExcelForFamilyData(excelFile=args.excel)
    if(not isdir(args.output)):
        makedirs(args.output)

    outputFileName=join(args.output, 'PircheInpuptFile.txt')
    writePircheOutputFile(outputFileName=outputFileName,familyData=familyData)
