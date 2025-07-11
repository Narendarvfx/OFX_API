/*
 * Copyright (c) 2023.
 * Designed & Developed by Narendar Reddy G, OscarFX Private Limited
 * All rights reserved.
 */

/*!
 SearchPanes 2.0.2
 2019-2022 SpryMedia Ltd - datatables.net/license
*/
var $jscomp = $jscomp || {};
$jscomp.scope = {};
$jscomp.getGlobal = function (l) {
    l = ["object" == typeof globalThis && globalThis, l, "object" == typeof window && window, "object" == typeof self && self, "object" == typeof global && global];
    for (var n = 0; n < l.length; ++n) {
        var k = l[n];
        if (k && k.Math == Math) return k;
    }
    throw Error("Cannot find global object");
};
$jscomp.global = $jscomp.getGlobal(this);
$jscomp.checkEs6ConformanceViaProxy = function () {
    try {
        var l = {},
            n = Object.create(
                new $jscomp.global.Proxy(l, {
                    get: function (k, q, v) {
                        return k == l && "q" == q && v == n;
                    },
                })
            );
        return !0 === n.q;
    } catch (k) {
        return !1;
    }
};
$jscomp.USE_PROXY_FOR_ES6_CONFORMANCE_CHECKS = !1;
$jscomp.ES6_CONFORMANCE = $jscomp.USE_PROXY_FOR_ES6_CONFORMANCE_CHECKS && $jscomp.checkEs6ConformanceViaProxy();
$jscomp.arrayIteratorImpl = function (l) {
    var n = 0;
    return function () {
        return n < l.length ? { done: !1, value: l[n++] } : { done: !0 };
    };
};
$jscomp.arrayIterator = function (l) {
    return { next: $jscomp.arrayIteratorImpl(l) };
};
$jscomp.ASSUME_ES5 = !1;
$jscomp.ASSUME_NO_NATIVE_MAP = !1;
$jscomp.ASSUME_NO_NATIVE_SET = !1;
$jscomp.SIMPLE_FROUND_POLYFILL = !1;
$jscomp.ISOLATE_POLYFILLS = !1;
$jscomp.defineProperty =
    $jscomp.ASSUME_ES5 || "function" == typeof Object.defineProperties
        ? Object.defineProperty
        : function (l, n, k) {
              if (l == Array.prototype || l == Object.prototype) return l;
              l[n] = k.value;
              return l;
          };
$jscomp.IS_SYMBOL_NATIVE = "function" === typeof Symbol && "symbol" === typeof Symbol("x");
$jscomp.TRUST_ES6_POLYFILLS = !$jscomp.ISOLATE_POLYFILLS || $jscomp.IS_SYMBOL_NATIVE;
$jscomp.polyfills = {};
$jscomp.propertyToPolyfillSymbol = {};
$jscomp.POLYFILL_PREFIX = "$jscp$";
var $jscomp$lookupPolyfilledValue = function (l, n) {
    var k = $jscomp.propertyToPolyfillSymbol[n];
    if (null == k) return l[n];
    k = l[k];
    return void 0 !== k ? k : l[n];
};
$jscomp.polyfill = function (l, n, k, q) {
    n && ($jscomp.ISOLATE_POLYFILLS ? $jscomp.polyfillIsolated(l, n, k, q) : $jscomp.polyfillUnisolated(l, n, k, q));
};
$jscomp.polyfillUnisolated = function (l, n, k, q) {
    k = $jscomp.global;
    l = l.split(".");
    for (q = 0; q < l.length - 1; q++) {
        var v = l[q];
        if (!(v in k)) return;
        k = k[v];
    }
    l = l[l.length - 1];
    q = k[l];
    n = n(q);
    n != q && null != n && $jscomp.defineProperty(k, l, { configurable: !0, writable: !0, value: n });
};
$jscomp.polyfillIsolated = function (l, n, k, q) {
    var v = l.split(".");
    l = 1 === v.length;
    q = v[0];
    q = !l && q in $jscomp.polyfills ? $jscomp.polyfills : $jscomp.global;
    for (var B = 0; B < v.length - 1; B++) {
        var C = v[B];
        if (!(C in q)) return;
        q = q[C];
    }
    v = v[v.length - 1];
    k = $jscomp.IS_SYMBOL_NATIVE && "es6" === k ? q[v] : null;
    n = n(k);
    null != n &&
        (l
            ? $jscomp.defineProperty($jscomp.polyfills, v, { configurable: !0, writable: !0, value: n })
            : n !== k &&
              (($jscomp.propertyToPolyfillSymbol[v] = $jscomp.IS_SYMBOL_NATIVE ? $jscomp.global.Symbol(v) : $jscomp.POLYFILL_PREFIX + v),
              (v = $jscomp.propertyToPolyfillSymbol[v]),
              $jscomp.defineProperty(q, v, { configurable: !0, writable: !0, value: n })));
};
$jscomp.initSymbol = function () {};
$jscomp.polyfill(
    "Symbol",
    function (l) {
        if (l) return l;
        var n = function (v, B) {
            this.$jscomp$symbol$id_ = v;
            $jscomp.defineProperty(this, "description", { configurable: !0, writable: !0, value: B });
        };
        n.prototype.toString = function () {
            return this.$jscomp$symbol$id_;
        };
        var k = 0,
            q = function (v) {
                if (this instanceof q) throw new TypeError("Symbol is not a constructor");
                return new n("jscomp_symbol_" + (v || "") + "_" + k++, v);
            };
        return q;
    },
    "es6",
    "es3"
);
$jscomp.initSymbolIterator = function () {};
$jscomp.polyfill(
    "Symbol.iterator",
    function (l) {
        if (l) return l;
        l = Symbol("Symbol.iterator");
        for (var n = "Array Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".split(" "), k = 0; k < n.length; k++) {
            var q = $jscomp.global[n[k]];
            "function" === typeof q &&
                "function" != typeof q.prototype[l] &&
                $jscomp.defineProperty(q.prototype, l, {
                    configurable: !0,
                    writable: !0,
                    value: function () {
                        return $jscomp.iteratorPrototype($jscomp.arrayIteratorImpl(this));
                    },
                });
        }
        return l;
    },
    "es6",
    "es3"
);
$jscomp.initSymbolAsyncIterator = function () {};
$jscomp.iteratorPrototype = function (l) {
    l = { next: l };
    l[Symbol.iterator] = function () {
        return this;
    };
    return l;
};
$jscomp.makeIterator = function (l) {
    var n = "undefined" != typeof Symbol && Symbol.iterator && l[Symbol.iterator];
    return n ? n.call(l) : $jscomp.arrayIterator(l);
};
$jscomp.owns = function (l, n) {
    return Object.prototype.hasOwnProperty.call(l, n);
};
$jscomp.polyfill(
    "WeakMap",
    function (l) {
        function n() {
            if (!l || !Object.seal) return !1;
            try {
                var p = Object.seal({}),
                    u = Object.seal({}),
                    y = new l([
                        [p, 2],
                        [u, 3],
                    ]);
                if (2 != y.get(p) || 3 != y.get(u)) return !1;
                y.delete(p);
                y.set(u, 4);
                return !y.has(p) && 4 == y.get(u);
            } catch (E) {
                return !1;
            }
        }
        function k() {}
        function q(p) {
            var u = typeof p;
            return ("object" === u && null !== p) || "function" === u;
        }
        function v(p) {
            if (!$jscomp.owns(p, C)) {
                var u = new k();
                $jscomp.defineProperty(p, C, { value: u });
            }
        }
        function B(p) {
            if (!$jscomp.ISOLATE_POLYFILLS) {
                var u = Object[p];
                u &&
                    (Object[p] = function (y) {
                        if (y instanceof k) return y;
                        Object.isExtensible(y) && v(y);
                        return u(y);
                    });
            }
        }
        if ($jscomp.USE_PROXY_FOR_ES6_CONFORMANCE_CHECKS) {
            if (l && $jscomp.ES6_CONFORMANCE) return l;
        } else if (n()) return l;
        var C = "$jscomp_hidden_" + Math.random();
        B("freeze");
        B("preventExtensions");
        B("seal");
        var H = 0,
            r = function (p) {
                this.id_ = (H += Math.random() + 1).toString();
                if (p) {
                    p = $jscomp.makeIterator(p);
                    for (var u; !(u = p.next()).done; ) (u = u.value), this.set(u[0], u[1]);
                }
            };
        r.prototype.set = function (p, u) {
            if (!q(p)) throw Error("Invalid WeakMap key");
            v(p);
            if (!$jscomp.owns(p, C)) throw Error("WeakMap key fail: " + p);
            p[C][this.id_] = u;
            return this;
        };
        r.prototype.get = function (p) {
            return q(p) && $jscomp.owns(p, C) ? p[C][this.id_] : void 0;
        };
        r.prototype.has = function (p) {
            return q(p) && $jscomp.owns(p, C) && $jscomp.owns(p[C], this.id_);
        };
        r.prototype.delete = function (p) {
            return q(p) && $jscomp.owns(p, C) && $jscomp.owns(p[C], this.id_) ? delete p[C][this.id_] : !1;
        };
        return r;
    },
    "es6",
    "es3"
);
$jscomp.MapEntry = function () {};
$jscomp.polyfill(
    "Map",
    function (l) {
        function n() {
            if ($jscomp.ASSUME_NO_NATIVE_MAP || !l || "function" != typeof l || !l.prototype.entries || "function" != typeof Object.seal) return !1;
            try {
                var r = Object.seal({ x: 4 }),
                    p = new l($jscomp.makeIterator([[r, "s"]]));
                if ("s" != p.get(r) || 1 != p.size || p.get({ x: 4 }) || p.set({ x: 4 }, "t") != p || 2 != p.size) return !1;
                var u = p.entries(),
                    y = u.next();
                if (y.done || y.value[0] != r || "s" != y.value[1]) return !1;
                y = u.next();
                return y.done || 4 != y.value[0].x || "t" != y.value[1] || !u.next().done ? !1 : !0;
            } catch (E) {
                return !1;
            }
        }
        if ($jscomp.USE_PROXY_FOR_ES6_CONFORMANCE_CHECKS) {
            if (l && $jscomp.ES6_CONFORMANCE) return l;
        } else if (n()) return l;
        var k = new WeakMap(),
            q = function (r) {
                this.data_ = {};
                this.head_ = C();
                this.size = 0;
                if (r) {
                    r = $jscomp.makeIterator(r);
                    for (var p; !(p = r.next()).done; ) (p = p.value), this.set(p[0], p[1]);
                }
            };
        q.prototype.set = function (r, p) {
            r = 0 === r ? 0 : r;
            var u = v(this, r);
            u.list || (u.list = this.data_[u.id] = []);
            u.entry
                ? (u.entry.value = p)
                : ((u.entry = { next: this.head_, previous: this.head_.previous, head: this.head_, key: r, value: p }), u.list.push(u.entry), (this.head_.previous.next = u.entry), (this.head_.previous = u.entry), this.size++);
            return this;
        };
        q.prototype.delete = function (r) {
            r = v(this, r);
            return r.entry && r.list ? (r.list.splice(r.index, 1), r.list.length || delete this.data_[r.id], (r.entry.previous.next = r.entry.next), (r.entry.next.previous = r.entry.previous), (r.entry.head = null), this.size--, !0) : !1;
        };
        q.prototype.clear = function () {
            this.data_ = {};
            this.head_ = this.head_.previous = C();
            this.size = 0;
        };
        q.prototype.has = function (r) {
            return !!v(this, r).entry;
        };
        q.prototype.get = function (r) {
            return (r = v(this, r).entry) && r.value;
        };
        q.prototype.entries = function () {
            return B(this, function (r) {
                return [r.key, r.value];
            });
        };
        q.prototype.keys = function () {
            return B(this, function (r) {
                return r.key;
            });
        };
        q.prototype.values = function () {
            return B(this, function (r) {
                return r.value;
            });
        };
        q.prototype.forEach = function (r, p) {
            for (var u = this.entries(), y; !(y = u.next()).done; ) (y = y.value), r.call(p, y[1], y[0], this);
        };
        q.prototype[Symbol.iterator] = q.prototype.entries;
        var v = function (r, p) {
                var u = p && typeof p;
                "object" == u || "function" == u ? (k.has(p) ? (u = k.get(p)) : ((u = "" + ++H), k.set(p, u))) : (u = "p_" + p);
                var y = r.data_[u];
                if (y && $jscomp.owns(r.data_, u))
                    for (r = 0; r < y.length; r++) {
                        var E = y[r];
                        if ((p !== p && E.key !== E.key) || p === E.key) return { id: u, list: y, index: r, entry: E };
                    }
                return { id: u, list: y, index: -1, entry: void 0 };
            },
            B = function (r, p) {
                var u = r.head_;
                return $jscomp.iteratorPrototype(function () {
                    if (u) {
                        for (; u.head != r.head_; ) u = u.previous;
                        for (; u.next != u.head; ) return (u = u.next), { done: !1, value: p(u) };
                        u = null;
                    }
                    return { done: !0, value: void 0 };
                });
            },
            C = function () {
                var r = {};
                return (r.previous = r.next = r.head = r);
            },
            H = 0;
        return q;
    },
    "es6",
    "es3"
);
$jscomp.findInternal = function (l, n, k) {
    l instanceof String && (l = String(l));
    for (var q = l.length, v = 0; v < q; v++) {
        var B = l[v];
        if (n.call(k, B, v, l)) return { i: v, v: B };
    }
    return { i: -1, v: void 0 };
};
$jscomp.polyfill(
    "Array.prototype.find",
    function (l) {
        return l
            ? l
            : function (n, k) {
                  return $jscomp.findInternal(this, n, k).v;
              };
    },
    "es6",
    "es3"
);
$jscomp.iteratorFromArray = function (l, n) {
    l instanceof String && (l += "");
    var k = 0,
        q = {
            next: function () {
                if (k < l.length) {
                    var v = k++;
                    return { value: n(v, l[v]), done: !1 };
                }
                q.next = function () {
                    return { done: !0, value: void 0 };
                };
                return q.next();
            },
        };
    q[Symbol.iterator] = function () {
        return q;
    };
    return q;
};
$jscomp.polyfill(
    "Array.prototype.keys",
    function (l) {
        return l
            ? l
            : function () {
                  return $jscomp.iteratorFromArray(this, function (n) {
                      return n;
                  });
              };
    },
    "es6",
    "es3"
);
$jscomp.polyfill(
    "Object.is",
    function (l) {
        return l
            ? l
            : function (n, k) {
                  return n === k ? 0 !== n || 1 / n === 1 / k : n !== n && k !== k;
              };
    },
    "es6",
    "es3"
);
$jscomp.polyfill(
    "Array.prototype.includes",
    function (l) {
        return l
            ? l
            : function (n, k) {
                  var q = this;
                  q instanceof String && (q = String(q));
                  var v = q.length;
                  k = k || 0;
                  for (0 > k && (k = Math.max(k + v, 0)); k < v; k++) {
                      var B = q[k];
                      if (B === n || Object.is(B, n)) return !0;
                  }
                  return !1;
              };
    },
    "es7",
    "es3"
);
$jscomp.checkStringArgs = function (l, n, k) {
    if (null == l) throw new TypeError("The 'this' value for String.prototype." + k + " must not be null or undefined");
    if (n instanceof RegExp) throw new TypeError("First argument to String.prototype." + k + " must not be a regular expression");
    return l + "";
};
$jscomp.polyfill(
    "String.prototype.includes",
    function (l) {
        return l
            ? l
            : function (n, k) {
                  return -1 !== $jscomp.checkStringArgs(this, n, "includes").indexOf(n, k || 0);
              };
    },
    "es6",
    "es3"
);
$jscomp.underscoreProtoCanBeSet = function () {
    var l = { a: !0 },
        n = {};
    try {
        return (n.__proto__ = l), n.a;
    } catch (k) {}
    return !1;
};
$jscomp.setPrototypeOf =
    $jscomp.TRUST_ES6_POLYFILLS && "function" == typeof Object.setPrototypeOf
        ? Object.setPrototypeOf
        : $jscomp.underscoreProtoCanBeSet()
        ? function (l, n) {
              l.__proto__ = n;
              if (l.__proto__ !== n) throw new TypeError(l + " is not extensible");
              return l;
          }
        : null;
$jscomp.polyfill(
    "Object.setPrototypeOf",
    function (l) {
        return l || $jscomp.setPrototypeOf;
    },
    "es6",
    "es5"
);
(function () {
    function l(h) {
        k = h;
        q = h.fn.dataTable;
    }
    function n(h) {
        D = h;
        G = h.fn.dataTable;
    }
    var k,
        q,
        v = (function () {
            function h(b, a, c, d, e) {
                var f = this;
                void 0 === e && (e = null);
                if (!q || !q.versionCheck || !q.versionCheck("1.10.0")) throw Error("SearchPane requires DataTables 1.10 or newer");
                if (!q.select) throw Error("SearchPane requires Select");
                b = new q.Api(b);
                this.classes = k.extend(!0, {}, h.classes);
                this.c = k.extend(!0, {}, h.defaults, a);
                a && a.hideCount && void 0 === a.viewCount && (this.c.viewCount = !this.c.hideCount);
                a = b.columns().eq(0).toArray().length;
                this.s = {
                    colExists: c < a,
                    colOpts: void 0,
                    customPaneSettings: e,
                    displayed: !1,
                    dt: b,
                    dtPane: void 0,
                    firstSet: !0,
                    index: c,
                    indexes: [],
                    listSet: !1,
                    name: void 0,
                    rowData: { arrayFilter: [], arrayOriginal: [], bins: {}, binsOriginal: {}, filterMap: new Map(), totalOptions: 0 },
                    scrollTop: 0,
                    searchFunction: void 0,
                    selections: [],
                    serverSelect: [],
                    serverSelecting: !1,
                    tableLength: null,
                    updating: !1,
                };
                this.s.colOpts = this.s.colExists ? this._getOptions() : this._getBonusOptions();
                this.dom = {
                    buttonGroup: k("<div/>").addClass(this.classes.buttonGroup),
                    clear: k('<button type="button">&#215;</button>')
                        .attr("disabled", "true")
                        .addClass(this.classes.disabledButton)
                        .addClass(this.classes.paneButton)
                        .addClass(this.classes.clearButton)
                        .html(this.s.dt.i18n("searchPanes.clearPane", this.c.i18n.clearPane)),
                    collapseButton: k('<button type="button"><span class="' + this.classes.caret + '">&#x5e;</span></button>')
                        .addClass(this.classes.paneButton)
                        .addClass(this.classes.collapseButton),
                    container: k("<div/>")
                        .addClass(this.classes.container)
                        .addClass(this.s.colOpts.className)
                        .addClass(this.classes.layout + (10 > parseInt(this.c.layout.split("-")[1], 10) ? this.c.layout : this.c.layout.split("-")[0] + "-9"))
                        .addClass(this.s.customPaneSettings && this.s.customPaneSettings.className ? this.s.customPaneSettings.className : ""),
                    countButton: k('<button type="button"></button>').addClass(this.classes.paneButton).addClass(this.classes.countButton),
                    dtP: k("<table><thead><tr><th>" + (this.s.colExists ? k(this.s.dt.column(this.s.index).header()).text() : this.s.customPaneSettings.header || "Custom Pane") + "</th><th/></tr></thead></table>"),
                    lower: k("<div/>").addClass(this.classes.subRow2).addClass(this.classes.narrowButton),
                    nameButton: k('<button type="button"></button>').addClass(this.classes.paneButton).addClass(this.classes.nameButton),
                    panesContainer: d,
                    searchBox: k("<input/>").addClass(this.classes.paneInputButton).addClass(this.classes.search),
                    searchButton: k('<button type = "button"/>').addClass(this.classes.searchIcon).addClass(this.classes.paneButton),
                    searchCont: k("<div/>").addClass(this.classes.searchCont),
                    searchLabelCont: k("<div/>").addClass(this.classes.searchLabelCont),
                    topRow: k("<div/>").addClass(this.classes.topRow),
                    upper: k("<div/>").addClass(this.classes.subRow1).addClass(this.classes.narrowSearch),
                };
                this.s.name = this.s.colOpts.name
                    ? this.s.colOpts.name
                    : this.s.customPaneSettings && this.s.customPaneSettings.name
                    ? this.s.customPaneSettings.name
                    : this.s.colExists
                    ? k(this.s.dt.column(this.s.index).header()).text()
                    : this.s.customPaneSettings.header || "Custom Pane";
                var g = this.s.dt.table(0).node();
                this.s.searchFunction = function (m, t, w) {
                    if (0 === f.s.selections.length || m.nTable !== g) return !0;
                    m = null;
                    f.s.colExists && ((m = t[f.s.index]), "filter" !== f.s.colOpts.orthogonal.filter && ((m = f.s.rowData.filterMap.get(w)), m instanceof k.fn.dataTable.Api && (m = m.toArray())));
                    return f._search(m, w);
                };
                k.fn.dataTable.ext.search.push(this.s.searchFunction);
                if (this.c.clear)
                    this.dom.clear.on("click.dtsp", function () {
                        f.dom.container.find("." + f.classes.search.replace(/\s+/g, ".")).each(function () {
                            k(this).val("").trigger("input");
                        });
                        f.clearPane();
                    });
                this.s.dt.on("draw.dtsp", function () {
                    return f.adjustTopRow();
                });
                this.s.dt.on("buttons-action.dtsp", function () {
                    return f.adjustTopRow();
                });
                this.s.dt.on("column-reorder.dtsp", function (m, t, w) {
                    f.s.index = w.mapping[f.s.index];
                });
                return this;
            }
            h.prototype.addRow = function (b, a, c, d, e, f, g) {
                f || (f = this.s.rowData.bins[a] ? this.s.rowData.bins[a] : 0);
                g || (g = this._getShown(a));
                for (var m, t = 0, w = this.s.indexes; t < w.length; t++) {
                    var A = w[t];
                    A.filter === a && (m = A.index);
                }
                void 0 === m && ((m = this.s.indexes.length), this.s.indexes.push({ filter: a, index: m }));
                return this.s.dtPane.row.add({ className: e, display: "" !== b ? b : this.emptyMessage(), filter: a, index: m, shown: g, sort: c, total: f, type: d });
            };
            h.prototype.adjustTopRow = function () {
                var b = this.dom.container.find("." + this.classes.subRowsContainer.replace(/\s+/g, ".")),
                    a = this.dom.container.find("." + this.classes.subRow1.replace(/\s+/g, ".")),
                    c = this.dom.container.find("." + this.classes.subRow2.replace(/\s+/g, ".")),
                    d = this.dom.container.find("." + this.classes.topRow.replace(/\s+/g, "."));
                (252 > k(b[0]).width() || 252 > k(d[0]).width()) && 0 !== k(b[0]).width()
                    ? (k(b[0]).addClass(this.classes.narrow), k(a[0]).addClass(this.classes.narrowSub).removeClass(this.classes.narrowSearch), k(c[0]).addClass(this.classes.narrowSub).removeClass(this.classes.narrowButton))
                    : (k(b[0]).removeClass(this.classes.narrow), k(a[0]).removeClass(this.classes.narrowSub).addClass(this.classes.narrowSearch), k(c[0]).removeClass(this.classes.narrowSub).addClass(this.classes.narrowButton));
            };
            h.prototype.clearData = function () {
                this.s.rowData = { arrayFilter: [], arrayOriginal: [], bins: {}, binsOriginal: {}, filterMap: new Map(), totalOptions: 0 };
            };
            h.prototype.clearPane = function () {
                this.s.dtPane.rows({ selected: !0 }).deselect();
                this.updateTable();
                return this;
            };
            h.prototype.collapse = function () {
                var b = this;
                this.s.displayed &&
                    (this.c.collapse || !0 === this.s.colOpts.collapse) &&
                    !1 !== this.s.colOpts.collapse &&
                    (k(this.s.dtPane.table().container()).addClass(this.classes.hidden),
                    this.dom.topRow.addClass(this.classes.bordered),
                    this.dom.nameButton.addClass(this.classes.disabledButton),
                    this.dom.countButton.addClass(this.classes.disabledButton),
                    this.dom.searchButton.addClass(this.classes.disabledButton),
                    this.dom.collapseButton.addClass(this.classes.rotated),
                    this.dom.topRow.one("click.dtsp", function () {
                        return b.show();
                    }));
            };
            h.prototype.destroy = function () {
                this.s.dtPane && this.s.dtPane.off(".dtsp");
                this.s.dt.off(".dtsp");
                this.dom.clear.off(".dtsp");
                this.dom.nameButton.off(".dtsp");
                this.dom.countButton.off(".dtsp");
                this.dom.searchButton.off(".dtsp");
                this.dom.collapseButton.off(".dtsp");
                k(this.s.dt.table().node()).off(".dtsp");
                this.dom.container.detach();
                for (var b = k.fn.dataTable.ext.search.indexOf(this.s.searchFunction); -1 !== b; ) k.fn.dataTable.ext.search.splice(b, 1), (b = k.fn.dataTable.ext.search.indexOf(this.s.searchFunction));
                this.s.dtPane && this.s.dtPane.destroy();
                this.s.listSet = !1;
            };
            h.prototype.emptyMessage = function () {
                var b = this.c.i18n.emptyMessage;
                this.c.emptyMessage && (b = this.c.emptyMessage);
                !1 !== this.s.colOpts.emptyMessage && null !== this.s.colOpts.emptyMessage && (b = this.s.colOpts.emptyMessage);
                return this.s.dt.i18n("searchPanes.emptyMessage", b);
            };
            h.prototype.getPaneCount = function () {
                return this.s.dtPane ? this.s.dtPane.rows({ selected: !0 }).data().toArray().length : 0;
            };
            h.prototype.rebuildPane = function (b, a) {
                void 0 === b && (b = null);
                void 0 === a && (a = !1);
                this.clearData();
                var c = [];
                this.s.serverSelect = [];
                var d = null;
                this.s.dtPane &&
                    (a && (this.s.dt.page.info().serverSide ? (this.s.serverSelect = this.s.dtPane.rows({ selected: !0 }).data().toArray()) : (c = this.s.dtPane.rows({ selected: !0 }).data().toArray())),
                    this.s.dtPane.clear().destroy(),
                    (d = this.dom.container.prev()),
                    this.destroy(),
                    (this.s.dtPane = void 0),
                    k.fn.dataTable.ext.search.push(this.s.searchFunction));
                this.dom.container.removeClass(this.classes.hidden);
                this.s.displayed = !1;
                this._buildPane(this.s.dt.page.info().serverSide ? this.s.serverSelect : c, b, d);
                return this;
            };
            h.prototype.resize = function (b) {
                this.c.layout = b;
                this.dom.container
                    .removeClass()
                    .addClass(this.classes.show)
                    .addClass(this.classes.container)
                    .addClass(this.s.colOpts.className)
                    .addClass(this.classes.layout + (10 > parseInt(b.split("-")[1], 10) ? b : b.split("-")[0] + "-9"))
                    .addClass(null !== this.s.customPaneSettings && this.s.customPaneSettings.className ? this.s.customPaneSettings.className : "");
                this.adjustTopRow();
            };
            h.prototype.setListeners = function () {
                var b = this;
                this.s.dtPane &&
                    (this.s.dtPane.select.style(
                        this.s.colOpts.dtOpts && this.s.colOpts.dtOpts.select && this.s.colOpts.dtOpts.select.style
                            ? this.s.colOpts.dtOpts.select.style
                            : this.c.dtOpts && this.c.dtOpts.select && this.c.dtOpts.select.style
                            ? this.c.dtOpts.select.style
                            : "os"
                    ),
                    this.s.dtPane.off("select.dtsp").on("select.dtsp", function () {
                        clearTimeout(b.s.deselectTimeout);
                        b._updateSelection(!b.s.updating);
                        b.dom.clear.removeClass(b.classes.disabledButton).removeAttr("disabled");
                    }),
                    this.s.dtPane.off("deselect.dtsp").on("deselect.dtsp", function () {
                        b.s.deselectTimeout = setTimeout(function () {
                            b._updateSelection(!0);
                            0 === b.s.dtPane.rows({ selected: !0 }).data().toArray().length && b.dom.clear.addClass(b.classes.disabledButton).attr("disabled", "true");
                        }, 50);
                    }),
                    this.s.firstSet &&
                        ((this.s.firstSet = !1),
                        this.s.dt.on("stateSaveParams.dtsp", function (a, c, d) {
                            if (k.isEmptyObject(d)) b.s.dtPane.state.clear();
                            else {
                                a = [];
                                if (b.s.dtPane) {
                                    a = b.s.dtPane
                                        .rows({ selected: !0 })
                                        .data()
                                        .map(function (w) {
                                            return w.filter.toString();
                                        })
                                        .toArray();
                                    var e = b.dom.searchBox.val();
                                    var f = b.s.dtPane.order();
                                    var g = b.s.rowData.binsOriginal;
                                    var m = b.s.rowData.arrayOriginal;
                                    var t = b.dom.collapseButton.hasClass(b.classes.rotated);
                                }
                                void 0 === d.searchPanes && (d.searchPanes = {});
                                void 0 === d.searchPanes.panes && (d.searchPanes.panes = []);
                                for (c = 0; c < d.searchPanes.panes.length; c++) d.searchPanes.panes[c].id === b.s.index && (d.searchPanes.panes.splice(c, 1), c--);
                                d.searchPanes.panes.push({ arrayFilter: m, bins: g, collapsed: t, id: b.s.index, order: f, searchTerm: e, selected: a });
                            }
                        })),
                    this.s.dtPane.off("user-select.dtsp").on("user-select.dtsp", function (a, c, d, e, f) {
                        f.stopPropagation();
                    }),
                    this.s.dtPane.off("draw.dtsp").on("draw.dtsp", function () {
                        return b.adjustTopRow();
                    }),
                    this.dom.nameButton.off("click.dtsp").on("click.dtsp", function () {
                        var a = b.s.dtPane.order()[0][1];
                        b.s.dtPane.order([0, "asc" === a ? "desc" : "asc"]).draw();
                        b.s.dt.state.save();
                    }),
                    this.dom.countButton.off("click.dtsp").on("click.dtsp", function () {
                        var a = b.s.dtPane.order()[0][1];
                        b.s.dtPane.order([1, "asc" === a ? "desc" : "asc"]).draw();
                        b.s.dt.state.save();
                    }),
                    this.dom.collapseButton.off("click.dtsp").on("click.dtsp", function (a) {
                        a.stopPropagation();
                        a = k(b.s.dtPane.table().container());
                        a.toggleClass(b.classes.hidden);
                        b.dom.topRow.toggleClass(b.classes.bordered);
                        b.dom.nameButton.toggleClass(b.classes.disabledButton);
                        b.dom.countButton.toggleClass(b.classes.disabledButton);
                        b.dom.searchButton.toggleClass(b.classes.disabledButton);
                        b.dom.collapseButton.toggleClass(b.classes.rotated);
                        if (a.hasClass(b.classes.hidden))
                            b.dom.topRow.on("click.dtsp", function () {
                                return b.dom.collapseButton.click();
                            });
                        else b.dom.topRow.off("click.dtsp");
                        b.s.dt.state.save();
                    }),
                    this.dom.clear.off("click.dtsp").on("click.dtsp", function () {
                        b.dom.container.find("." + b.classes.search.replace(/ /g, ".")).each(function () {
                            k(this).val("").trigger("input");
                        });
                        b.clearPane();
                    }),
                    this.dom.searchButton.off("click.dtsp").on("click.dtsp", function () {
                        return b.dom.searchBox.focus();
                    }),
                    this.dom.searchBox.off("click.dtsp").on("input.dtsp", function () {
                        var a = b.dom.searchBox.val();
                        b.s.dtPane.search(a).draw();
                        "string" === typeof a && (0 < a.length || (0 === a.length && 0 < b.s.dtPane.rows({ selected: !0 }).data().toArray().length))
                            ? b.dom.clear.removeClass(b.classes.disabledButton).removeAttr("disabled")
                            : b.dom.clear.addClass(b.classes.disabledButton).attr("disabled", "true");
                        b.s.dt.state.save();
                    }),
                    this.s.dtPane.select.style(
                        this.s.colOpts.dtOpts && this.s.colOpts.dtOpts.select && this.s.colOpts.dtOpts.select.style
                            ? this.s.colOpts.dtOpts.select.style
                            : this.c.dtOpts && this.c.dtOpts.select && this.c.dtOpts.select.style
                            ? this.c.dtOpts.select.style
                            : "os"
                    ));
            };
            h.prototype._serverPopulate = function (b) {
                if (b.tableLength) (this.s.tableLength = b.tableLength), (this.s.rowData.totalOptions = this.s.tableLength);
                else if (null === this.s.tableLength || this.s.dt.rows()[0].length > this.s.tableLength) (this.s.tableLength = this.s.dt.rows()[0].length), (this.s.rowData.totalOptions = this.s.tableLength);
                var a = this.s.dt.column(this.s.index).dataSrc();
                if (b.searchPanes.options[a]) {
                    var c = 0;
                    for (b = b.searchPanes.options[a]; c < b.length; c++) (a = b[c]), this.s.rowData.arrayFilter.push({ display: a.label, filter: a.value, sort: a.label, type: a.label }), (this.s.rowData.bins[a.value] = a.total);
                }
                c = Object.keys(this.s.rowData.bins).length;
                b = this._uniqueRatio(c, this.s.tableLength);
                !1 === this.s.displayed && ((void 0 === this.s.colOpts.show && null === this.s.colOpts.threshold ? b > this.c.threshold : b > this.s.colOpts.threshold) || (!0 !== this.s.colOpts.show && 1 >= c))
                    ? (this.dom.container.addClass(this.classes.hidden), (this.s.displayed = !1))
                    : ((this.s.rowData.arrayOriginal = this.s.rowData.arrayFilter), (this.s.rowData.binsOriginal = this.s.rowData.bins), (this.s.displayed = !0));
            };
            h.prototype.show = function () {
                this.s.displayed &&
                    (this.dom.topRow.removeClass(this.classes.bordered),
                    this.dom.nameButton.removeClass(this.classes.disabledButton),
                    this.dom.countButton.removeClass(this.classes.disabledButton),
                    this.dom.searchButton.removeClass(this.classes.disabledButton),
                    this.dom.collapseButton.removeClass(this.classes.rotated),
                    k(this.s.dtPane.table().container()).removeClass(this.classes.hidden));
            };
            h.prototype._uniqueRatio = function (b, a) {
                return 0 < a && ((0 < this.s.rowData.totalOptions && !this.s.dt.page.info().serverSide) || (this.s.dt.page.info().serverSide && 0 < this.s.tableLength)) ? b / this.s.rowData.totalOptions : 1;
            };
            h.prototype.updateTable = function () {
                var b = this.s.dtPane
                    .rows({ selected: !0 })
                    .data()
                    .toArray()
                    .map(function (a) {
                        return a.filter;
                    });
                this.s.selections = b;
                this._searchExtras();
            };
            h.prototype._getComparisonRows = function () {
                var b = this.s.colOpts.options ? this.s.colOpts.options : this.s.customPaneSettings && this.s.customPaneSettings.options ? this.s.customPaneSettings.options : void 0;
                if (void 0 !== b) {
                    var a = this.s.dt.rows(),
                        c = a.data().toArray(),
                        d = [];
                    this.s.dtPane.clear();
                    this.s.indexes = [];
                    for (var e = 0; e < b.length; e++) {
                        var f = b[e],
                            g = "" !== f.label ? f.label : this.emptyMessage(),
                            m = f.className,
                            t = g,
                            w = "function" === typeof f.value ? f.value : [],
                            A = g,
                            z = 0;
                        if ("function" === typeof f.value) {
                            for (var x = 0; x < c.length; x++) f.value.call(this.s.dt, c[x], a[0][x]) && z++;
                            "function" !== typeof w && w.push(f.filter);
                        }
                        d.push(this.addRow(t, w, A, g, m, z));
                    }
                    return d;
                }
            };
            h.prototype._getMessage = function (b) {
                return this.s.dt.i18n("searchPanes.count", this.c.i18n.count).replace(/{total}/g, b.total);
            };
            h.prototype._getShown = function (b) {};
            h.prototype._getPaneConfig = function () {
                var b = this,
                    a = q.Scroller,
                    c = this.s.dt.settings()[0].oLanguage;
                c.url = void 0;
                c.sUrl = void 0;
                return {
                    columnDefs: [
                        {
                            className: "dtsp-nameColumn",
                            data: "display",
                            render: function (d, e, f) {
                                if ("sort" === e) return f.sort;
                                if ("type" === e) return f.type;
                                f = b._getMessage(f);
                                f = '<span class="' + b.classes.pill + '">' + f + "</span>";
                                (b.c.viewCount && b.s.colOpts.viewCount) || (f = "");
                                return "filter" === e
                                    ? "string" === typeof d && null !== d.match(/<[^>]*>/)
                                        ? d.replace(/<[^>]*>/g, "")
                                        : d
                                    : '<div class="' +
                                          b.classes.nameCont +
                                          '"><span title="' +
                                          ("string" === typeof d && null !== d.match(/<[^>]*>/) ? d.replace(/<[^>]*>/g, "") : d) +
                                          '" class="' +
                                          b.classes.name +
                                          '">' +
                                          d +
                                          "</span>" +
                                          f +
                                          "</div>";
                            },
                            targets: 0,
                            type: this.s.dt.settings()[0].aoColumns[this.s.index] ? this.s.dt.settings()[0].aoColumns[this.s.index]._sManualType : null,
                        },
                        { className: "dtsp-countColumn " + this.classes.badgePill, data: "total", searchable: !1, targets: 1, visible: !1 },
                    ],
                    deferRender: !0,
                    dom: "t",
                    info: !1,
                    language: c,
                    paging: a ? !0 : !1,
                    scrollX: !1,
                    scrollY: "200px",
                    scroller: a ? !0 : !1,
                    select: !0,
                    stateSave: this.s.dt.settings()[0].oFeatures.bStateSave ? !0 : !1,
                };
            };
            h.prototype._makeSelection = function () {
                this.updateTable();
                this.s.updating = !0;
                this.s.dt.draw();
                this.s.updating = !1;
            };
            h.prototype._populatePaneArray = function (b, a, c, d) {
                void 0 === d && (d = this.s.rowData.bins);
                if ("string" === typeof this.s.colOpts.orthogonal) (c = c.oApi._fnGetCellData(c, b, this.s.index, this.s.colOpts.orthogonal)), this.s.rowData.filterMap.set(b, c), this._addOption(c, c, c, c, a, d);
                else {
                    var e = c.oApi._fnGetCellData(c, b, this.s.index, this.s.colOpts.orthogonal.search);
                    null === e && (e = "");
                    "string" === typeof e && (e = e.replace(/<[^>]*>/g, ""));
                    this.s.rowData.filterMap.set(b, e);
                    d[e]
                        ? d[e]++
                        : ((d[e] = 1),
                          this._addOption(
                              e,
                              c.oApi._fnGetCellData(c, b, this.s.index, this.s.colOpts.orthogonal.display),
                              c.oApi._fnGetCellData(c, b, this.s.index, this.s.colOpts.orthogonal.sort),
                              c.oApi._fnGetCellData(c, b, this.s.index, this.s.colOpts.orthogonal.type),
                              a,
                              d
                          ));
                }
                this.s.rowData.totalOptions++;
            };
            h.prototype._reloadSelect = function (b) {
                if (void 0 !== b) {
                    for (var a, c = 0; c < b.searchPanes.panes.length; c++)
                        if (b.searchPanes.panes[c].id === this.s.index) {
                            a = c;
                            break;
                        }
                    if (a) {
                        c = this.s.dtPane;
                        var d = c
                                .rows({ order: "index" })
                                .data()
                                .map(function (g) {
                                    return null !== g.filter ? g.filter.toString() : null;
                                })
                                .toArray(),
                            e = 0;
                        for (b = b.searchPanes.panes[a].selected; e < b.length; e++) {
                            a = b[e];
                            var f = -1;
                            null !== a && (f = d.indexOf(a.toString()));
                            -1 < f && ((this.s.serverSelecting = !0), c.row(f).select(), (this.s.serverSelecting = !1));
                        }
                    }
                }
            };
            h.prototype._updateSelection = function (b) {
                this.s.scrollTop = k(this.s.dtPane.table().node()).parent()[0].scrollTop;
                this.s.dt.page.info().serverSide && !this.s.updating ? this.s.serverSelecting || ((this.s.serverSelect = this.s.dtPane.rows({ selected: !0 }).data().toArray()), this.s.dt.draw(!1)) : b && this._makeSelection();
            };
            h.prototype._addOption = function (b, a, c, d, e, f) {
                if (Array.isArray(b) || b instanceof q.Api)
                    if ((b instanceof q.Api && ((b = b.toArray()), (a = a.toArray())), b.length === a.length))
                        for (var g = 0; g < b.length; g++) f[b[g]] ? f[b[g]]++ : ((f[b[g]] = 1), e.push({ display: a[g], filter: b[g], sort: c[g], type: d[g] })), this.s.rowData.totalOptions++;
                    else throw Error("display and filter not the same length");
                else "string" === typeof this.s.colOpts.orthogonal ? (f[b] ? f[b]++ : ((f[b] = 1), e.push({ display: a, filter: b, sort: c, type: d })), this.s.rowData.totalOptions++) : e.push({ display: a, filter: b, sort: c, type: d });
            };
            h.prototype._buildPane = function (b, a, c) {
                var d = this;
                void 0 === b && (b = []);
                void 0 === a && (a = null);
                void 0 === c && (c = null);
                this.s.selections = [];
                var e = this.s.dt.state.loaded();
                this.s.listSet && (e = this.s.dt.state());
                if (this.s.colExists) {
                    var f = -1;
                    if (e && e.searchPanes && e.searchPanes.panes)
                        for (var g = 0; g < e.searchPanes.panes.length; g++)
                            if (e.searchPanes.panes[g].id === this.s.index) {
                                f = g;
                                break;
                            }
                    if ((!1 === this.s.colOpts.show || (void 0 !== this.s.colOpts.show && !0 !== this.s.colOpts.show)) && -1 === f) return this.dom.container.addClass(this.classes.hidden), (this.s.displayed = !1);
                    if (!0 === this.s.colOpts.show || -1 !== f) this.s.displayed = !0;
                    if (this.s.dt.page.info().serverSide || (a && a.searchPanes && a.searchPanes.options)) a && a.searchPanes && a.searchPanes.options && this._serverPopulate(a);
                    else {
                        0 === this.s.rowData.arrayFilter.length && ((this.s.rowData.totalOptions = 0), this._populatePane(), (this.s.rowData.arrayOriginal = this.s.rowData.arrayFilter), (this.s.rowData.binsOriginal = this.s.rowData.bins));
                        g = Object.keys(this.s.rowData.binsOriginal).length;
                        f = this._uniqueRatio(g, this.s.dt.rows()[0].length);
                        if (!1 === this.s.displayed && ((void 0 === this.s.colOpts.show && null === this.s.colOpts.threshold ? f > this.c.threshold : f > this.s.colOpts.threshold) || (!0 !== this.s.colOpts.show && 1 >= g))) {
                            this.dom.container.addClass(this.classes.hidden);
                            this.s.displayed = !1;
                            return;
                        }
                        this.dom.container.addClass(this.classes.show);
                        this.s.displayed = !0;
                    }
                } else this.s.displayed = !0;
                this._displayPane();
                if (!this.s.listSet)
                    this.dom.dtP.on("stateLoadParams.dtsp", function (w, A, z) {
                        k.isEmptyObject(d.s.dt.state.loaded()) &&
                            k.each(z, function (x) {
                                delete z[x];
                            });
                    });
                null !== c && 0 < this.dom.panesContainer.has(c).length ? this.dom.container.insertAfter(c) : this.dom.panesContainer.prepend(this.dom.container);
                c = k.fn.dataTable.ext.errMode;
                k.fn.dataTable.ext.errMode = "none";
                this.s.dtPane = this.dom.dtP.DataTable(
                    k.extend(
                        !0,
                        this._getPaneConfig(),
                        this.c.dtOpts,
                        this.s.colOpts ? this.s.colOpts.dtOpts : {},
                        this.s.colOpts.options || !this.s.colExists
                            ? {
                                  createdRow: function (w, A) {
                                      k(w).addClass(A.className);
                                  },
                              }
                            : void 0,
                        null !== this.s.customPaneSettings && this.s.customPaneSettings.dtOpts ? this.s.customPaneSettings.dtOpts : {},
                        k.fn.dataTable.versionCheck("2") ? { layout: { bottomLeft: null, bottomRight: null, topLeft: null, topRight: null } } : {}
                    )
                );
                this.dom.dtP.addClass(this.classes.table);
                g = "Custom Pane";
                this.s.customPaneSettings && this.s.customPaneSettings.header
                    ? (g = this.s.customPaneSettings.header)
                    : this.s.colOpts.header
                    ? (g = this.s.colOpts.header)
                    : this.s.colExists && (g = k.fn.dataTable.versionCheck("2") ? this.s.dt.column(this.s.index).title() : this.s.dt.settings()[0].aoColumns[this.s.index].sTitle);
                g = this._escapeHTML(g);
                this.dom.searchBox.attr("placeholder", g);
                k.fn.dataTable.select.init(this.s.dtPane);
                k.fn.dataTable.ext.errMode = c;
                if (this.s.colExists)
                    for (g = 0, f = this.s.rowData.arrayFilter.length; g < f; g++)
                        if (this.s.dt.page.info().serverSide) {
                            c = this.addRow(this.s.rowData.arrayFilter[g].display, this.s.rowData.arrayFilter[g].filter, this.s.rowData.arrayFilter[g].sort, this.s.rowData.arrayFilter[g].type);
                            for (var m = 0, t = this.s.serverSelect; m < t.length; m++) t[m].filter === this.s.rowData.arrayFilter[g].filter && ((this.s.serverSelecting = !0), c.select(), (this.s.serverSelecting = !1));
                        } else
                            !this.s.dt.page.info().serverSide && this.s.rowData.arrayFilter[g]
                                ? this.addRow(this.s.rowData.arrayFilter[g].display, this.s.rowData.arrayFilter[g].filter, this.s.rowData.arrayFilter[g].sort, this.s.rowData.arrayFilter[g].type)
                                : this.s.dt.page.info().serverSide || this.addRow("", "", "", "");
                q.select.init(this.s.dtPane);
                (this.s.colOpts.options || (this.s.customPaneSettings && this.s.customPaneSettings.options)) && this._getComparisonRows();
                this.s.dtPane.draw();
                this.s.dtPane.table().node().parentNode.scrollTop = this.s.scrollTop;
                this.adjustTopRow();
                this.setListeners();
                this.s.listSet = !0;
                for (g = 0; g < b.length; g++)
                    if ((f = b[g]))
                        for (m = 0, t = this.s.dtPane.rows().indexes().toArray(); m < t.length; m++)
                            (c = t[m]),
                                this.s.dtPane.row(c).data() &&
                                    f.filter === this.s.dtPane.row(c).data().filter &&
                                    (this.s.dt.page.info().serverSide ? ((this.s.serverSelecting = !0), this.s.dtPane.row(c).select(), (this.s.serverSelecting = !1)) : this.s.dtPane.row(c).select());
                this.s.dt.page.info().serverSide && this.s.dtPane.search(this.dom.searchBox.val()).draw();
                if (((this.c.initCollapsed && !1 !== this.s.colOpts.initCollapsed) || this.s.colOpts.initCollapsed) && ((this.c.collapse && !1 !== this.s.colOpts.collapse) || this.s.colOpts.collapse))
                    if (this.s.dtPane.settings()[0]._bInitComplete) this.collapse();
                    else
                        this.s.dtPane.one("init", function () {
                            return d.collapse();
                        });
                if (e && e.searchPanes && e.searchPanes.panes && (!a || 1 === a.draw))
                    for (this._reloadSelect(e), a = 0, e = e.searchPanes.panes; a < e.length; a++)
                        (b = e[a]),
                            b.id === this.s.index &&
                                (b.searchTerm && 0 < b.searchTerm.length && this.dom.searchBox.val(b.searchTerm).trigger("input"), b.order && this.s.dtPane.order(b.order).draw(), b.collapsed ? this.collapse() : this.show());
                return !0;
            };
            h.prototype._displayPane = function () {
                this.dom.dtP.empty();
                this.dom.topRow.empty().addClass(this.classes.topRow);
                3 < parseInt(this.c.layout.split("-")[1], 10) && this.dom.container.addClass(this.classes.smallGap);
                this.dom.topRow.addClass(this.classes.subRowsContainer).append(this.dom.upper.append(this.dom.searchCont)).append(this.dom.lower.append(this.dom.buttonGroup));
                (!1 === this.c.dtOpts.searching ||
                    (this.s.colOpts.dtOpts && !1 === this.s.colOpts.dtOpts.searching) ||
                    !this.c.controls ||
                    !this.s.colOpts.controls ||
                    (this.s.customPaneSettings && this.s.customPaneSettings.dtOpts && void 0 !== this.s.customPaneSettings.dtOpts.searching && !this.s.customPaneSettings.dtOpts.searching)) &&
                    this.dom.searchBox.removeClass(this.classes.paneInputButton).addClass(this.classes.disabledButton).attr("disabled", "true");
                this.dom.searchBox.appendTo(this.dom.searchCont);
                this._searchContSetup();
                this.c.clear && this.c.controls && this.s.colOpts.controls && this.dom.clear.appendTo(this.dom.buttonGroup);
                this.c.orderable && this.s.colOpts.orderable && this.c.controls && this.s.colOpts.controls && this.dom.nameButton.appendTo(this.dom.buttonGroup);
                this.c.viewCount && this.s.colOpts.viewCount && this.c.orderable && this.s.colOpts.orderable && this.c.controls && this.s.colOpts.controls && this.dom.countButton.appendTo(this.dom.buttonGroup);
                ((this.c.collapse && !1 !== this.s.colOpts.collapse) || this.s.colOpts.collapse) && this.c.controls && this.s.colOpts.controls && this.dom.collapseButton.appendTo(this.dom.buttonGroup);
                this.dom.container.prepend(this.dom.topRow).append(this.dom.dtP).show();
            };
            h.prototype._escapeHTML = function (b) {
                return b
                    .toString()
                    .replace(/&amp;/g, "&")
                    .replace(/&lt;/g, "<")
                    .replace(/&gt;/g, ">")
                    .replace(/&quot;/g, '"');
            };
            h.prototype._getBonusOptions = function () {
                return k.extend(!0, {}, h.defaults, { threshold: null }, this.c ? this.c : {});
            };
            h.prototype._getOptions = function () {
                var b = this.s.dt.settings()[0].aoColumns[this.s.index].searchPanes,
                    a = k.extend(!0, {}, h.defaults, { collapse: null, emptyMessage: !1, initCollapsed: null, threshold: null }, b);
                b && b.hideCount && void 0 === b.viewCount && (a.viewCount = !b.hideCount);
                return a;
            };
            h.prototype._populatePane = function () {
                this.s.rowData.arrayFilter = [];
                this.s.rowData.bins = {};
                var b = this.s.dt.settings()[0];
                if (!this.s.dt.page.info().serverSide) for (var a = 0, c = this.s.dt.rows().indexes().toArray(); a < c.length; a++) this._populatePaneArray(c[a], this.s.rowData.arrayFilter, b);
            };
            h.prototype._search = function (b, a) {
                for (var c = this.s.colOpts, d = this.s.dt, e = 0, f = this.s.selections; e < f.length; e++) {
                    var g = f[e];
                    "string" === typeof g && "string" === typeof b && (g = this._escapeHTML(g));
                    if (Array.isArray(b))
                        if ("and" === c.combiner) {
                            if (!b.includes(g)) return !1;
                        } else {
                            if (b.includes(g)) return !0;
                        }
                    else if ("function" === typeof g)
                        if (g.call(d, d.row(a).data(), a)) {
                            if ("or" === c.combiner) return !0;
                        } else {
                            if ("and" === c.combiner) return !1;
                        }
                    else if (b === g || (("string" !== typeof b || 0 !== b.length) && b == g) || (null === g && "string" === typeof b && "" === b)) return !0;
                }
                return "and" === c.combiner ? !0 : !1;
            };
            h.prototype._searchContSetup = function () {
                this.c.controls && this.s.colOpts.controls && this.dom.searchButton.appendTo(this.dom.searchLabelCont);
                !1 === this.c.dtOpts.searching ||
                    !1 === this.s.colOpts.dtOpts.searching ||
                    (this.s.customPaneSettings && this.s.customPaneSettings.dtOpts && void 0 !== this.s.customPaneSettings.dtOpts.searching && !this.s.customPaneSettings.dtOpts.searching) ||
                    this.dom.searchLabelCont.appendTo(this.dom.searchCont);
            };
            h.prototype._searchExtras = function () {
                var b = this.s.updating;
                this.s.updating = !0;
                var a = this.s.dtPane.rows({ selected: !0 }).data().pluck("filter").toArray(),
                    c = a.indexOf(this.emptyMessage()),
                    d = k(this.s.dtPane.table().container());
                -1 < c && (a[c] = "");
                0 < a.length ? d.addClass(this.classes.selected) : 0 === a.length && d.removeClass(this.classes.selected);
                this.s.updating = b;
            };
            h.version = "2.0.0-dev";
            h.classes = {
                bordered: "dtsp-bordered",
                buttonGroup: "dtsp-buttonGroup",
                buttonSub: "dtsp-buttonSub",
                caret: "dtsp-caret",
                clear: "dtsp-clear",
                clearAll: "dtsp-clearAll",
                clearButton: "clearButton",
                collapseAll: "dtsp-collapseAll",
                collapseButton: "dtsp-collapseButton",
                container: "dtsp-searchPane",
                countButton: "dtsp-countButton",
                disabledButton: "dtsp-disabledButton",
                hidden: "dtsp-hidden",
                hide: "dtsp-hide",
                layout: "dtsp-",
                name: "dtsp-name",
                nameButton: "dtsp-nameButton",
                nameCont: "dtsp-nameCont",
                narrow: "dtsp-narrow",
                paneButton: "dtsp-paneButton",
                paneInputButton: "dtsp-paneInputButton",
                pill: "dtsp-pill",
                rotated: "dtsp-rotated",
                search: "dtsp-search",
                searchCont: "dtsp-searchCont",
                searchIcon: "dtsp-searchIcon",
                searchLabelCont: "dtsp-searchButtonCont",
                selected: "dtsp-selected",
                smallGap: "dtsp-smallGap",
                subRow1: "dtsp-subRow1",
                subRow2: "dtsp-subRow2",
                subRowsContainer: "dtsp-subRowsContainer",
                title: "dtsp-title",
                topRow: "dtsp-topRow",
            };
            h.defaults = {
                clear: !0,
                collapse: !0,
                combiner: "or",
                container: function (b) {
                    return b.table().container();
                },
                controls: !0,
                dtOpts: {},
                emptyMessage: null,
                hideCount: !1,
                i18n: { clearPane: "&times;", count: "{total}", emptyMessage: "<em>No data</em>" },
                initCollapsed: !1,
                layout: "auto",
                name: void 0,
                orderable: !0,
                orthogonal: { display: "display", filter: "filter", hideCount: !1, search: "filter", show: void 0, sort: "sort", threshold: 0.6, type: "type", viewCount: !0 },
                preSelect: [],
                threshold: 0.6,
                viewCount: !0,
            };
            return h;
        })(),
        B =
            (window && window.__extends) ||
            (function () {
                var h = function (b, a) {
                    h =
                        Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array &&
                            function (c, d) {
                                c.__proto__ = d;
                            }) ||
                        function (c, d) {
                            for (var e in d) d.hasOwnProperty(e) && (c[e] = d[e]);
                        };
                    return h(b, a);
                };
                return function (b, a) {
                    function c() {
                        this.constructor = b;
                    }
                    h(b, a);
                    b.prototype = null === a ? Object.create(a) : ((c.prototype = a.prototype), new c());
                };
            })(),
        C = (function (h) {
            function b(a, c, d, e, f) {
                return h.call(this, a, c, d, e, f) || this;
            }
            B(b, h);
            b.prototype._serverPopulate = function (a) {
                this.s.rowData.binsShown = {};
                this.s.rowData.arrayFilter = [];
                if (void 0 !== a.tableLength) (this.s.tableLength = a.tableLength), (this.s.rowData.totalOptions = this.s.tableLength);
                else if (null === this.s.tableLength || this.s.dt.rows()[0].length > this.s.tableLength) (this.s.tableLength = this.s.dt.rows()[0].length), (this.s.rowData.totalOptions = this.s.tableLength);
                var c = this.s.dt.column(this.s.index).dataSrc();
                if (void 0 !== a.searchPanes.options[c]) {
                    var d = 0;
                    for (a = a.searchPanes.options[c]; d < a.length; d++)
                        (c = a[d]),
                            this.s.rowData.arrayFilter.push({ display: c.label, filter: c.value, shown: +c.count, sort: c.label, total: +c.total, type: c.label }),
                            (this.s.rowData.binsShown[c.value] = +c.count),
                            (this.s.rowData.bins[c.value] = +c.total);
                }
                d = Object.keys(this.s.rowData.bins).length;
                a = this._uniqueRatio(d, this.s.tableLength);
                if (!this.s.colOpts.show && !1 === this.s.displayed && ((void 0 === this.s.colOpts.show && null === this.s.colOpts.threshold ? a > this.c.threshold : a > this.s.colOpts.threshold) || (!0 !== this.s.colOpts.show && 1 >= d)))
                    this.dom.container.addClass(this.classes.hidden), (this.s.displayed = !1);
                else if (((this.s.rowData.arrayOriginal = this.s.rowData.arrayFilter), (this.s.rowData.binsOriginal = this.s.rowData.bins), (this.s.displayed = !0), this.s.dtPane)) {
                    d = this.s.serverSelect;
                    this.s.dtPane.rows().remove();
                    for (var e = 0, f = this.s.rowData.arrayFilter; e < f.length; e++)
                        if (((a = f[e]), this._shouldAddRow(a))) {
                            c = this.addRow(a.display, a.filter, a.sort, a.type);
                            for (var g = 0; g < d.length; g++) {
                                var m = d[g];
                                if (m.filter === a.filter) {
                                    this.s.serverSelecting = !0;
                                    c.select();
                                    this.s.serverSelecting = !1;
                                    d.splice(g, 1);
                                    this.s.selections.push(a.filter);
                                    break;
                                }
                            }
                        }
                    for (e = 0; e < d.length; e++)
                        for (m = d[e], f = 0, g = this.s.rowData.arrayOriginal; f < g.length; f++)
                            (a = g[f]), a.filter === m.filter && ((c = this.addRow(a.display, a.filter, a.sort, a.type)), (this.s.serverSelecting = !0), c.select(), (this.s.serverSelecting = !1), this.s.selections.push(a.filter));
                    this.s.serverSelect = this.s.dtPane.rows({ selected: !0 }).data().toArray();
                    this.s.dtPane.draw();
                }
            };
            b.prototype.updateRows = function () {
                if (!this.s.dt.page.info().serverSide) {
                    this.s.rowData.binsShown = {};
                    for (var a = 0, c = this.s.dt.rows({ search: "applied" }).indexes().toArray(); a < c.length; a++) this._updateShown(c[a], this.s.dt.settings()[0], this.s.rowData.binsShown);
                }
                a = 0;
                for (c = this.s.dtPane.rows().data().toArray(); a < c.length; a++) {
                    var d = c[a];
                    d.shown = "number" === typeof this.s.rowData.binsShown[d.filter] ? this.s.rowData.binsShown[d.filter] : 0;
                    this.s.dtPane.row(d.index).data(d);
                }
                this.s.dtPane.draw();
                this.s.dtPane.table().node().parentNode.scrollTop = this.s.scrollTop;
            };
            b.prototype._makeSelection = function () {};
            b.prototype._reloadSelect = function () {};
            b.prototype._shouldAddRow = function (a) {
                return !0;
            };
            b.prototype._updateSelection = function () {
                !this.s.dt.page.info().serverSide || this.s.updating || this.s.serverSelecting || (this.s.serverSelect = this.s.dtPane.rows({ selected: !0 }).data().toArray());
            };
            b.prototype._updateShown = function (a, c, d) {
                void 0 === d && (d = this.s.rowData.binsShown);
                a = c.oApi._fnGetCellData(c, a, this.s.index, "string" === typeof this.s.colOpts.orthogonal ? this.s.colOpts.orthogonal : this.s.colOpts.orthogonal.search);
                if (Array.isArray(a))
                    for (c = 0; c < a.length; c++) {
                        var e = a[c];
                        d[e] ? d[e]++ : (d[e] = 1);
                    }
                else d[a] ? d[a]++ : (d[a] = 1);
            };
            return b;
        })(v),
        H =
            (window && window.__extends) ||
            (function () {
                var h = function (b, a) {
                    h =
                        Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array &&
                            function (c, d) {
                                c.__proto__ = d;
                            }) ||
                        function (c, d) {
                            for (var e in d) d.hasOwnProperty(e) && (c[e] = d[e]);
                        };
                    return h(b, a);
                };
                return function (b, a) {
                    function c() {
                        this.constructor = b;
                    }
                    h(b, a);
                    b.prototype = null === a ? Object.create(a) : ((c.prototype = a.prototype), new c());
                };
            })(),
        r,
        p = (function (h) {
            function b(a, c, d, e, f) {
                return h.call(this, a, r.extend({ i18n: { countFiltered: "{shown} ({total})" } }, c), d, e, f) || this;
            }
            H(b, h);
            b.prototype._getMessage = function (a) {
                var c = this.s.dt.i18n("searchPanes.count", this.c.i18n.count),
                    d = this.s.dt.i18n("searchPanes.countFiltered", this.c.i18n.countFiltered);
                return (this.s.filteringActive ? d : c).replace(/{total}/g, a.total).replace(/{shown}/g, a.shown);
            };
            b.prototype._getShown = function (a) {
                return this.s.rowData.binsShown && this.s.rowData.binsShown[a] ? this.s.rowData.binsShown[a] : 0;
            };
            return b;
        })(C),
        u =
            (window && window.__extends) ||
            (function () {
                var h = function (b, a) {
                    h =
                        Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array &&
                            function (c, d) {
                                c.__proto__ = d;
                            }) ||
                        function (c, d) {
                            for (var e in d) d.hasOwnProperty(e) && (c[e] = d[e]);
                        };
                    return h(b, a);
                };
                return function (b, a) {
                    function c() {
                        this.constructor = b;
                    }
                    h(b, a);
                    b.prototype = null === a ? Object.create(a) : ((c.prototype = a.prototype), new c());
                };
            })(),
        y,
        E = (function (h) {
            function b(a, c, d, e, f) {
                return h.call(this, a, y.extend({ i18n: { count: "{shown}" } }, c), d, e, f) || this;
            }
            u(b, h);
            b.prototype.updateRows = function () {
                var a = this.s.dtPane.rows({ selected: !0 }).data().toArray();
                if (this.s.colOpts.options || (this.s.customPaneSettings && this.s.customPaneSettings.options)) {
                    this._getComparisonRows();
                    for (var c = this.s.dtPane.rows().toArray()[0], d = 0; d < c.length; d++) {
                        var e = this.s.dtPane.row(c[d]),
                            f = e.data();
                        if (void 0 !== f)
                            if (0 === f.shown) e.remove(), (c = this.s.dtPane.rows().toArray()[0]), d--;
                            else
                                for (var g = 0, m = a; g < m.length; g++) {
                                    var t = m[g];
                                    if (f.filter === t.filter) {
                                        e.select();
                                        a.splice(d, 1);
                                        this.s.selections.push(f.filter);
                                        break;
                                    }
                                }
                    }
                } else {
                    if (!this.s.dt.page.info().serverSide)
                        for (this._activePopulatePane(), this.s.rowData.binsShown = {}, e = 0, t = this.s.dt.rows({ search: "applied" }).indexes().toArray(); e < t.length; e++)
                            this._updateShown(t[e], this.s.dt.settings()[0], this.s.rowData.binsShown);
                    this.s.dtPane.rows().remove();
                    f = 0;
                    for (g = this.s.rowData.arrayFilter; f < g.length; f++)
                        if (((c = g[f]), 0 !== c.shown))
                            for (e = this.addRow(c.display, c.filter, c.sort, c.type, void 0), d = 0; d < a.length; d++)
                                if (((t = a[d]), t.filter === c.filter)) {
                                    e.select();
                                    a.splice(d, 1);
                                    this.s.selections.push(c.filter);
                                    break;
                                }
                    for (d = 0; d < a.length; d++)
                        for (t = a[d], f = 0, g = this.s.rowData.arrayOriginal; f < g.length; f++)
                            (c = g[f]), c.filter === t.filter && ((e = this.addRow(c.display, c.filter, c.sort, c.type, void 0)), e.select(), this.s.selections.push(c.filter));
                }
                this.s.dtPane.draw();
                this.s.dtPane.table().node().parentNode.scrollTop = this.s.scrollTop;
                this.s.dt.page.info().serverSide || this.s.dt.draw();
            };
            b.prototype._activePopulatePane = function () {
                this.s.rowData.arrayFilter = [];
                this.s.rowData.bins = {};
                var a = this.s.dt.settings()[0];
                if (!this.s.dt.page.info().serverSide) for (var c = 0, d = this.s.dt.rows({ search: "applied" }).indexes().toArray(); c < d.length; c++) this._populatePaneArray(d[c], this.s.rowData.arrayFilter, a);
            };
            b.prototype._getComparisonRows = function () {
                var a = this.s.colOpts.options ? this.s.colOpts.options : this.s.customPaneSettings && this.s.customPaneSettings.options ? this.s.customPaneSettings.options : void 0;
                if (void 0 !== a) {
                    var c = this.s.dt.rows(),
                        d = this.s.dt.rows({ search: "applied" }),
                        e = c.data().toArray(),
                        f = d.data().toArray(),
                        g = [];
                    this.s.dtPane.clear();
                    this.s.indexes = [];
                    for (var m = 0; m < a.length; m++) {
                        var t = a[m],
                            w = "" !== t.label ? t.label : this.emptyMessage(),
                            A = t.className,
                            z = w,
                            x = "function" === typeof t.value ? t.value : [],
                            L = 0,
                            O = w,
                            M = 0;
                        if ("function" === typeof t.value) {
                            for (var F = 0; F < e.length; F++) t.value.call(this.s.dt, e[F], c[0][F]) && M++;
                            for (F = 0; F < f.length; F++) t.value.call(this.s.dt, f[F], d[0][F]) && L++;
                            "function" !== typeof x && x.push(t.filter);
                        }
                        g.push(this.addRow(z, x, O, w, A, M, L));
                    }
                    return g;
                }
            };
            b.prototype._getMessage = function (a) {
                return this.s.dt
                    .i18n("searchPanes.count", this.c.i18n.count)
                    .replace(/{total}/g, a.total)
                    .replace(/{shown}/g, a.shown);
            };
            b.prototype._getShown = function (a) {
                return this.s.rowData.binsShown && this.s.rowData.binsShown[a] ? this.s.rowData.binsShown[a] : 0;
            };
            b.prototype._shouldAddRow = function (a) {
                return 0 < a.shown;
            };
            return b;
        })(C),
        P =
            (window && window.__extends) ||
            (function () {
                var h = function (b, a) {
                    h =
                        Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array &&
                            function (c, d) {
                                c.__proto__ = d;
                            }) ||
                        function (c, d) {
                            for (var e in d) d.hasOwnProperty(e) && (c[e] = d[e]);
                        };
                    return h(b, a);
                };
                return function (b, a) {
                    function c() {
                        this.constructor = b;
                    }
                    h(b, a);
                    b.prototype = null === a ? Object.create(a) : ((c.prototype = a.prototype), new c());
                };
            })(),
        N,
        J = (function (h) {
            function b(a, c, d, e, f) {
                return h.call(this, a, N.extend({ i18n: { count: "{total}", countFiltered: "{shown} ({total})" } }, c), d, e, f) || this;
            }
            P(b, h);
            b.prototype._activePopulatePane = function () {
                this.s.rowData.arrayFilter = [];
                this.s.rowData.binsShown = {};
                var a = this.s.dt.settings()[0];
                if (!this.s.dt.page.info().serverSide) for (var c = 0, d = this.s.dt.rows({ search: "applied" }).indexes().toArray(); c < d.length; c++) this._populatePaneArray(d[c], this.s.rowData.arrayFilter, a, this.s.rowData.binsShown);
            };
            b.prototype._getMessage = function (a) {
                var c = this.s.dt.i18n("searchPanes.count", this.c.i18n.count),
                    d = this.s.dt.i18n("searchPanes.countFiltered", this.c.i18n.countFiltered);
                return (this.s.filteringActive ? d : c).replace(/{total}/g, a.total).replace(/{shown}/g, a.shown);
            };
            return b;
        })(E),
        D,
        G,
        I = (function () {
            function h(b, a, c, d) {
                var e = this;
                void 0 === c && (c = !1);
                void 0 === d && (d = v);
                if (!G || !G.versionCheck || !G.versionCheck("1.10.0")) throw Error("SearchPane requires DataTables 1.10 or newer");
                if (!G.select) throw Error("SearchPane requires Select");
                var f = new G.Api(b);
                this.classes = D.extend(!0, {}, h.classes);
                this.c = D.extend(!0, {}, h.defaults, a);
                this.dom = {
                    clearAll: D('<button type="button"/>').addClass(this.classes.clearAll).html(f.i18n("searchPanes.clearMessage", this.c.i18n.clearMessage)),
                    collapseAll: D('<button type="button"/>').addClass(this.classes.collapseAll).html(f.i18n("searchPanes.collapseMessage", this.c.i18n.collapseMessage)),
                    container: D("<div/>").addClass(this.classes.panes).html(f.i18n("searchPanes.loadMessage", this.c.i18n.loadMessage)),
                    emptyMessage: D("<div/>").addClass(this.classes.emptyMessage),
                    panes: D("<div/>").addClass(this.classes.container),
                    showAll: D('<button type="button"/>').addClass(this.classes.showAll).addClass(this.classes.disabledButton).attr("disabled", "true").html(f.i18n("searchPanes.showMessage", this.c.i18n.showMessage)),
                    title: D("<div/>").addClass(this.classes.title),
                    titleRow: D("<div/>").addClass(this.classes.titleRow),
                };
                this.s = { colOpts: [], dt: f, filterCount: 0, minPaneWidth: 260, page: 0, paging: !1, pagingST: !1, paneClass: d, panes: [], selectionList: [], serverData: {}, stateRead: !1, updating: !1 };
                if (!f.settings()[0]._searchPanes) {
                    this._getState();
                    if (this.s.dt.page.info().serverSide) {
                        var g = this.s.dt.settings()[0];
                        this.s.dt.on("preXhr.dtsps", function (m, t, w) {
                            if (g === t) {
                                void 0 === w.searchPanes && (w.searchPanes = {});
                                void 0 === w.searchPanes_null && (w.searchPanes_null = {});
                                m = 0;
                                for (t = e.s.selectionList; m < t.length; m++) {
                                    var A = t[m];
                                    var z = e.s.dt.column(A.column).dataSrc();
                                    void 0 === w.searchPanes[z] && (w.searchPanes[z] = {});
                                    void 0 === w.searchPanes_null[z] && (w.searchPanes_null[z] = {});
                                    for (var x = 0; x < A.rows.length; x++) (w.searchPanes[z][x] = A.rows[x]), null === w.searchPanes[z][x] && (w.searchPanes_null[z][x] = !0);
                                }
                                0 < e.s.selectionList.length && (w.searchPanesLast = z);
                            }
                        });
                    }
                    this._setXHR();
                    f.settings()[0]._searchPanes = this;
                    if (this.s.dt.settings()[0]._bInitComplete || c) this._paneDeclare(f, b, a);
                    else
                        f.one("preInit.dtsps", function () {
                            e._paneDeclare(f, b, a);
                        });
                    return this;
                }
            }
            h.prototype.clearSelections = function () {
                for (var b = 0, a = this.s.panes; b < a.length; b++) {
                    var c = a[b];
                    c.s.dtPane && (c.s.scrollTop = c.s.dtPane.table().node().parentNode.scrollTop);
                }
                this.dom.container.find("." + this.classes.search.replace(/\s+/g, ".")).each(function () {
                    D(this).val("").trigger("input");
                });
                this.s.selectionList = [];
                b = [];
                a = 0;
                for (var d = this.s.panes; a < d.length; a++) (c = d[a]), c.s.dtPane && b.push(c.clearPane());
                return b;
            };
            h.prototype.getNode = function () {
                return this.dom.container;
            };
            h.prototype.rebuild = function (b, a) {
                void 0 === b && (b = !1);
                void 0 === a && (a = !1);
                this.dom.emptyMessage.detach();
                !1 === b && this.dom.panes.empty();
                for (var c = [], d = 0, e = this.s.panes; d < e.length; d++) {
                    var f = e[d];
                    if (!1 === b || f.s.index === b) f.clearData(), f.rebuildPane(this.s.dt.page.info().serverSide ? this.s.serverData : void 0, a), this.dom.panes.append(f.dom.container), c.push(f);
                }
                this._updateSelection();
                this._updateFilterCount();
                this._attachPaneContainer();
                this._initSelectionListeners(!1);
                this.s.dt.draw(!a);
                this.resizePanes();
                return 1 === c.length ? c[0] : c;
            };
            h.prototype.resizePanes = function () {
                if ("auto" === this.c.layout) {
                    var b = D(this.s.dt.searchPanes.container()).width(),
                        a = Math.floor(b / this.s.minPaneWidth),
                        c = 1,
                        d = 0;
                    b = [];
                    for (var e = 0, f = this.s.panes; e < f.length; e++) {
                        var g = f[e];
                        g.s.displayed && b.push(g.s.index);
                    }
                    g = b.length;
                    if (a === g) c = a;
                    else
                        for (; 1 < a; a--)
                            if (((e = g % a), 0 === e)) {
                                c = a;
                                d = 0;
                                break;
                            } else e > d && ((c = a), (d = e));
                    var m = 0 !== d ? b.slice(b.length - d, b.length) : [];
                    this.s.panes.forEach(function (t) {
                        t.s.displayed && t.resize("columns-" + (m.includes(t.s.index) ? d : c));
                    });
                } else for (b = 0, a = this.s.panes; b < a.length; b++) (g = a[b]), g.adjustTopRow();
                return this;
            };
            h.prototype._initSelectionListeners = function (b) {};
            h.prototype._serverTotals = function () {};
            h.prototype._setXHR = function () {
                var b = this,
                    a = this.s.dt.settings()[0],
                    c = function (d) {
                        d && d.searchPanes && d.searchPanes.options && ((b.s.serverData = d), (b.s.serverData.tableLength = d.recordsTotal), b._serverTotals());
                    };
                this.s.dt.on("xhr.dtsps", function (d, e, f) {
                    a === e && c(f);
                });
                c(this.s.dt.ajax.json());
            };
            h.prototype._stateLoadListener = function () {
                var b = this;
                this.s.dt.on("stateLoadParams.dtsps", function (a, c, d) {
                    if (void 0 !== d.searchPanes) {
                        b.clearSelections();
                        b.s.selectionList = d.searchPanes.selectionList ? d.searchPanes.selectionList : [];
                        if (d.searchPanes.panes)
                            for (a = 0, d = d.searchPanes.panes; a < d.length; a++) {
                                c = d[a];
                                for (var e = 0, f = b.s.panes; e < f.length; e++) {
                                    var g = f[e];
                                    c.id === g.s.index && g.s.dtPane && (g.dom.searchBox.val(c.searchTerm), g.s.dtPane.order(c.order));
                                }
                            }
                        b._makeSelections(b.s.selectionList);
                    }
                });
            };
            h.prototype._updateSelection = function () {
                this.s.selectionList = [];
                for (var b = 0, a = this.s.panes; b < a.length; b++) {
                    var c = a[b];
                    if (c.s.dtPane) {
                        var d = c.s.dtPane
                            .rows({ selected: !0 })
                            .data()
                            .toArray()
                            .map(function (e) {
                                return e.filter;
                            });
                        d.length && this.s.selectionList.push({ column: c.s.index, rows: d });
                    }
                }
            };
            h.prototype._attach = function () {
                var b = this;
                this.dom.titleRow.removeClass(this.classes.hide).detach().append(this.dom.title);
                if (this.c.clear)
                    this.dom.clearAll.appendTo(this.dom.titleRow).on("click.dtsps", function () {
                        return b.clearSelections();
                    });
                this.c.collapse && (this.dom.showAll.appendTo(this.dom.titleRow), this.dom.collapseAll.appendTo(this.dom.titleRow), this._setCollapseListener());
                for (var a = 0, c = this.s.panes; a < c.length; a++) this.dom.panes.append(c[a].dom.container);
                this.dom.container.text("").removeClass(this.classes.hide).append(this.dom.titleRow).append(this.dom.panes);
                this.s.panes.forEach(function (d) {
                    return d.setListeners();
                });
                0 === D("div." + this.classes.container).length && this.dom.container.prependTo(this.s.dt);
            };
            h.prototype._attachMessage = function () {
                try {
                    var b = this.s.dt.i18n("searchPanes.emptyPanes", this.c.i18n.emptyPanes);
                } catch (a) {
                    b = null;
                }
                null === b
                    ? (this.dom.container.addClass(this.classes.hide), this.dom.titleRow.removeClass(this.classes.hide))
                    : (this.dom.container.removeClass(this.classes.hide), this.dom.titleRow.addClass(this.classes.hide), this.dom.emptyMessage.html(b).appendTo(this.dom.container));
            };
            h.prototype._attachPaneContainer = function () {
                for (var b = 0, a = this.s.panes; b < a.length; b++)
                    if (!0 === a[b].s.displayed) {
                        this._attach();
                        return;
                    }
                this._attachMessage();
            };
            h.prototype._checkCollapse = function () {
                for (var b = !0, a = !0, c = 0, d = this.s.panes; c < d.length; c++) {
                    var e = d[c];
                    e.s.displayed &&
                        (e.dom.collapseButton.hasClass(e.classes.rotated)
                            ? (this.dom.showAll.removeClass(this.classes.disabledButton).removeAttr("disabled"), (a = !1))
                            : (this.dom.collapseAll.removeClass(this.classes.disabledButton).removeAttr("disabled"), (b = !1)));
                }
                b && this.dom.collapseAll.addClass(this.classes.disabledButton).attr("disabled", "true");
                a && this.dom.showAll.addClass(this.classes.disabledButton).attr("disabled", "true");
            };
            h.prototype._checkMessage = function () {
                for (var b = 0, a = this.s.panes; b < a.length; b++)
                    if (!0 === a[b].s.displayed) {
                        this.dom.emptyMessage.detach();
                        this.dom.titleRow.removeClass(this.classes.hide);
                        return;
                    }
                this._attachMessage();
            };
            h.prototype._collapseAll = function () {
                for (var b = 0, a = this.s.panes; b < a.length; b++) a[b].collapse();
            };
            h.prototype._findPane = function (b) {
                for (var a = 0, c = this.s.panes; a < c.length; a++) {
                    var d = c[a];
                    if (b === d.s.name) return d;
                }
            };
            h.prototype._getState = function () {
                var b = this.s.dt.state.loaded();
                b && b.searchPanes && b.searchPanes.selectionList && (this.s.selectionList = b.searchPanes.selectionList);
            };
            h.prototype._makeSelections = function (b) {
                for (var a = 0; a < b.length; a++) {
                    for (var c = b[a], d = void 0, e = 0, f = this.s.panes; e < f.length; e++) {
                        var g = f[e];
                        if (g.s.index === c.column) {
                            d = g;
                            break;
                        }
                    }
                    if (d && d.s.dtPane) {
                        for (e = 0; e < d.s.dtPane.rows().data().toArray().length; e++)
                            c.rows.includes("function" === typeof d.s.dtPane.row(e).data().filter ? d.s.dtPane.cell(e, 0).data() : d.s.dtPane.row(e).data().filter) && d.s.dtPane.row(e).select();
                        d.updateTable();
                    }
                }
            };
            h.prototype._paneDeclare = function (b, a, c) {
                var d = this;
                b.columns(0 < this.c.columns.length ? this.c.columns : void 0)
                    .eq(0)
                    .each(function (g) {
                        d.s.panes.push(new d.s.paneClass(a, c, g, d.dom.panes));
                    });
                for (var e = b.columns().eq(0).toArray().length, f = 0; f < this.c.panes.length; f++) this.s.panes.push(new this.s.paneClass(a, c, e + f, this.dom.panes, this.c.panes[f]));
                0 < this.c.order.length &&
                    (this.s.panes = this.c.order.map(function (g) {
                        return d._findPane(g);
                    }));
                this.s.dt.settings()[0]._bInitComplete
                    ? this._startup(b)
                    : this.s.dt.settings()[0].aoInitComplete.push({
                          fn: function () {
                              return d._startup(b);
                          },
                      });
            };
            h.prototype._setCollapseListener = function () {
                var b = this;
                this.dom.collapseAll.on("click.dtsps", function () {
                    b._collapseAll();
                    b.dom.collapseAll.addClass(b.classes.disabledButton).attr("disabled", "true");
                    b.dom.showAll.removeClass(b.classes.disabledButton).removeAttr("disabled");
                    b.s.dt.state.save();
                });
                this.dom.showAll.on("click.dtsps", function () {
                    b._showAll();
                    b.dom.showAll.addClass(b.classes.disabledButton).attr("disabled", "true");
                    b.dom.collapseAll.removeClass(b.classes.disabledButton).removeAttr("disabled");
                    b.s.dt.state.save();
                });
                for (var a = 0, c = this.s.panes; a < c.length; a++)
                    c[a].dom.collapseButton.on("click.dtsps", function () {
                        return b._checkCollapse();
                    });
                this._checkCollapse();
            };
            h.prototype._showAll = function () {
                for (var b = 0, a = this.s.panes; b < a.length; b++) a[b].show();
            };
            h.prototype._startup = function (b) {
                var a = this;
                this._attach();
                this.dom.panes.empty();
                for (var c = 0, d = this.s.panes; c < d.length; c++) {
                    var e = d[c];
                    e.rebuildPane(0 < Object.keys(this.s.serverData).length ? this.s.serverData : void 0);
                    this.dom.panes.append(e.dom.container);
                }
                "auto" === this.c.layout && this.resizePanes();
                c = this.s.dt.state.loaded();
                !this.s.stateRead && c && this.s.dt.page(c.start / this.s.dt.page.len()).draw("page");
                this.s.stateRead = !0;
                this._checkMessage();
                b.on("preDraw.dtsps", function () {
                    a.s.updating || a.s.paging || (a._updateFilterCount(), a._updateSelection());
                    a.s.paging = !1;
                });
                D(window).on(
                    "resize.dtsps",
                    G.util.throttle(function () {
                        return a.resizePanes();
                    })
                );
                this.s.dt.on("stateSaveParams.dtsps", function (f, g, m) {
                    void 0 === m.searchPanes && (m.searchPanes = {});
                    m.searchPanes.selectionList = a.s.selectionList;
                });
                this._stateLoadListener();
                b.off("page.dtsps page-nc.dtsps").on("page.dtsps page-nc.dtsps", function (f, g) {
                    a.s.paging = !0;
                    a.s.pagingST = !0;
                    a.s.page = a.s.dt.page();
                });
                if (this.s.dt.page.info().serverSide)
                    b.off("preXhr.dtsps").on("preXhr.dtsps", function (f, g, m) {
                        m.searchPanes || (m.searchPanes = {});
                        m.searchPanes_null || (m.searchPanes_null = {});
                        g = f = 0;
                        for (var t = a.s.panes; g < t.length; g++) {
                            var w = t[g],
                                A = a.s.dt.column(w.s.index).dataSrc();
                            m.searchPanes[A] || (m.searchPanes[A] = {});
                            m.searchPanes_null[A] || (m.searchPanes_null[A] = {});
                            if (w.s.dtPane) {
                                w = w.s.dtPane.rows({ selected: !0 }).data().toArray();
                                for (var z = 0; z < w.length; z++) (m.searchPanes[A][z] = w[z].filter), m.searchPanes[A][z] || (m.searchPanes_null[A][z] = !0), f++;
                            }
                        }
                        0 < f && (f !== a.s.filterCount ? ((m.start = 0), (a.s.page = 0)) : (m.start = a.s.page * a.s.dt.page.len()), a.s.dt.page(a.s.page), (a.s.filterCount = f));
                        0 < a.s.selectionList.length && (m.searchPanesLast = a.s.dt.column(a.s.selectionList[a.s.selectionList.length - 1].column).dataSrc());
                    });
                else
                    b.on("preXhr.dtsps", function () {
                        return a.s.panes.forEach(function (f) {
                            return f.clearData();
                        });
                    });
                this.s.dt.on("xhr.dtsps", function (f, g) {
                    if (g.nTable === a.s.dt.table().node() && !a.s.dt.page.info().serverSide) {
                        var m = !1;
                        a.s.dt.one("preDraw.dtsps", function () {
                            if (!m) {
                                var t = a.s.dt.page();
                                m = !0;
                                a.s.updating = !0;
                                a.dom.panes.empty();
                                for (var w = 0, A = a.s.panes; w < A.length; w++) {
                                    var z = A[w];
                                    z.clearData();
                                    z.rebuildPane(void 0, !0);
                                    a.dom.panes.append(z.dom.container);
                                }
                                a.s.dt.page.info().serverSide || a.s.dt.draw();
                                a.s.updating = !1;
                                a._updateSelection();
                                a._checkMessage();
                                a.s.dt.one("draw.dtsps", function () {
                                    a.s.updating = !0;
                                    a.s.dt.page(t).draw(!1);
                                    a.s.updating = !1;
                                });
                            }
                        });
                    }
                });
                d = this.c.preSelect;
                c && c.searchPanes && c.searchPanes.selectionList && (d = c.searchPanes.selectionList);
                this._makeSelections(d);
                this._updateFilterCount();
                b.on("destroy.dtsps", function () {
                    for (var f = 0, g = a.s.panes; f < g.length; f++) g[f].destroy();
                    b.off(".dtsps");
                    a.dom.showAll.off(".dtsps");
                    a.dom.clearAll.off(".dtsps");
                    a.dom.collapseAll.off(".dtsps");
                    D(b.table().node()).off(".dtsps");
                    a.dom.container.detach();
                    a.clearSelections();
                });
                this.c.collapse && this._setCollapseListener();
                if (this.c.clear)
                    this.dom.clearAll.on("click.dtsps", function () {
                        return a.clearSelections();
                    });
                b.settings()[0]._searchPanes = this;
                this.s.dt.state.save();
            };
            h.prototype._updateFilterCount = function () {
                for (var b = 0, a = 0, c = this.s.panes; a < c.length; a++) {
                    var d = c[a];
                    d.s.dtPane && (b += d.getPaneCount());
                }
                this.dom.title.html(this.s.dt.i18n("searchPanes.title", this.c.i18n.title, b));
                this.c.filterChanged && "function" === typeof this.c.filterChanged && this.c.filterChanged.call(this.s.dt, b);
                0 === b ? this.dom.clearAll.addClass(this.classes.disabledButton).attr("disabled", "true") : this.dom.clearAll.removeClass(this.classes.disabledButton).removeAttr("disabled");
            };
            h.version = "2.0.2";
            h.classes = {
                clear: "dtsp-clear",
                clearAll: "dtsp-clearAll",
                collapseAll: "dtsp-collapseAll",
                container: "dtsp-searchPanes",
                disabledButton: "dtsp-disabledButton",
                emptyMessage: "dtsp-emptyMessage",
                hide: "dtsp-hidden",
                panes: "dtsp-panesContainer",
                search: "dtsp-search",
                showAll: "dtsp-showAll",
                title: "dtsp-title",
                titleRow: "dtsp-titleRow",
            };
            h.defaults = {
                clear: !0,
                collapse: !0,
                columns: [],
                container: function (b) {
                    return b.table().container();
                },
                filterChanged: void 0,
                i18n: {
                    clearMessage: "Clear All",
                    clearPane: "&times;",
                    collapse: { 0: "SearchPanes", _: "SearchPanes (%d)" },
                    collapseMessage: "Collapse All",
                    count: "{total}",
                    emptyMessage: "<em>No data</em>",
                    emptyPanes: "No SearchPanes",
                    loadMessage: "Loading Search Panes...",
                    showMessage: "Show All",
                    title: "Filters Active - %d",
                },
                layout: "auto",
                order: [],
                panes: [],
                preSelect: [],
            };
            return h;
        })(),
        Q =
            (window && window.__extends) ||
            (function () {
                var h = function (b, a) {
                    h =
                        Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array &&
                            function (c, d) {
                                c.__proto__ = d;
                            }) ||
                        function (c, d) {
                            for (var e in d) d.hasOwnProperty(e) && (c[e] = d[e]);
                        };
                    return h(b, a);
                };
                return function (b, a) {
                    function c() {
                        this.constructor = b;
                    }
                    h(b, a);
                    b.prototype = null === a ? Object.create(a) : ((c.prototype = a.prototype), new c());
                };
            })(),
        K = (function (h) {
            function b(a, c, d) {
                void 0 === d && (d = !1);
                var e = this,
                    f;
                c.cascadePanes && c.viewTotal ? (f = J) : c.cascadePanes ? (f = E) : c.viewTotal && (f = p);
                e = h.call(this, a, c, d, f) || this;
                var g = e.s.dt.state.loaded();
                e.s.dt.off("init.dtsps").on("init.dtsps", function () {
                    return e._initSelectionListeners(!0, g && g.searchPanes && g.searchPanes.selectionList ? g.searchPanes.selectionList : e.c.preSelect);
                });
                return e;
            }
            Q(b, h);
            b.prototype._initSelectionListeners = function (a, c) {
                void 0 === a && (a = !0);
                void 0 === c && (c = []);
                a && (this.s.selectionList = c);
                a = 0;
                for (c = this.s.panes; a < c.length; a++) {
                    var d = c[a];
                    if (d.s.displayed) d.s.dtPane.off("select.dtsp").on("select.dtsp", this._update(d)).off("deselect.dtsp").on("deselect.dtsp", this._updateTimeout(d));
                }
                this.s.dt.off("draw.dtsps").on("draw.dtsps", this._update());
                this._updateSelectionList();
            };
            b.prototype._serverTotals = function () {
                for (var a = 0, c = this.s.panes; a < c.length; a++) {
                    var d = c[a];
                    if (d.s.colOpts.show) {
                        var e = this.s.dt.column(d.s.index).dataSrc(),
                            f = !0;
                        if (this.s.serverData.searchPanes.options[e]) {
                            var g = 0;
                            for (e = this.s.serverData.searchPanes.options[e]; g < e.length; g++) {
                                var m = e[g];
                                if (m.total !== m.count) {
                                    f = !1;
                                    break;
                                }
                            }
                        }
                        d.s.filteringActive = !f;
                        d._serverPopulate(this.s.serverData);
                    }
                }
            };
            b.prototype._stateLoadListener = function () {
                var a = this,
                    c = function (d, e, f) {
                        if (void 0 !== f.searchPanes) {
                            a.s.selectionList = f.searchPanes.selectionList ? f.searchPanes.selectionList : [];
                            if (f.searchPanes.panes)
                                for (d = 0, f = f.searchPanes.panes; d < f.length; d++) {
                                    e = f[d];
                                    for (var g = 0, m = a.s.panes; g < m.length; g++) {
                                        var t = m[g];
                                        e.id === t.s.index && t.s.dtPane && (t.dom.searchBox.val(e.searchTerm), t.s.dtPane.order(e.order));
                                    }
                                }
                            a._updateSelectionList();
                        }
                    };
                this.s.dt.off("stateLoadParams.dtsps", c).on("stateLoadParams.dtsps", c);
            };
            b.prototype._updateSelection = function () {};
            b.prototype._update = function (a) {
                var c = this;
                void 0 === a && (a = void 0);
                return function () {
                    a && clearTimeout(a.s.deselectTimeout);
                    c._updateSelectionList(a);
                };
            };
            b.prototype._updateTimeout = function (a) {
                var c = this;
                void 0 === a && (a = void 0);
                return function () {
                    return a
                        ? (a.s.deselectTimeout = setTimeout(function () {
                              return c._updateSelectionList(a);
                          }, 50))
                        : c._updateSelectionList();
                };
            };
            b.prototype._updateSelectionList = function (a) {
                void 0 === a && (a = void 0);
                if (this.s.pagingST) this.s.pagingST = !1;
                else if (!(this.s.updating || (a && a.s.serverSelecting))) {
                    if (void 0 !== a) {
                        this.s.dt.page.info().serverSide && a._updateSelection();
                        var c = a.s.dtPane
                            .rows({ selected: !0 })
                            .data()
                            .toArray()
                            .map(function (d) {
                                return d.filter;
                            });
                        this.s.selectionList = this.s.selectionList.filter(function (d) {
                            return d.column !== a.s.index;
                        });
                        0 < c.length
                            ? (this.s.selectionList.push({ column: a.s.index, rows: c }), a.dom.clear.removeClass(this.classes.disabledButton).removeAttr("disabled"))
                            : a.dom.clear.addClass(this.classes.disabledButton).attr("disabled", "true");
                        this.s.dt.page.info().serverSide && this.s.dt.draw(!1);
                    }
                    this._remakeSelections();
                    this._updateFilterCount();
                }
            };
            b.prototype._remakeSelections = function () {
                this.s.updating = !0;
                if (this.s.dt.page.info().serverSide) {
                    e = void 0;
                    0 < this.s.selectionList.length && (e = this.s.panes[this.s.selectionList[this.s.selectionList.length - 1].column]);
                    for (var a = 0, c = this.s.panes; a < c.length; a++) (x = c[a]), !x.s.displayed || (e && x.s.index === e.s.index) || x.updateRows();
                } else {
                    e = this.s.selectionList;
                    a = !1;
                    this.clearSelections();
                    this.s.dt.draw();
                    this.s.dt.rows().toArray()[0].length > this.s.dt.rows({ search: "applied" }).toArray()[0].length && (a = !0);
                    this.s.selectionList = e;
                    c = 0;
                    for (var d = this.s.panes; c < d.length; c++) {
                        var e = d[c];
                        e.s.displayed && ((e.s.filteringActive = a), e.updateRows());
                    }
                    c = 0;
                    for (d = this.s.selectionList; c < d.length; c++) {
                        x = d[c];
                        e = void 0;
                        for (var f = 0, g = this.s.panes; f < g.length; f++) {
                            var m = g[f];
                            if (m.s.index === x.column) {
                                e = m;
                                break;
                            }
                        }
                        if (e.s.dtPane) {
                            f = e.s.dtPane.rows().indexes().toArray();
                            for (g = 0; g < x.rows.length; g++) {
                                m = !1;
                                for (var t = 0, w = f; t < w.length; t++) {
                                    var A = e.s.dtPane.row(w[t]),
                                        z = A.data();
                                    x.rows[g] === z.filter && (A.select(), (m = !0));
                                }
                                m || (x.rows.splice(g, 1), g--);
                            }
                            e.s.selections = x.rows;
                            if (0 !== x.rows.length) {
                                this.s.dt.draw();
                                t = f = m = g = 0;
                                for (w = this.s.panes; t < w.length; t++) {
                                    var x = w[t];
                                    x.s.dtPane && ((g += x.getPaneCount()), g > m && (f++, (m = g)));
                                }
                                g = 0 < g;
                                m = 0;
                                for (t = this.s.panes; m < t.length; m++)
                                    (x = t[m]), x.s.displayed && (a || e.s.index !== x.s.index || !g ? (x.s.filteringActive = g || a) : 1 === f && (x.s.filteringActive = !1), x.s.index !== e.s.index && x.updateRows());
                            }
                        }
                    }
                    this.s.dt.draw();
                }
                this.s.updating = !1;
            };
            return b;
        })(I);
    (function (h) {
        "function" === typeof define && define.amd
            ? define(["jquery", "datatables.net"], function (b) {
                  return h(b, window, document);
              })
            : "object" === typeof exports
            ? (module.exports = function (b, a) {
                  b || (b = window);
                  (a && a.fn.dataTable) || (a = require("datatables.net")(b, a).$);
                  return h(a, b, b.document);
              })
            : h(window.jQuery, window, document);
    })(function (h, b, a) {
        function c(e, f, g) {
            void 0 === f && (f = null);
            void 0 === g && (g = !1);
            e = new d.Api(e);
            f = f ? f : e.init().searchPanes || d.defaults.searchPanes;
            return (f && (f.cascadePanes || f.viewTotal) ? new K(e, f, g) : new I(e, f, g)).getNode();
        }
        l(h);
        n(h);
        N = y = r = h;
        var d = h.fn.dataTable;
        h.fn.dataTable.SearchPanes = I;
        h.fn.DataTable.SearchPanes = I;
        h.fn.dataTable.SearchPanesST = K;
        h.fn.DataTable.SearchPanesST = K;
        h.fn.dataTable.SearchPane = v;
        h.fn.DataTable.SearchPane = v;
        h.fn.dataTable.SearchPaneViewTotal = p;
        h.fn.DataTable.SearchPaneViewTotal = p;
        h.fn.dataTable.SearchPaneCascade = E;
        h.fn.DataTable.SearchPaneCascade = E;
        h.fn.dataTable.SearchPaneCascadeViewTotal = J;
        h.fn.DataTable.SearchPaneCascadeViewTotal = J;
        b = h.fn.dataTable.Api.register;
        b("searchPanes()", function () {
            return this;
        });
        b("searchPanes.clearSelections()", function () {
            return this.iterator("table", function (e) {
                e._searchPanes && e._searchPanes.clearSelections();
            });
        });
        b("searchPanes.rebuildPane()", function (e, f) {
            return this.iterator("table", function (g) {
                g._searchPanes && g._searchPanes.rebuild(e, f);
            });
        });
        b("searchPanes.resizePanes()", function () {
            var e = this.context[0];
            return e._searchPanes ? e._searchPanes.resizePanes() : null;
        });
        b("searchPanes.container()", function () {
            var e = this.context[0];
            return e._searchPanes ? e._searchPanes.getNode() : null;
        });
        h.fn.dataTable.ext.buttons.searchPanesClear = {
            action: function (e, f) {
                f.searchPanes.clearSelections();
            },
            text: "Clear Panes",
        };
        h.fn.dataTable.ext.buttons.searchPanes = {
            action: function (e, f, g, m) {
                this.popover(m._panes.getNode(), { align: "container", span: "container" });
                m._panes.rebuild(void 0, !0);
            },
            config: {},
            init: function (e, f, g) {
                var m = h.extend(
                    {
                        filterChanged: function (t) {
                            e.button(f).text(e.i18n("searchPanes.collapse", void 0 !== e.context[0].oLanguage.searchPanes ? e.context[0].oLanguage.searchPanes.collapse : e.context[0]._searchPanes.c.i18n.collapse, t));
                        },
                    },
                    g.config
                );
                m = m && (m.cascadePanes || m.viewTotal) ? new h.fn.dataTable.SearchPanesST(e, m) : new h.fn.dataTable.SearchPanes(e, m);
                e.button(f).text(g.text || e.i18n("searchPanes.collapse", m.c.i18n.collapse, 0));
                g._panes = m;
            },
            text: null,
        };
        h(a).on("preInit.dt.dtsp", function (e, f) {
            "dt" === e.namespace && (f.oInit.searchPanes || d.defaults.searchPanes) && (f._searchPanes || c(f, null, !0));
        });
        d.ext.feature.push({ cFeature: "P", fnInit: c });
        d.ext.features && d.ext.features.register("searchPanes", c);
    });
})();
