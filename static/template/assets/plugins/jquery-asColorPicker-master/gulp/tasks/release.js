/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

'use strict';

import config from '../../config';
import releaseIt     from 'release-it';
import handleErrors  from '../util/handleErrors';
import {argv} from 'yargs';

export default function release() {
  let options = {};
  options.increment = argv.increment || "patch";
  options.verbose = argv.verbose || true;
  options.debug = argv.debug || false;
  options.force = argv.force || false;
  options['dry-run'] = argv['dry-run'] || false;

  config.setEnv('production');

  return function(done) {
    releaseIt.execute(options).catch(handleErrors).finally(done);
  }
}
