/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

import config      from '../../config';
import gulp        from 'gulp';
import stylelint   from 'gulp-stylelint';
import getSrcFiles from '../util/getSrcFiles';

export function style(src = config.styles.src, files = '**/*.scss') {
  return function() {
    let srcFiles = getSrcFiles(src, files);

    return gulp.src(srcFiles)
      .pipe(stylelint({
        reporters: [{
          formatter: 'string',
          console: true
        }]
      }));
  };
}
