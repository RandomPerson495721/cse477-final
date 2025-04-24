// I need to do drag and select functionality
// to select the state of the div

// State to see if mouse is down
let isSelecting = false;
let startTarget = null;

const setSlotState = (element) => {
    const mode = document.getElementById('mode').value;
    switch (mode) {
        case 'available':
            element.classList.add('available');
            element.classList.remove('unavailable');
            element.classList.remove('maybe');
            break;

        case 'unavailable':
            element.classList.add('unavailable');
            element.classList.remove('available');
            element.classList.remove('maybe');
            break;

        case 'maybe':
            element.classList.add('maybe');
            element.classList.remove('available');
            element.classList.remove('unavailable');
            break;
    }
}

const mouseDownHandler = (e) => {
    isSelecting = true;
    startTarget = e.target;
    setSlotState(startTarget);
};

const mouseUpHandler = (e) => {
    isSelecting = false;
    startTarget = null;
};

const mouseOverHandler = (e) => {
    if (isSelecting) {
        const target = e.target;
        // loop through every element between the start and end target by the row and column data attributes
        startRow = parseInt(startTarget.getAttribute('data-row'));
        startCol = parseInt(startTarget.getAttribute('data-column'));

        endRow = parseInt(target.getAttribute('data-row'));
        endCol = parseInt(target.getAttribute('data-column'));

        // Loop through the rows and columns
        const rowStart = Math.min(startRow, endRow);
        const rowEnd = Math.max(startRow, endRow);

        const colStart = Math.min(startCol, endCol);
        const colEnd = Math.max(startCol, endCol);

        for (let row = rowStart; row <= rowEnd; row++) {
            for (let col = colStart; col <= colEnd; col++) {
                const element = document.getElementById(`slot_${row}_${col}`);
                if (element) {
                    // Set the class based on the mode
                    setSlotState(element);
                }

            }
        }
    }

    //     switch (mode) {
    //         case 'available':
    //             target.classList.add('available');
    //             target.classList.remove('unavailable');
    //             target.classList.remove('maybe');
    //             break;
    //
    //         case 'unavailable':
    //             target.classList.add('unavailable');
    //             target.classList.remove('available');
    //             target.classList.remove('maybe');
    //             break;
    //
    //         case 'maybe':
    //             target.classList.add('maybe');
    //             target.classList.remove('available');
    //             target.classList.remove('unavailable');
    //             break;
    //     }
    // }
};

document.addEventListener('mouseup', mouseUpHandler);


// var socket;
// $(document).ready(function () {
//
//     socket = io.connect('http://' + document.domain + ':' + location.port + '/availability');
//     // socket.on('connect', function () {
//     //     socket.emit('joined', {});
//     // });
//     //
//     // socket.on('status', function (data) {
//     //     let tag = document.createElement("p");
//     //     let text = document.createTextNode(data.msg);
//     //     let element = document.getElementById("chat");
//     //     tag.appendChild(text);
//     //     tag.style.cssText = data.style;
//     //     element.appendChild(tag);
//     //     $('#chat').scrollTop($('#chat')[0].scrollHeight);
//     //
//     // });
//
//
//
// });

