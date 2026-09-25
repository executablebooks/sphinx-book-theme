/**
 * Unit tests for fixSidebarToggle (executablebooks/sphinx-book-theme#935).
 *
 * When navbar_* is non-empty, pydata-sphinx-theme emits a hidden navbar
 * .primary-toggle earlier in the DOM than the visible article-header button.
 * querySelector('.primary-toggle') binds only the first (hidden) node.
 */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");

const ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const INDEX_JS = path.join(
  ROOT,
  "src/sphinx_book_theme/assets/scripts/index.js",
);

function extractFixSidebarToggleSource() {
  const src = readFileSync(INDEX_JS, "utf8");
  const start = src.indexOf("function fixSidebarToggle");
  if (start < 0) {
    throw new Error("function fixSidebarToggle not found in index.js");
  }
  let depth = 0;
  let started = false;
  let end = start;
  for (let i = start; i < src.length; i++) {
    if (src[i] === "{") {
      depth += 1;
      started = true;
    } else if (src[i] === "}") {
      depth -= 1;
      if (started && depth === 0) {
        end = i + 1;
        break;
      }
    }
  }
  return src.slice(start, end);
}

const FIX_SIDEBAR_TOGGLE_SRC = extractFixSidebarToggleSource();

function stubMatchMedia(window, isWide) {
  window.matchMedia = (query) => ({
    matches: Boolean(isWide && /min-width:\s*992px/.test(query)),
    media: query,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent() {
      return false;
    },
  });
}

function setupDom({ navbarToggles = true, isWide = true } = {}) {
  const navbar = navbarToggles
    ? `
      <header class="bd-header">
        <button class="pst-navbar-icon sidebar-toggle primary-toggle" type="button">navbar primary</button>
        <button class="pst-navbar-icon sidebar-toggle secondary-toggle" type="button">navbar secondary</button>
      </header>`
    : `<header class="bd-header"></header>`;

  const dom = new JSDOM(
    `<!DOCTYPE html>
    <html>
      <body>
        ${navbar}
        <div class="bd-header-article">
          <div class="header-article-item">
            <button class="sidebar-toggle primary-toggle btn btn-sm" type="button">article primary</button>
          </div>
          <div class="header-article-item">
            <button class="sidebar-toggle secondary-toggle btn btn-sm" type="button">article secondary</button>
          </div>
        </div>
        <aside id="pst-primary-sidebar"></aside>
        <aside id="pst-secondary-sidebar"></aside>
        <dialog id="pst-primary-sidebar-modal"></dialog>
        <dialog id="pst-secondary-sidebar-modal"></dialog>
      </body>
    </html>`,
    {
      pretendToBeVisual: true,
      url: "https://example.test/",
      runScripts: "dangerously",
    },
  );

  stubMatchMedia(dom.window, isWide);
  dom.window.eval(`${FIX_SIDEBAR_TOGGLE_SRC}; fixSidebarToggle();`);
  return dom;
}

function click(window, el) {
  const event = new window.MouseEvent("click", {
    bubbles: true,
    cancelable: true,
  });
  el.dispatchEvent(event);
  return event;
}

test("(A) navbar_center + desktop: article-header primary-toggle hides primary sidebar", () => {
  const dom = setupDom({ navbarToggles: true, isWide: true });
  const { document } = dom.window;
  const toggles = document.querySelectorAll(".primary-toggle");
  assert.equal(
    toggles.length,
    2,
    "navbar toggle must precede article-header toggle",
  );
  assert.ok(toggles[0].closest(".bd-header"));
  assert.ok(toggles[1].closest(".bd-header-article"));

  const articleToggle = document.querySelector(
    ".bd-header-article .primary-toggle",
  );
  const sidebar = document.querySelector("#pst-primary-sidebar");
  assert.equal(sidebar.classList.contains("pst-sidebar-hidden"), false);

  click(dom.window, articleToggle);
  assert.equal(
    sidebar.classList.contains("pst-sidebar-hidden"),
    true,
    "visible article-header Toggle Sidebar must toggle the primary sidebar",
  );

  click(dom.window, articleToggle);
  assert.equal(
    sidebar.classList.contains("pst-sidebar-hidden"),
    false,
    "a second click must show the primary sidebar again",
  );

  const navbarToggle = document.querySelector(".bd-header .primary-toggle");
  click(dom.window, navbarToggle);
  assert.equal(
    sidebar.classList.contains("pst-sidebar-hidden"),
    true,
    "each .primary-toggle is bound, including the earlier navbar button",
  );
});

test("(B) navbar_center + desktop: article-header secondary-toggle hides secondary sidebar", () => {
  const dom = setupDom({ navbarToggles: true, isWide: true });
  const { document } = dom.window;
  const toggles = document.querySelectorAll(".secondary-toggle");
  assert.equal(toggles.length, 2);
  assert.ok(toggles[0].closest(".bd-header"));
  assert.ok(toggles[1].closest(".bd-header-article"));

  const articleToggle = document.querySelector(
    ".bd-header-article .secondary-toggle",
  );
  const sidebar = document.querySelector("#pst-secondary-sidebar");
  assert.equal(sidebar.classList.contains("pst-sidebar-hidden"), false);

  click(dom.window, articleToggle);
  assert.equal(
    sidebar.classList.contains("pst-sidebar-hidden"),
    true,
    "visible article-header secondary toggle must toggle the secondary sidebar",
  );
});

test("(C) empty navbar_*: only article-header primary-toggle still works on desktop", () => {
  const dom = setupDom({ navbarToggles: false, isWide: true });
  const { document } = dom.window;
  assert.equal(document.querySelectorAll(".primary-toggle").length, 1);
  assert.ok(document.querySelector(".bd-header-article .primary-toggle"));

  const articleToggle = document.querySelector(
    ".bd-header-article .primary-toggle",
  );
  const sidebar = document.querySelector("#pst-primary-sidebar");
  click(dom.window, articleToggle);
  assert.equal(sidebar.classList.contains("pst-sidebar-hidden"), true);
});

test("(D) narrow/mobile: article-header primary-toggle does not intercept the dialog path", () => {
  const dom = setupDom({ navbarToggles: true, isWide: false });
  const { document } = dom.window;
  const articleToggle = document.querySelector(
    ".bd-header-article .primary-toggle",
  );
  const sidebar = document.querySelector("#pst-primary-sidebar");

  let bubbleReached = false;
  articleToggle.addEventListener("click", () => {
    bubbleReached = true;
  });

  const event = click(dom.window, articleToggle);
  assert.equal(
    sidebar.classList.contains("pst-sidebar-hidden"),
    false,
    "narrow viewport must not collapse via pst-sidebar-hidden",
  );
  assert.equal(event.defaultPrevented, false);
  assert.equal(
    bubbleReached,
    true,
    "capture handler must not stopImmediatePropagation so PST can open the dialog",
  );
});
