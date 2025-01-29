/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

import argv       from 'argv';
import path       from 'path';
import pathExists from 'path-exists';

export default function(src, files, argName = 'file') {
  let args = argv.option([
    {
      name: argName,
      type: 'string'
    }
  ]).run();

  let srcFiles = '';

  if(args.options[argName] && pathExists.sync(path.join(src, args.options[argName]))) {
    let arg = args.options[argName];
    srcFiles = `${src}/${arg}`;
  } else if(Array.isArray(files)) {
    srcFiles = files.map((file) => {
      if(file.indexOf('!') === 0) {
        file = file.substr(1);
        return `!${src}/${file}`;
      }

      return `${src}/${file}`;
    });
  } else {
    srcFiles = `${src}/${files}`;
  }

  return srcFiles;
}
