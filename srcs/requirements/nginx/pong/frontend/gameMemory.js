let numberCards;

function choiceCards() {
    var main = document.getElementById('content');
    main.innerHTML += `<div id="choice" style="display: flex; flex-direction:column;justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"><p style="padding-top: 2em; display: flex; " > How many cards do you want to play with: </p></div>`;
    var TwelveCards = document.createElement("button");
    TwelveCards.textContent = "12";
    TwelveCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(TwelveCards);
    var EighteenCards = document.createElement("button");
    EighteenCards.textContent = "18";
    EighteenCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(EighteenCards);
    var TwentyFourCards = document.createElement("button");
    TwentyFourCards.textContent = "24";
    TwentyFourCards.classList.add("styled-button");
    document.getElementById('choice').appendChild(TwentyFourCards);
    return new Promise(function (resolve) {
        TwelveCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 12;
            document.getElementById('choice').remove();
        });
        EighteenCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 18;
            document.getElementById('choice').remove();
        });
        TwentyFourCards.addEventListener("click", function() {
            resolve(true);
            numberCards = 24;
            document.getElementById('choice').remove();
        });
    });
}

async function showGameMemory() {
    var mainElement = document.getElementById('content');
    mainElement.innerHTML = '<p style="display: flex; text-align: center; justify-content:center; font-size: 3em;">Memory game</p>';    
    gameEnded = true;
    debug = 2;
    if (debug === 2)
    {
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
                numberCards = 12;
            }
        }
        else
        {
            if (await numPlayers())
            {
                await getNamePlayer();
                await choiceCards();
            }
        }

        if (namePlayer.length === numberPlayers && scoreToDo !== 0)
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

let firstSet12 = [
    'url("img/pictures_memory_level_1/bird1.png")',
    'url("img/pictures_memory_level_1/flower1.png")',
    'url("img/pictures_memory_level_1/leaf1.png")',
    'url("img/pictures_memory_level_1/mushroom1.png")',
    'url("img/pictures_memory_level_1/pink_flower1.png")',
    'url("img/pictures_memory_level_1/road1.png")',
];

let secondSet12 = [
    'url("img/pictures_memory_level_1/bird2.png")',
    'url("img/pictures_memory_level_1/flower2.png")',
    'url("img/pictures_memory_level_1/leaf2.png")',
    'url("img/pictures_memory_level_1/mushroom2.png")',
    'url("img/pictures_memory_level_1/pink_flower2.png")',
    'url("img/pictures_memory_level_1/road2.png")',
];

let setAlreadyUsed = [];

function randomSet(set, card) {
    let index = Math.floor(Math.random() * set.length);
    let ref = set[index];
    if (setAlreadyUsed.includes(set[index]))
        return randomSet(set, card);
    else
    {
        card.ref = ref;
        card.index = index;
        setAlreadyUsed.push(ref);
        return card;
    }
}
let PlayerToPlay;

function launchGameMemory() {
    var mainElement = document.getElementById('content');
    if (!namePlayer[0] || !namePlayer[1])
    {
        namePlayer[0] = "Player1";
        namePlayer[1] = "Player2";
    }
    PlayerToPlay = namePlayer[0];
    if (numberCards === 12)
    {
        let firstSet = firstSet12;
        let secondSet = secondSet12;
    }
    // if (numberCards === 16)
    // {        // Append the card to the memory-game container

    //     let firstSet = firstSet16;
    //     let secondSet = secondSet16;
    // }
    // if (numberCards === 25)
    // {
    //     let firstSet = firstSet25;
    //     let secondSet = secondSet25;
    // }
    // if (numberCards === 36)
    // {
    //     let firstSet = firstSet36;
    //     let secondSet = secondSet36;
    // }
    let widthBoard = (cards.width + cards.margin * 2 + cards.border * 2) * (Math.ceil(Math.sqrt(numberCards)));
    mainElement.innerHTML = '<div id="turn"></div><div id="memory-game" style = "width:' + widthBoard + 'px;"></div>';
    for (let i = 1; i <= numberCards; i++) {
        var card = document.createElement("div");
        card.classList.add("card");
        card.id = "card" + i;
        
        // Set the background image based on the condition
        if (i % 2 === 0)
        {
            randomSet(firstSet12, card);
            card.style.setProperty("--bg-image", card.ref);
        }
        else
        {
            randomSet(secondSet12, card);
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

function playTime()
{
    PlayerToPlay = namePlayer[0];
    var turn = document.getElementById('turn');
    turn.innerHTML = '<p style= "display:flex;text-align :left; "> Score ' + namePlayer[0] + ': ' + scorePlayer1 +
    ' <p style="display:flex; text-align:right;">Score ' + namePlayer[1] + ': ' + scorePlayer2 + '</p>' +
    '</p> <p style= "font-size:2em; text-align:center;"> Playing: ' + PlayerToPlay + '</p>';
    document.getElementById('memory-game').addEventListener("click", function(event) {
        if (event.target.classList.contains("card")) {
            console.log(event.target.index);
            if (cardTurned < 2)
            {
                event.target.classList.toggle("show-image");
                cardTurned++;
                cardTurnedArrayIndex.push(event.target.index);
                cardTurnedArrayId.push(event.target.id);
                if (cardTurned === 2)
                    checkCards();
            }
        }
    });
}

function checkCards() {
    if (cardTurnedArrayIndex[0] === cardTurnedArrayIndex[1])
    {
        console.log("eqalite des cartes");
        
        if (PlayerToPlay === namePlayer[0])
            scorePlayer1++;
        else if (PlayerToPlay === namePlayer[1])
            scorePlayer2++;
        turnUpdate(1); // mode 1, players do not  switch
    }
    else
    {
        console.log(cardTurnedArrayId[0]);
        console.log(cardTurnedArrayId[1]);
        console.log("retournement des cartes");
        console.log(cardTurnedArrayIndex[0]);
        console.log(cardTurnedArrayIndex[1]);
        setTimeout(function() {
        var card1 = document.getElementById(cardTurnedArrayId[0]);
        var card2 = document.getElementById(cardTurnedArrayId[1]);
        console.log(card1);
        console.log(card2);

        if (card1 && card2) {
            console.log("worked");
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
    var turn = document.getElementById('turn');
    turn.innerHTML = '<p style= "display:flex;text-align :left; "> Score ' + namePlayer[0] + ': ' + scorePlayer1 +
    ' <p style="display:flex; text-align:right;">Score ' + namePlayer[1] + ': ' + scorePlayer2 + '</p>' +
    '</p> <p style= "font-size:2em; text-align:center;"> Playing: ' + PlayerToPlay + '</p>';
}
