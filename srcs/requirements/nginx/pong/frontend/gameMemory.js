let numberCards;

function choiceCards() {
    var main = document.getElementById('content');
    main.innerHTML += `<div id="choice" style="display: flex; flex-direction:column;justify-content: center; align-items: center; width: 100%; height: 100%; overflow:hidden"><p style="padding-top: 2em; display: flex; " > How many cards do you want to play with: </p></div>`;
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
    mainElement.innerHTML = '<p style="display: flex; text-align: center; justify-content:center; font-size: 3em;">Memory game</p>';    
    gameEnded = true;
    debug = 1;
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

let natureFirstSet12 = [
    'url("img/Nature/bird1.png")',
    'url("img/Nature/bee1.png")',
    'url("img/Nature/flower1.png")',
    'url("img/Nature/leaf1.png")',
    'url("img/Nature/mushroom1.png")',
    'url("img/Nature/road1.png")',
];

let natureSecondSet12 = [
    'url("img/Nature/bird2.png")',
    'url("img/Nature/bee2.png")',
    'url("img/Nature/flower2.png")',
    'url("img/Nature/leaf2.png")',
    'url("img/Nature/mushroom2.png")',
    'url("img/Nature/road2.png")',
];

let natureFirstSet16 = [
    'url("img/Nature/bird1.png")',
    'url("img/Nature/bee1.png")',
    'url("img/Nature/flower1.png")',
    'url("img/Nature/leaf1.png")',
    'url("img/Nature/mushroom1.png")',
    'url("img/Nature/road1.png")',
    'url("img/Nature/butterfly_color1.png")',
    'url("img/Nature/kids1.png")',
];

let natureSecondSet16 = [
    'url("img/Nature/bird2.png")',
    'url("img/Nature/bee2.png")',
    'url("img/Nature/flower2.png")',
    'url("img/Nature/leaf2.png")',
    'url("img/Nature/mushroom2.png")',
    'url("img/Nature/road2.png")',
    'url("img/Nature/butterfly_color2.png")',
    'url("img/Nature/kids2.png")',
];

let natureFirstSet24 = [
    'url("img/Nature/bird1.png")',
    'url("img/Nature/bee1.png")',
    'url("img/Nature/flower1.png")',
    'url("img/Nature/leaf1.png")',
    'url("img/Nature/mushroom1.png")',
    'url("img/Nature/road1.png")',
    'url("img/Nature/butterfly_color1.png")',
    'url("img/Nature/kids1.png")',
    'url("img/Nature/snail1.png")',
    'url("img/Nature/rock1.png")',
    'url("img/Nature/rainbow1.png")',
    'url("img/Nature/frog1.png")',
];

let natureSecondSet24 = [
    'url("img/Nature/bird2.png")',
    'url("img/Nature/bee2.png")',
    'url("img/Nature/flower2.png")',
    'url("img/Nature/leaf2.png")',
    'url("img/Nature/mushroom2.png")',
    'url("img/Nature/road2.png")',
    'url("img/Nature/butterfly_color2.png")',
    'url("img/Nature/kids2.png")',
    'url("img/Nature/snail2.png")',
    'url("img/Nature/rock2.png")',
    'url("img/Nature/rainbow2.png")',
    'url("img/Nature/frog2.png")',
];

let natureFirstSet32 = [
    'url("img/Nature/bird1.png")',
    'url("img/Nature/bee1.png")',
    'url("img/Nature/flower1.png")',
    'url("img/Nature/leaf1.png")',
    'url("img/Nature/mushroom1.png")',
    'url("img/Nature/road1.png")',
    'url("img/Nature/butterfly_color1.png")',
    'url("img/Nature/kids1.png")',
    'url("img/Nature/snail1.png")',
    'url("img/Nature/rock1.png")',
    'url("img/Nature/rainbow1.png")',
    'url("img/Nature/frog1.png")',
    'url("img/Nature/caterpillar1.png")',
    'url("img/Nature/earth1.png")',
    'url("img/Nature/trees1.png")',
    'url("img/Nature/butterfly_black1.png")',
];

let natureSecondSet32 = [
    'url("img/Nature/bird2.png")',
    'url("img/Nature/bee2.png")',
    'url("img/Nature/flower2.png")',
    'url("img/Nature/leaf2.png")',
    'url("img/Nature/mushroom2.png")',
    'url("img/Nature/road2.png")',
    'url("img/Nature/butterfly_color2.png")',
    'url("img/Nature/kids2.png")',
    'url("img/Nature/snail2.png")',
    'url("img/Nature/rock2.png")',
    'url("img/Nature/rainbow2.png")',
    'url("img/Nature/frog2.png")',
    'url("img/Nature/caterpillar2.png")',
    'url("img/Nature/earth2.png")',
    'url("img/Nature/trees2.png")',
    'url("img/Nature/butterfly_black2.png")',
];

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
    if (numberCards === 12)
    {
        firstSet = natureFirstSet12
        secondSet = natureSecondSet12;
    }
    else if (numberCards === 16)
    { 
        firstSet = natureFirstSet16;
        secondSet = natureSecondSet16;
    }
    else if (numberCards === 24)
    {
        firstSet = natureFirstSet24;
        secondSet = natureSecondSet24;
    }
    else if (numberCards === 32)
    {
        firstSet = natureFirstSet32;
        secondSet = natureSecondSet32;
    }
    console.log(numberCards);
    // let widthBoard = (cards.width + cards.margin * 2 + cards.border * 2) * (Math.ceil(Math.sqrt(numberCards)));
    let widthBoard = (cards.width + cards.margin * 2 + cards.border * 2) * (Math.ceil(numberCards / 4));
    console.log(widthBoard);
    mainElement.innerHTML = '<div id="turn"></div><div id="memory-game" style = "width:' + widthBoard + 'px;"></div>';
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

function playTime()
{
    PlayerToPlay = namePlayer[0];
    var turn = document.getElementById('turn');
    turn.innerHTML = '<p style= "display:flex;text-align :left; "> Score ' + namePlayer[0] + ': ' + scorePlayer1 +
    ' <p style="display:flex; text-align:right;">Score ' + namePlayer[1] + ': ' + scorePlayer2 + '</p>' +
    '</p> <p style= "font-size:2em; text-align:center;"> Playing: ' + PlayerToPlay + '</p>';
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
