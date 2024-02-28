//set the board size according to the screen size and golden ratio
let boardWidth;
let boardHeight;
let board;
let context;
let velocity = 2;
let keysPressed = {};
let spaceKeyListenerAdded;
let gameEnded;

//player variables
let playerWidth = 10;
let playerHeight;
let playerVelocityY = 0;

let player1 = {
    x: 10,
    y: null,
    width: playerWidth,
    height: null, 
    velocityY: playerVelocityY,
    name: null
};

let player2 = {
    x: null,
    y: null,
    width: playerWidth,
    height: null,
    velocityY: playerVelocityY,
    name: null
};

let player1Score;
let player2Score;

//ball variables
let ballWidth = 10;
let ballHeight = 10;
let ballRadiusFactor = 10;
let ball = {
    x : null,
    y : null,
    width : ballWidth,
    height : ballHeight,
    radius: null,
    velocityX : null,
    velocityY : null
}

function initVariables() {
    spaceKeyListenerAdded = false;
    gameEnded = false;
    player1Score = 0;
    player2Score = 0;
    velocity = 2;
    playerVelocityY = 0;
    boardWidth = window.innerWidth / 1.618;
    boardHeight = window.innerHeight / 1.618;
    ball.velocityX = Math.cos(generateRandomAngle()) * boardWidth / 200 * velocity;
    ball.velocityY = Math.sin(generateRandomAngle()) * boardHeight / 100 * generateRandomNumber() * velocity;
    if (boardHeight >= boardWidth / 1.618)
        boardHeight = boardWidth / 1.618;
    playerHeight = boardHeight / 5;
    ball.radius = playerHeight / ballRadiusFactor;
    player1.height = playerHeight;
    player2.height = playerHeight;    
}

function launchGamePong() {
    initVariables();
    var mainElement = document.getElementById('content');
    if (!namePlayer[0] || !namePlayer[1])
    {
        namePlayer[0] = "Player1";
        namePlayer[1] = "Player2";
    }
    let htmlContent = '<div id="board-container" style="display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden">' +
    '<p class="name_player">' + namePlayer[0] + '</p>' +
    '<canvas id="board" width="' + boardWidth + '" height="' + boardHeight + '"></canvas>' +
    '<p class="name_player">' + namePlayer[1] + '</p>' +
    '</div>';

    mainElement.innerHTML = htmlContent;
    document.body.style.overflow = 'padding-bottom : 5em';
    board = document.getElementById('board');
    board.width = boardWidth;
    board.height = boardHeight;
    context = board.getContext('2d'); // 2d rendering context
    
    // Draw players
    player1.y = board.height / 2 - playerHeight / 2;
    player2.x = board.width - playerWidth - 10;
    player2.y = board.height / 2 - playerHeight / 2;
    player1.name = namePlayer[0];
    player2.name = namePlayer[1];
    //set ball
    ball.x = board.width / 2;
    ball.y = board.height / 2;
    context.fillStyle = "skyblue";
    context.fillRect(player1.x, player1.y, player1.width, player1.height);
    context.fillRect(player2.x, player2.y, player2.width, player2.height);
    requestAnimationFrame(update);
    // Event listener if key is pressed or release
    document.addEventListener("keydown", function(event) {
        keysPressed[event.code] = true;
        event.preventDefault();
        movePlayer();
    });
    
    document.addEventListener("keyup", function(event) {
        keysPressed[event.code] = false;
        event.preventDefault();
        movePlayer();
    });
}

function handleResize() {
    boardWidth = window.innerWidth / 1.618;
    boardHeight = window.innerHeight / 1.618;
    if (boardHeight >= boardWidth / 1.618)
        boardHeight = boardWidth / 1.618;
    board.width = boardWidth;
    board.height = boardHeight;
    playerHeight = boardHeight / 5;
    player1.height = playerHeight;
    player2.height = playerHeight;
    player1.y = board.height / 2 - playerHeight / 2;
    player2.x = board.width - playerWidth - 10;
    player2.y = board.height / 2 - playerHeight / 2;
    
    //variables for ball
    ball.radius = playerHeight / ballRadiusFactor;
    ball.x = board.width / 2;
    ball.y = board.height / 2;
    ball.velocityX = Math.cos(generateRandomAngle()) * boardWidth / 200  * velocity;
    ball.velocityY = Math.sin(generateRandomAngle()) * boardHeight / 100 * generateRandomNumber() * velocity;
}

function update() {
    // Update the game
    if (gameEnded === true)
        return;
    console.log("update");
    window.addEventListener('resize', handleResize);
    requestAnimationFrame(update);
    context.clearRect(0, 0, board.width, board.height);
    context.fillStyle = "skyblue";

    let newYPosition = player1.y + player1.velocityY;
    if (!outOfBounds(newYPosition))
        player1.y = newYPosition;
    context.fillRect(player1.x, player1.y, player1.width, player1.height);
    
    let newYPosition2 = player2.y + player2.velocityY;
    if (!outOfBounds(newYPosition2))
        player2.y = newYPosition2;
    context.fillRect(player2.x, player2.y, player2.width, player2.height);

    //ball
    context.beginPath();
    context.arc(ball.x + ball.radius, ball.y + ball.radius, ball.radius, 0, Math.PI * 2);
    context.fillStyle = "white";
    context.fill();
    
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    if (ball.y <= 0 || ball.y + ball.height >= board.height) {
        ball.velocityY *= -1;
    }
    checkCollision(ball.y, ball.x);
    if (ball.x < 0) {
        player2Score++;
        if (player2Score >= scoreToDo)
            endGame(player2.name);
        else
            resetGame(1);
    } 
    else if (ball.x + ball.width > board.width) {
        player1Score++;
        if (player1Score >= scoreToDo)
            endGame(player1.name);
        else
            resetGame(-1);
    }
    context.font = "45px sans-serif";
    context.fillText(player1Score, boardWidth / 5, 45);
    context.fillText(player2Score, boardWidth * 4/5 -45, 45);
    for (let i = 0; i < board.height; i += 25) {
        context.fillRect(board.width / 2 - 10, i, 5, 5);
    }
}

function checkCollision(ballY, ballX) {
    ballX -= 5;
    let LoclPad1XPos = player1.x + player1.width / 2;
    let distance1 = Math.abs(ballX - LoclPad1XPos);
    
    if (distance1 < 5 && ballY > (player1.y - playerWidth) && player1.y + player1.height + playerWidth > ballY) {
        ball.velocityX *= -1; // Reverse the x velocity
    }
    
    ballX += 10;
    let LoclPad2XPos = player2.x;
    let distance2 = Math.abs(ballX - LoclPad2XPos);
    
    if (distance2 < 5 && ballY > (player2.y - playerWidth) && player2.y + player2.height + playerWidth > ballY) {
        ball.velocityX *= -1; // Reverse the x velocity
    }
}

function outOfBounds(yPosition) {
    return (yPosition < 0 || yPosition > boardHeight - playerHeight);
}

function detectCollision(a, b) {
    return (a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y);
}

function movePlayer() {
    // Player 1 controls
    let newVelocity = 10;
    if (keysPressed["KeyW"]) {
        player1.velocityY = -newVelocity;
    } else if (keysPressed["KeyS"]) {
        player1.velocityY = newVelocity;
    } else {
        player1.velocityY = 0; // Stop movement if no key is pressed
    }
    
    // Player 2 controls
    if (keysPressed["ArrowUp"])
        player2.velocityY = -newVelocity;
    else if (keysPressed["ArrowDown"])
        player2.velocityY = newVelocity;
    else
        player2.velocityY = 0; // Stop movement if no key is pressed
}

function generateRandomAngle() {
    var minAngle = 30 * Math.PI / 180; // Convert degrees to radians
    var maxAngle = 150 * Math.PI / 180; // Convert degrees to radians
    var randomAngle = Math.random() * (maxAngle - minAngle) + minAngle;
    if (randomAngle > 1.2 && randomAngle < 1.8)
        randomAngle += 1;
    return randomAngle;
}

function generateRandomNumber() {
    var random = Math.random();
    if (random > 0.5)
        random = 1;
    else
        random = -1;
    return random;
}

function resetGame(direction)
{
    ball.x = board.width / 2 - ballWidth / 2;
    ball.y = Math.random() * (board.height -10);
    // Reset ball velocity
    
    ball.velocityX = Math.cos(generateRandomAngle()) * board.width / 200 * direction * velocity;
    ball.velocityY = Math.sin(generateRandomAngle()) * board.height / 100 * generateRandomNumber() * velocity;
}

function endGame(winner) {
    gameEnded = true;   
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = ''; // Remove all inner HTML content  
    mainElement.innerHTML = '<div id="endGame" style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; overflow: hidden;">' +
    '<p style="text-align: center; font-size:4em;">Game Over ! </p>' +
    '<iframe src="https://giphy.com/embed/OScDfyJIQaXe" width="480" height="480" frameborder="0" class="giphy-embed" allowfullscreen></iframe>' +
    '<p><a href="https://giphy.com/gifs/rabbids-dance-cute-OScDfyJIQaXe"></a></p>' +
    '<p style="text-align: center;">' + winner + ' won ! <br><br> If you want to play again with the same settings, press the button below.</p>' +
    '</div>';
    var startAgain = document.createElement("button");
    startAgain.textContent = "Start again";
    startAgain.classList.add("styled-button")
    document.getElementById('endGame').appendChild(startAgain);
    startAgain.addEventListener("click", function() {
        player1Score = 0;
        player2Score = 0;
        launchGamePong();
    });
    
}