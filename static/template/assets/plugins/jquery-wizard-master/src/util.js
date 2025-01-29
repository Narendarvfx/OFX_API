/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

import Support from './support';

export function emulateTransitionEnd ($el, duration) {
    'use strict';
  let called = false;

  $el.one(Support.transition.end, () => {
    called = true;
  });
  const callback = () => {
    if (!called) {
      $el.trigger(Support.transition.end);
    }
  };
  setTimeout(callback, duration);
}
