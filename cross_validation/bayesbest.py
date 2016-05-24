# Name: Jared Schifrien: Jss134 and Wyatt Cook : wsc147
# Date: May 11, 2016
# Description: 
#All group members were present and contributing during all work on this project.
#

import math, os, pickle, re
import random
from math import log10

class Bayes_Classifier:
   """ this class is our bayes classifier..."""
   posFreqDict = dict()
   neuFreqDict = dict()
   negFreqDict = dict()
   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      try:
         self.posFreqDict = self.load("posFreqDict")
         self.neuFreqDict = self.load("neuFreqDict")
         self.negFreqDict = self.load("negFreqDict")

      except:

         lFileList = []
         for fFileObj in os.walk("movies_reviews/"): 
            lFileList = fFileObj[2]
            break
         random.shuffle(lFileList)
         
         self.train(lFileList)
         Original_d = {}
         d = {}
         correct_positives =0
         incorrect_positives=0
         correct_negatives =0
         incorrect_negatives = 0
         for file in lFileList[int(float(len(lFileList))*.9):len(lFileList)+1]:
            rating = int(file[7])
            if rating in Original_d:
               Original_d[rating] = Original_d[rating]+1
            else:
               Original_d[rating]=1

            fileText = self.loadFile("movies_reviews/" + str(file))
            result = self.classify(fileText)
            if result in d:
               d[result]=d[result]+1
            else:
               d[result]=1
            if rating==5:
               if result =="positive":
                  correct_positives+=1
               else:
                  incorrect_positives+=1
            else:
               if result == "negative":
                  correct_negatives+=1
               else:
                  incorrect_negatives+=1
         print Original_d
         print d
         print correct_positives #Actually positive, we said positive
         print incorrect_positives #Actually positive, we said negative
         print correct_negatives #Actually negative, we said negative
         print incorrect_negatives #Actually negative, we said positive
         
         A = correct_positives
         B = incorrect_positives
         C = incorrect_negatives

         Recall = (A / (A + B)) *100
         Precision = (A / (A + C)) *100
         FScore = 2 * (Recall*Precision) / (Recall+Precision)

         print Recall
         print Precision
         print FScore

   def train(self, shuffled):   
      """Trains the Naive Bayes Sentiment Classifier."""

         
      for i in range(1,10):
         for file in shuffled[0: int(float(len(shuffled))*.9)]:

            rating = int(file[7])

            fileText = self.loadFile("movies_reviews/" + str(file))
            wordList = self.tokenize(fileText)

            for i in range(len(wordList)-1):
               #getting first and second words, with lower case
               first = wordList[i].lower()
               second = wordList[i+1].lower()
               #if it is bad rating 
               if rating == 1:
                  #check if in dict
                  if first+second in self.negFreqDict:
                     self.negFreqDict[first+second] += 1
                  else:
                     self.negFreqDict[first+second] = 1
                     #neutral rating
               elif rating < 4:
                  #check in dict
                  if first+second in self.neuFreqDict:
                     self.neuFreqDict[first+second] += 1
                  else:
                     self.neuFreqDict[first+second] = 1
               #positive rating
               else:
                  #check in dict
                  if first+second in self.posFreqDict:
                     self.posFreqDict[first+second] += 1
                  else:
                     self.posFreqDict[first+second] = 1

      self.save(self.posFreqDict,"posFreqDict")
      self.save(self.neuFreqDict,"neuFreqDict")
      self.save(self.negFreqDict,"negFreqDict")

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      threshold = .1
      #keeping track of probabilities and the size of each ones
      posCount = float(sum(self.posFreqDict.itervalues()))
      negCount = float(sum(self.negFreqDict.itervalues()))
      negProbability=0.0
      posProbability=0.0
      wordList = self.tokenize(sText)
      for i in range(len(wordList)-1):
         #getting first and second words
         first = wordList[i].lower()
         second = wordList[i+1].lower()
         #checking if pos
         if first+second in self.posFreqDict:
            posProbability+= log10(float( (1.0+float(self.posFreqDict[first+second]))/posCount))
         else:
            posProbability+=log10(float(1.0/posCount))
         #checing if neg
         if first+second in self.negFreqDict:
            negProbability+= log10(float( (1.0+float(self.negFreqDict[first+second]))/negCount))
         else:
            negProbability+= log10(float(1.0/negCount))
      #we determined .1 to be our threshold after some trial and error
      if abs(posProbability-negProbability)< .1 :
         return "neutral"
      elif posProbability>negProbability:
         return "positive"
      else:
         return "negative"   
   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens
