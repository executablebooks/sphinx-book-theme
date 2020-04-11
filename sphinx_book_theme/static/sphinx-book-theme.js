// Sidebar toggle button
var initTriggerSidebar = () => {
    if ($(window).width() < 768) {
        $("#navbar-toggler").trigger("click")
    }
}


// Sidebar scrolling
var scrollToActive = () => {
  var sidebar = document.getElementById('site-navigation')
  var active_pages = sidebar.querySelectorAll(".active")
  var active_page = active_pages[active_pages.length-1]
  sidebar.scrollTop = active_page.offsetTop - ($(window).height() * .2)
}

// Helper function to run when the DOM is finished
var sbRunWhenDOMLoaded = cb => {
    if (document.readyState != 'loading') {
      cb()
    } else if (document.addEventListener) {
      document.addEventListener('DOMContentLoaded', cb)
    } else {
      document.attachEvent('onreadystatechange', function() {
        if (document.readyState == 'complete') cb()
      })
    }
}

sbRunWhenDOMLoaded(initTriggerSidebar)
sbRunWhenDOMLoaded(scrollToActive)
