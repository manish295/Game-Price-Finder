$(document).ready(function() {
    $("#sendBtn").click(function() {
        var gameName = $("#game").val();
        var checklist = []
        $("input[type=checkbox]:checked").each(function() {
            var text = $(this).next('label').text();
            checklist.push(text)
        });
        postData({"game_name": gameName, "stores": checklist}, function(result) {
            console.log(result)
            for(var i = 0; i < checklist.length; i++) {
                var card = `
                <div class="col-8 col-lg-4 col-xl-3">
                    <div class='card'>
                        <img src=`+ result[i]["image"].replaceAll(" ","%20") + ` class="card-img-top">   
                        <div class='card-body'>
                            <h5 class="card-title">`+ result[i].price + `</h5>
                            <p class="card-text">` + result[i].game + `</p>
                            <a href="#" class="btn btn-primary">`+ result[i].store +`</a>
                        </div>
                    </div>
                </div>
                `
                document.getElementById("crd").insertAdjacentHTML('beforeend', card);
            }

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