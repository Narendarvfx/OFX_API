/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

/**
 * sass
 * ======
 *
 * Compile scss to css
 *
 * Link: https://github.com/gruntjs/grunt-contrib-sass
 */

'use strict';

module.exports = function (grunt) {
  return {
    dist: {
      files: [{
        expand: true,
        cwd: '<%= pkg.config.src %>/scss',
        src: ['*.scss'],
        dest: '<%= pkg.config.src %>/css',
        ext: '.css'
      }]
    }
  };
};
