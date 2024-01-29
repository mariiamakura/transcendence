
// Function to listen to hovering over the title and create 42 balls bouncing up and downs
document.addEventListener("DOMContentLoaded", function() {
    const title = document.getElementById("title");
    
    title.addEventListener("mouseenter", function() {
        const numBalls = 42;
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;
        const rangeTop = windowHeight * 0.02; 
        const rangeBottom = windowHeight * 0.14; 
        const leftMin = windowWidth * 0.2; // Minimum left position (40% of window width)
        const leftMax = windowWidth * 0.60; // Maximum left position (60% of window width)

        for (let i = 1; i <= numBalls; i++) {
            const ball = document.createElement("div");
            ball.className = "ball"; // Add 'ball' class to each ball element
            
            // Generate random positions within specified ranges
            const randomTop = rangeTop + Math.random() * (rangeBottom - rangeTop);
            const randomLeft = leftMin + Math.random() * (leftMax - leftMin);
            
            ball.style.top = `${randomTop}px`; // Adjust top position
            ball.style.left = `${randomLeft}px`; // Adjust left position
            ball.style.zIndex = -1; // Set z-index to place the ball behind other elements
            ball.style.animationDelay = `${i * 0.04}s`; // Delay animation for each ball
            title.appendChild(ball);
        }
    });
    
    title.addEventListener("mouseleave", function() {
        const balls = title.querySelectorAll(".ball");
        balls.forEach(function(ball) {
            ball.remove();
        });
    });
});

