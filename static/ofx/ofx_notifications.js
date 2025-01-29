/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */
function genUIDateFormat(from_date='12-12-2022',to_date='12-12-2022', format={date:"Do",month:"MMM",year:"YYYY"}){
    var d1DD = moment(from_date).format(format.date),
        d1MM = moment(from_date).format(format.month),
        d1YY = moment(from_date).format(format.year),
        d2DD = moment(to_date).format(format.date),
        d2MM = moment(to_date).format(format.month),
        d2YY = moment(to_date).format(format.year);
        if(d1YY!=d2YY){
            return moment(from_date).format(format.date+' '+format.month+', '+format.year)+' - '+moment(to_date).format(format.date+' '+format.month+', '+format.year);
            }else if(d1MM!=d2MM){
                return moment(from_date).format(format.date+' '+format.month)+' - '+moment(to_date).format(format.date+' '+format.month+', '+format.year);
                }else if(d1DD!=d2DD){
                    return moment(from_date).format(format.date)+' - '+moment(to_date).format(format.date+' '+format.month+', '+format.year);
                    }else{
                        return moment(from_date).format(format.date+' '+format.month+', '+format.year);
                        }
    }
function genUIDateFormatV2(from_date='12-12-2022',to_date='12-12-2022'){
    var d1DD = moment(from_date).format('DD'),
        d1MM = moment(from_date).format('MMMM'),
        d1YY = moment(from_date).format('YYYY'),
        d2DD = moment(to_date).format('DD'),
        d2MM = moment(to_date).format('MMMM'),
        d2YY = moment(to_date).format('YYYY'),
        diffCol = [[],[]], uniQ = [];
        if(d1YY!=d2YY){
            diffCol[0].push(`<span class="date">`+d1DD+`</span>`);
            diffCol[1].push(`<span class="date">`+d2DD+`</span>`);
            diffCol[0].push(`<span class="month">`+d1MM+`</span>`);
            diffCol[1].push(`<span class="month">`+d2MM+`</span>`);
            diffCol[0].push(`<span class="year">`+d1YY+`</span>`);
            diffCol[1].push(`<span class="year">`+d2YY+`</span>`);
            }else if(d1MM!=d2MM){
                diffCol[0].push(`<span class="date">`+d1DD+`</span>`);
                diffCol[1].push(`<span class="date">`+d2DD+`</span>`);
                diffCol[0].push(`<span class="month">`+d1MM+`</span>`);
                diffCol[1].push(`<span class="month">`+d2MM+`</span>`);
                uniQ.push(`<span class="year">`+d1YY+`</span>`);
                }else if(d1DD!=d2DD){
                    diffCol[0].push(`<span class="date">`+d1DD+`</span>`);
                    diffCol[1].push(`<span class="date">`+d2DD+`</span>`);
                    uniQ.push(`<span class="month">`+d1MM+`</span>`);
                    uniQ.push(`<span class="year">`+d1YY+`</span>`);
                    }else{
                        uniQ.push(`<span class="date">`+d1DD+`</span>`);
                        uniQ.push(`<span class="month">`+d1MM+`</span>`);
                        uniQ.push(`<span class="year">`+d1YY+`</span>`);
                        }
    return `<div class="date-tg-v2">
                `+(diffCol[0].length>0?`
                    <div class="spliter">
                        <div>`+diffCol[0].join('')+`</div>
                        <div>`+diffCol[1].join('')+`</div>
                    </div>
                `:``)+`
                `+(uniQ.length>0?`
                    <div class="uniq">`+uniQ.join('')+`</div>
                `:``)+`
            </div>`;
    }
function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
var formX = null;
$(document).on('submit', 'form.ofx-send-notfic', function (e) {
    formX = $(this);
    var formData = new FormData(this);
    e.preventDefault();
    formData.append('message_title','New Note Received');
    formData.append('dataId', makeid(32));
    formData.append('referenceId', parseInt($("#shot_notes_msg").attr('data-id')));
    formData.append('reference_type', "SHOT");
    // formData.append('from_group_key',"");
    formData.append('from_user', user_id);
    formData.append('from_user_apikey', $wsClient.apiKey);
    var toU = [], toG = [];
    // formData.append('from_user',$wsClient.apiKey);
    $.ajax({
        type: "GET",
        url: "/api/notify/shot_targets/?shot_id=" + $("#shot_notes_msg").attr('data-id') + "&shot_type=" + $("#shot_notes_msg").attr('data-type'),
        // data: {shot_id:$("#shot_notes_msg").attr('data-id'),shot_type:$("#shot_notes_msg").attr('data-type')}, // serializes the form's elements.
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        success: function (data) {
            let u = [], g = [];
            $.each(data.users, function (x, e) {
                u.push(e.id);
                toU.push(e.apikey);
            });
            $.each(data.groups, function (x, e) {
                g.push(e.id);
                toG.push(e.groupkey);
            });
            formData.append('to_users', u);
            formData.append('to_groups', g);
            $.ajax({
                type: "POST",
                url: "/api/wsnotifications/notes/",
                data: formData, // serializes the form's elements.
                contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                processData: false, // NEEDED, DON'T OMIT THIS
                success: function (data) {
                    $(formX).trigger("reset");
                    $(formX).find('textarea').each(function (e) {
                        $(this).html("");
                        });
                    data.from_user = $wsClient.userDataI;
                    let prntx = $(".comment-widgets-larg").length>0?$(".comment-widgets-larg"):$(".comment-widgets");
                    if($(prntx).hasClass("comment-widgets-larg")){
                        addComment2($(prntx), [data]);
                        }else{
                            addComment($(prntx), [data]);
                            }

                    $wsClient.sendMessage(data.dataId, '', toU, toG, {
                        title: data.message_title,
                        message: data.message,
                        referenceId: data.referenceId,
                    });
                },
                error: function (data, xhr) {
                    console.log(xhr, data)
                }
            });
        },
        error: function (data, xhr) {
            console.log(xhr, data)
        }
    });
    return false;
});
// var StatusCodes = {};
// $.ajax({
//         type: "GET",
//         url: "/api/production/status/",
//         data: {}, // serializes the form's elements.
//         contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
//         processData: false, // NEEDED, DON'T OMIT THIS
//         success: function (data) {
//             $.each(data,function(x,z){
//                 StatusCodes[z.code] = z;
//                 });
//             console.log(data);
//         },
//         error: function (data, xhr) {
//             console.log(xhr, data)
//         }
//     });

function ofx_shot_status_dropdown(department="",role="",nowin="",bgColor="",data={}){
    // let maping = {
    let maping = allowedRolePipelineSteps,
        tagsx = [], colors = {};
    $.each(maping,function(x,z){
        $.each(z,function(xx,zz){
            colors[xx]
            });
        });
    nowin = ofx_make_key(nowin);
    let idx = ofx_make_key(department)+'_'+ofx_make_key(role)+'_'+ofx_make_key(nowin);
    // (role.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '')+'_'+nowin).toLowerCase();
    $.each((typeof maping[idx] != "undefined"?maping[idx]:{}),function(z,x){
        tagsx.push(`<a class="dropdown-item change-shot-status to-status-`+ofx_make_key(z)+`" data-data='`+JSON.stringify(data)+`' data-bgcolor="`+StatusCodes[z].color+`" title="`+StatusCodes[z].code+`" data-set='`+JSON.stringify({status:StatusCodes[z].id})+`' data-key='`+JSON.stringify({status:z})+`' href="#" style="background: `+StatusCodes[z].color+`;padding: 2px 13px;color: #fff; font-size: smaller; text-align: center;">`+x+`</a>`);
        });
    // console.log(nowin,StatusCodes[nowin]);
    let tags = `<div class="btn-group">
                    <button type="button" class="btn dropdown-toggle" data-toggle="dropdown" title="`+StatusCodes[nowin].name+`" aria-haspopup="true" aria-expanded="true" style="color:white;padding: 0px 30px;font-size:0.8em;border-radius:10px; background-color:`+StatusCodes[nowin].color+`;">`+StatusCodes[nowin].code+`</button>
                    <div class="dropdown-menu" x-placement="top-start" style="position: absolute; transform: translate3d(0px, -197px, 0px); top: 0px; left: -14px; will-change: transform; padding: 0px; background: transparent;">
                        `+tagsx.join('')+`
                    </div>
                </div>`;
    return typeof maping[idx] != "undefined"? tags:`<div class="btn-group"><button type="button" class="btn " title="`+StatusCodes[nowin].name+`" style="color:white;padding: 0px 30px;font-size:0.8em;border-radius:10px;background-color:`+StatusCodes[nowin].color+`;">`+StatusCodes[nowin].code+`</button></div>`;
    }
function setTaskData(info={},data={},callVersion=false,submitNote=''){
    $.ajax({
        url: typeof info.task_id != "undefined" ? '/api/v2/shot/task/?id=' + info.task_id : '/api/v2/shot/?id=' + info.shot_id,
        type: 'PUT',
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        async: true, //displays data after loading the page
        processing: false,
        success: function (response) {
            // setTable();
            if(typeof info.task_id == "undefined"){
                $('.reload-table-row').attr('data-id',info.shot_id);
                if(callVersion){
                    $.ajax({
                        url: '/api/v2/clientversions/',
                        type: 'GET',
                        dataType: "json",
                        data: {shot__id:info.shot_id},
                        contentType: 'application/json; charset=utf-8',
                        "dataSrc": "",
                        "async": true, //displays data after loading the page
                        beforeSend: function(request) {
                            request.setRequestHeader("required", JSON.stringify(['id']));
                            },
                        success: function (response) {
                            if(response.length>0){
                                $.ajax({
                                    url: '/api/v2/clientversions/',
                                    type: 'PUT',
                                    dataType: "json",
                                    contentType: 'application/json; charset=utf-8',
                                    async: true, //displays data after loading the page
                                    processing: false,
                                    data: JSON.stringify([{ output_path: data[0].output_path, submission_notes: submitNote.trim(), __SELECT__: {id: response[response.length-1]['id']} }]),
                                    success: function (response) { },
                                    error: function (jqXHR, exception) {
                                        console.log(jqXHR.responseText)
                                        }
                                    });
                                }
                            },
                        error: function (jqXHR, exception) {
                            console.log(jqXHR.responseText)
                            }
                        });
                    }
                }
            $('.reload-table-row').click();
            $.toast({
                heading: 'Updated',
                showHideTransition: 'slide',
                text: (typeof info.task_id != "undefined" ?"Task":"Shot")+' Details Updated Successfully',
                icon: 'success',
                position: 'bottom-right',
                loader: true,        // Change it to false to disable loader
                loaderBg: '#da7b1c',// To change the background
                bgColor: '#1d6de5',
                textColor: 'white',
                hideAfter: 5000   // in milli seconds
                });
            },
        error: function (jqXHR, exception) {
            console.log(jqXHR.responseText)
            }
        });
    }
var updatePOPUP = false;
function shotUpdateDetected(shotId='',updateData={}){
    if(typeof showShotDetails != "undefined"&&updatePOPUP==true){
        showShotDetails(shotId,true);
        updatePOPUP=false;
        }
    console.log(shotId,updateData);
    }
function update_task_shot_status(info={},data={},callVersion=false,submitNote=''){
    setTaskData(info,[data],callVersion,submitNote);
    if(typeof info.task_id == "undefined"){
        shotUpdateDetected(info.shot_id,{status:data.status});
        }
    }
var acpt_inputdata = {};
$(document).on('change','.acpt-inputdata',function(e){
    acpt_inputdata[$(this).attr('name')] = $(this).val();
    
    });
$(document).on('click','.make-shot-qc',function(e){
    var opPath = $(this).parents('#select_qc_case').find('.stq-op-path').val(),
        submitNote = $(this).parents('#select_qc_case').find('.stq-submit-note').val(),
        dataX = JSON.parse($(this).attr('data-data'));
    if(opPath.trim().length > 0 && submitNote.trim().length > 0) {
        dataX.data.output_path = opPath.trim();
        update_task_shot_status(dataX.shot,dataX.data,true,submitNote);
        showShotDetails(dataX.shot.shot_id,false);
        $("#select_qc_case").modal('hide');
        }else{
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: `Output Path & Submission Note Required`,
                });
            }
    });
$(document).on('click','.change-shot-status',function(e){
    if($(this).closest(".btn-group").parent().hasClass("update-pop-status")){
        updatePOPUP = true;
        }else{
            updatePOPUP = false;
            }
    let info = JSON.parse($(this).attr('data-data')),
        data = {};
    data[(typeof info.task_id != "undefined" ?"task_":"")+"status"] = JSON.parse($(this).attr('data-set'))["status"];
    data["__SELECT__"] = {id: (typeof info.task_id != "undefined" ?info.task_id:info.shot_id)};
    if($(this).hasClass('dropdown-item')){
        Swal.fire({
            title: 'Do you want to change '+(typeof info.task_id != "undefined"?"Task":"Shot")+' Status?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Yes, Change',
            denyButtonText: `Don't Change`,
            }).then((result) => {
                if(result.value) {
                    update_task_shot_status(info,data);
                    let prnt = $(this).parents('.btn-group').parent();
                    $(prnt).html(ofx_shot_status_dropdown("{{user.employee.department}}","{{user.employee.role}}",JSON.parse($(this).attr('data-key'))["status"],$(this).attr('data-bgcolor'),JSON.parse($(this).attr('data-data'))));
                    }
                });
        }else{
            if(JSON.parse($(this).attr('data-key'))["status"]=='IAP'){
                $('.make-shot-qc').attr('data-data',JSON.stringify({shot:info,data:data}));
                $('.stq-op-path').val('');
                $('.stq-submit-note').val('');
                $("#select_qc_case").modal('show');
                }else{
                    Swal.fire({
                        title: 'Are you sure?',
                        showDenyButton: true,
                        showCancelButton: true,
                        confirmButtonText: 'Yes, '+$(this).attr('title'),
                        denyButtonText: `Cancel`,
                        }).then((result) => {
                            if(result.value) {
                                update_task_shot_status(info,data);
                                showShotDetails(info.shot_id,false);
                                }
                            });
                    } 
            }
    });
function reUpdateShotpersentage(parent,statusx){
    if($(parent).hasClass('markmin')){
        $(parent).attr('min',statusx);
        }
    if($(parent).hasClass('cross-update')){
        parent = $($($(parent).attr('data-cross')).find('.font-light'));
        $(parent).html(statusx+'%');
        }
    $(parent).parent().find('span').html(statusx+'%');
    $(parent).parents('.card-body').find('.css-bar').attr("data-label",statusx+'%');
    $(parent).parents('.card-body').find('.css-bar').attr("class","css-bar mb-0 css-bar-"+(parseInt(statusx/5)*5));
    $(parent).parents('.card-body').find('.css-bar').setProgressColor({ status:parseInt(statusx), prefix:'css-bar-' });
    }
$(document).on('change','input.shot_percentage',function(e){
    let min = parseFloat($(this).attr('min')), max = parseFloat($(this).attr('max')), now = parseFloat($(this).val());
    let deft = parseFloat($(this).parent().find('.progress-bar').html().split("%")[0]);
    if(now < 0||(min>=now && now != 0&&!(allowAllActions||userPermissions.indexOf('can_overwrite_shot_percentage')!=-1))){
        $(this).val(deft.toString());
        if($(this).hasClass('on-change-re-update')){
            reUpdateShotpersentage($(this),parseInt($(this).val()));
            }
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Entered percentage should not be less than '+min,
            });
        }else if(max<now && now != 100){
            $(this).val(deft.toString());
            if($(this).hasClass('on-change-re-update')){
                reUpdateShotpersentage($(this),parseInt($(this).val()));
                }
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Entered percentage should not be greater than 100',
                });
            }else{
                var myTag = $(this), data = JSON.parse($(this).attr('data-data'));
                if(typeof data.shot_id != "undefined"){
                    $.ajax({
                        url: '/api/production/shots/'+data.shot_id+'/',
                        type: 'GET',
                        dataType: "json",
                        contentType: 'application/json; charset=utf-8',
                        // data: {shot__id:shot_id},
                        async: true, //displays data after loading the page
                        processing: false,
                        success: function (_shotD) {
                            data.bidDays = parseFloat(_shotD.bid_days);
                            $.ajax({
                                url: '/api/production/daylogs/?shot_id='+data.shot_id,
                                type: 'GET',
                                dataType: "json",
                                contentType: 'application/json; charset=utf-8',
                                async: true, //displays data after loading the page
                                processing: false,
                                // data: JSON.stringify(post_data),
                                success: function (response) {
                                    let allowPercentage = 0, selctedDate = null, todayLog = null;
                                    $.each(response,function(x,z){
                                        if(!moment(moment(z.updated_date).format('YYYY-MM-DD')).isSame(moment().format('YYYY-MM-DD'))){
                                            if(selctedDate===null || moment(moment(z.updated_date).format('DD MMMM YYYY'))>selctedDate ){
                                                selctedDate = moment(moment(z.updated_date).format('DD MMMM YYYY'));
                                                allowPercentage = z.percentage;
                                                }
                                            }else{
                                                todayLog = z.id;
                                                }
                                        });
                                    if(parseFloat(allowPercentage)>=now&&(!(allowAllActions||userPermissions.indexOf('can_overwrite_shot_percentage')!=-1))){
                                        $(myTag).val(deft.toString());
                                        if($(myTag).hasClass('on-change-re-update')){
                                            reUpdateShotpersentage($(myTag),parseInt($(myTag).val()));
                                            }
                                        $(myTag).attr('min',allowPercentage);
                                        Swal.fire({
                                                icon: 'error',
                                                title: 'Oops...',
                                                text: 'Entered percentage should not be less than previous day percentage ('+allowPercentage+'%)',
                                            });
                                        }else{
                                            $.ajax({
                                                url: '/api/production/daylogs/'+(todayLog!=null?'?log_id='+todayLog:''),
                                                type: (todayLog!=null?'PUT':'POST'),
                                                dataType: "json",
                                                contentType: 'application/json; charset=utf-8',
                                                async: true, //displays data after loading the page
                                                processing: false,
                                                data: JSON.stringify(Object.assign({
                                                    shot_biddays: data.bidDays,
                                                    updated_shot_biddays: data.bidDays,
                                                    percentage:now,
                                                    day_percentage: now - allowPercentage,
                                                    consumed_man_day: ((data.bidDays/100)*(now - allowPercentage)).toFixed(2),
                                                    },(todayLog===null?{ 
                                                        artist: ofx_page_data.user.id,
                                                        shot:data.shot_id
                                                        }:{
                                                        updated_by: ofx_page_data.user.fullName,
                                                        }))),
                                                success: function (response) {
                                                    $.ajax({
                                                        url: '/api/production/shots/'+data.shot_id+'/',
                                                        type: 'PUT',
                                                        dataType: "json",
                                                        contentType: 'application/json; charset=utf-8',
                                                        async: true, //displays data after loading the page
                                                        processing: false,
                                                        data: JSON.stringify({
                                                            progress:now,
                                                            achieved_mandays: ((data.bidDays/100)*now).toFixed(2)
                                                            }),
                                                        success: function (response) {
                                                            let bartag = $(myTag).parent().find('.progress-bar');
                                                            $(bartag).setProgressColor({ status:parseInt(now), prefix:'bg-' });
                                                            $(bartag).html(now+"%");
                                                            $(bartag).css("width",now+"%");
                                                            $('.reload-table-row').attr('data-id',data.shot_id);
                                                            $('.reload-table-row').click();
                                                            if($(myTag).hasClass('on-change-re-update')){
                                                                reUpdateShotpersentage($(myTag),parseInt($(myTag).val()));
                                                                }
                                                            },
                                                        error: function (jqXHR, exception) {
                                                            console.log(jqXHR.responseText)
                                                            }
                                                        });
                                                    },
                                                error: function (jqXHR, exception) {
                                                    console.log(jqXHR.responseText)
                                                    }
                                                });
                                            }
                                    },
                                error: function (jqXHR, exception) {
                                    console.log(jqXHR.responseText)
                                    }
                                });
                            },
                        error: function (jqXHR, exception) {
                            console.log(jqXHR.responseText)
                            }
                        });
                    }else{
                        $.ajax({
                            url: '/api/production/taskdaylogs/?task_id='+data.task_id,
                            type: 'GET',
                            dataType: "json",
                            contentType: 'application/json; charset=utf-8',
                            async: true, //displays data after loading the page
                            processing: false,
                            // data: JSON.stringify(post_data),
                            success: function (response) {
                                let allowPercentage = 0, selctedDate = null, todayLog = null;
                                $.each(response,function(x,z){
                                    if(!moment(moment(z.updated_date).format('YYYY-MM-DD')).isSame(moment().format('YYYY-MM-DD'))){
                                        if(selctedDate===null || moment(moment(z.updated_date).format('DD MMMM YYYY'))>selctedDate ){
                                            selctedDate = moment(moment(z.updated_date).format('DD MMMM YYYY'));
                                            allowPercentage = z.percentage;
                                            }
                                        }else{
                                            todayLog = z.id;
                                            }
                                    });
                                if(parseFloat(allowPercentage)>=now&&(!(allowAllActions||userPermissions.indexOf('can_overwrite_task_percentage')!=-1))){
                                    $(myTag).val(deft.toString());
                                    if($(myTag).hasClass('on-change-re-update')){
                                        reUpdateShotpersentage($(myTag),parseInt($(myTag).val()));
                                        }
                                    $(myTag).attr('min',allowPercentage);
                                    Swal.fire({
                                            icon: 'error',
                                            title: 'Oops...',
                                            text: 'Entered percentage should not be less than previous day percentage ('+allowPercentage+'%)',
                                        });
                                    }else{
                                        $.ajax({
                                            url: '/api/production/mytask/'+data.task_id+'/',
                                            type: 'GET',
                                            dataType: "json",
                                            contentType: 'application/json; charset=utf-8',
                                            async: true, //displays data after loading the page
                                            processing: false,
                                            // data: JSON.stringify(post_data),
                                            success: function (taskR) {
                                                data.assigned_bids = parseFloat(taskR.assigned_bids);
                                                $.ajax({
                                                    url: '/api/production/taskdaylogs/'+(todayLog!=null?'?log_id='+todayLog:''),
                                                    type: (todayLog!=null?'PUT':'POST'),
                                                    dataType: "json",
                                                    contentType: 'application/json; charset=utf-8',
                                                    data: JSON.stringify(Object.assign({
                                                        task_biddays: data.assigned_bids,
                                                        updated_task_biddays: data.assigned_bids,
                                                        percentage: now,
                                                        day_percentage: now - allowPercentage,
                                                        consumed_man_day: ((data.assigned_bids/100)*(now - allowPercentage)).toFixed(2),
                                                        },(todayLog===null?{
                                                            artist: ofx_page_data.user.id,
                                                            task: data.task_id
                                                            }:{
                                                            updated_by: ofx_page_data.user.id,
                                                            }))),
                                                    success: function (response) {
                                                        let bartag = $(myTag).parent().find('.progress-bar');
                                                        $(bartag).setProgressColor({ status:parseInt(now), prefix:'bg-' });
                                                        $(bartag).html(now+"%");
                                                        $(bartag).css("width",now+"%");
                                                        if($(myTag).hasClass('on-change-re-update')){
                                                            reUpdateShotpersentage($(myTag),parseInt($(myTag).val()));
                                                            }
                                                        setTaskData(JSON.parse($(myTag).attr('data-data')),{
                                                            art_percentage: now,
                                                            "__SELECT__":{
                                                                id: JSON.parse($(myTag).attr('data-data'))['task_id']
                                                                } 
                                                            });
                                                    },
                                                    error: function (jqXHR, exception) {
                                                        console.log(jqXHR.responseText)
                                                    }
                                                });
                                                },
                                            error: function (jqXHR, exception) {
                                                console.log(jqXHR.responseText)
                                                }
                                            });
                                        }
                                },
                            error: function (jqXHR, exception) {
                                console.log(jqXHR.responseText)
                                }
                            });
                        }
            }
    });
$(document).on('keyup', 'input.only-numeric', function(e){
    if (/\D/g.test(this.value)){
        // Filter non-digits from input value.
        this.value = this.value.replace(/\D/g, '');
        }
    });
$(document).on('click', '.make-all-read',function(e){
    $.ajax({
        url: '/api/notifications/',
        type: 'GET',
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: {
            user_id: user_id,
            read: 'False'
            },
        success: function (response) {
            var idXlen = 0;
            $.each(response,function(_z,e){
                idXlen = idXlen + 1;
                $.ajax({
                    url: '/api/notifications/?user_id='+user_id+'&data_id='+e.dataId,
                    type: 'PUT',
                    dataType: "json",
                    contentType: 'application/json; charset=utf-8',
                    async: true, //displays data after loading the page
                    processing: false,
                    data: JSON.stringify({ read: true }),
                    success: function (res) {
                        if(idXlen==response.length){
                            if($('.current-url').length>0){
                                location.reload();
                                }
                            $('.message-center').empty();
                            }
                        },
                    error: function (jqXHR, exception) {
                        console.log(jqXHR.responseText)
                        }
                    });  
                });
            },
        error: function (jqXHR, exception) {
            console.log(jqXHR.responseText)
            }
        });
    return false;
    });