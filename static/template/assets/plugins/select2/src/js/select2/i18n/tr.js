/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

define(function () {
  // Turkish
  return {
    errorLoading: function (){
      return 'Sonuç yüklenemedi';
    },
    inputTooLong: function (args) {
      var overChars = args.input.length - args.maximum;

      var message = overChars + ' karakter daha girmelisiniz';

      return message;
    },
    inputTooShort: function (args) {
      var remainingChars = args.minimum - args.input.length;

      var message = 'En az ' + remainingChars + ' karakter daha girmelisiniz';

      return message;
    },
    loadingMore: function () {
      return 'Daha fazla…';
    },
    maximumSelected: function (args) {
      var message = 'Sadece ' + args.maximum + ' seçim yapabilirsiniz';

      return message;
    },
    noResults: function () {
      return 'Sonuç bulunamadı';
    },
    searching: function () {
      return 'Aranıyor…';
    }
  };
});
