/*<div class="csrf-ajax-token-shotassignments" style="display: none;">{% csrf_token %}</div> */
var shotassignments = {
    shotPosb: {},
    beforeArtists:[],
    makeKey: function(inData = []){
        var _dR = [];
        $.each(Object.prototype.toString.call(inData) == '[object String]'?[inData]:inData,function(_x,_e){
            _dR.push(_e==null?'blank_':String(_e).replace(/[^a-zA-Z ]/gi, "").replace(/[_\s]/g, '').toLowerCase());
            });
        return _dR.join('_');
        },
    _httpRequest: function(url='',method='GET',data={},callback=[{func:'myfunc',data:true}],required=[]){
        var CSRFToken = '';
        $('.csrf-ajax-token-shotassignments input').each(function(e){ CSRFToken = $(this).val(); });
        var urlParms = [];
        if(method=='DELETE'){
            $.each(data,function(z,e){
                urlParms.push(z+'='+((jQuery.type(e) === "string"||jQuery.type(e) === "number")?e:JSON.stringify(e)));
                });
            }
        $.ajax({
            url: url+(urlParms.length>0?"?"+urlParms.join('&'):""),
            type: method,
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            data: method!='DELETE'?data:{},
            async: true, //displays data after loading the page
            processing: false,
            beforeSend: function(request){
                if(required.length>0){
                    request.setRequestHeader("required", JSON.stringify(required));
                    }
                if(CSRFToken.length>0){
                    request.setRequestHeader("X-CSRFToken", CSRFToken);
                    }
                },
            success: function (response){
                $.each(callback,function(z,e){
                    if(typeof shotassignments[e.func] === 'function'){
                        if(e.data==true){
                            shotassignments[e.func](response);
                            }else if(e.data==false){
                                shotassignments[e.func]();
                                }else{
                                    shotassignments[e.func](e.data);
                                    }
                        }
                    });
                },
            error: function (jqXHR, exception){
                console.log(jqXHR.responseText)
                }
            });
        },
    
    dep_empFky: function(dep=[]){
        _dev = {};
        $.each(dep,function(_x_,_e_){
            _dev[shotassignments.makeKey(_e_.employee!=null?_e_.employee.fullName:[
                _e_.location!=null?_e_.location.name:null,
                _e_.department!=null?_e_.department.name:null,
                _e_.role!=null?_e_.role.name:null,
                ])] = JSON.parse(JSON.stringify(_e_));
            });
        return _dev;
        },

    serializeShotPossibilities:function(e){
        $.each(e,function(_x,_e){
            var xKey = shotassignments.makeKey([
                _e.location!=null?_e.location.name:null,
                _e.department!=null?_e.department.name:null,
                _e.shotStatus!=null?_e.shotStatus.code:null,
                _e.isSubShot?'sub':'main',
                ]);
            if(_e.isBeforeArtist&&shotassignments.beforeArtists.indexOf(xKey)==-1){
                shotassignments.beforeArtists.push(xKey);
                }
            shotassignments.shotPosb[xKey] = JSON.parse(
                JSON.stringify(
                    Object.assign(
                        JSON.parse(
                            JSON.stringify(_e)
                            ),
                        JSON.parse(
                            JSON.stringify({
                                authorizedRoles: shotassignments.dep_empFky(_e.authorizedRoles),
                                allowedSteps: shotassignments.dep_empFky(_e.allowedSteps),
                                })
                            )
                        )
                    )
                );
            });
        },
    
    getShotPossibilities: function(user={},permissions=[]){
        let qRx = {};
        if(permissions.indexOf('can_assign_all_location_shots')==-1){
            qRx['location__name'] = user.location;
            }
        if(permissions.indexOf('can_assign_all_dept_shots')==-1){
            qRx['department__name'] = user.department;
            }
        this._httpRequest("/api/shotassignments/",'GET',qRx,[{func:'serializeShotPossibilities',data:true}],[
            "id",
            "location__id",
            "location__name",
            "department__id",
            "department__name",
            "shotStatus__id",
            "shotStatus__code",
            "acceptCase__id",
            "acceptCase__code",
            "rejectCase__id",
            "rejectCase__code",
            "authorizedRoles__id",
            "authorizedRoles__location__id",
            "authorizedRoles__location__name",
            "authorizedRoles__department__id",
            "authorizedRoles__department__name",
            "authorizedRoles__role__id",
            "authorizedRoles__role__name",
            "authorizedRoles__employee__id",
            "authorizedRoles__employee__fullName",
            "authorizedRoles__employee__department__id",
            "authorizedRoles__employee__department__name",
            "authorizedRoles__employee__role__id",
            "authorizedRoles__employee__role__name",
            "authorizedRoles__shotStatus__id",
            "authorizedRoles__shotStatus__code",
            "authorizedRoles__roleIndex",
            "allowedSteps__id",
            "allowedSteps__location__id",
            "allowedSteps__location__name",
            "allowedSteps__department__id",
            "allowedSteps__department__name",
            "allowedSteps__role__id",
            "allowedSteps__role__name",
            "allowedSteps__employee__id",
            "allowedSteps__employee__fullName",
            "allowedSteps__employee__department__id",
            "allowedSteps__employee__department__name",
            "allowedSteps__employee__role__id",
            "allowedSteps__employee__role__name",
            "allowedSteps__shotStatus__id",
            "allowedSteps__shotStatus__code",
            "allowedSteps__roleIndex",
            "statusIndex",
            "isBeforeArtist",
            "isSubShot"
            ]);
        }
    };

shotassignments.getShotPossibilities(ofx_page_data.user,userPermissions);

// jQuery.fn.extend({
    
//     });