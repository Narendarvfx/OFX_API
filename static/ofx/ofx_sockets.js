/*
 * Copyright (c) 2022-2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */
jQuery.fn.extend({
    setProgressColor: function(e={
        status:0,
        prefix:'css-bar-'
        }) {
        let mainTag=$(this), lx = ['danger','warning','info','primary','success'], le = Object.assign({
        status:0,
        prefix:'css-bar-'
        },e);
        $.each(lx,function(z,x){
            $(mainTag).removeClass(le.prefix+x);
            });
        $(mainTag).addClass(le.prefix+lx[(le.status<25 ? 0 : (le.status<50 ? 1 : (le.status<75 ? 2 : (le.status<100 ? 3 : 4))))]);
        }
    });
$wsClient = {
    network: true,
    // isBooted: true,
    userId: null,
    reconnectTimeOut: 1000,
    allowReconncet: true,
    apiPath: null,
    wsHost: null,
    apiKey: (typeof ofx_page_data != "undefined" && typeof ofx_page_data.user != "undefined")?ofx_page_data.user.apikey:null,
    wsToken: null,
    userDataI: (typeof ofx_page_data != "undefined" && typeof ofx_page_data.user != "undefined")?ofx_page_data.user:{},
    lastSync: new Date(),
    ws: {},
    chkConnection: function () {
        if (this.network != navigator.onLine) {
            this.network = navigator.onLine;
            if (!this.network && typeof this.ws.readyState !== 'undefined' && this.ws.readyState == 1) {
                this.ws.close();
            }
        }
    },

    makeid: function (length = 10) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    },

    connectClient: function (force = false) {
        this.chkConnection();
        if (this.network) {
            this.allowReconncet = false;
            this.wsToken = this.makeid(10);
            if (this.apiKey == null) {
                $.ajax({
                    url: this.apiPath + this.userId + '/',
                    type: 'GET',
                    data: {
                        format:'json'
                    },
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function (response) {
                        if (typeof response == 'object' && typeof response.apikey != "undefined") {
                            $wsClient.userDataI = response
                            $wsClient.apiKey = response['apikey'];
                            $wsClient.connect(force);
                        } else {
                            console.log('Unexpected employee data');
                        }
                    },
                    error: function (data) {
                        $wsClient.connectClient(force);
                    }
                });
            } else {
                this.connect(force);
            }
        } else {
            setTimeout(function () {
                $wsClient.connectClient(true);
            }, this.reconnectTimeOut);
        }
    },
    incomingData: [],
    connect: function (force = false) {
        this.chkConnection();
        if (this.network) {
            if (force === true && typeof this.ws.readyState !== 'undefined') {
                this.ws.close();
            }
            try {
                console.log('socket', "uncomment code to connect socket");
                // this.ws = new WebSocket(this.wsHost + this.apiKey + '/' + this.wsToken + '/');
                // this.ws.binaryType = "arraybuffer";
                // this.ws.onopen = function () {
                //     $wsClient.allowReconncet = true;
                //     $wsClient.clientConnected();
                // };
                // this.ws.onmessage = function (evt) {
                //     $wsClient.lastSync = new Date();
                //     $wsClient.readData(evt);
                // };
                // this.ws.onclose = function () {
                //     $wsClient.clientClosed();
                //     $wsClient.allowReconncet = true;
                //     setTimeout(function () {
                //         $wsClient.connectClient(true);
                //     }, $wsClient.reconnectTimeOut);
                // };
            } catch (exception) {
                console.log('socket', exception);
            }
        } else {
            console.log('error', 'No Internet connection');
        }
    },
    readData: function (e) {
        let data = JSON.parse(e.data);
        if (typeof data.status != "undefined") {
            if (data.status == "conncetd") {
                this.clientConnectedMessage(data.message, data.userData, data.groups);
            } else if (data.status == "clientoffline") {
                this.clientOffline(data.clientId);
            } else if (data.status == "clientonline") {
                this.clientOnline(data.clientId);
            }
        } else if (jQuery.inArray(data.dataId, this.incomingData) == -1) {
            this.incomingData.push(data.dataId);
            this.received(data);
        } else {
            console.log('duplicate_incoming:', data);
        }
    },
    sendData: function (dataId = '', targetUsers = [], targetGroups = [], data = {}, saveData = null) {
        if (this.network && typeof this.ws.readyState !== 'undefined' && this.ws.readyState == 1) {
            if (dataId.length == 0) {
                dataId = this.makeid(32);
            }
            this.ws.send(JSON.stringify({
                type: "data",
                dataId: dataId,
                targetUsers: targetUsers,
                targetGroups: targetGroups,
                data: data,
                "__SAVE__": saveData
            }));
        }
    },
    received: function (data) {
    }
};

$wsClient = Object.assign($wsClient, {
    userId: user_id,
    reconnectTimeOut: 1000,
    apiPath: '/api/hrm/myprofile/',
    wsHost: `ws`+(location.protocol !== "https:"?'':'s')+`://${window.location.host}/ws/data/`,
    received: function (data) {
        if (typeof data.data.message != "undefined") {
            if (typeof data.data.fromGroup != "undefined" && data.data.fromGroup.length > 0) {
                this.groupMessage(data);
            } else {
                this.individualMessage(data);
            }
        } else {
            if (typeof data.data.fromGroup != "undefined" && data.data.fromGroup.length > 0) {
                this.groupData(data);
            } else {
                this.individualData(data);
            }
        }
    },
    clientOffline: function (clientApiKey = '') {
        console.log('offline', clientApiKey);
    },
    clientOnline: function (clientApiKey = '') {
        console.log('online', clientApiKey);
    },
    clientConnected: function () {
        console.log('connected');
        // $wsClient.sendMessage('','', [this.apiKey], [], message = {text:'Hi User',extradata:[{name:"file1.txt"}]},null);
    },
    clientConnectedMessage: function (message, userData, groups) {
        console.log('connected:', message);
        console.log('UserData:', userData);
        console.log('groups:', groups);
    },
    clientClosed: function () {
        console.log('Disconnected');
    },
    groupMessage: function (data) {
        this.toUi(data, true);
        // console.log('groupMessage:', data);
    },
    individualMessage: function (data) {
        this.toUi(data, false);
        // console.log('individualMessage:', data);
    },
    // groupData: function (data) {
    //     console.log('groupData:', data);
    // },
    // individualData: function (data) {
    //     console.log('individualData:', data);
    // },
    sendMessage: function (dataId = '', fromGroup = ''/*if user leave it blank*/, toUsers = [], toGroups = [], message = null, savedata = null) {
        this.sendData(dataId, toUsers, toGroups, {
            'fromGroup': fromGroup,
            'message': message
        }, savedata);
    },
    toUi: function (data, fromGroup) {
        if( typeof  data.data.message != "undefined"){
            let msg = typeof  data.data.message == "object"&&data.data.message.title!=null?{title:data.data.message.title, text: data.data.message.message}:{title:"Notification", text: typeof  data.data.message == "object"?data.data.message.message:data.data.message};
            let parent = $('.notification-bell-hold > .message-center');
            addNotifications($(parent),{
                from_user: data.fromUser.user,
                message_title: msg.title,
                message: msg.text,
                creation_date: moment(),
                dataId: data.dataId,
                referenceId: typeof data.data.message.referenceId != "undefined"?data.data.message.referenceId:0,
                read_recipients:[ ]
                },false);
            $.toast({
                heading: msg.title,
                showHideTransition: 'slide',
                text: msg.text,
                icon: 'info',
                position: 'top-right',
                loader: true,        // Change it to false to disable loader
                loaderBg: '#da7b1c',// To change the background
                bgColor: '#1d6de5',
                textColor: 'white',
                hideAfter: 5000   // in milli seconds
            });
        }
    }
});

/*
function ofx_ws_set_task(referenceId="",reference_type="",from_group_key="",to_users=[],to_groups=[],message="",attachments=null,notification=true,ws_data={},savedata=null){
    let notifyData = {
        referenceId:referenceId,
        reference_type:reference_type,
        from_group_key:from_group_key,
        to_users:to_users,
        to_groups:to_groups,
        message:message,
    };
    $.ajax({
        url: '/api/wsnotifications/notificationlogs/',
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(notifyData),
        success: function (response) {
            console.log(response)
            if (typeof response == "object"){

            }else {
                console.log("Unknown Response:", response)
            }
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR.responseText)
        }
    });

}
*/
function ofx_notify_save(data=[]){
    // console.log(data)
    $.ajax({
        url: '/api/wsnotifications/notificationlogs/',
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        async: true, //displays data after loading the page
        processing: false,
        success: function (response) { },
        error: function (jqXHR, exception) { console.log(jqXHR.responseText) }
    });
}
$wsClient.connectClient();
// console.log($wsClient);
// $wsClient.sendMessage('','', [this.apiKey], [], message = {text:'Hi User',extradata:[{name:"file1.txt"}]},null);
