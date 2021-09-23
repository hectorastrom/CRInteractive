// Enable Tooltips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
// Fade Flashes
setTimeout(function() {
    $('.alert').fadeOut('slow');
}, 2000);


function drawUserBellCurve(metric_name, metric_value, firstname)
{
    let html = `
    <button id="${metric_name}Button" type="button" class="btn btn-danger" data-toggle="modal" data-target="#${metric_name}modal">
            View Coach's ${metric_name} Rating
    </button> 
    <!-- Modal -->
    <div class="modal fade" id="${metric_name}modal" tabindex="-1" role="dialog" aria-labelledby="${metric_name}modallabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">${metric_name} Curve for ${firstname}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <p class="form-text text-muted text-center">${metric_name}</p>
            <svg
                width="100%"
                height="100%"
                viewBox="0 -3 320 210"
                version="1.1"
                style="margin-bottom:-36%;"
                class = "mt-2"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:svg="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="Gradient1" x1="0" x2=".75" y1="0" y2="0">
                        <stop offset="50%" stop-color="rgba(223,23,34,.5)"/>
                        <stop offset="100%" stop-color="rgba(223,23,200,.5)"/>
                    </linearGradient>
                </defs>
                <g>
                    <path
                    style="fill: url(#Gradient1);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                    d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
                    id="${metric_name}_curve" />
                </g>
                <circle
                    r="6"
                    cy="0"
                    cx="0"
                    id="${metric_name}_dot"
                    style="fill: rgba(177, 23, 49, .8)" />
            </svg>

        </div>
        <div class="modal-footer" style="margin-top: 50px;">
            <button type="button" class="btn btn-secondary close" data-dismiss="modal" aria-label="Close">Close</button>
        </div>
        </div>
    </div>
    </div>
    `;

    document.write(html);

    document.getElementById(`${metric_name}Button`).onclick = function() {
        let dot = document.getElementById(`${metric_name}_dot`);
        let curve = document.getElementById(`${metric_name}_curve`);
        let totalLength = curve.getTotalLength();

        var portion = parseInt(metric_value)/100.0;
        var coordinates = curve.getPointAtLength(portion * totalLength);
        dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);
    }
}


function drawCoachBellCurve(metric_name, metric_value, metric_importance, button_class, is_checked, firstname)
{
    let html = `
    <button id="${metric_name}Button" type="button" class="btn ${button_class}" data-toggle="modal" data-target="#${metric_name}modal">
            Indicate ${metric_name} Rating
    </button> 
    <div class="modal fade" id="${metric_name}modal" tabindex="-1" role="dialog" aria-labelledby="${metric_name}modallabel" aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${metric_name} Curve for ${firstname}</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
                <form action="" method="POST" class="mt-3">
                    <svg
                    width="100%"
                    height="100%"
                    viewBox="0 -3 320 210"
                    version="1.1"
                    style="margin-bottom:-36%;"
                    class = "mt-2"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:svg="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="Gradient1" x1="0" x2=".75" y1="0" y2="0">
                            <stop offset="50%" stop-color="rgba(223,23,34,.5)"/>
                            <stop offset="100%" stop-color="rgba(223,23,200,.5)"/>
                        </linearGradient>
                    </defs>
                    <g>
                        <path
                        style="fill: url(#Gradient1);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                        d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
                        id="${metric_name}_curve" />
                    </g>
                    <circle
                        r="6"
                        cy="0"
                        cx="0"
                        id="${metric_name}_dot"
                        style="fill: rgba(177, 23, 49, .8)" />
                </svg>
                    <p class="form-text text-muted text-center">${metric_name}</p>
                    <div class="form-group short">
                        <div class="slidecontainer">
                            <input type="range" min="0" max="100" value="${metric_value}" class="slider" id="${metric_name}_slider" name="${metric_name}_coach_rating">
                        </div>
                    </div>
                    <div class="form-check mt-4">
                        <div class="row">
                            <label class = "form-check-label" for="${metric_name}_view_allowed">Allow ${firstname} to view this chart: </label>
                            <input type="checkbox" id="${metric_name}_view_allowed" name="${metric_name}_view_allowed" class="form-check-input-xl" ${is_checked}>
                        </div>
                        <div class="form-group short mt-3">
                            <div class="slidecontainer">
                                <input type="range" min="0" max="10" step="1" value="${metric_importance}" class="slider" name="${metric_name}_coach_importance">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer" style="margin-top: 50px;">
                    <div class="form-group col text-center">
                        <button type="submit" class="btn btn-outline-danger rounded-pill">Update</button>
                    </div>
                </div>
            </form>
          </div>
        </div>
      </div>
    `;

    document.write(html);


    document.getElementById(`${metric_name}Button`).onclick = function() {
        let dot = document.getElementById(`${metric_name}_dot`);
        let curve = document.getElementById(`${metric_name}_curve`);
        let totalLength = curve.getTotalLength();
        let slider = document.getElementById(`${metric_name}_slider`);

        var portion = parseInt(metric_value)/100.0;
        var coordinates = curve.getPointAtLength(portion * totalLength);
        dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);

        slider.oninput = function() {
            portion = this.value/100.0;
            coordinates = curve.getPointAtLength(portion * totalLength);
            dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);
        }
    }

}


function enableSorting()
{
    $("#sortable").sortable();
    $("#sortable").disableSelection()
    
    $(".box").each(function(index) {
        console.log(index + ": " + $( this).text())
    })
}