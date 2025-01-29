
/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

//DAY INFO TABLE DATA
function show_day_info(uname, date){
  var day_data_json = $.ajax({
      type: "GET",
      url: "/api/attendance/"+uname+"/"+date[0]+"/"+date[1]+"/"+date[2]+"/",
      dataType: "application/json",
      async: false,
      error: function (xhr, status, errorThrown) {
        alert("No Info / Date Not selected")
      }
  }).responseText;

  var day_data = JSON.parse(day_data_json);
  console.log(day_data);
  var table = $('#dayInfoTable').DataTable({
      data: day_data['all_data'],
      "columns": [
          { "data": "event_type", title: "IO" },
          { "data": "event_point", title: "Door" },
          { "data": "event_time", title: "Time" },
          { "data": "event_description", title: "Description" },
      ]
  });
  $("#day_info_modal").modal('show')
}

// function show_month_info(id){
//   var date = document.getElementById("selected_date").value.split("-");
//   var day_data_json = $.ajax({
//       type: "GET",
//       url: "/api/attendance/"+id+"/"+date[0]+"/"+date[1]+"/",
//       dataType: "application/json",
//       async: false,
//       error: function (xhr, status, errorThrown) {
//       }
//   }).responseText;
//
//   var day_data = JSON.parse(day_data_json);
//   console.log(day_data);
// }

//MONTH INFO TABLE DATA

function monthChange(uname, month){
  console.log(uname, month)
  var attendance_data = $.ajax({
     url: '/api/attendance/'+uname+'/'+month[0]+'/'+month[1]+'/',
     type: "GET",
     dataType: "application/json",
     async: false
   }).responseText;
   var attendance = JSON.parse(attendance_data);
   console.log(attendance['total']['default']);
   //total
   document.getElementById("total_default").innerHTML = attendance['total']['default']
   document.getElementById("total_target").innerHTML = attendance['total']['target']
   document.getElementById("total_current").innerHTML = attendance['total']['current']
   document.getElementById("total_incomplete").innerHTML = attendance['total']['incomplete']
   //actual
   document.getElementById("actual_default").innerHTML = attendance['actual']['default']
   document.getElementById("actual_target").innerHTML = attendance['actual']['target']
   document.getElementById("actual_current").innerHTML = attendance['actual']['current']
   document.getElementById("actual_incomplete").innerHTML = attendance['actual']['incomplete']
   //days
   document.getElementById("days_default").innerHTML = attendance['days']['default']
   document.getElementById("days_target").innerHTML = attendance['days']['target']
   document.getElementById("days_incomplete").innerHTML = attendance['days']['incomplete']
}
