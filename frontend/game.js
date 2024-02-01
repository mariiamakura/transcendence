//set the board size according to the screen size and golden ratio
let boardWidth;
let boardHeight;
let board;
let context;

let keysPressed = {};

//player variables
let playerWidth = 10;
let playerHeight;
let playerVelocityY = 0;

let player1 = {
    x: 10,
    y: null,
    width: playerWidth,
    height: null, 
    velocityY: playerVelocityY
};

let player2 = {
    x: null,
    y: null,
    width: playerWidth,
    height: null,
    velocityY: playerVelocityY
};

let player1Score;
let player2Score;

boardWidth = window.innerWidth / 1.618;
boardHeight = window.innerHeight / 1.618;
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


let startGame;
let tournament;
let singleGame;
let numberPlayers;
let velocity = 2;

function showButton() {

    var main = document.getElementById('content');
    main.innerHTML = '<div id="choice" style="display: flex; flex-direction:column;justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"> <p style="padding-top:  5em;"> Which type of game do you wanna play ? </p>';
    var buttonTournament = document.createElement("button");
    var buttonSingle = document.createElement("button");
    buttonSingle.textContent = "1 vs 1";
    buttonTournament.textContent = "Tournament";
    buttonSingle.classList.add("styled-button")
    buttonTournament.classList.add("styled-button");
    document.getElementById('choice').appendChild(buttonTournament);
    document.getElementById('choice').appendChild(buttonSingle);
    return new Promise(function (resolve) {
        buttonTournament.addEventListener("click", function() {
            resolve(true);
            document.getElementById('choice').remove();
            tournament = true;
        });
        buttonSingle.addEventListener("click", function() {
            resolve(false);
            document.getElementById('choice').remove();
            singleGame = true;
        });
    });
}

function numPlayers() {
    var main = document.getElementById('content');
    main.innerHTML = '<div id="choice" style="display: flex; flex-direction:column;justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"><p style="padding-top: 5em; display: flex; " > How many players do you want to be ? </p>';
    var buttonTwo = document.createElement("button");
    var buttonFour = document.createElement("button");
    buttonTwo.textContent = "2 players";
    buttonFour.textContent = "4 players";
    buttonTwo.classList.add("styled-button")
    buttonFour.classList.add("styled-button");
    document.getElementById('choice').appendChild(buttonTwo);
    document.getElementById('choice').appendChild(buttonFour);
    if (tournament) {
        var buttonEight = document.createElement("button");
        var buttonSixteen= document.createElement("button");
        buttonEight.textContent = "8 players";
        buttonSixteen.textContent = "16 players";
        buttonEight.classList.add("styled-button");
        buttonSixteen.classList.add("styled-button");
        document.getElementById('choice').appendChild(buttonEight);
        document.getElementById('choice').appendChild(buttonSixteen);
    }
    return new Promise(function (resolve) {
        buttonTwo.addEventListener("click", function() {
            resolve(true);
            numberPlayers = 2;
            document.getElementById('choice').remove();
        });
        buttonFour.addEventListener("click", function() {
            resolve(true);
            numberPlayers = 4;
            document.getElementById('choice').remove();
        });
        if (tournament) {
            buttonEight.addEventListener("click", function() {
                resolve(true);
                numberPlayers = 8;
                document.getElementById('choice').remove();
            });
            buttonSixteen.addEventListener("click", function() {
                resolve(true);
                numberPlayers = 16;
                document.getElementById('choice').remove();
            });
        }
    });
}
let namePlayer = [];
function getNamePlayer() {
    var main = document.getElementById('content');
    let i = 1;
    while (i <= numberPlayers) {
        main.innerHTML = '<div id="choice" style="display: flex; flex-direction:column;justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"><p style="padding-top: 5em; display: flex; " > Name of player ' + i + ' : </p>';
        var input = document.createElement("input");
        input.type = "text";
        input.id = "name" + i;
        var Submit = document.createElement("button");
        Submit.textContent = "Submit";
        Submit.classList.add("styled-button");
        document.getElementById('choice').appendChild(input);
        document.getElementById('choice').appendChild(Submit);
        Submit.addEventListener("click", function() {
            namePlayer += input.value;
            document.getElementById('choice').remove();
        });
        i++;
    }
    console.log(namePlayer);
}

async function showGame() {
    startGame = false;
    tournament = false;
    singleGame = false;
    numberPlayers = 0;
    if (await showButton())
    {
        console.log("Tournament");
        if (await numPlayers())
        {
            console.log(numberPlayers);
            getNamePlayer();
        }
    }
    else
    {
        console.log("Single");
        if (await numPlayers())
        {
            console.log(numberPlayers);
            getNamePlayer();
        }
    }
    if (namePlayer != 0)
        launchGame();


    
    // Update the URL without reloading the page
    // history.pushState({ page: 'game' }, 'Game', '/game');
}

function startButton() {
    const startButton = document.createElement("button");
    startButton.textContent = "Start";
    startButton.addEventListener("click", launchGame);
    document.getElementById('content').appendChild(startButton);
}

function launchGame() {
    // resize the board when the window is resized and adjust the player
    player1Score = 0;
    player2Score = 0;
    // Create the board element in the HTML and update the CSS of main
    var mainElement = document.getElementById('content');
    boardWidth = window.innerWidth / 1.618;
    boardHeight = window.innerHeight / 1.618;
    if (boardHeight >= boardWidth / 1.618)
        boardHeight = boardWidth / 1.618;
    playerHeight = boardHeight / 5;
    ball.radius = playerHeight / ballRadiusFactor;
    player1.height = playerHeight;
    player2.height = playerHeight;
    ball.velocityX = Math.cos(generateRandomAngle()) * boardWidth / 200 * velocity;
    ball.velocityY = Math.sin(generateRandomAngle()) * boardHeight / 100 * generateRandomNumber() * velocity;

    document.body.style.overflow = 'padding-bottom : 5em';
    
    mainElement.innerHTML = '<div id="board-container" style="display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"><canvas id="board" width="' + boardWidth + '" height="' + boardHeight + '"></canvas></div>';    // Set up the canvas
    mainElement.style.display = 'flex';
    mainElement.style.flexDirection = 'column';
    mainElement.style.justifyContent = 'center';
    mainElement.style.alignItems = 'center';
    board = document.getElementById('board');
    context = board.getContext('2d'); // 2d rendering context
    
    // set players
    player1.y = board.height / 2 - playerHeight / 2;
    player2.x = board.width - playerWidth - 10;
    player2.y = board.height / 2 - playerHeight / 2;
    
    //set ball
    ball.x = board.width / 2;
    ball.y = board.height / 2;
    
    // Draw players
    context.fillStyle = "skyblue";
    context.fillRect(player1.x, player1.y, player1.width, player1.height);
    context.fillRect(player2.x, player2.y, player2.width, player2.height);
    
    requestAnimationFrame(update);
    // Event listener if key is pressed or release
    document.addEventListener("keydown", function(event) {
        keysPressed[event.code] = true;
        movePlayer();
    });
    
    document.addEventListener("keyup", function(event) {
        keysPressed[event.code] = false;
        movePlayer();
    });
}

function handleResize() {
    boardWidth = window.innerWidth / 1.618;
    boardHeight = window.innerHeight / 1.618;
    if (boardHeight >= boardWidth / 1.618)
    {
        boardHeight = boardWidth / 1.618;
        document.body.style.paddingBottom = '10em';
    }
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
    window.addEventListener('resize', handleResize);
    requestAnimationFrame(update);
    context.clearRect(0, 0, board.width, board.height);
    context.fillStyle = "skyblue";
    let newYPosition = player1.y + player1.velocityY;
    if (!outOfBounds(newYPosition)) {
        player1.y = newYPosition;
    }
    context.fillRect(player1.x, player1.y, player1.width, player1.height);
    let newYPosition2 = player2.y + player2.velocityY;
    if (!outOfBounds(newYPosition2)) {
        player2.y = newYPosition2;
    }boardWidth
    context.fillRect(player2.x, player2.y, player2.width, player2.height);

    //ball
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    context.beginPath();
    context.arc(ball.x + ball.radius, ball.y + ball.radius, ball.radius, 0, Math.PI * 2);
    context.fillStyle = "white";
    context.fill();
    
    if (ball.y <= 0 || ball.y + ball.height >= board.height) {
        ball.velocityY *= -1;
    }
    if (detectCollision(ball, player1) || detectCollision(ball, player2)) {
        if (ball.x <= player1.x + player1.width || ball.x + ball.width >= player2.x)
            ball.velocityX *= -1;
    }
    if (ball.x < 0) {
        player2Score++;
        resetGame(1);
    } 
    else if (ball.x + ball.width > board.width) {
        player1Score++;
        resetGame(-1);
    }

    context.font = "45px sans-serif";
    context.fillText(player1Score, boardWidth / 5, 45);
    context.fillText(player2Score, boardWidth * 4/5 -45, 45);
    for (let i = 0; i < board.height; i += 25) {
        context.fillRect(board.width / 2 - 10, i, 5, 5);
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
    if (keysPressed["KeyW"]) {
        player1.velocityY = -3;
    } else if (keysPressed["KeyS"]) {
        player1.velocityY = 3;
    } else {
        player1.velocityY = 0; // Stop movement if no key is pressed
    }

    // Player 2 controls
    if (keysPressed["ArrowUp"])
        player2.velocityY = -3;
    else if (keysPressed["ArrowDown"])
        player2.velocityY = 3;
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

    ball.velocityX = Math.cos(generateRandomAngle()) * boardWidth / 200 * direction * velocity;
    ball.velocityY = Math.sin(generateRandomAngle()) * boardHeight / 100 * generateRandomNumber() * velocity;
}