$(document).ready(function() {
    $("#sendBtn").click(function() {
        $("#game").attr("readonly", true);
        var gameName = $("#game").val();
        if(gameName == "") {
            alert("Please enter a game");
            return;
        }

        $("#crd").empty();
        var checklist = []
        $("input[type=checkbox]:checked").each(function() {
            var text = $(this).next('label').text();
            checklist.push(text)
        });
        if (checklist == []) {
            alert("Please select the stores");
            return;
        }
        postData({"game_name": gameName, "stores": checklist}, function(result) {
            console.log(result)
            for(var i = 0; i < checklist.length; i++) {
                var card = `
                <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch">
                    <div class='card'>
                        <img src=`+ result[i]["image"] + ` class="card-img-top" height="250">   
                        <div class='card-body d-flex flex-column'>
                            <h5 class="card-title">`+ result[i].price + `</h5>
                            <p class="card-text">` + result[i].game + `</p>
                            <a href=`+ result[i].link +` class="btn btn-primary mt-auto">`+ result[i].store +`</a>
                        </div>
                    </div>
                </div>
                `
                document.getElementById("crd").insertAdjacentHTML('beforeend', card);
            }
            $("#game").removeAttr("readonly");   
        });
    });
});

function postData(send, callback) {
    $.ajax ({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: 'json',
        url: "/scrape",
        
    
    }).done(function(data){
        callback(data);
    });
}