let startGame;
let tournament;
let singleGame;
let numberPlayers;

function showButton() {

    var main = document.getElementById('content');
    main.innerHTML += '<div id="choice"><p style="padding-top: 2em;"> Which type of game do you wanna play ? </p></div>';
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
    main.innerHTML += '<div id="choice"><p style="padding-top: 2em; display: flex; " > How many players do you want to be ? </p></div>';
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

function submitButton(submit) {
    return new Promise(function (resolve) {
        submit.addEventListener("click", function() {
            resolve(true);
        });
    });
}


async function getNamePlayer() {
    var main = document.getElementById('content');
    let i = 1;
    while (i <= numberPlayers) {
        main.innerHTML += '<div id="choice">' + 
            '<form style="display: flex; flex-direction: column; align-items: center;">' +
                '<p style="padding-top: 2em; display: flex; align-items:center; justify-content:center;" > Name of player ' + i + ' : </p>' +
                '<input type="text" id="name' + i + '">' +
                '<button type="submit" class="styled-button" style="margin-top: 1em;">Submit</button>' +
            '</form>' +
        '</div>';
        const Submit = main.querySelector('#choice:last-child button');
        const input = main.querySelector('#choice:last-child input');
        const isSubmitted = await submitButton(Submit);
        if (isSubmitted === true && input.value !== "") {
            namePlayer.push(input.value);
            main.querySelector('#choice:last-child').remove();
            i++;
        }
    }
}
   
let scoreToDo = 0;
let debugPong = 2; // 1 not debug. 2 is directly the game, 3 is the menu and the score todo will be 1 instead of 12

function scoreChoice() {
    var main = document.getElementById('content');
    main.innerHTML += `<div id="choice"><p style="padding-top: 2em; display: flex; " > Chose how many points wins: </p></div>`;
    var unlimited = document.createElement("button");
    unlimited.textContent = "Unlimited";
    unlimited.classList.add("styled-button");
    document.getElementById('choice').appendChild(unlimited);
    var scoreTwelve = document.createElement("button");
    scoreTwelve.textContent = "12";
    scoreTwelve.classList.add("styled-button");
    document.getElementById('choice').appendChild(scoreTwelve);
    var scoreEighteen = document.createElement("button");
    scoreEighteen.textContent = "18";
    scoreEighteen.classList.add("styled-button");
    document.getElementById('choice').appendChild(scoreEighteen);
    var scoreTwentyFour = document.createElement("button");
    scoreTwentyFour.textContent = "24";
    scoreTwentyFour.classList.add("styled-button");
    document.getElementById('choice').appendChild(scoreTwentyFour);
    return new Promise(function (resolve) {
        unlimited.addEventListener("click", function() {
            resolve(true);
            scoreToDo = -1;
            document.getElementById('choice').remove();
        });
        scoreTwelve.addEventListener("click", function() {
            resolve(true);
            if (debugPong === 3)
                scoreToDo = 12;
            else
                scoreToDo = 12;
            document.getElementById('choice').remove();
        });
        scoreEighteen.addEventListener("click", function() {
            resolve(true);
            scoreToDo = 18;
            document.getElementById('choice').remove();
        });
        scoreTwentyFour.addEventListener("click", function() {
            resolve(true);
            scoreToDo = 24;
            document.getElementById('choice').remove();
        });
    });
}

function startButton() {
    var main = document.getElementById('content');
    main.innerHTML += '<div id="choice"><p style="text-align: center; padding-top:5em;"> Ready to start ? <br> <br> Let\'s go !</p></div>';
    var startButton = document.createElement("button");
    startButton.textContent = "Start !";
    startButton.classList.add("styled-button");
    document.getElementById('choice').appendChild(startButton);
    return new Promise (function (resolve) {
        startButton.addEventListener("click", function() {
            startGame = true;
            document.getElementById('choice').remove();
            resolve(true);
        });
    });
}

async function showGamePong() {
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = '<p style="display: flex; text-align: center; justify-content:center; font-size: 3em;">Pong</p>';
    gameEnded = true;
    if (debugPong === 2)
    {
        scoreToDo = 12;
        launchGamePong();
    }
    else
    {
        startGame = false;
        tournament = false;
        singleGame = false;
        numberPlayers = 0;
        namePlayer = [];
        if (await showButton())
        {
            if (await numPlayers())
            {
                await getNamePlayer();
                scoreToDo = 12;
            }
        }
        else
        {
            if (await numPlayers())
            {
                await getNamePlayer();
                await scoreChoice();
            }
        }

        if (namePlayer.length === numberPlayers && scoreToDo !== 0)
        {
            await startButton();
            if (startGame === true)
                launchGamePong();
        }
    }
    // Update the URL without reloading the page
    // history.pushState({ page: 'game' }, 'Game', '/game');
}
