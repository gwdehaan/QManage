__author__ = 'HAANG'
"""
Python - VMS - Queue beheer op basis van sh /queue /out=sswrk:CBTQueue.txt
01-07-2014 / 30-10-2016

Gebruiksaanwijzing :
VMS : sh queue /out=sswrk:CBTQueue.txt
FTP : overhalen naar c:\temp
------ Voor Assign / Deassign ------ (Assign.txt / DeAssign.txt)
Vul Node met de Node die buiten werking is en waarvoor de queues moeten worden omgeleid.
Dit moet voor elke server worden uitgevoerd

Voor het resetten van Queue's 
Gebruik : QRes.txt
"""

printer=""
Node = "CBT2B"
i=open("D:\\temp\\cbtqueue.txt","rt")
o=open("D:\\temp\\Assign.txt","wt")
d=open("D:\\temp\\DeAssign.txt","wt")
r=open("D:\\temp\\QRes.txt","wt")



for Line in i :
    
    if "stopped" in Line :
        printer=Line[14:Line.index(",")]
        r.write('start /next ' + printer + '\n')
    if "stalled" in Line :
        printer=Line[14:Line.index(",")]
        r.write('stop /reset ' + printer + '\n')
        r.write('start /next ' + printer + '\n')
    if Node in Line and '\",' in Line :
        printer=Line[14:Line.index(",")]
        printerx=printer + "X"
        poort=Line[Line.index("::")+3:Line.index('\",')]
        # print Line.index("::"), Line.index('\",')
        # print printer, printerx, poort
        o.write('init /que ' + printerx  + ' /processor=tcpip$telnetsym /on=\"'+ poort + '\"\n')
        o.write('start /que ' + printerx + '\n')
        o.write('assign /system ' + printerx + " " + printer + "\n")
        d.write("deassign /system " + printer + "\n")
        d.write("stop /que /reset " + printerx + "\n")
        d.write("del /que "+ printerx + "\n")

r.close()
d.close()
i.close()
o.close()
