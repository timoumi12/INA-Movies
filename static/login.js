/* DOM is essentially a tree-like structure that represents the HTML content of a web page as a collection of objects that can be manipulated using JavaScript.
 * When a web page is loaded, the browser creates a DOM object model of the page, which consists of a hierarchy of objects that correspond to the various elements in the HTML code.
 * Each object in the DOM tree represents an HTML element, such as a paragraph, image, or link.
 */

document.addEventListener('DOMContentLoaded', function signIn() 
// Thus, The "DOMContentLoaded" event is fired by the browser when the DOM tree has been constructed.
// The addEventListener method is executed when the specified event (DOMContentLoaded) occurs.
{
    const dialogBox = document.querySelector('#my-dialog');
    const closeButton = document.querySelector('#close-dialog');
    //const sndclose = document.querySelector('#close_dialogg');
    const username = document.querySelector('#username');
    const pwd = document.querySelector('#pwd');
    //const emailRegex= /^[a-zA-z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$/
    
    function hideDialog() {
        dialogBox.style.display = 'none';
    }

    function showDialog() {
        dialogBox.style.display = 'block';
    }
    document.querySelector("#check").addEventListener('click', (event) => {
        console.log(pwd.value)
        if(username.value === "" || pwd.value === ""){
            // sets the inner HTML of the element with the m1 variable to the text specified.
            event.preventDefault();
            console.log((username.value === "" || pwd.value === ""))
            showDialog();
        }
        /*if(pwd.value.length < 8){
            pwd.style.color = "red";
            m2.innerHTML = "Password too Short";
            window.event.target.preventDefault();
        }*/
        /*document.addEventListener('click', (event) => {
            if (!dialogBox.contains(event.target)) {
              dialogBox.style.display = 'none';
            }
        });*/
    });
    
    closeButton.addEventListener('click', hideDialog);
    //sndclose.addEventListener('click', hideDialog);
}
);