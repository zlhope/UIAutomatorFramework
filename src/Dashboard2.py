__author__ = 'CWR368'
import os
import cPickle
import sys

#list all the dir named logs
#iterate over each list item and create list of folders starting from Stress, Stability, Sanity
#go into each folder and add all the info into list [path, deviceName, OS version, BuildName, Script Name,Link to file if over, ]

'''Device name	group all execution for that device\n'
 'OS version\n'
 'Build Name	group all execution for same build\n'
 '\n'
 'Script Name\n'
 'Start Time\n'
 'Execution Time if over\n'
 'Link to file if over\n'
 '\n'
 'Execution Summary\n'
 'Test case name 	Status	Time elapsed\n'
 '\n'
 'Crash Summary\n'
 'Crash Type	Test case 	Hours to crash	App if available')'''

def dashboard(path=None):
    try:

        list=[]
        if path is None:
            #root=os.getcwd()
            path=os.getcwd()
            if not os.path.exists(path):
                raise Exception("It is invalid valid path")
        else:
            if not os.path.exists(path):
                raise Exception("It is invalid valid path")

        for root, directories, filenames in os.walk(path):
            for directory in directories:
                list.append(os.path.join(root, directory))

        list2=[]
        for item in list:
            if item.endswith("\\Logs"):
                list2.append(item)

        print list2

        report = open("index.html", "w")
        report.write("<HTML>\n")
        report.write("<body bgcolor='#e6e6ff'>\n")
        report.write("<font color='#300E05'><h1><U>Dashboard</U></h1></font>\n")


        for x in list2:
            TestDirList=os.walk(x).next()[1]
            #print TestDirList
            for i in TestDirList[::-1]:
                try:

                    if os.path.exists(x+"\\"+i+"\\reportDetails"):
                        flag=True
                        report.write("<table border='1' cellpadding='10'>\n")
                        f1=open(x+"\\"+i+"\\reportDetails",'rb')
                        reportDetails=cPickle.load(f1)
                        #print "reportDetails:",reportDetails
                        report.write("<tr>\n")
                        report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Device Name </b></th>\n")
                        report.write("<th colspan=2 align='center'><b>" + reportDetails[0] + "</b></th>\n")
                        report.write("</tr>\n")
                        if len(reportDetails)>5:
                            report.write("<tr>\n")
                            report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>OS version </b></th>\n")
                            report.write("<th colspan=2 align='center'><b>" + reportDetails[5] + "</b></th>\n")
                            report.write("</tr>\n")
                        report.write("<tr>\n")
                        report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Build Name </b></th>\n")
                        report.write("<th colspan=2 align='center'><b>" + reportDetails[1] + "</b></th>\n")
                        report.write("</tr>\n")

                        report.write("<tr>\n")
                        report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Script Name </b></th>\n")
                        report.write("<th colspan=2 align='center'><b>" + reportDetails[2] + "</b></th>\n")
                        report.write("</tr>\n")

                        report.write("<tr>\n")
                        report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Start Time </b></th>\n")
                        report.write("<th colspan=2 align='center'><b>" + reportDetails[4] + "</b></th>\n")
                        report.write("</tr>\n")
                        if len(reportDetails)==7:
                            report.write("<tr>\n")
                            report.write("<th colspan=2 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Execution Time </b></th>\n")
                            report.write("<th colspan=2 align='center'><b>" + reportDetails[6] + "</b></th>\n")
                            report.write("</tr>\n")


                        #reportDetails=[productName,buildName,logName,self.relDirName + "/" + self.logname,self.startTime]

        #Execution Summary
        #Test case name 	Description	Status	Time elapsed

                    if os.path.exists(x+"\\"+i+"\\executionSummary"):
                        report.write("<table border='1' cellpadding='10'>\n")
                        report.write("<tr>\n")
                        report.write("<th colspan=4 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Execution Summary </b></th>\n")
                        report.write("</tr>\n")
                        f2=open(x+"\\"+i+"\\executionSummary",'rb')

                        report.write("<tr>\n")
                        report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Test case name </b></th>\n")

                        report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Description </b></th>\n")

                        report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Status </b></th>\n")

                        report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Time elapsed </b></th>\n")
                        report.write("</tr>\n")


                        f2=open(x+"\\"+i+"\\executionSummary",'rb')
                        executionSummary=cPickle.load(f2)
                        #print "executionSummary:",executionSummary


                        for j in executionSummary:
                            report.write("<tr>\n")
                            report.write("<th align='center'><b>" + j[0] + "</b></th>\n")



                            report.write("<th  align='left'><b>" + j[1] + "</b></th>\n")

                            report.write("<th align='center'><b>" + j[3] + "</b></th>\n")

                            if j[2] is not None:
                                report.write("<th  align='center'><b>" + j[2] + "</b></th>\n")
                            else:
                                report.write("<th  align='center'><b> NA </b></th>\n")
                            report.write("</tr>\n")
                        report.write("</table>\n")




                        #list of summary summary=[msg,info,None,'executing']
                        if os.path.exists(x+'\\'+i+"\\crashSummary"):

                            report.write("<table border='1' cellpadding='10'>\n")
                            report.write("<tr>\n")
                            report.write("<th colspan=5 bgcolor='#7F9A80' align='center'><b><font color='#033144'>Crash Summary </b></th>\n")
                            report.write("</tr>\n")

                            report.write("<tr>\n")
                            report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Crash Type </b></th>\n")

                            report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Test case  </b></th>\n")

                            report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Hours to crash </b></th>\n")

                            report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Log path </b></th>\n")


                            report.write("<th bgcolor='#C1CFE7' align='center'><b><font color='#033144'>Crashed App </b></th>\n")
                            report.write("</tr>\n")

                            f3=open(x+"\\"+i+"\\crashSummary",'rb')
                            crashSummary=cPickle.load(f3)
                            print "crashSummary:",crashSummary
                            anrCount=len(crashSummary[0])
                            print anrCount
                            if anrCount <= 0:
                                report.write("<tr>\n")
                                report.write("<th colspan=5 align='center'><b><font color='#033144'>No ANR observed. </b></th>\n")
                                report.write("</tr>\n")
                            else:
                                report.write("<tr>\n")
                                report.write("<th rowspan="+str(anrCount)+" align='center'><b><font color='#033144'>ANR </b></th>\n")
                                c=0
                                for k in crashSummary[0]:
                                    if c==0:
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[2]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\"+k[2] + "\">link</a></b></th>\n")
                                        report.write("<th  align='center'><b> NA </b></th>\n")
                                        report.write("</tr>\n")
                                    else:
                                        report.write("<tr>\n")
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[2]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\" + k[2] + "\">link</a></b></th>\n")
                                        report.write("<th  align='center'><b> NA </b></th>\n")
                                        report.write("</tr>\n")
                                    c=c+1



                            fcCount=len(crashSummary[2])
                            if fcCount <= 0:
                                report.write("<tr>\n")
                                report.write("<th colspan=5 align='center'><b><font color='#033144'>No Force Close observed. </b></th>\n")
                                report.write("</tr>\n")
                            else:
                                report.write("<tr>\n")
                                report.write("<th rowspan="+str(fcCount)+" align='center'><b><font color='#033144'>Force Close </b></th>\n")
                                c=0
                                for k in crashSummary[2]:
                                    if c==0:
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[3]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\" + k[3] + "\">link</a> </b></th>\n")
                                        report.write("<th  align='center'><b>" + k[2] + " </b></th>\n")
                                        report.write("</tr>\n")
                                    else:
                                        report.write("<tr>\n")
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[3]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\" + k[3] + "\">link</a> </b></th>\n")
                                        report.write("<th  align='center'><b>" + k[2] + " </b></th>\n")
                                        report.write("</tr>\n")

                                    c=c+1

                            resetCount=len(crashSummary[1])
                            if resetCount <= 0:
                                report.write("<tr>\n")
                                report.write("<th colspan=5 align='center'><b><font color='#033144'>No Reboot observed. </b></th>\n")
                                report.write("</tr>\n")
                            else:
                                report.write("<tr>\n")
                                report.write("<th rowspan="+str(resetCount)+" align='center'><b><font color='#033144'>Reset </b></th>\n")
                                c=0
                                for k in crashSummary[1]:
                                    if c==0:
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[2]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\" + k[2] + "\">link</a></b></th>\n")
                                        report.write("<th  align='center'><b> NA </b></th>\n")
                                        report.write("</tr>\n")
                                    else:
                                        report.write("<tr>\n")
                                        report.write("<th  align='center'><b>" + k[0] + "</b></th>\n")
                                        report.write("<th  align='center'><b>" + k[1] + "</b></th>\n")
                                        print k[2]
                                        report.write("<th  align='center'><b><a href=\"" + x+"\\"+i+"\\" + k[2] + "\">link</a> </b></th>\n")
                                        report.write("<th  align='center'><b> NA </b></th>\n")
                                        report.write("</tr>\n")
                                        report.write("</tr>\n")
                        if flag:
                            report.write("</table>\n")
                            report.write("<br><hr style='border: 3px dotted #0099CC' color='#000000'><br>\n")
                except Exception, e:
                    print e
        report.flush()
        report.close()

    except Exception, e:
        print e


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            print sys.argv
            print len(sys.argv)
            dashboard(sys.argv[1])


        else:
            dashboard()
    except Exception, e:
        print e
