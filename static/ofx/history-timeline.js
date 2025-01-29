//lead-report
jQuery.fn.extend({
    HistoryTimelineLog: function(e={
        type:'left|right',
        dateTime: null,
        createdBy:{},
        title:'',
        message:''
        },setToEnd=true) {
        let le = Object.assign({
            type:'left',
            dateTime: moment().format("YYYY-MM-DD")+'T23:59:59.999999',
            createdBy:{
                fullName:'N/A',
                photo:'/media/profiles/photo/default.png'
                },
            title:'N/A',
            message:'N/A'
            },e);

        var hBody = (le.type=='left'?`<div class="row timeline-right">
                <div class="col-md-6">
                    <p class="timeline-date">` + moment(le.dateTime).format("MMM Do YYYY, h:mm a") + `</p>
                </div>
                <div class="col-md-6">
                    <div class="timeline-box">
                        <div class="timeline-icon">
                        <img src="`+le.createdBy.photo+`" alt="`+le.createdBy.fullName+`" title="`+le.createdBy.fullName+`" onerror="this.src='/media/profiles/photo/default.png'" class="profile-pic" width="50" style="width: 100%;border-radius: 50%;margin-left: -10px;margin-top: -10px;">
                        </div>
                        <div class="timeline-text">
                            <h3>`+le.title+`</h3>
                            <p>`+le.message+`</p>
                        </div>
                    </div>
                </div>
            </div>`:`<div class="row timeline-left">
                        <div class="col-md-6 d-md-none d-block">
                            <p class="timeline-date">` + moment(le.dateTime).format("MMM Do YYYY, h:mm a") + `</p>
                        </div>
                        <div class="col-md-6">
                            <div class="timeline-box">
                                <div class="timeline-icon d-md-none d-block">
                                <img src="`+le.createdBy.photo+`" alt="`+le.createdBy.fullName+`" title="`+le.createdBy.fullName+`" onerror="this.src='/media/profiles/photo/default.png'" class="profile-pic" width="50" style="width: 100%;border-radius: 50%;margin-left: 10px;margin-top: -10px;">
                                </div>
                                <div class="timeline-text">
                                    <h3>`+le.title+`</h3>
                                    <p>`+le.message+`</p>
                                </div>
                                <div class="timeline-icon d-md-block d-none">
                                <img src="`+le.createdBy.photo+`" alt="`+le.createdBy.fullName+`" title="`+le.createdBy.fullName+`" onerror="this.src='/media/profiles/photo/default.png'" class="profile-pic" width="50" style="width: 100%;border-radius: 50%;margin-left: 10px;margin-top: -10px;">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 d-md-block d-none">
                            <p class="timeline-date">` + moment(le.dateTime).format("MMM Do YYYY, h:mm a") + `</p>
                        </div>
                    </div>`);
        if(setToEnd){
            $(this).append(hBody);
            }else{
                $(this).prepend(hBody)
                }
        }
    });