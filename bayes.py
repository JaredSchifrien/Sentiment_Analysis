# Name: Jared Schifrien: Jss134
# Date: May 11, 2016
# Description: 
#
#

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      self.posFreqDict = self.load("posFreqDict")
      self.neuFreqDict = self.load("neuFreqDict")
      self.negFreqDict = self.load("negFreqDict")

      if(self.posFreqDict is None or self.negFreqDict is None or self.neuFreqDict is None):
         train()


   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""

      lFileList = []
      for fFileObj in os.walk("movies_reviews/"): 
         lFileList = fFileObj[2]
         break


      for file in lFileList:
         rating = str(file[7:8])
         fileText = self.loadFile("movies_reviews/" + str(file))
         wordList = self.tokenize(fileText)

         for i in wordList:
            if(rating < 3):
               if i in self.negFreqDict:
                  self.negFreqDict[i] += 1
               else:
                  self.negFreqDict[i] = 1
            elif(rating < 4):
               if i in self.neuFreqDict:
                  self.neuFreqDict[i] += 1
               else:
                  self.neuFreqDict[i] = 1
            else:
               if i in self.posFreqDict:
                  self.posFreqDict[i] += 1
               else:
                  self.posFreqDict[i] = 1

      self.save(self.posFreqDict,"posFreqDict")
      self.save(self.neuFreqDict,"neuFreqDict")
      self.save(self.negFreqDict,"negFreqDict")
      print self.posFreqDict

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

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
