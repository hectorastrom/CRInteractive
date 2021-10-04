// Enable Tooltips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
// Fade Flashes
setTimeout(function() {
    $('.alert').fadeOut('slow');
}, 3000);


function drawUserBellCurve(metric_tag, metric_name, metric_desc, metric_value, metric_importance, metric_notes, firstname)
{
    let html = `
    <div class="row justify-content-center">
        <button id="${metric_tag}Button" type="button" class="btn metric-button" data-toggle="modal" data-target="#${metric_tag}modal">
                Coach's ${metric_name} Rating
        </button> 
    </div>
    <!-- Modal -->
    <div class="modal fade" id="${metric_tag}modal" tabindex="-1" role="dialog" aria-labelledby="${metric_tag}modallabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">${metric_name} Curve for ${firstname}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <h5><strong>Description:</strong> ${metric_desc}</h5>
            <svg
                width="100%"
                height="100%"
                viewBox="0 -3 320 210"
                version="1.1"
                style="margin-bottom:-36%;"
                class = "mt-2"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:svg="http://www.w3.org/2000/svg">
                <g>
                    <path
                    style="fill: url(#CurveGradient);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                    d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
                    id="${metric_tag}_curve" />
                </g>
                <circle
                    r="6"
                    cy="0"
                    cx="0"
                    id="${metric_tag}_dot"
                    style="fill: rgba(177, 23, 49, .8)" />
            </svg>
            <p class="form-text text-muted text-center">${metric_name}</p>

            <div class="slidecontainer mt-4">
                <label for="${metric_tag}_coach_importance" style="margin-left:14%;">Importance</label>
                <input type="range" min="0" max="10" step="1" value="${metric_importance}" class="slider slider-yellow disabled" disabled>
            </div>
            <div class="form-group mt-3">
                <label style="margin-left:14%;" for="${metric_tag}_coach_notes">Coach Notes:</label>
                <textarea style="opacity:.8;" disabled class="form-control notes" id="${metric_tag}_coach_notes" name="${metric_tag}_coach_notes">${metric_notes}</textarea>
            </div>

        </div>
        <div class="modal-footer" style="margin-top: 50px;">
            <button type="button" class="btn btn-secondary close" data-dismiss="modal" aria-label="Close">Close</button>
        </div>
        </div>
    </div>
    </div>
    `;

    document.write(html);

    document.getElementById(`${metric_tag}Button`).onclick = function() {
        let dot = document.getElementById(`${metric_tag}_dot`);
        let curve = document.getElementById(`${metric_tag}_curve`);
        let totalLength = curve.getTotalLength();

        var portion = parseInt(metric_value)/100.0;
        var coordinates = curve.getPointAtLength(portion * totalLength);
        dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);
    }
    let mod_button = document.getElementById(`${metric_tag}Button`)

    if (metric_value <= 25)
    {
        // Firebrick
        mod_button.style.backgroundColor = "rgb(178,34,34)"
    }
    else if (metric_value <= 50)
    {
        // Orangered
        mod_button.style.backgroundColor = "rgb(255,69,0)"
    }
    else if (metric_value <= 85)
    {
        // Green
        mod_button.style.backgroundColor = "rgb(34,139,34)"
    }
    else
    {
        // Golden rod
        mod_button.style.backgroundColor = "rgb(218,165,32)"
    }
}


function drawCoachBellCurve(metric_tag, metric_name, metric_desc, metric_value, metric_importance, metric_notes, button_class, active, firstname)
{
    let eyeball = ""
    if (active)
    {
        eyeball=`<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
        width="30" height="30"
        viewBox="0 0 30 30"
        style=" fill:#000000;">    <path d="M 15 5 C 6.081703 5 0.32098813 14.21118 0.21679688 14.378906 A 1 1 0 0 0 0 15 A 1 1 0 0 0 0.16210938 15.544922 A 1 1 0 0 0 0.16601562 15.550781 C 0.18320928 15.586261 5.0188313 25 15 25 C 24.938822 25 29.767326 15.678741 29.826172 15.564453 A 1 1 0 0 0 29.837891 15.544922 A 1 1 0 0 0 30 15 A 1 1 0 0 0 29.785156 14.380859 A 1 1 0 0 0 29.783203 14.378906 C 29.679012 14.21118 23.918297 5 15 5 z M 15 8 C 18.866 8 22 11.134 22 15 C 22 18.866 18.866 22 15 22 C 11.134 22 8 18.866 8 15 C 8 11.134 11.134 8 15 8 z M 15 12 A 3 3 0 0 0 12 15 A 3 3 0 0 0 15 18 A 3 3 0 0 0 18 15 A 3 3 0 0 0 15 12 z"></path></svg>`
    }
    let html = `
    <div class="metric-eye">
    <button id="${metric_tag}Button" type="button" class="btn ${button_class} metric-button" data-toggle="modal" data-target="#${metric_tag}modal">${metric_name}</button> 
    <p class="eyeball">${eyeball}</p>
    </div>

    <div class="modal fade" id="${metric_tag}modal" tabindex="-1" role="dialog" aria-labelledby="${metric_tag}modallabel" aria-hidden="true">
        <div class="modal-dialog modal-xl" role="document">
          <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">${metric_name} Curve for ${firstname}</h5>
                <svg id="${metric_tag}_allowEye" class="allow-eye ${active}"
                xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                width="30" height="30"
                viewBox="0 0 30 30"><path d="M 15 5 C 6.081703 5 0.32098813 14.21118 0.21679688 14.378906 A 1 1 0 0 0 0 15 A 1 1 0 0 0 0.16210938 15.544922 A 1 1 0 0 0 0.16601562 15.550781 C 0.18320928 15.586261 5.0188313 25 15 25 C 24.938822 25 29.767326 15.678741 29.826172 15.564453 A 1 1 0 0 0 29.837891 15.544922 A 1 1 0 0 0 30 15 A 1 1 0 0 0 29.785156 14.380859 A 1 1 0 0 0 29.783203 14.378906 C 29.679012 14.21118 23.918297 5 15 5 z M 15 8 C 18.866 8 22 11.134 22 15 C 22 18.866 18.866 22 15 22 C 11.134 22 8 18.866 8 15 C 8 11.134 11.134 8 15 8 z M 15 12 A 3 3 0 0 0 12 15 A 3 3 0 0 0 15 18 A 3 3 0 0 0 18 15 A 3 3 0 0 0 15 12 z"></path></svg>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <h5><strong>Description:</strong> ${metric_desc}</h5>
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
                    <g>
                        <path
                        style="fill: url(#CurveGradient);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                        d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
                        id="${metric_tag}_curve" />
                    </g>
                    <circle
                        r="6"
                        cy="0"
                        cx="0"
                        id="${metric_tag}_dot"
                        style="fill: rgba(177, 23, 49, 1)" />
                    </svg>
                    <p class="form-text text-muted text-center">${metric_name}</p>
                    <div class="form-group short">
                        <label for="${metric_tag}_slider" style="margin-left:14%;">Rating</label>
                        <div class="slidecontainer">
                            <input type="range" min="0" max="100" value="${metric_value}" class="slider" id="${metric_tag}_slider" name="${metric_tag}_coach_rating">
                        </div>
                    </div>
                    <div class="form-check mt-4">
                        <input type="hidden" value="${active}" id="${metric_tag}_view_allowed" name="${metric_tag}_view_allowed" />
                    </div>
                    <div class="form-group short mt-3">
                        <label for="${metric_tag}_coach_importance" style="margin-left:14%;">Coaches' Suggested Level of Prioritization in Practice/Racing</label>
                        <div class="slidecontainer">
                            <input type="range" min="0" max="10" step="1" value="${metric_importance}" class="slider slider-yellow" id="${metric_tag}_coach_importance" name="${metric_tag}_coach_importance">
                        </div>
                    </div>
                    <div class="form-group">
                        <label style="margin-left:14%;" for="${metric_tag}_coach_notes">Additional Notes:</label>
                        <textarea class="form-control notes" id="${metric_tag}_coach_notes" name="${metric_tag}_coach_notes" rows="2">${metric_notes}</textarea>
                    </div>
                </div>
                <div class="modal-footer" style="margin-top: 50px;">
                    <div class="form-group col text-center">
                        <button type="submit" class="btn btn-outline-danger rounded-pill">Update</button>
                    </div>
                </div>
                <input type="hidden" value="${metric_tag}" name="form_identifier" />
            </form>
          </div>
        </div>
      </div>
    `;

    document.write(html);


    document.getElementById(`${metric_tag}Button`).onclick = function() {
        let dot = document.getElementById(`${metric_tag}_dot`);
        let curve = document.getElementById(`${metric_tag}_curve`);
        let totalLength = curve.getTotalLength();
        let slider = document.getElementById(`${metric_tag}_slider`);
        
        var portion = parseInt(slider.value)/100.0;
        var coordinates = curve.getPointAtLength(portion * totalLength);
        dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);

        slider.oninput = function() {
            portion = this.value/100.0;
            coordinates = curve.getPointAtLength(portion * totalLength);
            dot.setAttribute("transform", `translate(${coordinates.x}, ${coordinates.y})`);
        }
    }
    let hidden_view_input = document.getElementById(`${metric_tag}_view_allowed`);
    document.getElementById(`${metric_tag}_allowEye`).onclick = function() {
        if (this.classList.contains("active"))
        {
            this.classList.remove("active");
            hidden_view_input.value = "";
        }
        else
        {
            this.classList.add("active");
            hidden_view_input.value = "active";
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