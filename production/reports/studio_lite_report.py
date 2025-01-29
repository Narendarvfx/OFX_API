import xlsxwriter
def writeStudioLiteReportWorksheet(buffer,data={}):
    workbook = xlsxwriter.Workbook(buffer)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    borderWithColor = workbook.add_format({'border': 1, 'border_color': 'black', 'bg_color': 'red', 'font_color':'#ffffff'})
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    worksheet = workbook.add_worksheet(name='Studio Report')

    rowIndex = -2
    colIndex = 0
    for type,_data in data.items():
        rowIndex = rowIndex + 3
        if type=="achievedMandays":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:B{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Achieved Mandays', merge_format)
            rowIndex = rowIndex + 1
            worksheet.write(rowIndex,0,'Departments: {department}'.format(department=', '.join(_data["details"].keys())), merge_format)
            worksheet.write(rowIndex,1,'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            rowIndex = rowIndex + 1
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Target Mandays', bold)
            worksheet.write(rowIndex,colIndex+1,'Achieved Mandays', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            worksheet.write(rowIndex,colIndex,float(_data["tmd"]), border)
            worksheet.write(rowIndex,colIndex+1,float(_data["amd"]), border)
            rowIndex = rowIndex + 1

            subRowIndex = 1
            achievedMandaysWorksheet = workbook.add_worksheet(name='Achieved Mandays')
            achievedMandaysWorksheet.write(subRowIndex,0,'Achieved Mandays', merge_format)
            achievedMandaysWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex,rowTo=subRowIndex+1),'Achieved Mandays', merge_format)
            achievedMandaysWorksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=subRowIndex,rowTo=subRowIndex+1),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            subRowIndex = subRowIndex + 1
            achievedMandaysWorksheet.write(subRowIndex,0,'Department', bold)
            achievedMandaysWorksheet.write(subRowIndex,1,'Target Mandays', bold)
            achievedMandaysWorksheet.write(subRowIndex,2,'Achieved Mandays', bold)
            subRowIndex = subRowIndex + 1
            for department,dep_data in _data["details"].items():
                achievedMandaysWorksheet.write(subRowIndex,0,department, border)
                achievedMandaysWorksheet.write(subRowIndex,1,float(dep_data["tmd"]), border)
                achievedMandaysWorksheet.write(subRowIndex,2,float(dep_data["amd"]), border)
                subRowIndex = subRowIndex + 1
        elif type=="monthlyAchievement":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Monthly Achievement', merge_format)
            rowIndex = rowIndex + 2
            worksheet.write(rowIndex-1,0,'Departments: {department}'.format(department=', '.join(_data["details"].keys())), merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Month', bold)
            worksheet.write(rowIndex,colIndex+1,'Target Mandays', bold)
            worksheet.write(rowIndex,colIndex+2,'Achieved Mandays', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            subRowIndex = 1
            monthlyAchievementWorksheet = workbook.add_worksheet(name='Monthly Achievement')
            monthlyAchievementWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex,rowTo=subRowIndex+1),'Monthly Achievement', merge_format)
            monthlyAchievementWorksheet.merge_range('B{rowFrom}:{char}{rowTo}'.format(char=chr(65+(len(_data["data"])*2)),rowFrom=subRowIndex,rowTo=subRowIndex+1),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            subRowIndex = subRowIndex + 1
            monthlyAchievementWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex+1,rowTo=subRowIndex+2),'Departments', merge_format)
            subColIndex = 1
            itemNames = {}
            for d in _data["data"]:
                itemNames[d["y"]] = {
                    "y":d["y"],
                    "tmd":0,
                    "amd":0,
                    }
                monthlyAchievementWorksheet.merge_range('{char1}{rowFrom}:{char2}{rowTo}'.format(char1=chr(65+subColIndex),char2=chr(66+subColIndex),rowFrom=subRowIndex+1,rowTo=subRowIndex+1),d["y"], merge_format)
                monthlyAchievementWorksheet.write(subRowIndex+1,subColIndex,'Target Mandays', bold)
                monthlyAchievementWorksheet.write(subRowIndex+1,subColIndex+1,'Achieved Mandays', bold)
                worksheet.write(rowIndex,colIndex,d["y"], border)
                worksheet.write(rowIndex,colIndex+1,float(d["tmd"]), border)
                worksheet.write(rowIndex,colIndex+2,float(d["amd"]), border)
                rowIndex = rowIndex + 1
                subColIndex = subColIndex + 2
            monthlyAchievementWorksheet.merge_range('{char1}{rowFrom}:{char2}{rowTo}'.format(char1=chr(65+subColIndex),char2=chr(66+subColIndex),rowFrom=1,rowTo=subRowIndex+1),'Total', merge_format)
            monthlyAchievementWorksheet.write(subRowIndex+1,subColIndex,'Target Mandays', merge_format)
            monthlyAchievementWorksheet.write(subRowIndex+1,subColIndex+1,'Achieved Mandays', merge_format)
            lastSubColIndex = subColIndex
            subRowIndex = subRowIndex + 2
            for department,dep_data in _data["details"].items():
                monthlyAchievementWorksheet.write(subRowIndex,0,department, border)
                subColIndex = 1
                _itemNames = itemNames.copy()
                for _dep_data in dep_data["data"]:
                    _itemNames[_dep_data["y"]] = {
                        "y":_dep_data["y"],
                        "tmd":_dep_data["tmd"],
                        "amd":_dep_data["amd"],
                        }
                for _dep_data in list(_itemNames.values()):
                    monthlyAchievementWorksheet.write(subRowIndex,subColIndex,float(_dep_data['tmd']), border)
                    monthlyAchievementWorksheet.write(subRowIndex,subColIndex+1,float(_dep_data['amd']), border)
                    subColIndex = subColIndex + 2
                monthlyAchievementWorksheet.write(subRowIndex,lastSubColIndex,float(dep_data['tmd']), border)
                monthlyAchievementWorksheet.write(subRowIndex,lastSubColIndex+1,float(dep_data['amd']), border)
                subRowIndex = subRowIndex + 1
        elif type=="artistsReport":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Artists by Grades', merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Total Artists: {totalArtists}'.format(totalArtists=_data["totalArtists"]), merge_format)
            rowIndex = rowIndex + 2
            worksheet.write(rowIndex-1,0,'Departments: {department}'.format(department=', '.join(_data["details"].keys())), merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Grade', bold)
            worksheet.write(rowIndex,colIndex+1,'Artists', bold)
            worksheet.write(rowIndex,colIndex+2,'Ability per day', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            subRowIndex = 1
            artistsReportWorksheet = workbook.add_worksheet(name='Artists Report')
            artistsReportWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex,rowTo=subRowIndex+1),'Artists by Grades', merge_format)
            artistsReportWorksheet.merge_range('B{rowFrom}:{char}{rowTo}'.format(char=chr(65+(len(_data["grades"])*2)),rowFrom=subRowIndex,rowTo=subRowIndex+1),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            subRowIndex = subRowIndex + 1
            artistsReportWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex+1,rowTo=subRowIndex+2),'Departments', merge_format)
            subColIndex = 1
            itemNames = {}
            for d in _data["grades"]:
                itemNames[d["y"]] = {
                    "y":d["y"],
                    "a":0,
                    }
                grd = float(d["y"].split('(')[1].split(')')[0])
                worksheet.write(rowIndex,colIndex,d["y"], border)
                worksheet.write(rowIndex,colIndex+1,int(d["a"]), border)
                worksheet.write(rowIndex,colIndex+2,float(int(d["a"])*grd), border)
                artistsReportWorksheet.merge_range('{char1}{rowFrom}:{char2}{rowTo}'.format(char1=chr(65+subColIndex),char2=chr(66+subColIndex),rowFrom=subRowIndex+1,rowTo=subRowIndex+1),d["y"], merge_format)
                artistsReportWorksheet.write(subRowIndex+1,subColIndex,'Artists', bold)
                artistsReportWorksheet.write(subRowIndex+1,subColIndex+1,'Ability per day', bold)
                rowIndex = rowIndex + 1
                subColIndex = subColIndex + 2
            artistsReportWorksheet.merge_range('{char1}{rowFrom}:{char2}{rowTo}'.format(char1=chr(65+subColIndex),char2=chr(68+subColIndex),rowFrom=1,rowTo=subRowIndex+1),'Total', merge_format)
            artistsReportWorksheet.write(subRowIndex+1,subColIndex,'Artists', merge_format)
            artistsReportWorksheet.write(subRowIndex+1,subColIndex+1,'Ability per day', merge_format)
            artistsReportWorksheet.write(subRowIndex+1,subColIndex+2,'On Leave', merge_format)
            artistsReportWorksheet.write(subRowIndex+1,subColIndex+3,'Available Mandays', merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Present', bold)
            worksheet.write(rowIndex,colIndex+1,'On Leave', bold)
            worksheet.write(rowIndex,colIndex+2,'Today Target Mandays', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            worksheet.write(rowIndex,colIndex,float(_data["totalArtists"])-float(_data["onleave"]), border)
            worksheet.write(rowIndex,colIndex+1,float(_data["onleave"]), border)
            worksheet.write(rowIndex,colIndex+2,float(_data["ttm"]), border)
            rowIndex = rowIndex + 1
            lastSubColIndex = subColIndex
            subRowIndex = subRowIndex + 2
            for department,dep_data in _data["details"].items():
                artistsReportWorksheet.write(subRowIndex,0,department, border)
                subColIndex = 1
                _itemNames = itemNames.copy()
                for _dep_data in dep_data["grades"]:
                    _itemNames[_dep_data["y"]] = {
                        "y":_dep_data["y"],
                        "a":_dep_data["a"],
                        }
                for _dep_data in list(_itemNames.values()):
                    grd = float(_dep_data["y"].split('(')[1].split(')')[0])
                    artistsReportWorksheet.write(subRowIndex,subColIndex,int(_dep_data["a"]), border)
                    artistsReportWorksheet.write(subRowIndex,subColIndex+1,float(int(_dep_data["a"])*grd), border)
                    subColIndex = subColIndex + 2
                artistsReportWorksheet.write(subRowIndex,lastSubColIndex,float(dep_data['totalArtists']), border)
                artistsReportWorksheet.write(subRowIndex,lastSubColIndex+1,float(dep_data['prDay']), border)
                artistsReportWorksheet.write(subRowIndex,lastSubColIndex+2,float(dep_data['onleave']), border)
                artistsReportWorksheet.write(subRowIndex,lastSubColIndex+3,float(dep_data['ttm']), border)
                subRowIndex = subRowIndex + 1
        elif type=="mandaysAvailability":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:E{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Mandays Availability', merge_format)
            rowIndex = rowIndex + 2
            worksheet.merge_range('A{rowFrom}:B{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Departments: {department}'.format(department=', '.join(_data["details"].keys())), merge_format)
            worksheet.merge_range('C{rowFrom}:E{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,_data["labels"]["y"], bold)
            for k,x in _data["labels"].items():
                if k!="y":
                    colIndex = colIndex + 1
                    worksheet.write(rowIndex,colIndex,x, bold)
            rowIndex = rowIndex + 1
            subRowIndex = 1
            calc = 65+(len(_data["data"])*4)
            mandaysAvailabilityWorksheet = workbook.add_worksheet(name='Mandays Availability')
            mandaysAvailabilityWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex,rowTo=subRowIndex+1),'Mandays Availability', merge_format)
            mandaysAvailabilityWorksheet.merge_range('B{rowFrom}:{charX}{char}{rowTo}'.format(charX='A' if calc > 91 else '',char=chr(calc - 26 if calc > 91 else calc),rowFrom=subRowIndex,rowTo=subRowIndex+1),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            subRowIndex = subRowIndex + 1
            mandaysAvailabilityWorksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=subRowIndex+1,rowTo=subRowIndex+2),'Departments', merge_format)
            subColIndex = 1
            itemNames = {}
            for rd in _data["data"]:
                itemNames[rd["y"]] = {
                    "y":rd["y"],
                    "a":0,
                    "b":0,
                    "c":0,
                    "d":0,
                    }
                colIndex = 0
                worksheet.write(rowIndex,colIndex,rd["y"], border)
                mergeSelect = '{charA}{char1}{rowFrom}:{charB}{char2}{rowTo}'.format(charA='A' if (65+subColIndex) > 91 else '',charB='A' if (68+subColIndex) > 91 else '',char1=chr((65+subColIndex) - 26 if (65+subColIndex) > 91 else (65+subColIndex)),char2=chr((68+subColIndex) - 26 if (68+subColIndex) > 91 else (68+subColIndex)),rowFrom=subRowIndex+1,rowTo=subRowIndex+1)
                mandaysAvailabilityWorksheet.merge_range(mergeSelect,rd["y"],merge_format)
                for k,x in _data["labels"].items():
                    if k!="y":
                        mandaysAvailabilityWorksheet.write(subRowIndex+1,subColIndex,x, bold)
                        colIndex = colIndex + 1
                        subColIndex = subColIndex + 1
                        worksheet.write(rowIndex,colIndex,rd[k], border)
                rowIndex = rowIndex + 1
            lastSubColIndex = subColIndex
            subRowIndex = subRowIndex + 2
            for department,dep_data in _data["details"].items():
                mandaysAvailabilityWorksheet.write(subRowIndex,0,department, border)
                subColIndex = 1
                _itemNames = itemNames.copy()
                for _dep_data in dep_data["data"]:
                    _itemNames[_dep_data["y"]] = {
                        "y":_dep_data["y"],
                        "a":_dep_data["a"],
                        "b":_dep_data["b"],
                        "c":_dep_data["c"],
                        "d":_dep_data["d"],
                        }
                for _dep_data in list(_itemNames.values()):
                    for k,x in _data["labels"].items():
                        if k!="y":
                            mandaysAvailabilityWorksheet.write(subRowIndex,subColIndex,float(_dep_data[k]), border)
                            subColIndex = subColIndex + 1
                subRowIndex = subRowIndex + 1
    workbook.close()
    return buffer