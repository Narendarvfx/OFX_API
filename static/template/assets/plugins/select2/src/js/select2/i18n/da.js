/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

define(function () {
  // Danish
  return {
    errorLoading: function () {
      return 'Resultaterne kunne ikke indlæses.';
    },
    inputTooLong: function (args) {
      var overChars = args.input.length - args.maximum;

      return 'Angiv venligst ' + overChars + ' tegn mindre';
    },
    inputTooShort: function (args) {
      var remainingChars = args.minimum - args.input.length;

      return 'Angiv venligst ' + remainingChars + ' tegn mere';
    },
    loadingMore: function () {
      return 'Indlæser flere resultater…';
    },
    maximumSelected: function (args) {
      var message = 'Du kan kun vælge ' + args.maximum + ' emne';

      if (args.maximum != 1) {
        message += 'r';
      }

      return message;
    },
    noResults: function () {
      return 'Ingen resultater fundet';
    },
    searching: function () {
      return 'Søger…';
    }
  };
});