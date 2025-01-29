/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */
/*var ofx_page_data = {};
$.ajax({
    url: '/production/default.json',
    type: 'GET',
    dataType: "json",
    contentType: 'application/json; charset=utf-8',
    data: {},
    async: true, //displays data after loading the page
    processing: false,
    success: function (response){
        ofx_page_data = response;
        },
    error: function (jqXHR, exception){
        console.log(jqXHR.responseText)
        }
    });*/
var noUpdateOnShot = ['IAP','DTC','CAP','HLD','OMT'];
var ofx_page_data = `{{ page_data }}`.replace(/&quot;/g,`\'`).replace(/&#x27;/g,'"').replace(/None/g,'null').replace(/False/g,'false').replace(/True/g,'true').replace(/\t/g,' ').replace(/\n/g,' '); 
// console.log(ofx_page_data);
ofx_page_data = JSON.parse(ofx_page_data); 
function getGetParam(get={}){
    let searchParams = new URLSearchParams(window.location.search);
    let val = {};
    $.each(get,function(z,x){
        if(searchParams.has(z)){
            val[z] = searchParams.get(z);
            }else{
                val[z] = x;
                }
        });
    return val;
    }
var status_list = [];
var allowedRolePipelineSteps = {}, ofx_key_x = '';
var StatusCodes = {};
function ofx_make_key(inData = ''){
    if(inData==null){
        console.log("ofx_make_key",inData);
        }
    return inData!=null?String(inData).replace(/[^a-zA-Z ]/gi, "").replace(/[_\s]/g, '').toLowerCase():null;
    }
for(let i = 0; i < ofx_page_data.StatusCodes.length; i++){
    StatusCodes[ofx_make_key(ofx_page_data.StatusCodes[i].code)] = ofx_page_data.StatusCodes[i];
    if(ofx_page_data.ignoreStatusCodes.indexOf(ofx_page_data.StatusCodes[i].code)==-1){
        status_list.push(ofx_page_data.StatusCodes[i].code);
        }
    }
status_list = status_list.join('|');
for(let i = 0; i < ofx_page_data.rolePipelineSteps.length; i++){
    ofx_key_x = ofx_make_key(ofx_page_data.rolePipelineSteps[i].department)+'_'+ofx_make_key(ofx_page_data.rolePipelineSteps[i].role)+'_'+ofx_make_key(ofx_page_data.rolePipelineSteps[i].status);
    if(typeof allowedRolePipelineSteps[ofx_key_x] == "undefined"){
        allowedRolePipelineSteps[ofx_key_x] = {};
        }
    for(let j = 0; j < ofx_page_data.rolePipelineSteps[i].allowed_steps.length; j++){
        allowedRolePipelineSteps[ofx_key_x][ofx_make_key(ofx_page_data.rolePipelineSteps[i].allowed_steps[j])] = ofx_page_data.rolePipelineSteps[i].allowed_steps[j];
        }
    }
//assignmentStepsOrder

function sortKeys(data){
    let ordered = Object.keys(data).sort().reduce(
        (obj, key) => { 
          obj[key] = data[key]; 
          return obj;
        }, 
        {}
      );
    return ordered;
    }

// let assignmentStepsOrder_i = [],assignmentStepsOrder_keys = {};
// var assignmentStepsOrder = {}, assignmentStepsOrderIndex = {}, assignmentStepsOrderStatus = {}, assignmentStepsBeforeArtist={}, assignmentStepsAfterArtist={};
// let dept = '';
// let role = '';
// let isArtistDone = {};
// for(let i = 0; i < ofx_page_data.assignmentStepsOrder.length; i++){
//     dept = ofx_make_key(ofx_page_data.assignmentStepsOrder[i].department.name);
//     role = ofx_make_key(ofx_page_data.assignmentStepsOrder[i].role.name);
//     if(typeof assignmentStepsOrder_keys[dept] == 'undefined'){
//         assignmentStepsOrder_keys[dept] = [];
//         assignmentStepsOrder_i[dept] = [];
//         assignmentStepsOrder[dept] = {};
//         assignmentStepsOrderIndex[dept] = [];
//         assignmentStepsOrderStatus[dept] = [];
//         assignmentStepsBeforeArtist[dept] = [];
//         assignmentStepsAfterArtist[dept] = [];
//         isArtistDone[dept] = false;
//         }
//     assignmentStepsOrder_keys[dept][ofx_page_data.assignmentStepsOrder[i].roleIndex] = dept+'_'+role;
//     assignmentStepsOrder_i[dept][ofx_page_data.assignmentStepsOrder[i].roleIndex] = ofx_page_data.assignmentStepsOrder[i];
//     }
// let objKeys = Object.keys(assignmentStepsOrder_i);
// for(let i = 0; i < objKeys.length; i++){
//     for(let j = 0; j < assignmentStepsOrder_i[objKeys[i]].length; j++){
//         if(typeof assignmentStepsOrder_i[objKeys[i]][j] != 'undefined'){
//             dept = objKeys[i];
//             role = ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].role.name);
//             assignmentStepsOrderIndex[dept].push(role);
//             assignmentStepsOrderStatus[dept].push(assignmentStepsOrder_i[objKeys[i]][j].shotStatus != null ? assignmentStepsOrder_i[objKeys[i]][j].shotStatus.code:null);
//             if(role!='vfxartist'){
//                 if(!isArtistDone[dept]){
//                     assignmentStepsBeforeArtist[dept].push(role);
//                     }else{
//                         assignmentStepsAfterArtist[dept].push(role);
//                         }
//                 }else{
//                     isArtistDone[dept] = true;
//                     }
//             assignmentStepsOrder[objKeys[i]][role] = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j]));
//             assignmentStepsOrder[objKeys[i]][role].allowed_steps = [];
//             for(let z = 0; z < assignmentStepsOrder_i[objKeys[i]][j].allowed_steps.length; z++){
//                 if(assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name)) != -1){
//                     let di = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j]));
//                     delete di.allowed_steps;
//                     di.role = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z]));
//                     assignmentStepsOrder[objKeys[i]][role].allowed_steps[assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name))] = JSON.parse(JSON.stringify(di));
//                     }
//                 }
//             let di = JSON.parse(JSON.stringify(assignmentStepsOrder[objKeys[i]][role].allowed_steps));
//             assignmentStepsOrder[objKeys[i]][role].allowed_steps = [];
//             for(let z = 0; z < di.length; z++){
//                 if(typeof di[z] != "undefined" && di[z] != null){
//                     assignmentStepsOrder[objKeys[i]][role].allowed_steps.push(di[z]);
//                     }
//                 }
//             }
//         }
//     }

// array.slice(0, n);

userPermissions = [];
if(ofx_page_data.userRole!=null){
    for(let i = 0; i < ofx_page_data.userRole.permissions.length; i++){
        userPermissions.push(ofx_page_data.userRole.permissions[i].permission_key);
        }
    }
//individual user permissions
if(ofx_page_data.user.permissions.length > 0){
    for(let i = 0; i < ofx_page_data.user.permissions.length; i++){
        if(!userPermissions.includes(ofx_page_data.user.permissions[i].permission_key)) {
            userPermissions.push(ofx_page_data.user.permissions[i].permission_key);
        }
    }
}
var allowAllActions = userPermissions.indexOf("all")!=-1?true:false;
var viewShortsBy = (allowAllActions||userPermissions.indexOf("can_view_all_dept_shots")!=-1)?'ALL':((userPermissions.indexOf("view_all_shots")!=-1)?'DEPT':(userPermissions.indexOf("can_view_shots_by_artists")!=-1?'ARTIST':((userPermissions.indexOf("can_view_only_my_shots")!=-1)?'MY':null)));
// for(let i = 0; i < objKeys.length; i++){
//     assignmentStepsOrder[objKeys[i]] = [];
//     for(let j = 0; j < assignmentStepsOrder_i[objKeys[i]].length; j++){
//         if(typeof assignmentStepsOrder_i[objKeys[i]][j] != 'undefined'){
//             role = ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].role.name);
//             assignmentStepsOrder[objKeys[i]][role] = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j]));
//             assignmentStepsOrder[objKeys[i]][role].allowed_steps = [];
//             // assignmentStepsOrder[objKeys[i]][role] = [];
//             for(let z = 0; z < assignmentStepsOrder_i[objKeys[i]][j].allowed_steps.length; z++){
//                 if(assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name)) != -1){
//                     assignmentStepsOrder[objKeys[i]][role].allowed_steps[assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name))] = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j]));
                        
//                     assignmentStepsOrder[objKeys[i]][role].allowed_steps[assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name))].role = JSON.parse(JSON.stringify(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z]));
//                     delete assignmentStepsOrder[objKeys[i]][role].allowed_steps[assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name))].allowed_steps;
//                     // delete assignmentStepsOrder[objKeys[i]][role].allowed_steps[assignmentStepsOrder_keys[objKeys[i]].indexOf(objKeys[i]+"_"+ofx_make_key(assignmentStepsOrder_i[objKeys[i]][j].allowed_steps[z].name))].allowed_steps;
//                     }
//                 }
//             }
//         }
//     }

var userDepartment = ofx_page_data.user.department!=null?ofx_make_key(ofx_page_data.user.department):null;
var userRole = ofx_page_data.user.role!=null?ofx_make_key(ofx_page_data.user.role):null;
// var userRoleChain = (userDepartment!=null && userRole!=null && typeof assignmentStepsOrder[userDepartment] != "undefined" && typeof assignmentStepsOrder[userDepartment][userRole] != "undefined")?assignmentStepsOrder[userDepartment][userRole]:null;

crossRoles = {
    employeesId:[],
    employees:[],
    roles:{},
    departmentsId:[],
    departments:[],
    };
let prps = '';
for(let i = 0; i < ofx_page_data.userCrossBinding.length; i++){
    if(ofx_page_data.userCrossBinding[i].bindWithEmployee!=null&&crossRoles.employeesId.indexOf(ofx_page_data.userCrossBinding[i].bindWithEmployee.id)==-1){
        crossRoles.employeesId.push(ofx_page_data.userCrossBinding[i].bindWithEmployee.id);
        crossRoles.employees.push(ofx_page_data.userCrossBinding[i].bindWithEmployee);
        }
    if(ofx_page_data.userCrossBinding[i].bindWithRole!=null){
        prps = ofx_make_key((ofx_page_data.userCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.userCrossBinding[i].bindWithDepartment.name:'departmentself');
        if(typeof crossRoles.roles[prps] == "undefined"){
            crossRoles.roles[prps] = {
                department: (ofx_page_data.userCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.userCrossBinding[i].bindWithDepartment.name:'__SELF__',
                rolesId:[],
                roles:[]
                };
            }
    
        if(ofx_page_data.userCrossBinding[i].bindWithRole!=null&&crossRoles.roles[prps].rolesId.indexOf(ofx_page_data.userCrossBinding[i].bindWithRole.id)==-1){
            crossRoles.roles[prps].rolesId.push(ofx_page_data.userCrossBinding[i].bindWithRole.id);
            crossRoles.roles[prps].roles.push(ofx_page_data.userCrossBinding[i].bindWithRole);
            }
        }
    if(ofx_page_data.userCrossBinding[i].bindWithRole==null&&ofx_page_data.userCrossBinding[i].bindWithDepartment!=null&&crossRoles.departmentsId.indexOf(ofx_page_data.userCrossBinding[i].bindWithDepartment.id)==-1){
        crossRoles.departmentsId.push(ofx_page_data.userCrossBinding[i].bindWithDepartment.id);
        crossRoles.departments.push(ofx_page_data.userCrossBinding[i].bindWithDepartment);
        }
    }

for(let i = 0; i < ofx_page_data.roleCrossBinding.length; i++){
    if(ofx_page_data.roleCrossBinding[i].bindWithEmployee!=null&&crossRoles.employeesId.indexOf(ofx_page_data.roleCrossBinding[i].bindWithEmployee.id)==-1){
        crossRoles.employeesId.push(ofx_page_data.roleCrossBinding[i].bindWithEmployee.id);
        crossRoles.employees.push(ofx_page_data.roleCrossBinding[i].bindWithEmployee);
        }
    if(ofx_page_data.roleCrossBinding[i].bindWithRole!=null){
        prps = ofx_make_key((ofx_page_data.roleCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.roleCrossBinding[i].bindWithDepartment.name:'departmentself');
        if(typeof crossRoles.roles[prps] == "undefined"){
            crossRoles.roles[prps] = {
                department: (ofx_page_data.roleCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.roleCrossBinding[i].bindWithDepartment:'__SELF__',
                rolesId:[],
                roles:[]
                };
            }
    
        if(ofx_page_data.roleCrossBinding[i].bindWithRole!=null&&crossRoles.roles[prps].rolesId.indexOf(ofx_page_data.roleCrossBinding[i].bindWithRole.id)==-1){
            crossRoles.roles[prps].rolesId.push(ofx_page_data.roleCrossBinding[i].bindWithRole.id);
            crossRoles.roles[prps].roles.push(ofx_page_data.roleCrossBinding[i].bindWithRole);
            }
        }
    if(ofx_page_data.roleCrossBinding[i].bindWithRole==null&&ofx_page_data.roleCrossBinding[i].bindWithDepartment!=null&&crossRoles.departmentsId.indexOf(ofx_page_data.roleCrossBinding[i].bindWithDepartment.id)==-1){
        crossRoles.departmentsId.push(ofx_page_data.roleCrossBinding[i].bindWithDepartment.id);
        crossRoles.departments.push(ofx_page_data.roleCrossBinding[i].bindWithDepartment);
        }
    }

for(let i = 0; i < ofx_page_data.departmentCrossBinding.length; i++){
    if(ofx_page_data.departmentCrossBinding[i].bindWithEmployee!=null&&crossRoles.employeesId.indexOf(ofx_page_data.departmentCrossBinding[i].bindWithEmployee.id)==-1){
        crossRoles.employeesId.push(ofx_page_data.departmentCrossBinding[i].bindWithEmployee.id);
        crossRoles.employees.push(ofx_page_data.departmentCrossBinding[i].bindWithEmployee);
        }
    if(ofx_page_data.departmentCrossBinding[i].bindWithRole!=null){
        prps = ofx_make_key((ofx_page_data.departmentCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.departmentCrossBinding[i].bindWithDepartment.name:'departmentself');
        if(typeof crossRoles.roles[prps] == "undefined"){
            crossRoles.roles[prps] = {
                department: (ofx_page_data.departmentCrossBinding[i].bindWithDepartment!=null)?ofx_page_data.departmentCrossBinding[i].bindWithDepartment.name:'__SELF__',
                rolesId:[],
                roles:[]
                };
            }
    
        if(ofx_page_data.departmentCrossBinding[i].bindWithRole!=null&&crossRoles.roles[prps].rolesId.indexOf(ofx_page_data.departmentCrossBinding[i].bindWithRole.id)==-1){
            crossRoles.roles[prps].rolesId.push(ofx_page_data.departmentCrossBinding[i].bindWithRole.id);
            crossRoles.roles[prps].roles.push(ofx_page_data.departmentCrossBinding[i].bindWithRole);
            }
        }
    if(ofx_page_data.departmentCrossBinding[i].bindWithRole==null&&ofx_page_data.departmentCrossBinding[i].bindWithDepartment!=null&&crossRoles.departmentsId.indexOf(ofx_page_data.departmentCrossBinding[i].bindWithDepartment.id)==-1){
        crossRoles.departmentsId.push(ofx_page_data.departmentCrossBinding[i].bindWithDepartment.id);
        crossRoles.departments.push(ofx_page_data.departmentCrossBinding[i].bindWithDepartment);
        }
    }

 
var workingDays = {},
    calenderWorkingDays = {},
    selectLocation = ofx_page_data.user.location==null?"HYDERABAD":ofx_page_data.user.location;
for(let i = 0; i < ofx_page_data.workingDays.length; i++){
    if(ofx_make_key(selectLocation)==ofx_make_key(ofx_page_data.workingDays[i].location)){
        workingDays[ofx_page_data.workingDays[i].code] = ofx_page_data.workingDays[i];
        }
    if(typeof calenderWorkingDays[ofx_make_key(ofx_page_data.workingDays[i].location)] == "undefined"){
        calenderWorkingDays[ofx_make_key(ofx_page_data.workingDays[i].location)] = {};
        }
    calenderWorkingDays[ofx_make_key(ofx_page_data.workingDays[i].location)][ofx_page_data.workingDays[i].code] = ofx_page_data.workingDays[i];
    }



var fas_file_icons = {
    'default': 'fa-file-alt',
    'xlsx': 'fa-file-excel',
    'csv': 'fa-file-excel',
    'pdf': 'fa-file-pdf',
    'png': 'fa-file-image',
    'jpg': 'fa-file-image',
    'jpeg': 'fa-file-image',
    'zip': 'fa-file-archive',
    'mp3': 'fa-file-audio',
    'mp4': 'fa-file-video',
    'doc': 'fa-file-word',
    'docx': 'fa-file-word',
    };

function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

// function getAssignmentsInfo(department='',role='',deep=1){
//     let ableToDo = (typeof assignmentStepsOrder[department] != "undefined" && typeof assignmentStepsOrder[department][role] != "undefined")?assignmentStepsOrder[department][role]:{};
//     let withVFXartist = false;
//     let checkList = {};
//     if(deep){
//         $.each(assignmentStepsOrder[department],function(z,e){
//             $.each(e.authorised_roles,function(zz,ee){
//                 let crosName = ofx_make_key(ee.name);
//                 if(role!=crosName && typeof assignmentStepsOrder[department][crosName] != "undefined"){
//                     $.each(assignmentStepsOrder[department][crosName].authorised_roles,function(_x,_e){
//                         if(role==ofx_make_key(_e.name)){
//                             checkList[crosName] = getAssignmentsInfo(department,crosName,0);
//                             }
//                         });
//                     }
//                 });
//             });
//         }
    
//     if(typeof ableToDo.allowed_steps != "undefined"){
//         $.each(ableToDo.allowed_steps,function(z,e){
//             if(e.role.name=='VFX ARTIST'){
//                 withVFXartist = true;
//                 }
//             });
//         return {
//             status:true,
//             crossStatus: Object.keys(checkList).length>0?true:false,
//             self: JSON.parse(JSON.stringify(ableToDo.allowed_steps)),
//             cross: JSON.parse(JSON.stringify(checkList)),
//             withVFXartist: withVFXartist
//             };
//         }else{
//             return {
//                 status:false,
//                 crossStatus: Object.keys(checkList).length>0?true:false,
//                 cross: JSON.parse(JSON.stringify(checkList))
//                 };
//             }
//     }
function makeId(length = 10) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
    return result;
    }
var empOptions = {};
function getEmpData(department='',role=''){
    let dep = ofx_make_key(department),
        roleI = ofx_make_key(role);
    if(typeof empOptions[dep] == "undefined"){
        empOptions[dep] = {};
        }
    if(typeof empOptions[dep][roleI] == "undefined"){
        empOptions[dep][roleI] = [];
        $.ajax({
            url: '/api/hrm/employee/',
            type: 'GET',
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            async: true, //displays data after loading the page
            processing: false,
            data: {dept:department, role:role},
            success: function (response) {
                $.each(response,function(z,e){
                    if(e.department!=null&&e.role!=null){
                        empOptions[ofx_make_key(e.department)][ofx_make_key(e.role)].push(JSON.parse(JSON.stringify(e)));
                        }
                    });
                },
            error: function (jqXHR, exception) {
                console.log(jqXHR.responseText)
                }
            });
        }
    }
console.log("ofx_page_data",ofx_page_data);
console.log("workingDays",workingDays);
console.log('userPermissions',userPermissions);
console.log("allowedRolePipelineSteps",allowedRolePipelineSteps);
// console.log("assignmentStepsBeforeArtist",assignmentStepsBeforeArtist);
// console.log("assignmentStepsAfterArtist",assignmentStepsAfterArtist);
// console.log("ofx_page_data.assignmentStepsOrder",ofx_page_data.assignmentStepsOrder);
// console.log("assignmentStepsOrderIndex",assignmentStepsOrderIndex);
// console.log("assignmentStepsOrderStatus",assignmentStepsOrderStatus);
// console.log("assignmentStepsOrder",assignmentStepsOrder);
console.log('crossRoles',crossRoles);