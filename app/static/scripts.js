// Enable Tooltips and Popovers
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover()
});
// Fade Flashes
setTimeout(function() {
    $('.alert').fadeOut('slow');
}, 3000);


function drawUserBellCurve(has_update, metric_tag, metric_name, metric_desc, coach_value, coach_importance, user_value, metric_notes, firstname)
{
    let coach_info_html = ""
    let user_curve_html = ""
    let lock_image = ""

    if (has_update)
    {
        lock_image = "lock.png"
        user_curve_html = `
        <h4 class="mt-4">Before viewing the coach's rating, indicate your perceived ${metric_name} competence:</h4>
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
                style="fill: url(#CurveGradient2);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
                d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
                id="${metric_tag}_user_curve" />
            </g>
            <circle
                r="6"
                cy="0"
                cx="0"
                id="${metric_tag}_user_dot"
                style="fill: rgba(177, 23, 49, 1)" />
            </svg>
            <p class="form-text text-muted text-center">${metric_name}</p>
            <div class="form-group short">
                <label for="${metric_tag}_user_slider" style="margin-left:14%;">Your Rating</label>
                <div class="slidecontainer">
                    <input type="range" min="0" max="100" value="${user_value}" class="slider" id="${metric_tag}_user_slider" name="${metric_tag}_user_rating">
                </div>
            </div>
            <div class="form-group col text-center">
                <button type="submit" class="btn btn-outline-danger rounded-pill mt-4">Indicate</button>
            </div>
            <input type="hidden" value="${metric_tag}" name="form_identifier" />
        </form>
        `
    }
    // If there is no new update:
    else 
    {
    lock_image = "unlock.png"
        coach_info_html = `
    <div class="row justify-content-center"> 
        <h1 style="font-size: 4vh;">Per Coaches:</h1>
    </div>
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
            style="fill: url(#CurveGradient1);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
            d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
            id="${metric_tag}_coach_curve" />
        </g>
        <circle
            r="6"
            cy="0"
            cx="0"
            id="${metric_tag}_coach_dot"
            style="fill: rgba(177, 23, 49, 1)" />
    </svg>
    <p class="form-text text-muted text-center">${metric_name}</p>

    <div class="slidecontainer mt-4">
        <label for="${metric_tag}_coach_importance" style="margin-left:14%;">Coaches' Suggested Level of Prioritization in Practice/Racing: <span style="font-weight: bold;">${coach_importance}</span></label>
        <input type="range" min="0" max="10" step="1" value="${coach_importance}" class="slider slider-yellow disabled" disabled>
    </div>
    <div class="form-group mt-3">
        <label style="margin-left:14%;" for="${metric_tag}_coach_notes">Coach Notes:</label>
        <textarea style="opacity:.8;" disabled class="form-control notes" id="${metric_tag}_coach_notes" name="${metric_tag}_coach_notes">${metric_notes}</textarea>
    </div>
    `
        user_curve_html = `
    <div class="row justify-content-center"> 
        <h1 style="font-size: 4vh;" class="mt-4">Per You:</h1>
    </div>
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
            style="fill: url(#CurveGradient2);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
            d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
            id="${metric_tag}_user_display_curve" />
        </g>
        <circle
            r="6"
            cy="0"
            cx="0"
            id="${metric_tag}_user_display_dot"
            style="fill: rgba(177, 23, 49, 1)" />
    </svg>
    <p class="form-text text-muted text-center">${metric_name}</p>
    `
    }



    let html = `
    
    <div class="metric-group">
        <button id="${metric_tag}Button" type="button" class="btn metric-button" data-toggle="modal" data-target="#${metric_tag}modal">
                ${metric_name} Rating
        </button>
        <img width="30" height="30" class="eyeball" src="/static/${lock_image}">
    </div>
    <!-- Modal -->
    <div class="modal fade" id="${metric_tag}modal" tabindex="-1" role="dialog" aria-labelledby="${metric_tag}modallabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h4 class="modal-title">${metric_name} Curves for ${firstname}</h4>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <h5 class="border-bottom border-dark pb-2" style="border-width:2px !important;"><strong>Description:</strong> ${metric_desc}</h5>
            ${coach_info_html}
            ${user_curve_html}
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
        if (has_update)
        {
            let user_dot = document.getElementById(`${metric_tag}_user_dot`);
            let user_curve = document.getElementById(`${metric_tag}_user_curve`);
            let user_total_length = user_curve.getTotalLength();
            let user_slider = document.getElementById(`${metric_tag}_user_slider`);
            
            var user_portion = parseInt(user_slider.value)/100.0;
            var user_coords = user_curve.getPointAtLength(user_portion * user_total_length);
            user_dot.setAttribute("transform", `translate(${user_coords.x}, ${user_coords.y})`);
            
            user_slider.oninput = function() {
                user_portion = this.value/100.0;
                user_coords = user_curve.getPointAtLength(user_portion * user_total_length);
                user_dot.setAttribute("transform", `translate(${user_coords.x}, ${user_coords.y})`);
            }

        }
        else
        {
            let coach_dot = document.getElementById(`${metric_tag}_coach_dot`);
            let coach_curve = document.getElementById(`${metric_tag}_coach_curve`);
            let coach_total_length = coach_curve.getTotalLength();
    
            var coach_portion = parseInt(coach_value)/100.0;
            var coach_coords = coach_curve.getPointAtLength(coach_portion * coach_total_length);
            coach_dot.setAttribute("transform", `translate(${coach_coords.x}, ${coach_coords.y})`);

            let user_display_dot = document.getElementById(`${metric_tag}_user_display_dot`);
            let user_display_curve = document.getElementById(`${metric_tag}_user_display_curve`);
            let user_display_total_length = user_display_curve.getTotalLength();
    
            var user_display_portion = parseInt(user_value)/100.0;
            var user_display_coords = user_display_curve.getPointAtLength(user_display_portion * user_display_total_length);
            user_display_dot.setAttribute("transform", `translate(${user_display_coords.x}, ${user_display_coords.y})`);

        }

    }
    let mod_button = document.getElementById(`${metric_tag}Button`)

    if (coach_value <= 25)
    {
        mod_button.style.backgroundColor = "#fb5607";
    }
    else if (coach_value <= 50)
    {
        mod_button.style.backgroundColor = "#ff006e";
    }
    else if (coach_value <= 85)
    {
        mod_button.style.backgroundColor = "#8338ec";
    }
    else
    {
        mod_button.style.backgroundColor = "#3a86ff";
    }
}


function drawCoachBellCurve(has_update, metric_tag, metric_name, metric_desc, coach_value, coach_importance, user_value, metric_notes, button_class, active, firstname)
{
    let user_curve_html = ""
    if (!has_update)
    {
        user_curve_html = `
    <div class="row justify-content-center"> 
        <h1 style="font-size: 4vh;" class="mt-4">${firstname}'s Rating:</h1>
    </div>
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
            style="fill: url(#CurveGradient2);fill-opacity:0.529138;stroke:rgba(0, 0, 0, .6);stroke-width:2.365;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
            d="m 43.19351,92.098556 c 0,0 19.633412,1.07091 37.48197,-11.42308 17.848559,-12.49399 32.48437,-36.054082 32.48437,-36.054082 0,0 17.55469,-24.234497 20.41046,-27.528229 2.0916,-2.412365 10.16471,-12.6418523 21.58779,-12.2848823 11.42307,0.356971 18.32988,5.1869094 24.39839,12.6833043 6.06851,7.496392 28.11147,38.775991 28.11147,38.775991 0,0 19.6434,24.001346 27.35292,27.888368 7.66874,3.866459 10.50607,5.916948 30.90469,7.18536"
            id="${metric_tag}_user_display_curve" />
        </g>
        <circle
            r="6"
            cy="0"
            cx="0"
            id="${metric_tag}_user_display_dot"
            style="fill: rgba(177, 23, 49, 1)" />
    </svg>
    <p class="form-text text-muted text-center">${metric_name}</p>
    `
    }

    let eyeball = ""
    if (active)
    {
        eyeball=`<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
        width="30" height="30"
        viewBox="0 0 30 30"
        style=" fill:#000000;">    <path d="M 15 5 C 6.081703 5 0.32098813 14.21118 0.21679688 14.378906 A 1 1 0 0 0 0 15 A 1 1 0 0 0 0.16210938 15.544922 A 1 1 0 0 0 0.16601562 15.550781 C 0.18320928 15.586261 5.0188313 25 15 25 C 24.938822 25 29.767326 15.678741 29.826172 15.564453 A 1 1 0 0 0 29.837891 15.544922 A 1 1 0 0 0 30 15 A 1 1 0 0 0 29.785156 14.380859 A 1 1 0 0 0 29.783203 14.378906 C 29.679012 14.21118 23.918297 5 15 5 z M 15 8 C 18.866 8 22 11.134 22 15 C 22 18.866 18.866 22 15 22 C 11.134 22 8 18.866 8 15 C 8 11.134 11.134 8 15 8 z M 15 12 A 3 3 0 0 0 12 15 A 3 3 0 0 0 15 18 A 3 3 0 0 0 18 15 A 3 3 0 0 0 15 12 z"></path></svg>`
    }
    let html = `
    <div class="metric-group">
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
                ${user_curve_html}
                <div class="row justify-content-center"> 
                    <h1 style="font-size: 4vh;" class="mt-4">Coach's Rating:</h1>
                </div>
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
                            <input type="range" min="0" max="100" value="${coach_value}" class="slider" id="${metric_tag}_slider" name="${metric_tag}_coach_rating">
                        </div>
                    </div>
                    <div class="form-check mt-4">
                        <input type="hidden" value="${active}" id="${metric_tag}_view_allowed" name="${metric_tag}_view_allowed" />
                    </div>
                    <div class="form-group short mt-3">
                        <label for="${metric_tag}_coach_importance" style="margin-left:14%;">Coaches' Suggested Level of Prioritization in Practice/Racing: <span style="font-weight: bold;" id="${metric_tag}_importance_num">${coach_importance}</span></label>
                        <div class="slidecontainer">
                            <input type="range" min="0" max="10" step="1" value="${coach_importance}" class="slider slider-yellow" id="${metric_tag}_coach_importance" name="${metric_tag}_coach_importance">
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

        let importance_num = document.getElementById(`${metric_tag}_importance_num`)
        let importance_slider = document.getElementById(`${metric_tag}_coach_importance`);
        importance_slider.oninput = function() {
            importance_num.innerHTML = this.value;
        }


        if (!has_update)
        {
            let user_display_dot = document.getElementById(`${metric_tag}_user_display_dot`);
            let user_display_curve = document.getElementById(`${metric_tag}_user_display_curve`);
            let user_display_total_length = user_display_curve.getTotalLength();
    
            var user_display_portion = parseInt(user_value)/100.0;
            var user_display_coords = user_display_curve.getPointAtLength(user_display_portion * user_display_total_length);
            user_display_dot.setAttribute("transform", `translate(${user_display_coords.x}, ${user_display_coords.y})`);
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