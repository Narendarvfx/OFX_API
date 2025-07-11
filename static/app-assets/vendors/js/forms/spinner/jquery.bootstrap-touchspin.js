/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

/*
 *  Bootstrap TouchSpin - v4.3.0
 *  A mobile and touch friendly input spinner component for Bootstrap 3 & 4.
 *  http://www.virtuosoft.eu/code/bootstrap-touchspin/
 *
 *  Made by István Ujj-Mészáros
 *  Under Apache License v2.0 License
 */

!(function (o) {
  'function' == typeof define && define.amd
    ? define(['jquery'], o)
    : 'object' == typeof module && module.exports
    ? (module.exports = function (t, n) {
        return void 0 === n && (n = 'undefined' != typeof window ? require('jquery') : require('jquery')(t)), o(n), n;
      })
    : o(jQuery);
})(function (D) {
  'use strict';
  var N = 0;
  D.fn.TouchSpin = function (k) {
    var C = {
        min: 0,
        max: 100,
        initval: '',
        replacementval: '',
        firstclickvalueifempty: null,
        step: 1,
        decimals: 0,
        stepinterval: 100,
        forcestepdivisibility: 'round',
        stepintervaldelay: 500,
        verticalbuttons: !1,
        verticalup: '+',
        verticaldown: '-',
        verticalupclass: '',
        verticaldownclass: '',
        prefix: '',
        postfix: '',
        prefix_extraclass: '',
        postfix_extraclass: '',
        booster: !0,
        boostat: 10,
        maxboostedstep: !1,
        mousewheel: !0,
        buttondown_class: 'btn btn-primary',
        buttonup_class: 'btn btn-primary',
        buttondown_txt: '-',
        buttonup_txt: '+',
        callback_before_calculation: function (t) {
          return t;
        },
        callback_after_calculation: function (t) {
          return t;
        }
      },
      j = {
        min: 'min',
        max: 'max',
        initval: 'init-val',
        replacementval: 'replacement-val',
        firstclickvalueifempty: 'first-click-value-if-empty',
        step: 'step',
        decimals: 'decimals',
        stepinterval: 'step-interval',
        verticalbuttons: 'vertical-buttons',
        verticalupclass: 'vertical-up-class',
        verticaldownclass: 'vertical-down-class',
        forcestepdivisibility: 'force-step-divisibility',
        stepintervaldelay: 'step-interval-delay',
        prefix: 'prefix',
        postfix: 'postfix',
        prefix_extraclass: 'prefix-extra-class',
        postfix_extraclass: 'postfix-extra-class',
        booster: 'booster',
        boostat: 'boostat',
        maxboostedstep: 'max-boosted-step',
        mousewheel: 'mouse-wheel',
        buttondown_class: 'button-down-class',
        buttonup_class: 'button-up-class',
        buttondown_txt: 'button-down-txt',
        buttonup_txt: 'button-up-txt'
      };
    return this.each(function () {
      var i,
        o,
        s,
        u,
        p,
        a,
        t,
        n,
        e,
        r,
        c = D(this),
        l = c.data(),
        d = 0,
        f = !1;
      function b() {
        '' === i.prefix && (o = p.prefix.detach()), '' === i.postfix && (s = p.postfix.detach());
      }
      function h() {
        var t, n, o;
        '' !== (t = i.callback_before_calculation(c.val()))
          ? (0 < i.decimals && '.' === t) ||
            ((n = parseFloat(t)),
            isNaN(n) && (n = '' !== i.replacementval ? i.replacementval : 0),
            (o = n).toString() !== t && (o = n),
            null !== i.min && n < i.min && (o = i.min),
            null !== i.max && n > i.max && (o = i.max),
            (o = (function (t) {
              switch (i.forcestepdivisibility) {
                case 'round':
                  return (Math.round(t / i.step) * i.step).toFixed(i.decimals);
                case 'floor':
                  return (Math.floor(t / i.step) * i.step).toFixed(i.decimals);
                case 'ceil':
                  return (Math.ceil(t / i.step) * i.step).toFixed(i.decimals);
                default:
                  return t.toFixed(i.decimals);
              }
            })(o)),
            Number(t).toString() !== o.toString() && (c.val(o), c.trigger('change')))
          : '' !== i.replacementval && (c.val(i.replacementval), c.trigger('change'));
      }
      function v() {
        if (i.booster) {
          var t = Math.pow(2, Math.floor(d / i.boostat)) * i.step;
          return (
            i.maxboostedstep && t > i.maxboostedstep && ((t = i.maxboostedstep), (a = Math.round(a / t) * t)),
            Math.max(i.step, t)
          );
        }
        return i.step;
      }
      function x() {
        return 'number' == typeof i.firstclickvalueifempty ? i.firstclickvalueifempty : (i.min + i.max) / 2;
      }
      function g() {
        h();
        var t,
          n = (a = parseFloat(i.callback_before_calculation(p.input.val())));
        isNaN(a) ? (a = x()) : ((t = v()), (a += t)),
          null !== i.max && a > i.max && ((a = i.max), c.trigger('touchspin.on.max'), y()),
          p.input.val(i.callback_after_calculation(Number(a).toFixed(i.decimals))),
          n !== a && c.trigger('change');
      }
      function m() {
        h();
        var t,
          n = (a = parseFloat(i.callback_before_calculation(p.input.val())));
        isNaN(a) ? (a = x()) : ((t = v()), (a -= t)),
          null !== i.min && a < i.min && ((a = i.min), c.trigger('touchspin.on.min'), y()),
          p.input.val(i.callback_after_calculation(Number(a).toFixed(i.decimals))),
          n !== a && c.trigger('change');
      }
      function w() {
        y(),
          (d = 0),
          (f = 'down'),
          c.trigger('touchspin.on.startspin'),
          c.trigger('touchspin.on.startdownspin'),
          (e = setTimeout(function () {
            t = setInterval(function () {
              d++, m();
            }, i.stepinterval);
          }, i.stepintervaldelay));
      }
      function _() {
        y(),
          (d = 0),
          (f = 'up'),
          c.trigger('touchspin.on.startspin'),
          c.trigger('touchspin.on.startupspin'),
          (r = setTimeout(function () {
            n = setInterval(function () {
              d++, g();
            }, i.stepinterval);
          }, i.stepintervaldelay));
      }
      function y() {
        switch ((clearTimeout(e), clearTimeout(r), clearInterval(t), clearInterval(n), f)) {
          case 'up':
            c.trigger('touchspin.on.stopupspin'), c.trigger('touchspin.on.stopspin');
            break;
          case 'down':
            c.trigger('touchspin.on.stopdownspin'), c.trigger('touchspin.on.stopspin');
        }
        (d = 0), (f = !1);
      }
      !(function () {
        if (c.data('alreadyinitialized')) return;
        if ((c.data('alreadyinitialized', !0), (N += 1), c.data('spinnerid', N), !c.is('input')))
          return console.log('Must be an input.');
        (i = D.extend(
          {},
          C,
          l,
          (function () {
            var s = {};
            return (
              D.each(j, function (t, n) {
                var o = 'bts-' + n;
                c.is('[data-' + o + ']') && (s[t] = c.data(o));
              }),
              s
            );
          })(),
          k
        )),
          '' !== i.initval && '' === c.val() && c.val(i.initval),
          h(),
          (function () {
            var t = c.val(),
              n = c.parent();
            '' !== t && (t = i.callback_after_calculation(Number(t).toFixed(i.decimals)));
            c.data('initvalue', t).val(t),
              c.addClass('form-control'),
              n.hasClass('input-group')
                ? (function (t) {
                    t.addClass('bootstrap-touchspin');
                    var n,
                      o,
                      s = c.prev(),
                      p = c.next(),
                      a =
                        '<span class="input-group-addon bootstrap-touchspin-prefix bootstrap-touchspin-injected"><span class="input-group-text">' +
                        i.prefix +
                        '</span></span>',
                      e =
                        '<span class="input-group-addon bootstrap-touchspin-postfix bootstrap-touchspin-injected"><span class="input-group-text">' +
                        i.postfix +
                        '</span></span>';
                    s.hasClass('input-group-btn') || s.hasClass('input-group-text')
                      ? ((n =
                          '<button class="' +
                          i.buttondown_class +
                          ' bootstrap-touchspin-down bootstrap-touchspin-injected" type="button">' +
                          i.buttondown_txt +
                          '</button>'),
                        s.append(n))
                      : ((n =
                          '<span class="input-group-btn bootstrap-touchspin-injected"><button class="' +
                          i.buttondown_class +
                          ' bootstrap-touchspin-down" type="button">' +
                          i.buttondown_txt +
                          '</button></span>'),
                        D(n).insertBefore(c));
                    p.hasClass('input-group-btn') || p.hasClass('input-group-text')
                      ? ((o =
                          '<button class="' +
                          i.buttonup_class +
                          ' bootstrap-touchspin-up bootstrap-touchspin-injected" type="button">' +
                          i.buttonup_txt +
                          '</button>'),
                        p.text(o))
                      : ((o =
                          '<span class="input-group-btn bootstrap-touchspin-injected"><button class="' +
                          i.buttonup_class +
                          ' bootstrap-touchspin-up" type="button">' +
                          i.buttonup_txt +
                          '</button></span>'),
                        D(o).insertAfter(c));
                    D(a).insertBefore(c), D(e).insertAfter(c), (u = t);
                  })(n)
                : (function () {
                    var t,
                      n = '';
                    c.hasClass('input-sm') && (n = 'input-group-sm');
                    c.hasClass('input-lg') && (n = 'input-group-lg');
                    t = i.verticalbuttons
                      ? '<div class="input-group ' +
                        n +
                        ' bootstrap-touchspin bootstrap-touchspin-injected"><span class="input-group-addon bootstrap-touchspin-prefix"><span class="input-group-text">' +
                        i.prefix +
                        '</span></span><span class="input-group-addon bootstrap-touchspin-postfix"><span class="input-group-text">' +
                        i.postfix +
                        '</span></span><span class="input-group-btn-vertical"><button class="' +
                        i.buttondown_class +
                        ' bootstrap-touchspin-up ' +
                        i.verticalupclass +
                        '" type="button">' +
                        i.verticalup +
                        '</button><button class="' +
                        i.buttonup_class +
                        ' bootstrap-touchspin-down ' +
                        i.verticaldownclass +
                        '" type="button">' +
                        i.verticaldown +
                        '</button></span></div>'
                      : '<div class="input-group bootstrap-touchspin bootstrap-touchspin-injected"><span class="input-group-btn"><button class="' +
                        i.buttondown_class +
                        ' bootstrap-touchspin-down" type="button">' +
                        i.buttondown_txt +
                        '</button></span><span class="input-group-addon bootstrap-touchspin-prefix"><span class="input-group-text">' +
                        i.prefix +
                        '</span></span><span class="input-group-addon bootstrap-touchspin-postfix"><span class="input-group-text">' +
                        i.postfix +
                        '</span></span><span class="input-group-btn"><button class="' +
                        i.buttonup_class +
                        ' bootstrap-touchspin-up" type="button">' +
                        i.buttonup_txt +
                        '</button></span></div>';
                    (u = D(t).insertBefore(c)),
                      D('.bootstrap-touchspin-prefix', u).after(c),
                      c.hasClass('input-sm')
                        ? u.addClass('input-group-sm')
                        : c.hasClass('input-lg') && u.addClass('input-group-lg');
                  })();
          })(),
          (p = {
            down: D('.bootstrap-touchspin-down', u),
            up: D('.bootstrap-touchspin-up', u),
            input: D('input', u),
            prefix: D('.bootstrap-touchspin-prefix', u).addClass(i.prefix_extraclass),
            postfix: D('.bootstrap-touchspin-postfix', u).addClass(i.postfix_extraclass)
          }),
          b(),
          c.on('keydown.touchspin', function (t) {
            var n = t.keyCode || t.which;
            38 === n
              ? ('up' !== f && (g(), _()), t.preventDefault())
              : 40 === n && ('down' !== f && (m(), w()), t.preventDefault());
          }),
          c.on('keyup.touchspin', function (t) {
            var n = t.keyCode || t.which;
            (38 !== n && 40 !== n) || y();
          }),
          c.on('blur.touchspin', function () {
            h(), c.val(i.callback_after_calculation(c.val()));
          }),
          p.down.on('keydown', function (t) {
            var n = t.keyCode || t.which;
            (32 !== n && 13 !== n) || ('down' !== f && (m(), w()), t.preventDefault());
          }),
          p.down.on('keyup.touchspin', function (t) {
            var n = t.keyCode || t.which;
            (32 !== n && 13 !== n) || y();
          }),
          p.up.on('keydown.touchspin', function (t) {
            var n = t.keyCode || t.which;
            (32 !== n && 13 !== n) || ('up' !== f && (g(), _()), t.preventDefault());
          }),
          p.up.on('keyup.touchspin', function (t) {
            var n = t.keyCode || t.which;
            (32 !== n && 13 !== n) || y();
          }),
          p.down.on('mousedown.touchspin', function (t) {
            p.down.off('touchstart.touchspin'),
              c.is(':disabled') || (m(), w(), t.preventDefault(), t.stopPropagation());
          }),
          p.down.on('touchstart.touchspin', function (t) {
            p.down.off('mousedown.touchspin'), c.is(':disabled') || (m(), w(), t.preventDefault(), t.stopPropagation());
          }),
          p.up.on('mousedown.touchspin', function (t) {
            p.up.off('touchstart.touchspin'), c.is(':disabled') || (g(), _(), t.preventDefault(), t.stopPropagation());
          }),
          p.up.on('touchstart.touchspin', function (t) {
            p.up.off('mousedown.touchspin'), c.is(':disabled') || (g(), _(), t.preventDefault(), t.stopPropagation());
          }),
          p.up.on(
            'mouseup.touchspin mouseout.touchspin touchleave.touchspin touchend.touchspin touchcancel.touchspin',
            function (t) {
              f && (t.stopPropagation(), y());
            }
          ),
          p.down.on(
            'mouseup.touchspin mouseout.touchspin touchleave.touchspin touchend.touchspin touchcancel.touchspin',
            function (t) {
              f && (t.stopPropagation(), y());
            }
          ),
          p.down.on('mousemove.touchspin touchmove.touchspin', function (t) {
            f && (t.stopPropagation(), t.preventDefault());
          }),
          p.up.on('mousemove.touchspin touchmove.touchspin', function (t) {
            f && (t.stopPropagation(), t.preventDefault());
          }),
          c.on('mousewheel.touchspin DOMMouseScroll.touchspin', function (t) {
            if (i.mousewheel && c.is(':focus')) {
              var n = t.originalEvent.wheelDelta || -t.originalEvent.deltaY || -t.originalEvent.detail;
              t.stopPropagation(), t.preventDefault(), (n < 0 ? m : g)();
            }
          }),
          c.on('touchspin.destroy', function () {
            !(function () {
              var t = c.parent();
              y(),
                c.off('.touchspin'),
                t.hasClass('bootstrap-touchspin-injected')
                  ? (c.siblings().remove(), c.unwrap())
                  : (D('.bootstrap-touchspin-injected', t).remove(), t.removeClass('bootstrap-touchspin'));
              c.data('alreadyinitialized', !1);
            })();
          }),
          c.on('touchspin.uponce', function () {
            y(), g();
          }),
          c.on('touchspin.downonce', function () {
            y(), m();
          }),
          c.on('touchspin.startupspin', function () {
            _();
          }),
          c.on('touchspin.startdownspin', function () {
            w();
          }),
          c.on('touchspin.stopspin', function () {
            y();
          }),
          c.on('touchspin.updatesettings', function (t, n) {
            !(function (t) {
              (function (t) {
                if (((i = D.extend({}, i, t)), t.postfix)) {
                  0 === c.parent().find('.bootstrap-touchspin-postfix').length && s.insertAfter(c),
                    c.parent().find('.bootstrap-touchspin-postfix .input-group-text').text(t.postfix);
                }
                if (t.prefix) {
                  0 === c.parent().find('.bootstrap-touchspin-prefix').length && o.insertBefore(c),
                    c.parent().find('.bootstrap-touchspin-prefix .input-group-text').text(t.prefix);
                }
                b();
              })(t),
                h();
              var n = p.input.val();
              '' !== n &&
                ((n = Number(i.callback_before_calculation(p.input.val()))),
                p.input.val(i.callback_after_calculation(Number(n).toFixed(i.decimals))));
            })(n);
          });
      })();
    });
  };
});
