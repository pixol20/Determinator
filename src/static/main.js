$(document).ready(function()
{
    var TurnedSound = false;
    var sendGenerationsBox = $("#sendGenerations");
    var saveSound = new Audio("../static/savepoint.mp3");
    var typeSound = new Audio("../static/voice.mp3");
    var BGMusic = new Audio("../static/home.ogg");
    BGMusic.loop = true;

    //#region readPreferences
    $.ajax({url: "/preferences", type: "POST", contentType: "application/json", data: JSON.stringify({intent: "get"}), success: function(response)
    {
        if (response === "False")
        {
            sendGenerationsBox.prop("checked", false); 
        }
        else
        {
            $("#didYouLikeOutputContainer").show();
            sendGenerationsBox.prop("checked", true); 
        }
    }});
    //#endregion

    //#region SAVEButton
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
    //#endregion
    
    //#region soundButton 
    $("#soundButton").on("click", function()
    {
        if (TurnedSound === false)
        {
            $("#soundIcon").attr("src","../static/soundicon.png");
            TurnedSound = true
            BGMusic.play();
        }
        else
        {
            $("#soundIcon").attr("src","../static/turnedoffsoundicon.png");
            TurnedSound = false;
            BGMusic.pause();

        }
    })
    //#endregion




    sendGenerationsBox.change(function()
    {
        var checkboxChecked = sendGenerationsBox.prop("checked");
        if (checkboxChecked)
        {
            $("#didYouLikeOutputContainer").show();
        }
        else
        {
            $("#didYouLikeOutputContainer").hide();
        }

        $.ajax({url: "/preferences", type: "POST", contentType: "application/json", data: JSON.stringify({intent: "set", sendData: checkboxChecked})});

    });

});