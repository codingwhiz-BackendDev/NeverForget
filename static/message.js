document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.message').forEach(function(msg) {
        setTimeout(function() {
            msg.classList.remove('message');
            setTimeout(function() {
                msg.remove();
            }, 1000); // Remove after fade-out animation
        }, 5000); // 5 seconds
    });
}); 