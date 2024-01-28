$(document).ready(function()
{
    //#region globalVariables
    var alreadyRated = false;
    var generated = false;
    var turnedSound = false;
    var placeholder = $("#textPlaceholder");
    didYouLikeOutputContainer = $("#didYouLikeOutputContainer");
    var sendGenerationsBox = $("#sendGenerations");
    var likeButton = $("#like")
    var dislikeButton = $("#dislike")
    var saveSound = new Audio("../static/savepoint.mp3");
    var typeSound = new Audio("../static/voice.mp3");
    var BGMusic = new Audio("../static/home.ogg");
    BGMusic.loop = true;
    //#endregion

    //#region readPreferences
    $.ajax({url: "/preferences", type: "POST", contentType: "application/json", data: JSON.stringify({intent: "get"}), success: function(response)
    {
        if (response === "False")
        {
            sendGenerationsBox.prop("checked", false); 
        }
        else
        {
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
            generated = true;
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
                    alreadyRated = false;
                    if(sendGenerationsBox.prop("checked"))
                    {
                        didYouLikeOutputContainer.show();
                    }
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
        if (turnedSound === false)
        {
            $("#soundIcon").attr("src","../static/soundicon.png");
            turnedSound = true
            BGMusic.play();
        }
        else
        {
            $("#soundIcon").attr("src","../static/turnedoffsoundicon.png");
            turnedSound = false;
            BGMusic.pause();

        }
    })
    //#endregion

    //#region sendGenerationsBox
    sendGenerationsBox.change(function()
    {
        var checkboxChecked = sendGenerationsBox.prop("checked");
        if (checkboxChecked)
        {
            // Checks if we generated output before changing checkbox state
            if(generated && !(alreadyRated))
            {
                didYouLikeOutputContainer.show();
            }
        }
        else
        {
            didYouLikeOutputContainer.hide();
        }

        $.ajax({url: "/preferences", type: "POST", contentType: "application/json", data: JSON.stringify({intent: "set", sendData: checkboxChecked})});

    });
    //#endregion

    //#region rating
    likeButton.on("click", function()
    {
        $.ajax({url: "/rate", type: "POST", contentType: "application/json", data: JSON.stringify({rate: "like"})});
        didYouLikeOutputContainer.hide();
        alreadyRated = true;
    });

    dislikeButton.on("click", function()
    {
        $.ajax({url: "/rate", type: "POST", contentType: "application/json", data: JSON.stringify({rate: "dislike"})});
        didYouLikeOutputContainer.hide();
        alreadyRated = true;
    })
    //#endregion
});