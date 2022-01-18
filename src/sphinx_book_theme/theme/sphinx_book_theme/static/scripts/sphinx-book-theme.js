!(function (t) {
  var e = {};
  function o(n) {
    if (e[n]) return e[n].exports;
    var r = (e[n] = { i: n, l: !1, exports: {} });
    return t[n].call(r.exports, r, r.exports, o), (r.l = !0), r.exports;
  }
  (o.m = t),
    (o.c = e),
    (o.d = function (t, e, n) {
      o.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: n });
    }),
    (o.r = function (t) {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(t, "__esModule", { value: !0 });
    }),
    (o.t = function (t, e) {
      if ((1 & e && (t = o(t)), 8 & e)) return t;
      if (4 & e && "object" == typeof t && t && t.__esModule) return t;
      var n = Object.create(null);
      if (
        (o.r(n),
        Object.defineProperty(n, "default", { enumerable: !0, value: t }),
        2 & e && "string" != typeof t)
      )
        for (var r in t)
          o.d(
            n,
            r,
            function (e) {
              return t[e];
            }.bind(null, r)
          );
      return n;
    }),
    (o.n = function (t) {
      var e =
        t && t.__esModule
          ? function () {
              return t.default;
            }
          : function () {
              return t;
            };
      return o.d(e, "a", e), e;
    }),
    (o.o = function (t, e) {
      return Object.prototype.hasOwnProperty.call(t, e);
    }),
    (o.p = ""),
    o((o.s = 0));
})([
  function (t, e, o) {
    t.exports = o(1);
  },
  function (t, e, o) {
    "use strict";
    o.r(e);
    o.p;
    var n = (t) => {
      "loading" != document.readyState
        ? t()
        : document.addEventListener
        ? document.addEventListener("DOMContentLoaded", t)
        : document.attachEvent("onreadystatechange", function () {
            "complete" == document.readyState && t();
          });
    };
    n(() => {
      $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
      });
    }),
      n(() => {
        var t = document.getElementById("site-navigation"),
          e = t.querySelectorAll(".active"),
          o = e[e.length - 1];
        void 0 !== o &&
          o.offsetTop > 0.5 * $(window).height() &&
          (t.scrollTop = o.offsetTop - 0.2 * $(window).height());
      }),
      n(() => {
        var t,
          e =
            $("#bd-toc-nav").outerHeight(!0) +
            $(".bd-toc").outerHeight(!0) +
            200;
        $(window).on("scroll", function () {
          t ||
            (t = setTimeout(function () {
              $(
                ".margin, .tag_margin, .full-width, .full_width, .tag_full-width, .tag_full_width, .sidebar, .tag_sidebar, .popout, .tag_popout"
              ).each((t, o) => {
                var n = $(o).offset().top - $(window).scrollTop(),
                  r = n + $(o).outerHeight(!0);
                if (n < e && r >= 0 && window.pageYOffset > 20)
                  return $("div.bd-toc").removeClass("show"), !1;
                $("div.bd-toc").addClass("show");
              }),
                window.scrollY > 0
                  ? document.body.classList.add("scrolled")
                  : document.body.classList.remove("scrolled"),
                (t = null);
            }, 200));
        });
      });
  },
]);
