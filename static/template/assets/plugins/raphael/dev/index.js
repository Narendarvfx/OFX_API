/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

var core = require('./raphael.core');
if(core.svg){
  require('./raphael.svg');
}
if(core.vml){
  require('./raphael.vml');
}
module.exports = core;