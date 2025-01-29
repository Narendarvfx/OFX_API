/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

import { Server as KarmaServer } from 'karma';

export default function (options = {}) {
  return function(done) {
    options = Object.assign({
      configFile: `${__dirname}/../../karma.conf.js`,
    }, options);

    let karma = new KarmaServer(options, done);

    karma.start();
  };
}
