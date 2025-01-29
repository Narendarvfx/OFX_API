/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

define(function () {
  // Albanian
  return {
    errorLoading: function () {
      return 'Rezultatet nuk mund të ngarkoheshin.';
    },
    inputTooLong: function (args) {
      var overChars = args.input.length - args.maximum;

      var message = 'Të lutem fshi ' + overChars + ' karakter';

      if (overChars != 1) {
        message += 'e';
      }

      return message;
    },
    inputTooShort: function (args) {
      var remainingChars = args.minimum - args.input.length;

      var message = 'Të lutem shkruaj ' + remainingChars + 
          ' ose më shumë karaktere';

      return message;
    },
    loadingMore: function () {
      return 'Duke ngarkuar më shumë rezultate…';
    },
    maximumSelected: function (args) {
      var message = 'Mund të zgjedhësh vetëm ' + args.maximum + ' element';

      if (args.maximum != 1) {
        message += 'e';
      }

      return message;
    },
    noResults: function () {
      return 'Nuk u gjet asnjë rezultat';
    },
    searching: function () {
      return 'Duke kërkuar…';
    }
  };
});
