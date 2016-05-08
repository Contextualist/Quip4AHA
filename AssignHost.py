# -*- coding: utf-8 -*-  
'''
Adapt to fit Flask in GAE
CAUTION: Make sure there is only ONE doc in the AHA BC folder,
         otherwise the doc catcher may catch a wrong one.
NOTICE:  To update the broadcast structure, you need to update
         1) KeyWord, 2) BWeight, 3) PNperB;
         To update the host list, you need to update
         1) Host.
Main idea: 
  i. group sections into portions
  ii. then distribute the portions to each host, so that
      a. the STD of hosts' word counts is minimized *future feature
      b. the continuity is maximized
B_   block(column)
S_   section(paragraph)
P_   portion(read by a host)
_N   number, count
For those who are new to Python, remember, 
1. The index of a Python list starts with 0.
2. Variables in Python are pointers. So to copy a list but not the address of the list, use a=copy.deepcopy(b), instead of a=b.
Progress: Hope to improve efficiency of DISTRIBUTE
'''

from HTMLParser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__BNNow = -1
        self.__SNNow = 0
        self.__newline = 0 #when there are total two <p> and <br/> between two data, new section
        self.__SIDNow = ''
        self.SWordCount = []
        self.SID = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.__SIDNow = attrs[0][1] #extract the ID attr
            self.__newline += 1

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.__newline += 1

    def handle_data(self, data):
        wordcount = len(re.findall(r"\b\w+\b", data))
        if wordcount == 0: return 0
        if (self.__BNNow+1<=BN-1 and data.find(KeyWord[self.__BNNow+1])!=-1):
            self.__BNNow += 1 #new block
            self.__SNNow = 0
            self.SWordCount += [[0]]
            self.SID += [[self.__SIDNow]]
        elif self.__newline>=2:
            self.__SNNow += 1 #new section
            self.SWordCount[self.__BNNow] += [0]
            self.SID[self.__BNNow] += [self.__SIDNow]
        self.SWordCount[self.__BNNow][self.__SNNow] += wordcount
        self.__newline = 0

import quip
import copy

class AssignHost(object):

    def __init__(self):
        '''
        ==================INITIALIATION==================
        '''
        #--------------------Block----------------------
        '''SET'''
        self.KeyWord = ("Good Morning AHA",
                        "Now for this week in history",
                        "In World News",
                        "Now for the fun facts",
                        "In AHA News")
        self.BN = len(self.KeyWord)
        #                  Greet   History   World  Fun   AHA
        '''SET'''
        self.BWeight = (1.00,   1.30,    1.50,  1.20, 1.00)  # B[]
        #--------------------Section----------------------
        self.SWordCount = []
        self.SID = []
        self.SNperB = []     # B[SN]
        #---------------------Host----------------------
        '''SET'''
        self.Host = ["Edward", "Katherine", "Sissy", "Harry"]
        import random
        random.shuffle(self.Host)
        self.HostN = len(self.Host)
        self.HostWordCount = [0.00] * self.HostN
        self.Ans_HostWordCountSTD = 1000.00
        #--------------------Portion----------------------
        '''SET'''
        self.PNperB =  (   1,      1,       2,     1,    3)  # B[PN]
        self.CutSign = [ [0]*pn for pn in self.PNperB ]
        self.PWordCount = [ [0]*pn for pn in self.PNperB ]
        self.PAssign = [ [0]*pn for pn in self.PNperB ]
        self.IsBetterPDivision = 0
        #self.Continuity = 0
        for i in xrange(self.BN) :
            if self.PNperB[i] > self.SNperB[i]: self.PNperB[i] = self.SNperB[i]
        self.Ans_CutSign = []
        self.Ans_PAssign = []
        #self.Ans_Continuity = 0
        #----------------------DOC----------------------
        self.client = quip.QuipClient(access_token="Wk9EQU1BcDZFS04=|1483091850|CF037JVoITJPnAET8aHWnZwEZACvrIm7jtkRIQCaX3g=")
        self.FolderID = "PCeAOAQx6sO" # folder AHA BC
        '''
        ====================DOC CATCHER====================
        '''
        '''
        AHA_BC = self.client.get_folder(self.FolderID)
        self.docID = ""
        for td in AHA_BC['children'] :
            if 'thread_id' in td :
                self.docID = td['thread_id'] #find a doc
                break
        self.thread = self.client.get_thread(id=self.docID)
        '''
        #self.docURL = "Z0R5AhbLjUxu" # test doc 0309-c
        docURL = "YHb8AyYLNgvi" # test doc 0309-cc
        self.thread = self.client.get_thread(id=docURL)
        self.docID = self.thread['thread']['id']
        

    def _std(d):
        m = 0.00
        for x in d : m += x
        m = m / len(d)
        s = 0.00
        for x in d : s += ( x - m ) ** 2
        return (s / len(d)) ** 0.5

    def _AssignP(b, p) :
        op = range(HostN)
        if p == 0 : #forbid the host to cross a block
            op = range(PAssign[b-1][PNperB[b-1]-1])+range(PAssign[b-1][PNperB[b-1]-1]+1,HostN)
        for i in op:
            PAssign[b][p] = i
            HostWordCount[i] += PWordCount[b][p]
            #if (p!=0)&&(i!=PAssign[b][p-1]) : Continuity += 1
            if p == PNperB[b]-1 :
                if b == BN-1 :
                    t = self._std(HostWordCount)
                    if t < Ans_HostWordCountSTD :
                        Ans_HostWordCountSTD = t
                        Ans_PAssign = copy.deepcopy(PAssign)
                        IsBetterPDivision = 1
                else :
                    AssignP(b+1,0)
            else :
                AssignP(b,p+1)
            HostWordCount[i] -= PWordCount[b][p]

    def _GenerateP(b, p) : #block 'b' from 'CutSign[b,p]+1' to the end start dividing the 'p'th sections
        if p == PNperB[b]-1 :
            PWordCount[b][PNperB[b]-1] = sum(SWordCount[b][CutSign[b][p]:])
            if b < BN-1 :
                CutSign[b+1][0] = 0
                self._GenerateP(b+1,0)   #next B
            else :
                IsBetterPDivision = 0
                HostWordCount = [0] * HostN
                PAssign[0][0] = 0
                HostWordCount[0] += PWordCount[0][0]
                if PNperB[0]>1 :
                    self._AssignP(0, 1)
                else : 
                    self._AssignP(1, 0) #start assigning hosts
                if IsBetterPDivision : 
                    Ans_CutSign = copy.deepcopy(CutSign)
        else :
            PWordCount[b][p] = 0
            for i in xrange(CutSign[b][p]+1,SNperB[b]) :
                PWordCount[b][p] += SWordCount[b][i-1]
                CutSign[b][p+1] = i
                self._GenerateP(b,p+1)


    def do():
        return "Underconstruction. . ."
        '''
        ====================DOC PRE-PROCESSOR====================
        extract SWordCount and SID
        '''
        if self.thread["html"].find(r'<i>//')!=-1 : return "You have run this at least once!"
        self.docHTML = self.thread["html"].decode('utf-8').encode('ascii', 'ignore') #clear all non-ascii
        self.docHTML = re.sub(r'<h1.+<\/h1>', '', self.docHTML, count=1) #delete the header
        
        parser = MyHTMLParser()
        parser.feed(self.docHTML)
        
        '''
        =====================SETTINGS====================
        '''    
        self.SWordCount = parser.SWordCount
        self.SWordCount = [ [ swc*self.BWeight[b] for swc in self.SWordCount[b] ] for b in xrange(self.BN) ]     # B[S[]], weighted
        self.SID = parser.SID
        self.SNperB = [ len(b) for b in SWordCount ]     # B[SN]
        self.CutSign[0][0] = 0
        
        '''
        ====================DISTRIBUTE(S->P)====================
        '''
        self._GenerateP(0, 0)
        #    CutSign =   [[0],   [0],     [],       , []] # B[P[SN]] generated first
        #    PWordCount =[ ,      ,   [],       , []] # B[P[]] generated first
        #        PAssign =   [[0],   [1],     [],       , []] # B[P[Host]] subsequent
        
        '''
        ====================POST DIVISIONS====================
        '''
        for b in xrange(self.BN) :
            for p in xrange(self.PNperB[b]) :
                client.edit_document(thread_id=self.docID, content=r"<i>//%s</i>" % (self.Host[self.Ans_PAssign[b][p]]), format="html",
                                     operation=self.client.BEFORE_SECTION, section_id=self.SID[b][self.Ans_CutSign[b][p]])
        return "Done!"
        
if __name__=="__main__":
    NewDocAction = NewDoc()
    NewDocAction.do()
