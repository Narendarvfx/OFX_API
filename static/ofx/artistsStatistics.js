function dateSanitization(from_date,to_date,type='month|week|null'){
    var _fDate = String(from_date),
        _tDate = String(to_date);
    if(type=='month'){
        return {
            from_date: moment(_fDate).startOf('month').format('YYYY-MM-DD'),
            to_date: moment(_tDate).endOf('month').format('YYYY-MM-DD'),
            };
        }else if(type=='week'){
            return {
                from_date: moment(_fDate).startOf('week').add(1,'days').format('YYYY-MM-DD'),
                to_date: ((moment(_tDate).format('dddd').substring(0,3)=="Sun")?_tDate:moment(_tDate).endOf('week').add(1,'days').format('YYYY-MM-DD')),
                };
            }else{
                return {
                    from_date: from_date,
                    to_date: to_date
                    }
                }
    }

function calenderSort(from_date,to_date,type='month|week'){
    var diff = moment(to_date).diff(moment(from_date), 'days');
    var data = [[]];
    for(let i = diff; i >=0 ; i-- ){
        tdate = moment(to_date).subtract(i,'days');
        if(type=="week" && tdate.format('dddd').substring(0,3)=='Mon'){
            if(data[data.length-1].length!=0){
                data.push([]);
                }
            }
        if(type=="month" && parseInt(tdate.format('DD'))==1){
            if(data[data.length-1].length!=0){
                data.push([]);
                }
            }
        data[data.length-1].push(tdate.format('YYYY-MM-DD'));
        }
    return data;
    }



function addStatisticsToBody(parent,title={title:'Week-01',hover:''},e){
    $(parent).prepend(`<div class="pl-1 pr-1">
                            <div class="card text-white bg-light pt-0 mt-2 mb-2 border border-round pb-0">
                                <div class="card-header date-head-v2" title="`+title.hover+`">`+title.title+`</div>
                                <div class="card-body">
                                    <div class="pt-2 pl-2 pr-2">
                                        <div class="col-md-12 pl-0 pr-0 mb-1">
                                            <div class="card pl-2 pr-2">
                                                <div class="card-body">
                                                    <h4 class="card-title mb-0 pl-2 pr-2" style="font-size: small;">Activity Timings</h4>
                                                    <div class="row">
                                                        <div class="col-4 pl-1 pr-0 text-center">
                                                            <span class="display-6 text-primary" style="font-size: x-large;">`+parseInt(e.rwh)+`</span>
                                                            <h5 style="font-size: x-small;line-height: initial;">Required Working Hours</h5>
                                                        </div>
                                                        <div class="col-4 pl-1 pr-0 text-center">
                                                            <span class="display-6 text-primary" style="font-size: x-large;">`+parseInt(e.aeh)+`</span>
                                                            <h5 style="font-size: x-small;line-height: initial;">Available/ESSL Hours</h5>
                                                        </div>
                                                        <div class="col-4 pl-1 pr-0 text-center">
                                                            <span class="display-6 text-primary" style="font-size: x-large;">`+parseInt(e.ash)+`</span>
                                                            <h5 style="font-size: x-small;line-height: initial;">Active/System Hours</h5>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12 pl-0 pr-0 mb-1">
                                            <div class="card bg-info">
                                                <div class="card-body text-center">
                                                    <h1 class="font-light text-white mb-0" style="font-size: x-large;line-height: initial;">`+e.tmd.toFixed(1)+`</h1>
                                                    <h6 class="text-white mb-0" style="font-size: small;">Target Mandays</h6>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12 pl-0 pr-0 mb-1">
                                            <div class="card bg-success">
                                                <div class="card-body text-center">
                                                    <h1 class="font-light text-white mb-0" style="font-size: x-large;line-height: initial;">`+e.amd.toFixed(2)+`</h1>
                                                    <h6 class="text-white mb-0" style="font-size: small;">Achieved Mandays</h6>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12 pl-0 pr-0 mb-1">
                                            <div class="card bg-primary">
                                                <div class="card-body text-center">
                                                    
                                                    <h1 class="font-light text-white mb-0" style="font-size: x-large;line-height: initial;">`+e.leaves.toFixed(1)+`</h1>
                                                    <h6 class="text-white mb-0" style="font-size: small;">Leaves</h6>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12 pl-0 pr-0 mb-3" style="display: none; margin-bottom: 0!important;">
                                            <div class="card bg-warning">
                                                <div class="card-body text-center">
                                                    
                                                    <h1 class="font-light text-white mb-0" style="font-size: x-large;line-height: initial;">0</h1>
                                                    <h6 class="text-white mb-0" style="font-size: small;">Missing ETA's</h6>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`);
    }

function addDailyStatisticsLogs(e){
    if(Object.keys(e).length>0){
        let keys = ["tmd", "amd", "rwh", "aeh", "ash", "leaves"], data = {}, fDate = e[Object.keys(e)[0]].logDate, tDate = (e.length>1?e[e.length-1].logDate:e[Object.keys(e)[0]].logDate);
        $.each(keys,function(zz,ee){ data[ee] = 0; });
        $.each(e,function(zx,ex){ 
                $.each(keys,function(zz,ee){
                    data[ee] = data[ee] + ex[ee];
                    if(moment(fDate).diff(moment(ex.logDate), 'days')>0){
                        fDate = ex.logDate;
                        }
                    if(moment(ex.logDate).diff(moment(tDate), 'days')>0){
                        tDate = ex.logDate;
                        }
                });
            });
        return {
                data:data,
                range:{
                    from_date: fDate,
                    to_date: tDate,
                    }
                }
        }else{
            return {
                data:{},
                range:{
                    from_date:null,
                    to_date:null,
                    }
                }
            }
    }

function getWeekIndex(from_date,to_date,select){
    var diff = moment(to_date).diff(moment(from_date).startOf('week').add(1,'days'), 'days')+1;
    var count = 0, tdate=null;
    for(let i = 0; i < diff; i++ ){
        tdate = moment(from_date).add(i,'days');
        if(tdate.format('dddd').substring(0,3)=='Mon'){
            count = count + 1;
            }
        if(moment(select).diff(tdate, 'days') == 0){
            return count;
            }
        }
    return count;
    }
function sorkKeys(dataObj){
    return Object.keys(dataObj).sort().reduce(
        (obj, key) => { 
            obj[key] = dataObj[key]; 
            return obj;
        }, 
        {}
        );
    }
function sortDailyStatistics(e,from_date,to_date){
    var uStatistics = {},
        dateTypes = {
            month: dateSanitization(from_date,to_date,'month'),
            week: dateSanitization(from_date,to_date,'week')
            },
        dateRange = {
            month: calenderSort(dateTypes.month.from_date,dateTypes.month.to_date,'month'),
            week: calenderSort(dateTypes.week.from_date,dateTypes.week.to_date,'week')
            },
        userData = {};
    // console.log("dateRange",dateRange);
    // console.log("dateTypes",dateTypes);
    $.each(e,function(z,e){
        let _okey = 'key_'+(typeof e.employee.employee_id == "undefined"?e.employee.toLowerCase():(e.employee.employee_id!=null?e.employee.employee_id.toLowerCase():'blank'))
        if(typeof uStatistics[_okey] == "undefined"){
            uStatistics[_okey] = {
                employeeId: (typeof e.employee.id == "undefined"?e.employee:e.employee.id),
                employee_id: (typeof e.employee.employee_id == "undefined"?e.employee:e.employee.employee_id),
                fullName:  (typeof e.employee.fullName == "undefined"?e.employee:e.employee.fullName),
                department:  (typeof e.employee.department == "undefined"?e.employee:e.employee.department),
                week: [],
                month: [],
                };
            }
        let cDate = moment(e.logDate).format('YYYY-MM-DD');
        $.each(dateRange,function(_z,_e){
            if(moment(cDate).diff(moment(dateTypes[_z].from_date), 'days')>=0 && moment(dateTypes[_z].to_date).diff(moment(cDate), 'days')>=0){
                $.each(_e,function(__z,__e){
                    if(typeof uStatistics[_okey][_z][__z]  == "undefined"){
                        uStatistics[_okey][_z][__z] = {};
                        }
                    if(__e.indexOf(cDate)!=-1){
                        uStatistics[_okey][_z][__z][cDate] = {}
                        $.each(["tmd", "amd", "rwh", "aeh", "ash", "leaves", "logDate"],function(zz,ee){ uStatistics[_okey][_z][__z][cDate][ee] = JSON.parse(JSON.stringify(e[ee])); });
                        }
                    });
                }
            }); 
        });
    return uStatistics;
    }
