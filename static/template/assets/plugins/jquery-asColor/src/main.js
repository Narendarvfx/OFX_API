/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

import $ from 'jquery';
import AsColor from './asColor';
import info from './info';
import Converter from './converter';

const OtherAsColor = $.asColor;

const jQueryAsColor = function(...args) {
  return new AsColor(...args);
}

$.asColor = jQueryAsColor;
$.asColor.Constructor = AsColor;

$.extend($.asColor, {
  matchString: AsColor.matchString,
  setDefaults: AsColor.setDefaults,
  noConflict: function() {
    $.asColor = OtherAsColor;
    return jQueryAsColor;
  }
}, Converter, info);

export default $.asColor;
