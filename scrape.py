import requests 
from bs4 import BeautifulSoup

def get_content(url, params):
    response = requests.get(url, params=params)
    html = response.content
    soup = BeautifulSoup(html, 'xml')
    return soup

def get_rows(soup, class_name, summary):
    results = soup.find("table", {"class": class_name, "summary": summary})
    trs = results.findAll("tr")
    return trs
        
# this function navigates to the latest report and return the url
def find_latest_report(cik):
    
    url = "https://www.sec.gov/cgi-bin/browse-edgar"
    query_params = {"CIK": str(cik), "owner": "exclude", "action": "getcompany"}
    soup = get_content(url, query_params)
    trs = get_rows(soup, "tableFile2", "Results")
    
    for r in trs:
        tds = r.findAll('td')
        if len(tds) >= 2:
            if ('13F-HR' in tds[0].text):
#             for getting older report we could continue the loop with a decreasing variable counter.
#             counter is assigned based on how old the report needs to be  
#             if counter>0: counter-=1 continue
#             if ('13F' in tds[0].text) and counter == 0:
                trail = (tds[1].a.attrs['href'])
                break
        
    nextpage = 'https://www.sec.gov'+trail
   
    soup = get_content(nextpage, {})
    trs = get_rows(soup, "tableFile", "Document Format Files")
    
    for r in trs :
        tds = r.findAll('td')
        if len(tds)>0:
            if tds[3].string == 'INFORMATION TABLE' and tds[2].string[-3:] =='xml':
                return ("https://www.sec.gov"+str(tds[2].find('a')['href']))            
            

# this function creates a tsv file if the correct url for the report is passed. 
def tsvcreator(url,cik):
    soup = get_content(url, {})
    infotables = soup.findAll('infoTable')
    
    file_name = "outputs/{}.tsv".format(cik)
    with open(file_name, "w") as rf:
        rf.write("NAME OF ISSUER"+"\t"+"TITLE OF CLASS"+"\t"+"CUSIP"+"\t"+"VALUE(x$1000)"+"\t"+"SHRS OR PRN AMT"+"\t"+"SH/PRN"+"\t"+"PUT/CALL"+"\t"+"INVESTMENT DISCRETION"+"\t"+"OTHER MANAGER"+"\t"+"VOTING AUTHORITY SOLE"+"\t"+"VOTING AUTHORITY - SHARED"+"\t"+"VOTING AUTHORITY - NONE\n")
        
        for x in range(len(infotables)):
            if not infotables[x].putCall:
                putcall = infotables[x].putCall = ' '
            else:
                putcall = str(infotables[x].putCall.string)
            if not infotables[x].otherManager:
                othermanager = infotables[x].otherManager = ' '
            else:
                othermanager = str(infotables[x].otherManager.string)
            row = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(str(infotables[x].nameOfIssuer.string),str(infotables[x].titleOfClass.string),str(infotables[x].cusip.string),str(infotables[x].value.string),str(infotables[x].shrsOrPrnAmt.sshPrnamt.string),str(infotables[x].shrsOrPrnAmt.sshPrnamtType.string),putcall,str(infotables[x].investmentDiscretion.string),othermanager,str(infotables[x].votingAuthority.Sole.string),str(infotables[x].votingAuthority.Shared.string),str(infotables[x].votingAuthority.find('None').string))
            rf.write(row)
    return file_name
            
# main funtion that takes in a CIK and scrapes the data to create a file
def __main__():
    cik = input("Enter the CIK for the Company's report ")
    # Make sure the input is an integer.
    try:
        cik = int(cik)
    except:
        print("Please enter a valid integer!!")
        return

    try:
        latest_report_url = find_latest_report(cik)
        if latest_report_url:
            file_name = tsvcreator(latest_report_url, cik)
            print("Successfully created file in {}".format(file_name))
        else:
            print('The Information Table is not available')
    except Exception as exc:
        print("CIK entered is not valid. Please try a different value!")

__main__()
