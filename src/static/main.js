$(document).ready(function()
{
    $("#save").on("click", function()
    {
        $.ajax({url: "/generate", type:"POST", success: function(response)
        {
            placeholder = $("#textPlaceholder")
            var speed = 30;
            var letterIndex = 0;
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
            }
            eraseAndWrite();
        }});
    });
});