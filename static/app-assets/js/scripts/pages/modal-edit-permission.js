/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

$(function () {
  ('use strict');
  var editPermissionForm = $('#editPermissionForm');

  // jQuery Validation
  // --------------------------------------------------------------------
  if (editPermissionForm.length) {
    editPermissionForm.validate({
      rules: {
        editPermissionName: {
          required: true
        }
      }
    });
  }
});
