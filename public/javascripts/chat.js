$(document).ready(function () {
    console.log("Page loaded!");

    let username = getCookie("username");
    let textBox = $('#text');
    let chatBox = $('#Chatbox');
    let submitBtn = $('#submitButton');
    let validateBtn = $('#validateBtn');
    let welcomeText = $('#Welcome');
    let userSettings;
    
    $.get('/users', function(data) { 
    populateData(data)
//      userSettings = JSON.stringify(data);
//      login(); 
    });
    
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

        text = `<p><em style= "color: ${userSettings[username][1]}>${username}:</em> ${text}</p>`;
        console.log(`message sent: ${text}`);
        chatBox.append(text);
        writeLog(text);

        textBox.val('');
    }
    
    function writeLog(text) {
        text += "\n";

        $.post(
            '/messages',
            {msg: text}
        )
    }
    
    function readLog() {
        $.get(
            '/messages',
            function (data, status) {
                chatBox.html(data);
            });
    }

    // -- AUTH METHODS--
    
    function populateData(data) {
      userSettings = JSON.stringify(data);
      
      login();
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
    
    function verify(uname, pass) {
      console.log(`userSettings = ${userSetings}`);
      let isValid = userSettings[uname][0] === pass;
      
      if (isValid) {
        $('#text').prop("disabled", false);
        welcomeText.text(`Welcome ${username}!`);
        chatBox.append(readLog());
      }
      
      return isValid;
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
