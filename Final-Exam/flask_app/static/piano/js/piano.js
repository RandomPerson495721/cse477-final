const sound = {
    65:"https://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87:"https://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83:"https://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69:"https://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68:"https://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70:"https://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84:"https://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71:"https://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89:"https://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72:"https://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85:"https://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74:"https://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75:"https://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79:"https://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76:"https://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80:"https://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    // Firefox uses 59 for semicolon, the rest use 186
    59:"https://carolinegabriel.com/demo/js-keyboard/sounds/056.wav",
    186:"https://carolinegabriel.com/demo/js-keyboard/sounds/056.wav",
};

const history = [];
let awoken = false;

// Key elements
const whiteKeys = document.getElementsByClassName('white-key');
const blackKeys = document.getElementsByClassName('black-key');

// Function to show the note names when the mouse is over the keys
const showNote = function () {
    for (let i = 0; i < whiteKeys.length; i++) {
        whiteKeys[i].style.color = 'rgba(0,0,0,1)';
    }

    for (let i = 0; i < blackKeys.length; i++) {
        blackKeys[i].style.color = 'rgba(255,255,255,1)';
    }
}

// Function to hide the note names when the mouse is not over the keys
const hideNote = function () {
    for (let i = 0; i < whiteKeys.length; i++) {
        whiteKeys[i].style.color = 'rgba(0,0,0,0)';
    }

    for (let i = 0; i < blackKeys.length; i++) {
        blackKeys[i].style.color = 'rgba(255,255,255,0)';
    }
}

// Function to handle the key press event
const keyPress = function (event) {
    let key = document.getElementById(event.key.toUpperCase());
    if (key === null || awoken) {
        return;
    }
    const audio = new Audio(sound[event.keyCode]);
    audio.play();
    if (key.className === 'white-key') {
        key.style.backgroundColor = 'rgba(255,255,255,0.5)';
    } else {
        key.style.backgroundColor = 'rgba(0,0,0,0.5)';
    }
}

// Function to handle the key release event
const keyRelease = function (event) {
    let key = document.getElementById(event.key.toUpperCase());
    if (key === null || awoken) {
        return;
    }

    // Add the key to the history
    history.push(event.key.toUpperCase());
    // If the history is longer than 8, remove the first element
    if (history.length > 8) {
        history.shift();
    }

    // If it's a white key, style appropriately, else style black key
    if (key.className === 'white-key') {
        key.style.backgroundColor = 'rgba(255,255,255,1)';
    } else {
        key.style.backgroundColor = 'rgba(0,0,0,1)';
    }

    // If the history is "WESEEYOU", show the great old one, converted to uppercase for consistency
    if (history.join('') === "WESEEYOU")
    {
        document.getElementById('great-old-one').classList.replace('hidden', 'visible');
        awoken = true;
        /* Play creepy music */
        const audio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
        audio.play();
    }
}

// Add event listeners to the document to handle user keyboard input
document.addEventListener('keydown', keyPress);
document.addEventListener('keyup', keyRelease);

// Add event listeners to the keys
for (let i = 0; i < blackKeys.length; i++) {
    blackKeys[i].addEventListener('mouseover', showNote);
    blackKeys[i].addEventListener('mouseout', hideNote);
}

for (let i = 0; i < whiteKeys.length; i++) {
    whiteKeys[i].addEventListener('mouseover', showNote);
    whiteKeys[i].addEventListener('mouseout', hideNote);
}