/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

export default {
  format: false,
  shortenHex: false,
  hexUseName: false,
  reduceAlpha: false,
  alphaConvert: { // or false will disable convert
    'RGB': 'RGBA',
    'HSL': 'HSLA',
    'HEX': 'RGBA',
    'NAMESPACE': 'RGBA',
  },
  nameDegradation: 'HEX',
  invalidValue: '',
  zeroAlphaAsTransparent: true
};
