// I need to do drag and select functionality
// to select the state of the div

// State to see if mouse is down
let isSelecting = false;
let startTarget = null;
//


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
};

const updateHeatmap = (data) => {
    data = JSON.parse(data);
    const noData = Object.keys(data).length === 0;

    // General event data
    const event_data = document.getElementById('event__data');
    const event_start_date = new Date(event_data.getAttribute('data-event-start-date'));
    const event_start_time = parseTime(event_data.getAttribute('data-event-start-time'));

    // Heatmap slots
    const slots = document.querySelectorAll('.heatmap_slot');

    sort_slots = []

    slots.forEach(slot => {
        const row = parseInt(slot.getAttribute('data-row'));
        const column = parseInt(slot.getAttribute('data-column'));
        const a = `${row}_${column}`
        const available_count = data[a]?.['available'] || 0;
        const unavailable_count = data[`${row}_${column}`]?.['unavailable'] || 0;
        const maybe_count = data[`${row}_${column}`]?.['maybe'] || 0;
        sort_slots.push([available_count, unavailable_count, ((row + 1)) + (1000 * column + 1), data[`${row}_${column}`], row, column]);

        slot.classList.remove('hm__available_1', 'hm__available_2', 'hm__available_3', 'hm__maybe', 'hm__unavailable');

        if (available_count > 0) {
            switch (available_count) {
                case 1:
                    slot.classList.add('hm__available_1');
                    break;
                case 2:
                    slot.classList.add('hm__available_2');
                    break;
                default:
                    slot.classList.add('hm__available_3');
            }
        } else if (maybe_count > 0) {
            slot.classList.add('hm__maybe');
        } else if (unavailable_count > 0) {
            slot.classList.add('hm__unavailable');
        }

    });

    // Sort the slots based on available count
    sort_slots.sort((a, b) => {
        // Available count descending, then unavailable count ascending, then row * column ascending
        if (b[0] !== a[0]) {
            return b[0] - a[0];
        } else if (a[1] !== b[1]) {
            return a[1] - b[1];
        } else {
            return a[2] - b[2];
        }
    });

    // Get the best time to meet span
    const best_time_text = document.getElementById('best_time');
    const best_time_row = sort_slots[0][4];
    const best_time_col = sort_slots[0][5];
    const best_time_slot = document.getElementById(`heatmap_${best_time_row}_${best_time_col}`).getAttribute('data-time');

    let hours = parseInt(best_time_slot.split(':')[0]);
    let minutes = parseInt(best_time_slot.split(':')[1]);
    minutes = minutes < 10 ? '0' + minutes : minutes;
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;

    day = best_time_col;

    best_time_text.innerHTML = noData ? 'No availability submitted yet' : sort_slots[0][0] > 0 ? `${hours}:${minutes} ${ampm} on Day ${day}` : `No available slots - earliest time slot is ${event_start_date.toLocaleDateString()} at ${event_start_time.toLocaleTimeString()}`;

};

const parseTime = (timeString) => {
    const timeParts = timeString.split(':');
    let hours = parseInt(timeParts[0]);
    const minutes = parseInt(timeParts[1]);

    const time = new Date();
    time.setHours(hours, minutes, 0, 0);

    return new Date(time);
}

var socket;
$(document).ready(function () {
    // get the event id from the data-event-id attribute of the div with the id event__data
    const event_id = parseInt(document.getElementById('event__data').getAttribute('data-event-id'));

    socket = io.connect(document.location.protocol + '//' + document.domain + ':' + location.port + '/availability');
    // socket.on('connect', function () {
    //     socket.emit('connected', event_id);
    // });
    //
    // socket.on('disconnect', function () {
    //     socket.emit('disconnected', event_id);
    // });

    socket.emit('get_heatmap', event_id, (data) => {
        if (!data) {
            return;
        }
        updateHeatmap(data);
    });

    socket.on('update_heatmap', (data) => {
        if (!data) {
            return;
        }
        if (data['event_id'] !== event_id) {
            return;
        }

        updateHeatmap(data['slot_states']);
    });
    //
    // socket.on('status', function (data) {
    //     let tag = document.createElement("p");
    //     let text = document.createTextNode(data.msg);
    //     let element = document.getElementById("chat");
    //     tag.appendChild(text);
    //     tag.style.cssText = data.style;
    //     element.appendChild(tag);
    //     $('#chat').scrollTop($('#chat')[0].scrollHeight);
    //
    // });

    document.addEventListener('mouseup', function (e) {
        let prevIsSelecting = isSelecting;
        isSelecting = false;
        startTarget = null;

        if (!prevIsSelecting) {
            return;
        }
        // Loop through the rows and columns
        const slots = document.querySelectorAll('.slot');
        let slot_states = [];
        slots.forEach(slot => {
            if (slot.classList.contains('available') || slot.classList.contains('unavailable') || slot.classList.contains('maybe')) {
                const row = parseInt(slot.getAttribute('data-row'));
                const column = parseInt(slot.getAttribute('data-column'));
                const status = slot.classList.contains('available') ? 'available' : slot.classList.contains('unavailable') ? 'unavailable' : 'maybe';
                slot_states.push({row, column, status});
            }
        });

        if (slot_states.length === 0) {
            return;
        }

        // Send the data to the server
        const data = {
            'event_id': event_id,
            'slot_states': slot_states
        };
        socket.emit('update_availability', data);


    });




});
