$(document).ready(function() {
    $("#sendBtn").click(function() {
        var gameName = $("#game").val();
        alert(gameName);
        var checklist = []
        $("input[type=checkbox]:checked").each(function() {
            var text = $(this).next('label').text();
            checklist.push(text)
        });
    });
});
