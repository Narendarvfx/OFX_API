// Render left side card
function render_employee_detail_card(employee) {
    var department = 'Department';
    if (employee.department) {
        var department = employee.department;
    }
    var designation = 'Designation';
    if (employee.designation) {
        var designation = employee.designation.name;
    }
    var location = 'Location';
    if (employee.location) {
        var location = employee.location.name;
    }
    var role = 'Role';
    if (employee.role) {
        var role = employee.role.name;
    }
    $('#Employee_Card_Modal').empty();
    var employee_detail_div = `
            <div class="card">
              <div class="card-body">
              <form id="upload_file" class="form-material" role="form" enctype="multipart/form-data">
                <center class="mt-4"> <img id="profile_pic"  src="${employee.photo}" onerror="this.src='/media/profiles/photo/default.png'" class="img-circle" width="150" />
                    <input type="file" id="FileUpload" style="display: none" />
                    <h4 class="card-title mt-2">${employee.full_name}</h4>
                    <h6 class="card-subtitle">${employee.department}</h6>
                    <h6 class="card-subtitle">${employee.location}</h6>
                </center>

               </form>

              </div>

              <div>
                  <hr> </div>
                  <div class="card-body"> <small class="text-muted">Email address </small>
                    <h6>${employee.work_email}</h6> <small class="text-muted p-t-30 db">Phone</small>
                    <h6>+91-${employee.phone}</h6> <small class="text-muted p-t-30 db">Address</small>
                    <h6>${employee.address_1},</h6><h6>${employee.address_city},${employee.address_state},</h6><h6>${employee.address_zip}</h6>

              </div>
            </div>
    `;
    $('#Employee_Card_Modal').append(employee_detail_div);
}

//Render Employee Details General tab
function render_employee_detail_general(employee) {
    $('#general').empty();
    var employee_detail_general_div = `
      <div class="card-body">
        <form id="update_general" class="form-horizontal form-material">

          <div class="form-group">
            <label class="col-md-12">Full Name</label>
            <div class="col-md-12">
              <input id="general_full_name" type="text" name="text" value="${employee.full_name}" class="form-control form-control-line">
              </input>
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">First Name</label>
            <div class="col-md-12">
              <input id="general_first_name" type="text" name="text" value="${employee.first_name}" class="form-control form-control-line">
              </input>
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Last Name</label>
            <div class="col-md-12">
              <input id="general_last_name" type="text" name="text" value="${employee.last_name}" class="form-control form-control-line">
              </input>
            </div>
          </div>
          <div class="form-group">
            <label for="example-email" class="col-md-12">Email</label>
            <div class="col-md-12">
              <input id="general_email" type="email" value="${employee.work_email}" class="form-control form-control-line" name="example-email" id="example-email">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Date of Birth</label>
            <div class="col-md-12">
              <input id="general_dob" type="date" value="${employee.date_of_birth}" class="form-control form-control-line">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Phone</label>
            <div class="col-md-12">
              <input id="general_phone" type="text" value="${employee.phone}" class="form-control form-control-line">
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Gender</label>
            <div class="col-sm-12">
              <select id="general_gender" class="form-control form-control-line">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-md-12">Martial Status</label>
            <div class="col-sm-12">
              <select id="general_marital" value="${employee.marital_status}" class="form-control form-control-line">
                  <option value="single">Single</option>
                  <option value="married">Married</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-12">
              <button type="submit" onclick="updateGeneral(${employee.id})" class="btn btn-success">Update Profile</button>
            </div>
          </div>
        </form>
      </div>
    `;
    $('#general').append(employee_detail_general_div);
    $('#general_gender').val(employee.gender);
    $('#general_marital').val(employee.marital_status);

}

//Render Employee Details Contact tab
function render_employee_detail_contact(employee) {
    $('#contact').empty();
    var employee_detail_contact_div = `
    <div class="card-body">
      <form id ="update_contact" class="form-horizontal form-material" >

        <div class="form-group">
          <label class="col-md-12">Address_1</label>
          <div class="col-md-12">
            <input type="text" id="contact_address_1" value="${employee.address_1}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-12">Address_2</label>
          <div class="col-md-12">
            <input type="text" id="contact_address_2" value="${employee.address_2}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-12">City</label>
          <div class="col-md-12">
            <input type="text" id="contact_address_city" value="${employee.address_city}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-12">State</label>
          <div class="col-md-12">
            <input type="text" id="contact_address_state" value="${employee.address_state}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-12">Zip</label>
          <div class="col-md-12">
            <input type="number" id="contact_address_zip" value="${employee.address_zip}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-12">Country</label>
          <div class="col-md-12">
            <input type="text" id="contact_address_country" value="${employee.address_country}" class="form-control form-control-line">
          </div>
        </div>
        <div class="form-group">
          <div class="col-sm-12">
            <button class="btn btn-success" type="submit" onclick="updateContact(${employee.id})">Update Profile</button>
          </div>
        </div>
      </form>
    </div>
    `;
    $('#contact').append(employee_detail_contact_div);

}

// Render upload Button in attachments
function render_attach_button(employee){
  $('#forid').empty();
  var id= `
    <button class="btn btn-success" type="submit" id="attachFile" onclick="attachUpload('${employee.id}')" >Upload File</button>
    `;
    $('#forid').append(id);
}
//Render Employee Attachments tab
function render_employee_detail_attach(attach) {
  var employee_detail_attach_div = `
  <tr>
    <td><a href="${attach.file}" data-fancybox="gallery" data-caption="${attach.attachment_type}"><img src="${attach.file}" alt="files" width="70" height="70"  /></a></td>
    <td>${attach.attachment_type}</td>
    <td>${attach.creation_date}</td>
  </tr>
    `;
    $('#attachments_tbody_view').append(employee_detail_attach_div);
  }

//Render Employee Details Entitlement tab
function render_employee_detail_entitle(entitle, lop) {
  var sum = 0;
  for(i in lop){
    sum += lop[i]['lop_days'];
  }
  console.log(sum);
  var date = new Date();
  var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
  var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

  var lastDayWithSlashes = lastDay.getFullYear()+'-'+(lastDay.getMonth() + 1) +'-'+(lastDay.getDate()) ;
  var firstDayWithSlashes = firstDay.getFullYear()+'-'+(firstDay.getMonth() + 1) +'-'+(firstDay.getDate());

  if(entitle.start_date >= firstDayWithSlashes){

  }

    $('#entitle').empty();
    var employee_detail_entitle_div = `
    <div class="card-body">
      <form id = "update_entitle" class="form-horizontal form-material" role="form" >

           <h3 class="box-title">Entitlement Info</h3>
           <hr class="mt-0 mb-5">
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Remaining Casual Leaves :</label>
                    <div class="col-md-3">
                        <span class="label label-rounded label-success">${entitle.cl_leaves}</span>
                    </div>
                </div>
             </div>
           </div>
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Remaining Earned Leaves :</label>
                    <div class="col-md-3">
                        <span class="label label-rounded label-success">${entitle.el_leaves}</span>
                    </div>
                </div>
             </div>
           </div>
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Total LOP's in this Month:</label>
                    <div class="col-md-3">
                        <span class="label label-rounded label-success">${sum}</span>
                    </div>
                </div>
             </div>
           </div>
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Total LOP's in this Year:</label>
                    <div class="col-md-3">
                        <p class="form-control-static">  </p>
                    </div>
                </div>
             </div>
           </div>
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Total taken Leaves in this Month:</label>
                    <div class="col-md-3">
                        <p class="form-control-static">  </p>
                    </div>
                </div>
             </div>
           </div>
           <div class="row">
             <div class="col-lg-6 col-md-12">
                <div class="form-group row">
                    <label class="control-label text-right col-md-8">Total taken Leaves in this Year:</label>
                    <div class="col-md-3">
                        <p class="form-control-static">  </p>
                    </div>
                </div>
             </div>
           </div>
      </form>
    </div>
    `;
    $('#entitle').append(employee_detail_entitle_div);
}

function updateGeneral(employee_id) {

    $("#update_general").on("submit", function () {
        $.ajax({
            url: '/api/hrm/employee/' + employee_id + '/',
            type: "PUT",
            dataType: 'application/json',
            data: {
                "work_email": $("#general_email").val(),
                "full_name": $("#general_full_name").val(),
                "first_name": $("#general_first_name").val(),
                "last_name": $("#general_last_name").val(),
                "date_of_birth": $("#general_dob").val(),
                "phone": $("#general_phone").val(),
                "gender": $("#general_gender option:selected").val(),
                "marital_status": $("#general_marital option:selected").val(),
            },
        });
    })
}

// Update Employee Contact Data
function updateContact(employee_id) {

    $("#update_contact").on("submit", function (event) {
        $.ajax({
            url: '/api/hrm/employee/' + employee_id + '/',
            type: "PUT",
            dataType: 'application/json',
            data: {
                "address_1": $("#contact_address_1").val(),
                "address_2": $("#contact_address_2").val(),
                "address_city": $("#contact_address_city").val(),
                "address_state": $("#contact_address_state").val(),
                "address_zip": $("#contact_address_zip").val(),
                "address_country": $("#contact_address_country").val()
            }
        });
    })
}

// Update Employee Job Data
function updateJob(employee_id) {

    $("#update_job").on("submit", function (event) {
        $.ajax({
            url: '/api/hrm/employee/' + employee_id + '/',
            type: "PUT",
            dataType: 'application/json',
            data: {
                "employee_id": $("#job_employee_id").val(),
                "joining_date": $("#job_doj").val(),
                "designation": $("#job_designation option:selected").val(),
                "department": $("#job_department option:selected").val(),
                "location": $("#job_location option:selected").val(),
                "role": $("#job_role option:selected").val()
            }
        });
    })
}
