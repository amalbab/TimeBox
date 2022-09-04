

var eventsList;

function myfunction_onload(){
    const containers = document.querySelectorAll('.container')
    eventsList = []
    containers.forEach(container => {
    console.log("HERE")
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const draggable = document.querySelector('.dragging');
        container.appendChild(draggable);
    })

    $.ajax({
      url:"/onload",
      type:"POST"
  });

})
}

/**
 * grab the text input from HTML
 * */
function myfunction_clickevent(){
    const data = document.getElementById("data").value
    const dict_values = {data}
    const s = JSON.stringify(dict_values)
    get_event_data(s)

}

function myfunction_schedule(){
    console.log('here');
    $.ajax({
      url:"/schedule",
      type:"POST"  
    });
}

/**
 * @param {JSON} x the text grabbed from HTML
 * Use api to schedule events on Google Calendar
 * */
function get_event_data(s){
  $.ajax({
        url:"/test",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s),
        dataType:'json',
        success : function(data){
            calendarHandler(data);
        }
    });
}



// create the boxes from the tasks
function calendarHandler(s){

    // const element = document.getElementById('task-visuals')

    for (var key in s){
        console.log(s[key].summary);

        eventsList.push(s)

        // const text = document.createTextNode(s[key].summary);

        // box.classList.add('task-box');
        // box.classList.add('round-corners');
        // box.classList.add('draggable');

        const event_date = s[key]
        const parent = get_parent(event_date);
        const box = create_list_event(event_date);

        const a_tag = document.createElement("a");
        a_tag.setAttribute('href', "#0")

        const content = document.createElement("em");
        content.classList.add("event-name")

        const text = document.createTextNode(s[key].summary);
        


        // box.setAttribute('draggable', true)

        // box.appendChild(text);

        // make_draggable(box);
        // console.log(box.style.height)
        parent.appendChild(box);
        box.appendChild(a_tag)
        a_tag.appendChild(content)
        content.appendChild(text)
    }

}

function get_parent(event_data){
    const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    var startDate = event_data.start.dateTime
    startDate = new Date(startDate);



    const startDay = weekday[startDate.getDay()].toLowerCase();



    return document.getElementById(startDay + "-events")


}

function create_list_event(event_data){
    const box = document.createElement('li');

    var startDate = event_data.start.dateTime
    var endDate = event_data.end.dateTime

    startDate = new Date(startDate);
    endDate = new Date(endDate);

    const startTime = startDate.getHours() + ":" + (startDate.getMinutes() < 10?"0":"") + startDate.getMinutes();
    const endTime = endDate.getHours() + ":" + (endDate.getMinutes() < 10?"0":"") + endDate.getMinutes();

    console.log(endTime)


    box.classList.add('single-event')

    box.setAttribute('data-start', startTime)
    box.setAttribute('date-end', endTime)
    box.setAttribute('data-event', "event-1")

    css = add_schedule_UI(startDate, endDate)
    $(box).css(css)


    return box

}

function add_schedule_UI(startDate, endDate, box){

    calStart = 9;
    calHours = 9;
    total_height = document.getElementById('monday-events').clientHeight;

    startTime = startDate.getHours() + startDate.getMinutes() / 60;
    endTime = endDate.getHours() + endDate.getMinutes() / 60;

    eventTop = ((startTime - calStart)/calHours) * total_height;

    eventHeight = ((endTime- startTime) / calHours) * total_height;


    const css =  {top : (eventTop - 4) + 'px',height : (eventHeight + 4) + 'px'};
    return css;


}

function make_draggable(draggable){
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')
    })

}