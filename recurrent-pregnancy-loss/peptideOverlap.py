import argparse
import datetime
from os.path import isdir, join
from os import makedirs


def readPeptideFile(peptideFileName=None, delimiter=';'):
    print('Reading Peptides from (' + str(peptideFileName) + ")")
    with open(peptideFileName, 'r') as peptideFile:
        peptideDataLines = peptideFile.readlines()

        sampleNamesByColumn = {}
        peptidesByColumn = {}

        for lineIndex, line in enumerate(peptideDataLines):


            # HeaderRow
            if(lineIndex == 0):
                #print('header#' + str(lineIndex) + ':' + str(line))
                for columnIndex, columnToken in enumerate(line.split(delimiter)):
                    sampleNamesByColumn[columnIndex]=columnToken.strip() # Store sample Name
                    peptidesByColumn[columnIndex]=[] # Initialize a list to store peptides in.
            else:
                #print('row#' + str(lineIndex) + ':' + str(line))
                for columnIndex, columnToken in enumerate(line.split(delimiter)):
                    peptideCleaned=columnToken.strip()
                    if(len(peptideCleaned)>1):
                        peptidesByColumn[columnIndex].append(peptideCleaned) # Store peptide, cleaned from the extra whitespace
                        #print('Column ' + str(columnIndex) + ' (' + str(sampleNamesByColumn[columnIndex]) + ') has peptide ' + peptideCleaned)

        return sampleNamesByColumn, peptidesByColumn


def calculateOverlap(immunizerHeaders=None, immunizerPeptides=None, recallHeaders=None, recallPeptides=None):
    print('Calculating overlapping peptides (Present in both lists')

    # Some quick checks to see if I understand the data
    if(len(immunizerHeaders.keys()) != len(recallHeaders.keys())):
        raise Exception('Different number of headers')
    if(len(immunizerHeaders.keys()) != len(immunizerPeptides.keys())):
        raise Exception('Different number of immunizer headers and peptides')
    if(len(immunizerPeptides.keys()) != len(recallPeptides.keys())):
        raise Exception('Different number of peptide lists')

    # Check that the samples match up.
    for columnIndex in sorted(immunizerHeaders.keys()):
        immunizerSampleID = immunizerHeaders[columnIndex]
        recallSampleID = recallHeaders[columnIndex]
        #print('Column ' + str(columnIndex) + ' sample ids: ' + str(immunizerSampleID) + ' : ' + str(recallSampleID))
        # Assuming that the first two digits match
        if(immunizerSampleID[0:2] != recallSampleID[0:2]):
            raise Exception ('Mismatch sample ID: ' + str(immunizerSampleID) + ' : ' + str(recallSampleID))

    overlapHeaders = {}
    overlapPeptides = {}

    for columnIndex in sorted(immunizerHeaders.keys()):
        overlapSampleID = immunizerHeaders[columnIndex][0:2] + 'overlap'

        overlapHeaders[columnIndex] = overlapSampleID
        overlapPeptides[columnIndex] = []

        for immunizerPeptide in immunizerPeptides[columnIndex]:
            if(immunizerPeptide in recallPeptides[columnIndex]):
                overlapPeptides[columnIndex].append(immunizerPeptide)
            # if it is in the recall list
                # Store it.

    return overlapHeaders, overlapPeptides


def writeOutput(overlapHeaders=None, overlapPeptides=None, outputFileName=None, delimiter=';', newline='\r\n'):
    print('Writing file ' + str(outputFileName))

    # Calculate the maximum length of the peptide lists, to use for iteration
    maxPeptideLength = 0
    for columnIndex in sorted(overlapHeaders.keys()):
        currentColumnLength = len(overlapPeptides[columnIndex])
        overlapHeaders[columnIndex] = overlapHeaders[columnIndex] + '(N=' + str(currentColumnLength) + ')'
        if(currentColumnLength > maxPeptideLength):
            #print('column ' + str(columnIndex) + ' is the biggest list so far, length = ' + str(currentColumnLength))
            maxPeptideLength = currentColumnLength



    with open(outputFileName, 'w') as outputFile:
        # Header
        for columnIndex in sorted(overlapHeaders.keys()):
            # TODO: I'm adding an extra delimiter at the end here, that is not necessary.
            outputFile.write(overlapHeaders[columnIndex] + delimiter)
        outputFile.write(newline)

        # Arbitrarily large number, like 300 is enough, I should actually just calculate the maximum length of the peptide lists.
        for peptideIndex in range(0,maxPeptideLength):
            for columnIndex in sorted(overlapHeaders.keys()):
                try:
                    overlapPeptide = overlapPeptides[columnIndex][peptideIndex]
                    outputFile.write(overlapPeptide + delimiter)
                except IndexError as e:
                    # Hopefully this means there just isnt a peptide in the list at this spot.
                    outputFile.write(delimiter)
            outputFile.write(newline)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--immunizer", help="input immunizer peptide file", required=True)
    parser.add_argument("-r", "--recall", help="input recall peptide file", required=True)

    args = parser.parse_args()

    immunizerHeaders, immunizerPeptides = readPeptideFile(peptideFileName=args.immunizer)
    recallHeaders, recallPeptides = readPeptideFile(peptideFileName=args.recall)

    overlapHeaders, overlapPeptides = calculateOverlap(immunizerHeaders=immunizerHeaders, immunizerPeptides=immunizerPeptides,recallHeaders=recallHeaders, recallPeptides=recallPeptides)
    outputFileName = 'OverlapPeptides.csv'

    writeOutput(overlapHeaders=overlapHeaders, overlapPeptides=overlapPeptides, outputFileName=outputFileName)


    print('Done.')