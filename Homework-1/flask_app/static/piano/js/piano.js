const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};


let whiteKeys = document.getElementsByClassName('white-key');
let blackKeys = document.getElementsByClassName('black-key');

// Function to show the note names when the mouse is over the keys
function showNote() {
    let i;
    for (i = 0; i < whiteKeys.length; i++) {
        whiteKeys[i].style.color = 'rgba(0,0,0,1)';
    }

    for (i = 0; i < blackKeys.length; i++) {
        blackKeys[i].style.color = 'rgba(255,255,255,1)';
    }
}

// Function to hide the note names when the mouse is not over the keys
function hideNote() {
    let i;
    for (i = 0; i < whiteKeys.length; i++) {
        whiteKeys[i].style.color = 'rgba(0,0,0,0)';
    }

    for (i = 0; i < blackKeys.length; i++) {
        blackKeys[i].style.color = 'rgba(255,255,255,0)';
    }
}

// Function to handle the key press event
function keyPress(event) {
    let key = document.getElementById(event.key.toUpperCase());
    if (key === null) {
        return;
    }
    if (key.className === 'white-key') {
        key.style.backgroundColor = 'rgba(255,255,255,0.5)';
    } else {
        key.style.backgroundColor = 'rgba(0,0,0,0.5)';
    }
}

// Function to handle the key release event
function keyRelease(event) {
    let key = document.getElementById(event.key.toUpperCase());
    if (key === null) {
        return;
    }
    if (key.className === 'white-key') {
        key.style.backgroundColor = 'rgba(255,255,255,1)';
    } else {
        key.style.backgroundColor = 'rgba(0,0,0,1)';
    }
}

document.addEventListener('keydown', keyPress);
document.addEventListener('keyup', keyRelease);

// Add event listeners to the keys
for (let i = 0; i < blackKeys.length; i++) {
    blackKeys[i].addEventListener('mouseover', showNote);
    blackKeys[i].addEventListener('mouseout', hideNote);

    // blackKeys[i].addEventListener('mouseleave', keyRelease);

}
for (let i = 0; i < whiteKeys.length; i++) {
    whiteKeys[i].addEventListener('mouseover', showNote);
    whiteKeys[i].addEventListener('mouseout', hideNote);
    // whiteKeys[i].addEventListener('mouseleave', keyRelease);
}