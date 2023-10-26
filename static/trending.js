document.addEventListener('DOMContentLoaded', () => {
    const dialogBox = document.querySelector('#my-dialog');
    const closeButton = document.querySelector('#close-dialog');

    //const search_res = document.querySelector('#search-res');
    //const close_sr = document.querySelector('#close-search-res');

    const form = document.querySelector('.selection');
    const sel = form.querySelectorAll('select');

    function showDialog() {
        dialogBox.style.display = 'block';
    }

    /*function showSearchRes() {
        search_res.style.display = 'flex';
        if (!localStorage.getItem('searchResVisible')){
            localStorage.setItem('searchResVisible', 'true');
        }
    }

    function hideSearchRes() {
        search_res.style.display = 'none';
        localStorage.removeItem('searchResVisible')
    }*/

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

    /*window.addEventListener('load', (event) => {
        const searchResVisible = localStorage.getItem('searchResVisible');
        if (searchResVisible === 'true') {
            showSearchRes();
        }
    });
    
    window.addEventListener('beforeunload', (event) => {
        const searchResVisible = localStorage.getItem('searchResVisible');
        if (searchResVisible !== null)
            search_res.style.display = searchResVisible === 'true' ? 'flex' : 'none';
    });*/
    form.addEventListener('submit', (event) => {
        console.log(checkS());
        if (!checkS()){
            console.log(checkS());
            event.preventDefault();
            showDialog();
        }
        /*else {
            console.log(checkS());
                 showSearchRes();
        }*/
    });
    window.addEventListener('click', (event) => {
        if (!dialogBox.contains(event.target)) {
          dialogBox.style.display = 'none';
        }
    });
    /*window.addEventListener('click', (event) => {
        if (search_res && !search_res.contains(event.target)) {
          search_res.style.display = 'none';
        }
    });*/
    closeButton.addEventListener('click', hideDialog);
    //close_sr.addEventListener('click', hideSearchRes);
});
