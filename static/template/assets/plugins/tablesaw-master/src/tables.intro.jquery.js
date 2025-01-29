/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(["jquery"], function (jQuery) {
      return (root.Tablesaw = factory(jQuery, root));
    });
  } else if (typeof exports === 'object') {
    if( "document" in root ) {
      module.exports = factory(require('jquery'), root);
    } else {
      // special jQuery case for CommonJS (pass in a window)
      module.exports = factory(require('jquery')(root), root);
    }
  } else {
    root.Tablesaw = factory(jQuery, root);
  }
}(typeof window !== "undefined" ? window : this, function ($, window) {
	"use strict";

  var document = window.document;
