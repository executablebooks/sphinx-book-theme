// Import CSS variables
// ref: https://css-tricks.com/getting-javascript-to-talk-to-css-and-sass/
import "../styles/index.scss";

// NavBar scrolling
var scrollToActive = () => {
  var navbar = document.getElementById("site-navigation");
  var active_pages = navbar.querySelectorAll(".active");
  var active_page = active_pages[active_pages.length - 1];
  // Only scroll the navbar if the active link is lower than 50% of the page
  if (
    active_page !== undefined &&
    active_page.offsetTop > $(window).height() * 0.5
  ) {
    navbar.scrollTop = active_page.offsetTop - $(window).height() * 0.2;
  }
};

// Helper function to run when the DOM is finished
var sbRunWhenDOMLoaded = (cb) => {
  if (document.readyState != "loading") {
    cb();
  } else if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", cb);
  } else {
    document.attachEvent("onreadystatechange", function () {
      if (document.readyState == "complete") cb();
    });
  }
};

// Toggle full-screen with button
// Safari requires a `webkit` prefix, so this uses conditionals to check for that
// ref: https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API
var toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    } else if (document.documentElement.webkitRequestFullscreen) {
      document.documentElement.webkitRequestFullscreen();
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
};

// Enable tooltips
var initTooltips = () => {
  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
};

/**
 * Hide the Table of Contents any time sidebar content is on the screen.
 *
 * This will be triggered any time a sidebar item enters or exits the screen.
 * It adds/removes items from an array if they have entered the screen, and
 * removes them when they exit the screen. It hides the TOC if anything is
 * on-screen.
 *
 * ref: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
 */
var initTocHide = () => {
  var onScreenItems = [];
  let hideTocCallback = (entries, observer) => {
    // Check whether any sidebar item is displayed
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // If an element just came on screen, add it our list
        onScreenItems.push(entry.target);
      } else {
        // Otherwise, if it's in our list then remove it
        for (let ii = 0; ii < onScreenItems.length; ii++) {
          if (onScreenItems[ii] === entry.target) {
            onScreenItems.splice(ii, 1);
            break;
          }
        }
      }
    });

    // Hide the TOC if any margin content is displayed on the screen
    if (onScreenItems.length > 0) {
      $("div.bd-toc").removeClass("show");
    } else {
      $("div.bd-toc").addClass("show");
    }
  };
  let manageScrolledClassOnBody = (entries, observer) => {
    // The pixel is at the top, so if we're < 0 that it means we've scrolled
    if (entries[0].boundingClientRect.y < 0) {
      document.body.classList.add("scrolled");
    } else {
      document.body.classList.remove("scrolled");
    }
  };

  // Set up the intersection observer to watch all margin content
  let tocObserver = new IntersectionObserver(hideTocCallback);
  const selectorClasses = [
    "margin",
    "margin-caption",
    "full-width",
    "sidebar",
    "popout",
  ];
  let marginSelector = [];
  selectorClasses.forEach((ii) => {
    // Use three permutations of each class name because `tag_` and `_` used to be supported
    marginSelector.push(
      ...[
        `.${ii}`,
        `.tag_${ii}`,
        `.${ii.replace("-", "_")}`,
        `.tag_${ii.replace("-", "_")}`,
      ]
    );
  });
  document.querySelectorAll(marginSelector.join(", ")).forEach((ii) => {
    tocObserver.observe(ii);
  });

  // Set up the observer to check if we've scrolled from top of page
  let scrollObserver = new IntersectionObserver(manageScrolledClassOnBody);
  scrollObserver.observe(document.querySelector(".sbt-scroll-pixel-helper"));
};

var printPdf = (el) => {
  // Detach the tooltip text from DOM to hide in PDF
  // and then reattach it for HTML
  let tooltipID = $(el).attr("aria-describedby");
  let tooltipTextDiv = $("#" + tooltipID).detach();
  window.print();
  $("body").append(tooltipTextDiv);
};

var initThebeSBT = () => {
  var title = $("div.section h1")[0];
  if (!$(title).next().hasClass("thebe-launch-button")) {
    $("<button class='thebe-launch-button'></button>").insertAfter($(title));
  }
  initThebe();
};

window.initThebeSBT = initThebeSBT;
window.printPdf = printPdf;
window.toggleFullScreen = toggleFullScreen;

sbRunWhenDOMLoaded(initTooltips);
sbRunWhenDOMLoaded(scrollToActive);
sbRunWhenDOMLoaded(initTocHide);
