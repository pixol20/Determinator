$(document).ready(function()
{
    var audioContext = new (window.AudioContext || window.webkitAudioContext)();
    var music = new Audio("../static/home.ogg");

    // Create a source node from the audio element
    var sourceNode = audioContext.createMediaElementSource(music);
    // Connect the source node to the audio context
    sourceNode.connect(audioContext.destination);
    music.loop = true;
    music.play();
    var saveSound = new Audio("../static/savepoint.mp3");
    var typeSound = new Audio("../static/voice.mp3");
    $("#save").on("click", function()
    {
        saveSound.play();
        
        function successFunction(response)
        {
            var placeholder = $("#textPlaceholder")
            var speed = 30;
            var letterIndex = 0;
            typeSound.play();
            // Function to erase text letter by letter and write a new one
            function eraseAndWrite() 
            {
                var textContent = placeholder.text();
                var textLength = textContent.length;
            
                var interval = setInterval(function() {
                        textLength--;
                        placeholder.text(textContent.substr(0, textLength));
                
                        if (textLength === 0) {
                            clearInterval(interval);
                            writeText();
                        }
                    }, speed);
            }

            function writeText()
            {
                if(letterIndex < response.length)
                {
                    placeholder.html(placeholder.html()+response[letterIndex]);
                    letterIndex++;
                    setTimeout(writeText, speed);
                }
                else
                {
                    typeSound.pause();
                    typeSound.currentTime = 0;
                }
            }
            eraseAndWrite();
        }
        determinationPurpose = $("#determinationPurpose").val()
        $.ajax({url: "/generate", type:"POST", contentType: 'application/json', data: JSON.stringify({DeterminationPurpose: determinationPurpose}), success: successFunction});
    });
});