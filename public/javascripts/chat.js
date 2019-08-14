$(document).ready(function () {
    console.log("Page loaded!");

    let username = getCookie("username");
    let textBox = $('#text');
    let chatBox = $('#Chatbox');
    let submitBtn = $('#submitButton');
    let validateBtn = $('#validateBtn');
    let welcomeText = $('#Welcome');
    login();

    // -- EVENT HANDLERS --

    textBox.on('keypress', function (e) {
       if (e.which === 13){
           sendMsg(textBox.val());
       }
    });

    submitBtn.on('click', function () {
        sendMsg(textBox.val());
    });

    validateBtn.on('click', function () {
        document.cookie = "username=";

    });

    window.setInterval(readLog, 500);
    // -- CHAT METHODS --

    function sendMsg(text) {
        verify(username, getCookie('password'));

        text = `<p><em>${username}:</em> ${text}</p>`;
        console.log(`message sent: ${text}`);
        chatBox.append(text);
        writeLog(text);

        textBox.val('');
    }
    
    function writeLog(text) {
        text += "\n";

        $.post(
            'http://localhost:3000/messages',
            {msg: text},
            function (data) {
                console.log(`Response is ${data}`);
            }
        )
    }
    
    function readLog() {
        $.get(
            'http://localhost:3000/messages',
            function (data, status) {
                console.log(`Response is ${data}\nStatus is ${status}`);
                chatBox.html(data);
            });
    }

    // -- AUTH METHODS--

    function authorize() {
        console.log("Logging in..." + username);

        $('#text').prop("disabled", false);
        welcomeText.text(`Welcome ${username}!`);
        chatBox.append(readLog());
    }

    function verify(uname, pass) {
        console.log(`username is: ${uname}, password is ${pass}`);
        let isValid = false;

        $.get(
            'http://localhost:3000/users',(function (data){
            console.log(`username is: ${uname}, password is ${pass}`);
            console.log("response from /users: " + JSON.stringify(data));

            if (data['users'][uname] === pass){
                authorize();
            }
        }));

        return isValid;
    }

    function login() {
        if (username === "") {
            let uname = window.prompt("Enter username");
            let pass = window.prompt("Enter password");
            verify(uname, pass);

            createCookie("username", uname, 0);
            createCookie("password", pass, 0);

        } else {
            verify(username, getCookie("password"));
        }
    }

    // -- HELPER FUNCTIONS --

   function createCookie(key, val, exp) {
       let ttl = new Date();
       if (exp < 0) {
           ttl.setTime(ttl.getTime() + exp);
       } else {
           ttl.setTime(ttl.getTime() + 10e100);
       }
       document.cookie = `${key} = ${val}; expires = ${ttl.toUTCString()}; path=/`
   }

    function getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
});