// Function to toggle the visibility of the feedback form
document.getElementById('feedback__button').addEventListener('click', function (e) {
    var feedbackForm = document.getElementById('feedback__form');

    if (feedbackForm.classList.contains('feedback__form--hidden')) {
        feedbackForm.classList.replace('feedback__form--hidden', 'feedback__form--visible');
    } else {
        feedbackForm.classList.replace('feedback__form--visible', 'feedback__form--hidden');
    }

});