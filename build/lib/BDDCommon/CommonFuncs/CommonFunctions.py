import psycopg2
import csv
import datetime
import cx_Oracle
dbName=None
dbUser=None
dbHost=None
dbPassword=None
dbPort=None
dbService=None;
con=None;
def connect_db(schema1='None',dbEnv1='None'):
    try:
        if(schema1.lower()=='ingest' or schema1.lower()=='exposure'):
            if(dbEnv1.lower()=='ccdev'):
               dbName="ccdb"; dbUser="ls_qa"; dbHost="localhost"; dbPassword="7TGObNhMgfugC#bP"; dbPort="5432";
               print("<<<<<<<CCDEV Environment excuted..>>>>>>>>!!")
            elif(dbEnv1.lower()=='ccprod'):
               dbName = "ccdb"; dbUser = "ls_read_only"; dbHost = "localhost"; dbPassword = "ls_read_only"; dbPort = "5433";
               print("<<<<<<<CCPROD Environment excuted..>>>>>>>>!!")
            else:
               print(" ***** No Ingest or Exposure Connection spitted out *****...!!!!!!!!!")
            con = psycopg2.connect(dbname=dbName, user=dbUser, host=dbHost, password=dbPassword, port=dbPort)
        elif(schema1.lower()=='staging'):
           print("In Oracle Staging Connection...!!")
           if(dbEnv1.lower()=='stable'):
               dbUser = "staging_ro"; dbPassword = "stagingR0_Qa"; dbHost = "localhost"; dbPort = "1521";  dbService = "staging.stable";
               print("<<<<<<<STABLE ORACLE Environment excuted..>>>>>>>>!!")
           elif (dbEnv1.lower() == 'prod'):
                dbUser = "staging_ro"; dbPassword = "stagingR0_Prod"; dbHost = "staging-prod-active-db.int.thomsonreuters.com";
                dbPort = "1521"; dbService = "staging.prod"
                print("<<<<<<<PROD ORACLE Environment excuted..>>>>>>>>!!")
           else:
                print("------========= NO Oracle Environment excuted..========---------!!")
           ora_dsn = cx_Oracle.makedsn('localhost', 1521, service_name='staging.stable')
           con = cx_Oracle.connect('staging_ro', 'stagingR0_Qa', ora_dsn)
           print('Qa Oracle Version :- ' + con.version);
        else:
            print("=====>>>>========= No Connection spitted out========<<<<=======...!!!!!!!!!")
            return None;

        print("dbEnv :", dbEnv1, " -- schema :", schema1);
        print("++++++++++++++++++Connected to DB..!+++++++++++++++++");
        return con;

    except Exception as e:
        print("========------------DB is not connected-----------------======...!!",e);
        con.close();
        return None;

def write_csv(context,diffList, diffSchema1ToSchema2FileName):
    print("-------------------In CSV------------ diffList:", diffList)
    dateTime = datetime.datetime.today().strftime('%d_%b_%Y_%H_%M_%S');
    diffFileName=diffSchema1ToSchema2FileName+'_'+dateTime+'.csv'
    try:
        diffFile=open(".\\"+diffFileName,'w',newline='')
        writer=csv.writer(diffFile)
        writer.writerows(diffList)
        diffFile.close()
        print("-------------------End of CSV------------ diffList:")
    except Exception as e:
        print("Can't write to the file {}",diffSchema1ToSchema2FileName);
        diffFile.close()
def write_html(context,caption,tableList):
    dateTime = datetime.datetime.today().strftime('%d_%b_%Y_%H_%M_%S');
    tableCaption = caption.title() +' Tables\'s Counts'
    tableList = tableList
    print("tableList[0][0]", tableList[0][1])
    htmlString = """<html><head>
    <style> body {padding: 20px; background-color: snow;}
    caption   {padding-bottom:10px; font-weight:bold; border-collapse:collapse; color:blue; border-color: black;}
    table {border-collapse: collapse;}
    table,th,td {border: 1px solid black;}
    td {padding-left:5px;}
    </style>
    </head><body><table border="1" width="300" height="200"><caption>""" + tableCaption + """</caption><tr>"""
    count = 0
    a = 1
    if (type(a) is int):
        print("a is int")
    else:
        print("a is NOT")
    bgColor = 'white'
    for row in tableList:
        for col in row:
            if (count == 0):
                htmlString = htmlString + '<th bgcolor="grey">' + col + '</th>'
            else:
                if (type(col) is int and row[1] != col):
                    print("col value difference :", row[1], " --- ", col);
                    bgColor = 'tomato'
                elif (type(col) is int and row[1] == col):
                    bgColor = 'palegreen'
                else:
                    bgColor = 'gainsboro'
                htmlString = htmlString + '<td bgcolor="' + bgColor + '">' + str(col) + '</td>'
        htmlString = htmlString + '</tr>'
        count += 1

    htmlString = htmlString + """</table></body></head></html>"""
    print(htmlString)
    file = '.\\'+caption+'\\outputFiles\\OutputFile_'+dateTime+'.htm';
    writer = open(file, 'w')
    writer.write(htmlString);
    writer.close()