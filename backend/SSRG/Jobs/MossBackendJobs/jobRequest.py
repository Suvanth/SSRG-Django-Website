import os
import glob
from mailNotificationSender import sendMail
from heatV2 import completeReport

#my issue is that if the text file is only a line it gets stuck

class jobRequest:
    count = 0
    emailSent = False
    jobSuccess = False

    def __init__(self, courseID, submissionLanguage, directoryFormat, baseFile, userEmail, toggleEmail):
        self.courseID = courseID
        self.submissionLanguage = submissionLanguage
        self.directoryFormat = directoryFormat
        self.baseFile = baseFile
        self.userEmail = userEmail
        self.toggleEmail = toggleEmail
    
    def constructMossShellCommand(self):
        print('unzipping')
        os.system("python3 folderizer.py > folder_out.txt")
        print("unzipping done")
        subPathList = " ".join(glob.glob(f"jobOutput/jobOutput/*.{self.submissionLanguage}"))
        if(self.directoryFormat==True) and (len(self.baseFile)>1):
            osCommand = f"perl mossnet.pl -l {self.submissionLanguage} -d -b {self.baseFile} {subPathList} > myMossRun.txt"
        if(self.directoryFormat==True) and (len(self.baseFile)==0):
            osCommand = f"perl mossnet.pl -l {self.submissionLanguage} -d {subPathList} > myMossRun.txt"
        if(self.directoryFormat==False) and (len(self.baseFile)==0):
            osCommand = f"perl mossnet.pl -l {self.submissionLanguage} {subPathList} > myMossRun.txt"
        print(osCommand)
        return osCommand
    
    def jobSender(self):
        #email
        #code to send off a job
        if self.toggleEmail == True and self.emailSent == False:
            print('we will send you mail for this job')
            sendMail(self.userEmail, False, "")
            self.emailSent = True
        ##important
        os.system(self.constructMossShellCommand())
        #code to check for success
        self.persistenceCheck('myMossRun.txt')
       

       
    def persistenceCheck(self,fileName):
        url = self.retrieveUrl(fileName)
        if ('http://moss.stanford.edu/results/' in url):
            print('results are present')
            completeReport(self.courseID, url )
            print('report done')

            
            if(self.toggleEmail == True):
                print('email sent with reports')
                sendMail(self.userEmail, True, f"/Users/suvanth/Desktop/test/Suvanth/{self.courseID}report.pdf")
        else:
            print('lastline wasnt a url we will resend')
            self.jobSender()

    
    def retrieveUrl(self, mossFileName):
        with open(mossFileName, "rb") as file:
            file.seek(-2, os.SEEK_END)
            
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR) 
               
            return file.readline().decode()



#job = jobRequest("CSC3002F", "c", False, "", "rmrsuv002@myuct.ac.za", True)
job = jobRequest("CSC3002F", "java", False, "", "rsuvanth@gmail.com", True)
job.jobSender()


#print(job.constructMossShellCommand())
#print("go to your text file")

# print(str(sys.argv[1]))#user
# print(str(sys.argv[2]))#lang
# print(eval(sys.argv[3]))#bool dir
# print(str(sys.argv[4]))#Bfile
# print(str(sys.argv[5]))#email
# print(eval(sys.argv[6]))#bool toggle


# python3 jobRequest.py "CSC3002F" "java" "False" "" "rmrsuv002@gmail.com" "False"