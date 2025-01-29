import json, datetime
import xlsxwriter
from OFX_API import apiRequestManager
from production.models import Projects, Task_Type
from ofx_statistics.models import ClientArtistStatistics


def convert_date(conversion_date):
    '''
    Converts Date Time Object to date
    params: datetime
    returns: converted date
    '''

    try:
        _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%dT%H:%M:%S.%f').strftime("%d-%m-%Y")
    except:
        _date = datetime.datetime.strptime(conversion_date, '%Y-%m-%d.%f').strftime("%d-%m-%Y")
    return _date

def writeClientreportWorksheet(buffer,query={},data=[],clientName=""):
    # myKeys = list(data.keys())
    # myKeys.sort(reverse=True)
    # data = json.loads(json.dumps({i: data[i] for i in myKeys}))
    projectsName = list(Projects.objects.filter(id=query['project__id']).values('name'))[0]['name'] if query.get('project__id',None) is not None else 'All Projects'
    departmentName = list(Task_Type.objects.filter(id=query['dep__id']).values('name'))[0]['name'] if query.get('dep__id',None) is not None else 'All Departments'
    workbook = xlsxwriter.Workbook(buffer)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    borderWithColor = workbook.add_format({'border': 1, 'border_color': 'black', 'bg_color': 'red', 'font_color':'#ffffff'})
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black', 'align': 'center', 'valign': 'vcenter'})
    worksheet1 = workbook.add_worksheet(name='Client Report')
    worksheet2 = workbook.add_worksheet(name='Report Details')
    

    detalsRowStart = 1
 
    worksheet2.merge_range('A{a}:A{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"PROJECTS", merge_format)
    worksheet2.merge_range('B{a}:B{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"DEPARTMENTS", merge_format)
    worksheet2.merge_range('C{a}:C{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"TOTAL SHOTS", merge_format)
    worksheet2.merge_range('D{a}:E{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"MANDAYS", merge_format)
    worksheet2.merge_range('F{a}:H{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"HIGHEST VERSION", merge_format)
    worksheet2.merge_range('I{a}:J{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"VFX ARTISTS", merge_format)
    worksheet2.merge_range('K{a}:K{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"RETAKE PERCENTAGE", merge_format)
    worksheet2.merge_range('L{a}:M{b}'.format(a=detalsRowStart,b=detalsRowStart+1),"MISSED ETA", merge_format)
    
    
    worksheet2.write('A{a}'.format(a=detalsRowStart+2), 'PROJECT', bold)
    worksheet2.write('B{a}'.format(a=detalsRowStart+2), 'DEPARTMENT', bold)
    worksheet2.write('C{a}'.format(a=detalsRowStart+2), 'SHOTS', bold)
    worksheet2.write('D{a}'.format(a=detalsRowStart+2), 'TARGET', bold)
    worksheet2.write('E{a}'.format(a=detalsRowStart+2), 'ACHIEVED', bold)
    worksheet2.write('F{a}'.format(a=detalsRowStart+2), 'VERSION', bold)
    worksheet2.write('G{a}'.format(a=detalsRowStart+2), 'SHOTS', bold)
    worksheet2.write('H{a}'.format(a=detalsRowStart+2), 'PERCENTAGE', bold)
    worksheet2.write('I{a}'.format(a=detalsRowStart+2), 'ARTISTS', bold)
    worksheet2.write('J{a}'.format(a=detalsRowStart+2), 'MANDAYS/DAY', bold)
    worksheet2.write('K{a}'.format(a=detalsRowStart+2), 'PERCENTAGE', bold)
    worksheet2.write('L{a}'.format(a=detalsRowStart+2), 'SHOTS', bold)
    worksheet2.write('M{a}'.format(a=detalsRowStart+2), 'PERCENTAGE', bold)
    totalLog = {
        "tmd":0,
        "amd":0,
        "totalshots":0,
        "highest_ver":None,
        "highest_ver_shotCount":None,
        "artistcount":0,
        "artistTMD":0,
        "retake_per":0,
        "retake_per_count":0,
        "missedEta":0,
        }

    totalLogByDep = {}
    totalLogByProject = {}

    for rowId,xd in enumerate(data):
        totalLog["tmd"] = + xd["tmd"]
        totalLog["amd"] = + xd["amd"]
        totalLog["totalshots"] = + xd["totalshots"]
        totalLog["highest_ver_shotCount"] = xd["highest_ver_shotCount"] if totalLog["highest_ver"] is None or totalLog["highest_ver"] < xd["highest_ver"] else totalLog["highest_ver_shotCount"]
        totalLog["highest_ver"] = xd["highest_ver"] if totalLog["highest_ver"] is None or totalLog["highest_ver"] < xd["highest_ver"] else totalLog["highest_ver"]
        totalLog["artistcount"] = + xd["artistcount"]
        totalLog["artistTMD"] = + xd["artistTMD"]
        totalLog["retake_per"] = + xd["retake_per"]
        totalLog["retake_per_count"] = + 1
        totalLog["missedEta"] = + xd["missedEta"]
        if totalLogByDep.get(xd["dep"]["name"],None) is None:
            totalLogByDep[xd["dep"]["name"]] = {
                "tmd":0,
                "amd":0,
                "totalshots":0,
                "highest_ver":None,
                "highest_ver_shotCount":None,
                "artistcount":0,
                "artistTMD":0,
                "retake_per":0,
                "retake_per_count":0,
                "missedEta":0,
                }
        totalLogByDep[xd["dep"]["name"]]["tmd"] = + xd["tmd"]
        totalLogByDep[xd["dep"]["name"]]["amd"] = + xd["amd"]
        totalLogByDep[xd["dep"]["name"]]["totalshots"] = + xd["totalshots"]
        totalLogByDep[xd["dep"]["name"]]["highest_ver_shotCount"] = xd["highest_ver_shotCount"] if totalLogByDep[xd["dep"]["name"]]["highest_ver"] is None or totalLogByDep[xd["dep"]["name"]]["highest_ver"] < xd["highest_ver"] else totalLogByDep[xd["dep"]["name"]]["highest_ver_shotCount"]
        totalLogByDep[xd["dep"]["name"]]["highest_ver"] = xd["highest_ver"] if totalLogByDep[xd["dep"]["name"]]["highest_ver"] is None or totalLogByDep[xd["dep"]["name"]]["highest_ver"] < xd["highest_ver"] else totalLogByDep[xd["dep"]["name"]]["highest_ver"]
        totalLogByDep[xd["dep"]["name"]]["artistcount"] = + xd["artistcount"]
        totalLogByDep[xd["dep"]["name"]]["artistTMD"] = + xd["artistTMD"]
        totalLogByDep[xd["dep"]["name"]]["retake_per"] = + xd["retake_per"]
        totalLogByDep[xd["dep"]["name"]]["retake_per_count"] = + 1
        totalLogByDep[xd["dep"]["name"]]["missedEta"] = + xd["missedEta"]

        if totalLogByProject.get(xd["project"]["name"],None) is None:
            totalLogByProject[xd["project"]["name"]] = {
                "tmd":0,
                "amd":0,
                "totalshots":0,
                "highest_ver":None,
                "highest_ver_shotCount":None,
                "artistcount":0,
                "artistTMD":0,
                "retake_per":0,
                "retake_per_count":0,
                "missedEta":0,
                }
        totalLogByProject[xd["project"]["name"]]["tmd"] = + xd["tmd"]
        totalLogByProject[xd["project"]["name"]]["amd"] = + xd["amd"]
        totalLogByProject[xd["project"]["name"]]["totalshots"] = + xd["totalshots"]
        totalLogByProject[xd["project"]["name"]]["highest_ver_shotCount"] = xd["highest_ver_shotCount"] if totalLogByProject[xd["project"]["name"]]["highest_ver"] is None or totalLogByProject[xd["project"]["name"]]["highest_ver"] < xd["highest_ver"] else totalLogByProject[xd["project"]["name"]]["highest_ver_shotCount"]
        totalLogByProject[xd["project"]["name"]]["highest_ver"] = xd["highest_ver"] if totalLogByProject[xd["project"]["name"]]["highest_ver"] is None or totalLogByProject[xd["project"]["name"]]["highest_ver"] < xd["highest_ver"] else totalLogByProject[xd["project"]["name"]]["highest_ver"]
        totalLogByProject[xd["project"]["name"]]["artistcount"] = + xd["artistcount"]
        totalLogByProject[xd["project"]["name"]]["artistTMD"] = + xd["artistTMD"]
        totalLogByProject[xd["project"]["name"]]["retake_per"] = + xd["retake_per"]
        totalLogByProject[xd["project"]["name"]]["retake_per_count"] = + 1
        totalLogByProject[xd["project"]["name"]]["missedEta"] = + xd["missedEta"]

        worksheet2.write(rowId+detalsRowStart+2,0,xd["project"]["name"], border)
        worksheet2.write(rowId+detalsRowStart+2,1,xd["dep"]["name"], border)
        worksheet2.write(rowId+detalsRowStart+2,2,xd["totalshots"], border)
        worksheet2.write(rowId+detalsRowStart+2,3,xd["tmd"], border)
        worksheet2.write(rowId+detalsRowStart+2,4,xd["amd"], border)
        worksheet2.write(rowId+detalsRowStart+2,5,"V{:03d}".format(xd["highest_ver"]), border)
        worksheet2.write(rowId+detalsRowStart+2,6,xd["highest_ver_shotCount"], border)
        worksheet2.write(rowId+detalsRowStart+2,7,"{c}%".format(c=int((100/xd["totalshots"])*xd["highest_ver_shotCount"])), border)
        worksheet2.write(rowId+detalsRowStart+2,8,xd["artistcount"], border)
        worksheet2.write(rowId+detalsRowStart+2,9,xd["artistTMD"], border)
        worksheet2.write(rowId+detalsRowStart+2,10,"{c}%".format(c=int(xd["retake_per"])), border)
        worksheet2.write(rowId+detalsRowStart+2,11,xd["missedEta"], border)
        worksheet2.write(rowId+detalsRowStart+2,12,"{c}%".format(c=int((100/xd["totalshots"])*xd["missedEta"])), border)


    worksheet1.merge_range('A1:C2', 'CLIENT: {clientName}'.format(clientName=clientName), merge_format)
    worksheet1.merge_range('D1:E2', 'PROJECT: {projectsName}'.format(projectsName=projectsName), merge_format)
    worksheet1.merge_range('F1:H2', 'DEPARTMENT: {departmentName}'.format(departmentName=departmentName), merge_format)
    worksheet1.merge_range('I1:J2', 'TOTAL SHOTS: {totalshots}'.format(totalshots=totalLog["totalshots"]), merge_format)
    worksheet1.merge_range('K1:L1', 'MANDAYS', merge_format)
    worksheet1.write('K2','TARGET: {tmd}'.format(tmd=totalLog["tmd"]), bold)
    worksheet1.write('L2','ACHIEVED: {amd}'.format(amd=totalLog["amd"]), bold)

    worksheet1.merge_range('M1:O1', 'HIGHEST VERSION', merge_format)
    worksheet1.write('M2','VERSION: V{:03d}'.format(totalLog["highest_ver"]), bold)
    worksheet1.write('N2','SHOTS: {hvShots}'.format(hvShots=totalLog["highest_ver_shotCount"]), bold)
    worksheet1.write('O2','PERCENTAGE: {hvPercnt}%'.format(hvPercnt=int((100/totalLog["totalshots"])*totalLog["highest_ver_shotCount"])), bold)
    
    worksheet1.merge_range('P1:S1', 'VFX ARTISTS', merge_format)
    worksheet1.merge_range('P2:Q2','ARTISTS: {artist}'.format(artist=totalLog["artistcount"]), merge_format)
    worksheet1.merge_range('R2:S2','MANDAYS/DAY: {artmnday}'.format(artmnday=totalLog["artistTMD"]), merge_format)
 
    worksheet1.merge_range('T1:W1', 'MISSED ETA', merge_format)
    worksheet1.merge_range('T2:U2', 'SHOTS: {eta}'.format(eta=totalLog["totalshots"]), bold)
    worksheet1.merge_range('V2:W2', 'PERCENTAGE: {etaPernct}%'.format(etaPernct=int((100/totalLog["totalshots"])*totalLog["missedEta"])), bold)

    worksheet1.merge_range('X1:Z2', 'RETAKE PERCENTAGE: {retake_per}%'.format(retake_per=int(totalLog["retake_per"]/totalLog["retake_per_count"])), merge_format)

    dRowStart = 4
    # BY PROJECTS
    worksheet1.merge_range('A{a}:L{b}'.format(a=dRowStart,b=dRowStart+1),"BY PROJECTS", merge_format)

    worksheet1.merge_range('A{a}:A{b}'.format(a=dRowStart+2,b=dRowStart+3), 'PROJECT', merge_format)

    worksheet1.merge_range('B{a}:C{b}'.format(a=dRowStart+2,b=dRowStart+2), 'MANDAYS', merge_format)
    worksheet1.write('B{a}'.format(a=dRowStart+3),'TARGET', bold)
    worksheet1.write('C{a}'.format(a=dRowStart+3),'ACHIEVED', bold)

    worksheet1.merge_range('D{a}:F{b}'.format(a=dRowStart+2,b=dRowStart+2), 'HIGHEST VERSION', merge_format)
    worksheet1.write('D{a}'.format(a=dRowStart+3),'VERSION', bold)
    worksheet1.write('E{a}'.format(a=dRowStart+3),'SHOTS', bold)
    worksheet1.write('F{a}'.format(a=dRowStart+3),'PERCENTAGE', bold)

    worksheet1.merge_range('G{a}:H{b}'.format(a=dRowStart+2,b=dRowStart+2), 'VFX ARTISTS', merge_format)
    worksheet1.write('G{a}'.format(a=dRowStart+3),'ARTISTS', bold)
    worksheet1.write('H{a}'.format(a=dRowStart+3),'MANDAYS/DAY', bold)

    worksheet1.merge_range('I{a}:J{b}'.format(a=dRowStart+2,b=dRowStart+2), 'MISSED ETA', merge_format)
    worksheet1.write('I{a}'.format(a=dRowStart+3),'SHOTS', bold)
    worksheet1.write('J{a}'.format(a=dRowStart+3),'PERCENTAGE', bold)

    worksheet1.merge_range('K{a}:L{b}'.format(a=dRowStart+2,b=dRowStart+3), 'RETAKE PERCENTAGE', merge_format)

    row = dRowStart+3
    for project,xd in totalLogByProject.items():
        worksheet1.write(row,0,project, border)
        worksheet1.write(row,1,xd["tmd"], border)
        worksheet1.write(row,2,xd["amd"], border)
        worksheet1.write(row,3,"V{:03d}".format(xd["highest_ver"]), border)
        worksheet1.write(row,4,xd["highest_ver_shotCount"], border)
        worksheet1.write(row,5,"{c}%".format(c=int((100/xd["totalshots"])*xd["highest_ver_shotCount"])), border)
        worksheet1.write(row,6,xd["artistcount"], border)
        worksheet1.write(row,7,xd["artistTMD"], border)
        worksheet1.write(row,8,xd["missedEta"], border)
        worksheet1.write(row,9,"{c}%".format(c=int((100/xd["totalshots"])*xd["missedEta"])), border)
        worksheet1.merge_range('K{a}:L{b}'.format(a=row+1,b=row+1),"{c}%".format(c=int(xd["retake_per"]/xd["retake_per_count"])), border)
        row += 1
    byProjectMax = row


    # BY DEPARTMENTS
    worksheet1.merge_range('O{a}:Z{b}'.format(a=dRowStart,b=dRowStart+1),"BY DEPARTMENTS", merge_format)

    worksheet1.merge_range('O{a}:O{b}'.format(a=dRowStart+2,b=dRowStart+3), 'DEPARTMENT', merge_format)

    worksheet1.merge_range('P{a}:Q{b}'.format(a=dRowStart+2,b=dRowStart+2), 'MANDAYS', merge_format)
    worksheet1.write('P{a}'.format(a=dRowStart+3),'TARGET', bold)
    worksheet1.write('Q{a}'.format(a=dRowStart+3),'ACHIEVED', bold)

    worksheet1.merge_range('R{a}:T{b}'.format(a=dRowStart+2,b=dRowStart+2), 'HIGHEST VERSION', merge_format)
    worksheet1.write('R{a}'.format(a=dRowStart+3),'VERSION', bold)
    worksheet1.write('S{a}'.format(a=dRowStart+3),'SHOTS', bold)
    worksheet1.write('T{a}'.format(a=dRowStart+3),'PERCENTAGE', bold)

    worksheet1.merge_range('U{a}:V{b}'.format(a=dRowStart+2,b=dRowStart+2), 'VFX ARTISTS', merge_format)
    worksheet1.write('U{a}'.format(a=dRowStart+3),'ARTISTS', bold)
    worksheet1.write('V{a}'.format(a=dRowStart+3),'MANDAYS/DAY', bold)

    worksheet1.merge_range('W{a}:X{b}'.format(a=dRowStart+2,b=dRowStart+2), 'MISSED ETA', merge_format)
    worksheet1.write('W{a}'.format(a=dRowStart+3),'SHOTS', bold)
    worksheet1.write('X{a}'.format(a=dRowStart+3),'PERCENTAGE', bold)

    worksheet1.merge_range('Y{a}:Z{b}'.format(a=dRowStart+2,b=dRowStart+3), 'RETAKE PERCENTAGE', merge_format)

    row = dRowStart+3
    for dep,xd in totalLogByDep.items():
        worksheet1.write(row,14,dep, border)
        worksheet1.write(row,15,xd["tmd"], border)
        worksheet1.write(row,16,xd["amd"], border)
        worksheet1.write(row,17,"V{:03d}".format(xd["highest_ver"]), border)
        worksheet1.write(row,18,xd["highest_ver_shotCount"], border)
        worksheet1.write(row,19,"{c}%".format(c=int((100/xd["totalshots"])*xd["highest_ver_shotCount"])), border)
        worksheet1.write(row,20,xd["artistcount"], border)
        worksheet1.write(row,21,xd["artistTMD"], border)
        worksheet1.write(row,22,xd["missedEta"], border)
        worksheet1.write(row,23,"{c}%".format(c=int((100/xd["totalshots"])*xd["missedEta"])), border)
        worksheet1.merge_range('Y{a}:Z{b}'.format(a=row+1,b=row+1),"{c}%".format(c=int(xd["retake_per"]/xd["retake_per_count"])), border)
        row += 1
    byDepMax = row

    # STATISTICS
    apiRequestManagers = apiRequestManager()
    statistics = apiRequestManagers.getDBData(model=ClientArtistStatistics,queryFilter=query,select_related=["project","dep","artist","artist__location","artist__role", "artist__grade","tl","supervisor","hod"],queryPerams=[
                "id",
                "project__id",
                "project__name",
                "dep__id",
                "dep__name",
                "artist__id",
                "artist__creation_date",
                "artist__doe",
                "artist__fullName",
                "artist__employee_id",
                "artist__location__id",
                "artist__location__name",
                "artist__role__id",
                "artist__role__name",
                "artist__grade__id",
                "artist__grade__name",
                "artist__grade__a_man_day",
                "tl__id",
                "tl__fullName",
                "supervisor__id",
                "supervisor__fullName",
                "hod__id",
                "hod__fullName",
                "tmd",
                "amd",
                "shotsCount"
                ])

    dRowStart = 4
    worksheet3 = workbook.add_worksheet(name='Statistics')

    totalLog = {
        "tmd":0,
        "amd":0,
        "totalshots":0,
        "artistcount":0,
        "artistTMD":0
        }
    
    worksheet3.write('A{a}'.format(a=dRowStart+1),'ARTIST', bold)
    worksheet3.write('B{a}'.format(a=dRowStart+1),'DOJ', bold)
    worksheet3.write('C{a}'.format(a=dRowStart+1),'DOE', bold)
    worksheet3.write('D{a}'.format(a=dRowStart+1),'ROLE', bold)
    worksheet3.write('E{a}'.format(a=dRowStart+1),'GRADE', bold)
    worksheet3.write('F{a}'.format(a=dRowStart+1),'PROJECT', bold)
    worksheet3.write('G{a}'.format(a=dRowStart+1),'DEPARTMENT', bold)
    worksheet3.write('H{a}'.format(a=dRowStart+1),'SHOTS', bold)
    worksheet3.write('I{a}'.format(a=dRowStart+1),'TEAM LEAD', bold)
    worksheet3.write('J{a}'.format(a=dRowStart+1),'SUPERVISOR', bold)
    worksheet3.write('K{a}'.format(a=dRowStart+1),'HOD', bold)
    worksheet3.write('L{a}'.format(a=dRowStart+1),'TMD', bold)
    worksheet3.write('M{a}'.format(a=dRowStart+1),'AMD', bold)
    worksheet3.write('N{a}'.format(a=dRowStart+1),'LOCATION', bold)
    usedArtists = []
    row = dRowStart+1
    for rowX,xd in enumerate(statistics):
        totalLog["totalshots"] += xd["shotsCount"]
        totalLog["tmd"] += xd["tmd"]
        totalLog["amd"] += xd["amd"]
        if xd["artist"]["id"] not in usedArtists:
            usedArtists.append(xd["artist"]["id"])
            totalLog["artistcount"] += 1
            if xd["artist"]["grade"] is not None:
                totalLog["artistTMD"] = totalLog["artistTMD"] + xd["artist"]["grade"]["a_man_day"]
        worksheet3.write(row+rowX,0,xd["artist"]["fullName"], border)
        worksheet3.write(row+rowX,1,convert_date(xd["artist"]['creation_date'].split(" ")[0]+"T00:00:00.000000"), border)
        worksheet3.write(row+rowX,2,convert_date(xd["artist"]["doe"]+"T00:00:00.000000") if xd["artist"]["doe"] is not None else "N/A", merge_format if xd["artist"]["doe"] is not None else border)
        worksheet3.write(row+rowX,3,xd["artist"]["role"]["name"] if xd["artist"]["role"] is not None else "N/A", border)
        worksheet3.write(row+rowX,4,"{grade}({manday})".format(grade=xd["artist"]["grade"]["name"],manday=xd["artist"]["grade"]["a_man_day"]) if xd["artist"]["grade"] is not None else "N/A", border)
        worksheet3.write(row+rowX,5,xd["project"]["name"], border)
        worksheet3.write(row+rowX,6,xd["dep"]["name"], border)
        worksheet3.write(row+rowX,7,xd["shotsCount"], border)
        worksheet3.write(row+rowX,8,xd["tl"]["fullName"] if xd["tl"] is not None else "N/A", border)
        worksheet3.write(row+rowX,9,xd["supervisor"]["fullName"] if xd["supervisor"] is not None else "N/A", border)
        worksheet3.write(row+rowX,10,xd["hod"]["fullName"] if xd["hod"] is not None else "N/A", border)
        worksheet3.write(row+rowX,11,xd["tmd"], border)
        worksheet3.write(row+rowX,12,xd["amd"], border)
        worksheet3.write(row+rowX,13,xd["artist"]["location"]["name"] if xd["artist"]["location"] is not None else "GLOBAL", border)


    worksheet3.merge_range('A1:C3', 'CLIENT: {clientName}'.format(clientName=clientName), merge_format)
    worksheet3.merge_range('D1:F3', 'PROJECTS: {projectsName}'.format(projectsName=projectsName), merge_format)
    worksheet3.merge_range('G1:H3', 'DEPARTMENTS: {departmentName}'.format(departmentName=departmentName), merge_format)
    worksheet3.merge_range('I1:J3', 'TOTAL SHOTS: {totalshots}'.format(totalshots=totalLog["totalshots"]), merge_format)
    worksheet3.merge_range('K1:L2', 'MANDAYS', merge_format)
    worksheet3.write('K3','TARGET: {tmd}'.format(tmd=totalLog["tmd"]), bold)
    worksheet3.write('L3','ACHIEVED: {amd}'.format(amd=totalLog["amd"]), bold)
 
    worksheet3.merge_range('M1:N2', 'VFX ARTISTS', merge_format)
    worksheet3.write('M3','ARTISTS: {artist}'.format(artist=totalLog["artistcount"]), bold)
    worksheet3.write('N3','MANDAYS/DAY: {artmnday}'.format(artmnday=totalLog["artistTMD"]), bold) 

    workbook.close()
    return buffer