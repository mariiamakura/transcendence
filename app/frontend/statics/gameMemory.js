let numberCards;
let set;

function choiceSet() {
    var main = document.getElementById('content');
    main.innerHTML += `<div id="choice"><p style="padding-top: 1em; display: flex; " > Which set do you want to play with ? </p></div>`;
    var Nature = document.createElement("button");
    Nature.textContent = "Nature (easy)";
    Nature.classList.add("styled-button");
    document.getElementById('choice').appendChild(Nature);
    var Robot = document.createElement("button");
    Robot.textContent = "Robot (hard)";
    Robot.classList.add("styled-button");
    document.getElementById('choice').appendChild(Robot);
    return new Promise(function (resolve) {
        Nature.addEventListener("click", function() {
            resolve(true);
            set = 1;
            document.getElementById('choice').remove();
        });
        Robot.addEventListener("click", function() {
            resolve(true);
            set = 2;
            document.getElementById('choice').remove();
        });
    });
}

function choiceCards() {
    var main = document.getElementById('content');
    main.innerHTML += `<div id="choice"><p style="padding-top: 2em; display: flex; " > How many cards do you want to play with: </p></div>`;
    var TwelveCards = document.createElement("button");
    TwelveCards.textContent = "12";
    TwelveCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(TwelveCards);
    var SixteenCards = document.createElement("button");
    SixteenCards.textContent = "16";
    SixteenCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(SixteenCards);
    var TwentyFourCards = document.createElement("button");
    TwentyFourCards.textContent = "24";
    TwentyFourCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(TwentyFourCards);
    var ThirtyTwoCards = document.createElement("button");
    ThirtyTwoCards.textContent = "32";
    ThirtyTwoCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(ThirtyTwoCards);
    return new Promise(function (resolve) {
        TwelveCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 12;
            document.getElementById('choice').remove();
        });
        SixteenCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 16;
            document.getElementById('choice').remove();
        });
        TwentyFourCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 24;
            document.getElementById('choice').remove();
        });
        ThirtyTwoCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 32;
            document.getElementById('choice').remove();
        });
    });
}

async function showGameMemory() {
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = '<p style="display: flex; text-align: center; justify-content:center; font-size: 3em; ">Memory game</p>';    
    gameEnded = true;
    debug = 0;
    if (debug === 2)
    {
        set = 2;
        numberCards = 12;
        launchGameMemory();
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
                await choiceSet();
                numberCards = 12;
            }
        }
        else
        {
            if (await numPlayers())
            {
                await getNamePlayer();
                await choiceSet();
                await choiceCards();
            }
        }
        if (namePlayer.length === numberPlayers && numberCards !== 0)
        {
            await startButton();
            if (startGame === true)
                launchGameMemory();
        }
    }
    // Update the URL without reloading the page
    // history.pushState({ page: 'game' }, 'Game', '/game');
}

let cards = {
    id: null,
    width: 100,
    margin: 10,
    border: 2,
    ref: null,
    index: null
}

let setAlreadyUsed = [];

function randomSet(set, card) {
    let index;
    let ref;

    do {
        index = Math.floor(Math.random() * set.length);
        ref = set[index];
    } while (setAlreadyUsed.includes(ref));

    card.ref = ref;
    card.index = index;
    setAlreadyUsed.push(ref);
    return card;
}

let PlayerToPlay;
let firstSet;
let secondSet;

function launchGameMemory() {
    var mainElement = document.getElementById('content');
    if (!namePlayer[0] || !namePlayer[1])
    {
        namePlayer[0] = "Player1";
        namePlayer[1] = "Player2";
    }
    PlayerToPlay = namePlayer[0];
    let sets = [natureFirstSet12, natureSecondSet12, natureFirstSet16, natureSecondSet16, natureFirstSet24, natureSecondSet24, natureFirstSet32, natureSecondSet32, 
                        robotFirstSet12, robotSecondSet12, robotFirstSet16, robotSecondSet16, robotFirstSet24, robotSecondSet24, robotFirstSet32, robotSecondSet32]
    if (set === 1)
        sets = sets.slice(0, 8);
    else if (set === 2)
        sets = sets.slice(8, 16);
    switch (numberCards) {
        case 12:
            firstSet = sets[0];
            secondSet = sets[1];
            break;
        case 16:
            firstSet = sets[2];
            secondSet = sets[3];
            break;
        case 24:
            firstSet = sets[4];
            secondSet = sets[5];
            break;
        case 32:
            firstSet = sets[6];
            secondSet = sets[7];
            break;
    }

    let widthBoard = (cards.width + cards.margin * 2 + cards.border * 2) * (Math.ceil(numberCards / 4));
    mainElement.innerHTML = '<div id="whole">' + 
                                '<div id="Player1"><p id = "turn1"></p><div id = "progress-bar-container1"></div></div>' +
                                '<div id="memory-game" style = "width:' + widthBoard + 'px;"></div>' + 
                                '<div id="Player2"><p id = "turn2"></p><div id = "progress-bar-container2"></div></div>' +
                            '</div>';
    for (let i = 1; i <= numberCards; i++) {
        var card = document.createElement("div");
        card.classList.add("card");
        card.id = "card" + i;
        // Set the background image based on the condition
        if (i % 2 === 0)
        {
            randomSet(firstSet, card);
            card.style.setProperty("--bg-image", card.ref);
        }
        else
        {
            randomSet(secondSet, card);
            card.style.setProperty("--bg-image", card.ref);
        }        
        document.getElementById('memory-game').appendChild(card);
    }
    playTime();
}

let scorePlayer1 = 0;
let scorePlayer2 = 0;
let cardTurned = 0;
let cardTurnedArrayIndex = [];
let cardTurnedArrayId = [];

function updatePlayerTurns() {
    if (PlayerToPlay === namePlayer[0])
    {
        document.getElementById('Player1').style.backgroundColor = 'skyblue';
        document.getElementById('Player2').style.backgroundColor =  'white';
    }
    else
    {
        document.getElementById('Player1').style.backgroundColor =  'white';
        document.getElementById('Player2').style.backgroundColor = 'skyblue';
    }
}

function updatePlayerScore(playerNumber) {
    var score_max = numberCards / 2;
    var progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');
    progressBar.style.backgroundColor = (playerNumber === 1 ? document.getElementById('Player1').style.backgroundColor : document.getElementById('Player2').style.backgroundColor);
    let height = 20 * numberCards / 2;
    progressBar.style.width = '20px';
    progressBar.style.height = height + 'px';
    var progressBarContainerId = 'progress-bar-container' + playerNumber;
    document.getElementById(progressBarContainerId).innerHTML = '';
    document.getElementById(progressBarContainerId).appendChild(progressBar);
    var pourcentageScored = (playerNumber === 1 ? scorePlayer1 : scorePlayer2) / score_max * 100;
    progressBar.style.position = 'relative';
    progressBar.innerHTML = `<div class="scored"></div><div class="back"></div><span class="score-text"></span>`; // Include a span for the score text
    progressBar.querySelector('.scored').style.width = '100%';
    progressBar.querySelector('.back').style.width = '100%'; 
    progressBar.querySelector('.scored').style.height = pourcentageScored +'%';
    progressBar.querySelector('.back').style.height = (100 - pourcentageScored )+'%'; 
    progressBar.querySelector('.scored').style.backgroundColor = '#1e90ff'; // blue
    progressBar.querySelector('.back').style.backgroundColor = (playerNumber === 1 ? document.getElementById('Player1').style.backgroundColor : document.getElementById('Player2').style.backgroundColor);
    progressBar.querySelector('.scored').style.position = 'absolute';
    progressBar.querySelector('.scored').style.bottom = '0';
    progressBar.querySelector('.back').style.position = 'absolute';
    progressBar.querySelector('.back').style.bottom = pourcentageScored + '%';
    var scoreTextElement = progressBar.querySelector('.score-text');
    scoreTextElement.innerText = (playerNumber === 1 ? scorePlayer1 : scorePlayer2);
    scoreTextElement.style.position = 'absolute';
    scoreTextElement.style.bottom = '100%';
    scoreTextElement.style.left = '50%';
    scoreTextElement.style.transform = 'translateX(-50%)';
}

function playTime()
{
    PlayerToPlay = namePlayer[0];
    var turn1 = document.getElementById('turn1');
    var turn2 = document.getElementById('turn2');
    turn1.innerHTML = '<p> ' + namePlayer[0] + ' </p>';
    turn2.innerHTML = '<p> ' + namePlayer[1] + ' </p>';
    updatePlayerTurns();
    updatePlayerScore(1);
    updatePlayerScore(2);
    document.getElementById('memory-game').addEventListener("click", function(event) {
        if (event.target.classList.contains("card")) {
            if (cardTurned < 2 && !event.target.classList.contains("show-image"))
            {
                event.target.classList.toggle("show-image");
                cardTurned++;
                cardTurnedArrayIndex.push(event.target.index);
                cardTurnedArrayId.push(event.target.id);
                if (cardTurned === 2)
                    checkCards();
                if (scorePlayer1 + scorePlayer2 === numberCards / 2)
                    endGameMemory(scorePlayer1 > scorePlayer2 ? namePlayer[0] : namePlayer[1]);
        }
    }
});
}

function endGameMemory(winner)
{
    fetch('/update_game_result_memory/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ winner: winner }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Game result updated successfully');
            // Optionally, handle success response
        } else {
            console.error('Failed to update game result');
            // Optionally, handle error response
        }
    })
    .catch(error => {
        console.error('Error updating game result:', error);
        // Optionally, handle fetch error
    });
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = ''; // Remove all inner HTML content  
    mainElement.innerHTML = '<div id="endGame" style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; overflow: hidden;">' +
    '<p style="text-align: center; font-size:4em;">' + winner + ' won ! </p>' +
    '<p><img src="img/gif_robot.gif" alt="Victory logo" style = "width: 50vh; height: 50vh;"></p>' +
    '<p style="text-align: center;"> If you want to play again with the same settings, press the button below.</p>' +
    '</div>';
    var startAgain = document.createElement("button");
    startAgain.textContent = "Start again";
    startAgain.classList.add("styled-button")
    document.getElementById('endGame').appendChild(startAgain);
    startAgain.addEventListener("click", function() {
        cardTurned = 0;
        cardTurnedArrayIndex.length = 0;
        cardTurnedArrayId.length = 0;
        scorePlayer1 = 0;
        scorePlayer2 = 0;
        setAlreadyUsed.length = 0;
        launchGameMemory();
    });
}


function checkCards() {
    if (cardTurnedArrayIndex[0] === cardTurnedArrayIndex[1])
    {        
        if (PlayerToPlay === namePlayer[0])
            scorePlayer1++;
        else if (PlayerToPlay === namePlayer[1])
            scorePlayer2++;
        turnUpdate(1); // mode 1, players do not  switch
    }
    else
    {
        setTimeout(function() {
        var card1 = document.getElementById(cardTurnedArrayId[0]);
        var card2 = document.getElementById(cardTurnedArrayId[1]);
        if (card1 && card2) {
            card1.classList.toggle("show-image");
            card2.classList.toggle("show-image");
            turnUpdate(2); // mode 2, players switch
        }
        }, 2000);
    }
} 


function turnUpdate(mode)
{
    if (mode === 2)
    {
        if (PlayerToPlay === namePlayer[0])
            PlayerToPlay = namePlayer[1];
        else
            PlayerToPlay = namePlayer[0];
    }
    cardTurnedArrayId.length = 0;
    cardTurnedArrayIndex.length = 0;
    cardTurned -= 2;
    updatePlayerTurns();
    updatePlayerScore(1);
    updatePlayerScore(2);
}