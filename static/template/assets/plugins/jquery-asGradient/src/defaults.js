/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

export default {
  prefixes: ['-webkit-', '-moz-', '-ms-', '-o-'],
  forceStandard: true,
  angleUseKeyword: true,
  emptyString: '',
  degradationFormat: false,
  cleanPosition: true,
  color: {
    format: false, // rgb, rgba, hsl, hsla, hex
    hexUseName: false,
    reduceAlpha: true,
    shortenHex: true,
    zeroAlphaAsTransparent: false,
    invalidValue: {
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }
  }
};
