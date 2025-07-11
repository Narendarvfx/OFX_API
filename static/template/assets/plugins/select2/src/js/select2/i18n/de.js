/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

define(function () {
  // German
  return {
    errorLoading: function () {
      return 'Die Ergebnisse konnten nicht geladen werden.';
    },
    inputTooLong: function (args) {
      var overChars = args.input.length - args.maximum;

      return 'Bitte ' + overChars + ' Zeichen weniger eingeben';
    },
    inputTooShort: function (args) {
      var remainingChars = args.minimum - args.input.length;

      return 'Bitte ' + remainingChars + ' Zeichen mehr eingeben';
    },
    loadingMore: function () {
      return 'Lade mehr Ergebnisse…';
    },
    maximumSelected: function (args) {
      var message = 'Sie können nur ' + args.maximum + ' Eintr';

      if (args.maximum === 1) {
        message += 'ag';
      } else {
        message += 'äge';
      }

      message += ' auswählen';

      return message;
    },
    noResults: function () {
      return 'Keine Übereinstimmungen gefunden';
    },
    searching: function () {
      return 'Suche…';
    }
  };
});
