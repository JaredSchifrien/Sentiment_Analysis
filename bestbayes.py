# Name: Jared Schifrien: Jss134
# Date: May 11, 2016
# Description: 
#
#

import math, os, pickle, re
from math import log10

class Bayes_Classifier:
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

         self.train()


   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""

      lFileList = []
      for fFileObj in os.walk("movies_reviews/"): 
         lFileList = fFileObj[2]
         break

      d= {}    
      for file in lFileList:
         rating = int(file[7])
         if rating in d:
            d[rating] = d[rating]+1
         else:
            d[rating]=1
         fileText = self.loadFile("movies_reviews/" + str(file))
         wordList = self.tokenize(fileText)

         for i in range(len(wordList)-1):
            first = wordList[i].lower()
            second = wordList[i+1].lower()
            if rating == 1:
               if first+second in self.negFreqDict:
                  self.negFreqDict[first+second] += 1
               else:
                  self.negFreqDict[first+second] = 1
            elif rating < 4:
               if first+second in self.neuFreqDict:
                  self.neuFreqDict[first+second] += 1
               else:
                  self.neuFreqDict[first+second] = 1
            else:
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
      posCount = float(sum(self.posFreqDict.itervalues()))
      negCount = float(sum(self.negFreqDict.itervalues()))
      negProbability=0.0
      posProbability=0.0
      wordList = self.tokenize(sText)
      for i in range(len(wordList)-1):
         first = wordList[i].lower()
         second = wordList[i+1].lower()
         if first+second in self.posFreqDict:
            posProbability+= log10(float( (1.0+float(self.posFreqDict[first+second]))/posCount))
         else:
            posProbability+=log10(float(1.0/posCount))
         if first+second in self.negFreqDict:
            negProbability+= log10(float( (1.0+float(self.negFreqDict[first+second]))/negCount))
         else:
            negProbability+= log10(float(1.0/negCount))
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
