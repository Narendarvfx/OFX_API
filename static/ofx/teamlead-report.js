//lead-report
jQuery.fn.extend({
    setLeadReport: function(e={
        emp_id:1,
        emp_location: "PUNE",
        emp_department: "MM",
        tagArtists: ".r-artists",
        tagTeamAbility: ".r-team-ability",
        tagTMD: ".r-tmd",
        tagAMD: ".r-amd",
        tagDif: ".r-dif",
        from_date: "2023-02-18",
        to_date: "2023-03-30"
        }) {
        // var defaultDays = 30; //Days 
        // var instelDate = moment().subtract(defaultDays,'d').format("YYYY-MM-DD");
        // var getKeys = getGetParam({'from_date':instelDate+'T00:00:00.000000','to_date':moment().format("YYYY-MM-DD")+'T23:59:59.999999'});
        var getKeys = getGetParam({'from_date':moment().startOf('month').format("YYYY-MM-DD")+'T00:00:00.000000','to_date':moment().endOf('month').format("YYYY-MM-DD")+'T23:59:59.999999'});
        var leadRepTag = $(this);
        let le = Object.assign({
            emp_id:1,
            emp_location:"PUNE",
            emp_department:"MM",
            tagArtists: ".r-artists",
            tagTeamAbility: ".r-team-ability",
            tagTMD: ".r-tmd",
            tagAMD: ".r-amd",
            tagDif: ".r-dif",
            from_date: getKeys.from_date,
            to_date: getKeys.to_date
            },e);
        
        $.ajax({
            url: '/api/v2/employeerolebinding/',
            type: 'GET',
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            async: true, //displays data after loading the page
            processing: false,
            data: Object.assign({employee__role__name:"VFX ARTIST"},((typeof qRole=="undefined"||qRole!='HEAD OF DEPARTMENT')?{bindWith__id__in:le.emp_id,role__name: typeof qRole=="undefined"?"TEAM LEAD":qRole}:{})),
            beforeSend: function(request) {
                request.setRequestHeader("required", JSON.stringify(["id", "employee__id","employee__department__id","employee__department__name", "employee__grade__id","employee__grade__a_man_day","employee__location__id","employee__location__name"]));
                },
            success: function (teamLeadBind) {
                let tagArtists = [], tagTeamAbility = 0;
                $.each(teamLeadBind,function(_i,ix){
                    if(tagArtists.indexOf(ix["employee"]["id"])==-1 && ix["employee"]["grade"] != null  && ix["employee"]["grade"]["a_man_day"] != null&&(typeof qRole=="undefined"||qRole!='HEAD OF DEPARTMENT'||(le.emp_location==ix.employee.location.id&&le.emp_department==ix.employee.department.name))){
                        tagArtists.push(ix["employee"]["id"]);
                        tagTeamAbility = tagTeamAbility + parseFloat(ix["employee"]["grade"]["a_man_day"]);
                        }
                    });
                $(le.tagArtists).html(tagArtists.length);
                $(le.tagTeamAbility).html(parseFloat(tagTeamAbility.toFixed(2)).toFixed(2));
                },
            error: function (jqXHR, exception) {
                console.log(jqXHR.responseText)
                }
            });

        $.ajax({
            url: `/api/v2/leaddailystatistics/`,
            type: 'GET',
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            async: true, //displays data after loading the page
            processing: false,
            data: Object.assign({logDate__range:moment(le.from_date).format("YYYY-MM-DD")+'|'+moment(le.to_date).format("YYYY-MM-DD")},{role__name__in: typeof qRole=="undefined"?"TEAM LEAD":qRole, lead__id:le.emp_id}),
            beforeSend: function(request) {
                request.setRequestHeader("required", JSON.stringify(['id','tmd','amd','shot_amd','logDate']));
                },
            success: function (teamLeadReport) {
                let tagTMD = 0, tagAMD = 0, tagDif = 0;
                $.each(teamLeadReport,function(_z,_e){
                    tagTMD = tagTMD + _e.tmd;
                    // tagAMD = tagAMD + _e.shot_amd;
                    tagAMD = tagAMD + _e.amd;
                    });
                $(le.tagTMD).html(parseFloat(tagTMD.toFixed(2)).toFixed(2));
                $(le.tagAMD).html(parseFloat(tagAMD.toFixed(2)).toFixed(2));
                tagDif = parseFloat(tagAMD.toFixed(2)) - parseFloat(tagTMD.toFixed(2));
                $(le.tagDif).html((tagDif>0?'+':'')+parseFloat(tagDif).toFixed(2));
                },
            error: function (jqXHR, exception) {
                console.log(jqXHR.responseText)
                }
            });
        }
    });