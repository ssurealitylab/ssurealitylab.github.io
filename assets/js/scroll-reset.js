// Scroll position preservation - Enhanced version
(function() {
    'use strict';
    
    // Store scroll position
    var savedScrollPosition = 0;
    var isManualScroll = false;
    
    // Save scroll position during user interaction
    function saveScrollPosition() {
        savedScrollPosition = window.pageYOffset || document.documentElement.scrollTop || 0;
        isManualScroll = true;
    }
    
    // Restore scroll position
    function restoreScrollPosition() {
        if (isManualScroll && savedScrollPosition > 0) {
            // Disable smooth scrolling temporarily for restoration
            var originalBehavior = document.documentElement.style.scrollBehavior;
            document.documentElement.style.scrollBehavior = 'auto';
            
            window.scrollTo(0, savedScrollPosition);
            document.documentElement.scrollTop = savedScrollPosition;
            document.body.scrollTop = savedScrollPosition;
            
            // Restore smooth behavior
            setTimeout(function() {
                document.documentElement.style.scrollBehavior = originalBehavior || 'smooth';
            }, 100);
        }
    }
    
    // Listen for user scroll events
    var scrollTimer;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(saveScrollPosition, 50);
    }, { passive: true });
    
    // Save position on user interactions
    ['mousewheel', 'wheel', 'touchstart', 'keydown'].forEach(function(event) {
        window.addEventListener(event, saveScrollPosition, { passive: true });
    });
    
    // Restore position on page events
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(restoreScrollPosition, 100);
        });
    }
    
    window.addEventListener('load', function() {
        setTimeout(restoreScrollPosition, 100);
        setTimeout(restoreScrollPosition, 200);
    });
    
    // Handle back/forward button
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            setTimeout(restoreScrollPosition, 50);
        }
    });
    
    // Save position before leaving
    window.addEventListener('beforeunload', function() {
        saveScrollPosition();
    });
})();