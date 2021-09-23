// Enable Tooltips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
// Fade Flashes
setTimeout(function() {
    $('.alert').fadeOut('slow');
}, 2000);


function drawBellCurve(metric_name, metric_value)
{
    let header = `
    <h1>This is a multi-line string which will be written to the html file. We can have "quotes" in here and we can have ${metric_value} variables in here!</h1>
    `
    document.write(header)
}

function enableSorting()
{
    $("#sortable").sortable();
    $("#sortable").disableSelection()
    
    $(".box").each(function(index) {
        console.log(index + ": " + $( this).text())
    })
}