const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");

// Paddles
const paddleWidth = 10, paddleHeight = 60;
let player1Y = (canvas.height - paddleHeight) / 2;
let player2Y = (canvas.height - paddleHeight) / 2;
const paddleSpeed = 5;

// Ball
const ballSize = 10;
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;
let ballSpeedX = 3;
let ballSpeedY = 3;

// Event listeners for paddle movement
document.addEventListener("keydown", movePaddle);
document.addEventListener("keyup", stopPaddle);

function movePaddle(event) {
    if (event.key === "ArrowUp" && player1Y > 0) {
        player1Y -= paddleSpeed;
    } else if (event.key === "ArrowDown" && player1Y < canvas.height - paddleHeight) {
        player1Y += paddleSpeed;
    } else if (event.key === "w" && player2Y > 0) {
        player2Y -= paddleSpeed;
    } else if (event.key === "s" && player2Y < canvas.height - paddleHeight) {
        player2Y += paddleSpeed;
    }
}

function stopPaddle(event) {
    // You can add additional logic here if needed
}

function drawPaddles() {
    // Draw player 1 paddle
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(0, player1Y, paddleWidth, paddleHeight);

    // Draw player 2 paddle
    ctx.fillRect(canvas.width - paddleWidth, player2Y, paddleWidth, paddleHeight);
}

function drawBall() {
    ctx.fillStyle = "#00FF00";
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballSize, 0, Math.PI * 2);
    ctx.fill();
}

function moveBall() {
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    // Add collision logic for walls
    if (ballY - ballSize < 0 || ballY + ballSize > canvas.height) {
        ballSpeedY = -ballSpeedY;
    }

    // Add collision logic for paddles
    if (
        (ballX - ballSize < paddleWidth && ballY > player1Y && ballY < player1Y + paddleHeight) ||
        (ballX + ballSize > canvas.width - paddleWidth && ballY > player2Y && ballY < player2Y + paddleHeight)
    ) {
        ballSpeedX = -ballSpeedX;
    }
}

function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw paddles
    drawPaddles();

    // Draw ball
    drawBall();

    // Move ball
    moveBall();

    // Call draw function every 10 milliseconds
    requestAnimationFrame(draw);
}

// Call draw function to start the game loop
draw();