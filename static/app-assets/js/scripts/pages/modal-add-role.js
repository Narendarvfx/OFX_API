/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

// Add new role Modal JS
//------------------------------------------------------------------
(function () {
  var addRoleForm = $('#addRoleForm');

  // add role form validation
  if (addRoleForm.length) {
    addRoleForm.validate({
      rules: {
        modalRoleName: {
          required: true
        }
      }
    });
  }

  // reset form on modal hidden
  $('.modal').on('hidden.bs.modal', function () {
    $(this).find('form')[0].reset();
  });

  // Select All checkbox click
  const selectAll = document.querySelector('#selectAll'),
    checkboxList = document.querySelectorAll('[type="checkbox"]');
  selectAll.addEventListener('change', t => {
    checkboxList.forEach(e => {
      e.checked = t.target.checked;
    });
  });
})();
