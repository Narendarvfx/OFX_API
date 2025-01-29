import xlsxwriter
def writeDepartmentLiteReportWorksheet(buffer,data={}):
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
    worksheet = workbook.add_worksheet(name='Department Report')

    rowIndex = -2
    colIndex = 0
    for type,_data in data.items():
        rowIndex = rowIndex + 3
        if type=="achievedMandays":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:B{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Achieved Mandays', merge_format)
            rowIndex = rowIndex + 1
            worksheet.write(rowIndex,0,'Department: {department}'.format(department=_data["department"]), merge_format)
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
        elif type=="monthlyAchievement":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Monthly Achievement', merge_format)
            rowIndex = rowIndex + 2
            worksheet.write(rowIndex-1,0,'Department: {department}'.format(department=_data["department"]), merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Month', bold)
            worksheet.write(rowIndex,colIndex+1,'Target Mandays', bold)
            worksheet.write(rowIndex,colIndex+2,'Achieved Mandays', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            for d in _data["data"]:
                worksheet.write(rowIndex,colIndex,d["y"], border)
                worksheet.write(rowIndex,colIndex+1,float(d["tmd"]), border)
                worksheet.write(rowIndex,colIndex+2,float(d["amd"]), border)
                rowIndex = rowIndex + 1
        elif type=="artistsReport":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:A{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Artists by Grades', merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Total Artists: {totalArtists}'.format(totalArtists=_data["totalArtists"]), merge_format)
            rowIndex = rowIndex + 2
            worksheet.write(rowIndex-1,0,'Department: {department}'.format(department=_data["department"]), merge_format)
            worksheet.merge_range('B{rowFrom}:C{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,'Grade', bold)
            worksheet.write(rowIndex,colIndex+1,'Artists', bold)
            worksheet.write(rowIndex,colIndex+2,'Ability per day', bold)
            rowIndex = rowIndex + 1
            colIndex = 0
            for d in _data["grades"]:
                grd = float(d["y"].split('(')[1].split(')')[0])
                worksheet.write(rowIndex,colIndex,d["y"], border)
                worksheet.write(rowIndex,colIndex+1,int(d["a"]), border)
                worksheet.write(rowIndex,colIndex+2,float(int(d["a"])*grd), border)
                rowIndex = rowIndex + 1
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

        elif type=="mandaysAvailability":
            colIndex = 0
            worksheet.merge_range('A{rowFrom}:E{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex+1), 'Mandays Availability', merge_format)
            rowIndex = rowIndex + 2
            worksheet.merge_range('A{rowFrom}:B{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Department: {department}'.format(department=_data["department"]), merge_format)
            worksheet.merge_range('C{rowFrom}:E{rowTo}'.format(rowFrom=rowIndex,rowTo=rowIndex),'Date: {from_date} to {to_date}'.format(from_date=_data["date"]["from"],to_date=_data["date"]["to"]), merge_format)
            colIndex = 0
            worksheet.write(rowIndex,colIndex,_data["labels"]["y"], bold)
            for k,x in _data["labels"].items():
                if k!="y":
                    colIndex = colIndex + 1
                    worksheet.write(rowIndex,colIndex,x, bold)
            rowIndex = rowIndex + 1
            for rd in _data["data"]:
                colIndex = 0
                worksheet.write(rowIndex,colIndex,rd["y"], border)
                for k,x in _data["labels"].items():
                    if k!="y":
                        colIndex = colIndex + 1
                        worksheet.write(rowIndex,colIndex,rd[k], border)
                rowIndex = rowIndex + 1
    workbook.close()
    return buffer