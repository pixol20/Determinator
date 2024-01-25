$(document).ready(function()
{
    $("#save").on("click", function()
    {
        $.ajax({url: "/generate", type:"POST", success: function(response)
        {
            $("#textPlaceholder").html(response);
        }});
    });
});