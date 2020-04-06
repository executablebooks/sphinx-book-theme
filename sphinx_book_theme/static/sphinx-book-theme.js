var initTriggerSidebar = () => {
    console.log($(window).width())
    if ($(window).width() < 768) {
        $("#navbar-toggler").trigger("click")
    }    
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
