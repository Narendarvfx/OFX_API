/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

/**
 * Grunt Configurations
 * ====================
 *
 * Seperate tasks and configurations are declared in '/tasks'.
 *
 * Link: https://github.com/firstandthird/load-grunt-config
 */

'use strict';

module.exports = function (grunt) {

  // tracks how long a tasks take
  require('time-grunt')(grunt);

  // load task and configurations
  require('load-grunt-config')(grunt, {
    configPath: __dirname +  '/tasks',
    data: {
      pkg: grunt.file.readJSON('package.json'),
      year: new Date().getFullYear()
    }
  });
};
