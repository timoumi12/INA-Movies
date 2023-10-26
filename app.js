document.addEventListener('DOMContentLoaded', () => {
    const dialogBox = document.querySelector('#my-dialog');
    const closeButton = document.querySelector('#close-dialog');

    const form = document.querySelector('.selection');
    const sel = form.querySelectorAll('select');

    function showDialog() {
        dialogBox.style.display = 'block';
    }

    function hideDialog() {
        dialogBox.style.display = 'none';
    }

    function checkS(){
        let selected = false;
        sel.forEach((element) => {
            if (element.value !== '')
                selected = true;
        });
        return selected;
    }

    form.addEventListener('submit', (event) => {
        console.log(checkS());
        if (!checkS()){
            console.log(checkS());
            event.preventDefault();
            showDialog();
        }
    });
    window.addEventListener('click', (event) => {
        if (!dialogBox.contains(event.target)) {
          dialogBox.style.display = 'none';
        }
    });
    closeButton.addEventListener('click', hideDialog);
});
