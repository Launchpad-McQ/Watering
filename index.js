
var ws;
var state;
// state.relayon and state.sensorval
var message = {relaynum: 0, duration: 2, turn: false};
var first = true;




function WebSocketTest()
{
    if ("WebSocket" in window)
    {
        // Let us open a web socket
        //ws = new WebSocket("ws://laser.xkz.se:9998");
//        ws = new WebSocket("ws://192.168.2.144:9998");
       ws = new WebSocket("ws://192.168.1.202:9998");
        //ws = new WebSocket("ws://192.168.1.210:9998");
                        
        // does this when web socket is opened.
        ws.onopen = function()
        {
        };
        
        ws.onmessage = function (event) {
            state = JSON.parse(event.data);
            if (first) {
                message.duration = state.duration;
                document.getElementById("msg").innerHTML = message.duration;
                first = false;
                }
    var myElements = document.querySelectorAll("button");
                for (var i = 0; i < myElements.length; i++) {
                    myElements[i].disabled = state.onschedule;
                }

            for (i = 0; i < 16; i++) { 
                if (state.relayon[i] == true && document.getElementById("btn" + String(i+1)).className == "button") {
                        document.getElementById("btn"+ String(i+1)).className = "button2";
                } else if (state.relayon[i] == false && document.getElementById("btn" + String(i+1)).className == "button2") {
                    document.getElementById("btn"+ String(i+1)).className = "button";
                }
            }

        var elmnt = document.createElement("li");
        var elmnt2 = document.createElement("li");
        var content1 = document.createTextNode(state.relayon);
        var content2 = document.createTextNode(state.duration);    
        elmnt.appendChild(content1);
        elmnt2.appendChild(content2);

        var item = document.getElementById("myList");
        item.replaceChild(elmnt, item.childNodes[0]);
        item.replaceChild(elmnt2, item.childNodes[1]);
        };
                
        ws.onclose = function()
        { 
            // websocket is closed.
            alert("Connection is closed..."); 
        };
                                
        window.onbeforeunload = function(event) {
            socket.close();
        };
    }

    else
    {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
    }
}
function Relay(relaynum)
    {
            // Web Socket is connected, send data using send()
    message.duration = document.getElementById("msg").innerHTML;
    message.relaynum = relaynum;
    message.turn = true;
    ws.send(JSON.stringify(message));
//            document.getElementById("btn1").style.backgroundColor = "red";
    };

function myfunction(){
    state.onschedule=true;
};

        // Watering duration selection
function sampleMenu(item) {
    var elem = document.getElementById('msg');
    event.preventDefault();
    message.duration = item;
    message.turn = false;
    ws.send(JSON.stringify(message));
    elem.innerHTML = message.duration;
};

function dropmenu() {
    message.duration = document.getElementById("mySelect").value;
    message.turn = false;
    ws.send(JSON.stringify(message));
    document.getElementById("mySelect").value = message.duration;
};


// Sensor gauges.
function Sensorgauge(gaugeidx) {

    i=gaugeidx
        var col=document.createElement("div");
        col.className = "column";
        var card=document.createElement("div");
        card.className = "card";
        var tbl=document.createElement("table");
        tbl.setAttribute("align", "center");
        var tr1=document.createElement("tr");
        var tr2=document.createElement("tr");
        var td1=document.createElement("td");
        var td2=document.createElement("td");
        var gauge=document.createElement("div");
        gauge.setAttribute("id", "chart_div"+ String(i));
        gauge.setAttribute("style", "width: 120px; height: 120px;");
        td1.appendChild(gauge);
        tr1.appendChild(td1);
        var btn=document.createElement("button");
        btn.setAttribute("id", "btn" + String(i+1));
        btn.setAttribute("class", "button");
        btn.setAttribute("onclick", "Relay("+String(i)+")");

        var textnode = document.createTextNode("Relay "+i);

        btn.appendChild(textnode);
        
        td2.appendChild(btn);
        tr2.appendChild(td2);

        tbl.appendChild(tr1);
        tbl.appendChild(tr2);
        card.appendChild(tbl);
        col.appendChild(card);
        
        btn.className="button";
        document.getElementById("GaugeBtnCards").appendChild(col);


    google.charts.load('current', {'packages':['gauge']});
    google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        // Label sensor gauges.
        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
            [String(gaugeidx + 1), 50]
        ]);

        var options = {
          width: 120, height: 120,
          redFrom: 80, redTo: 100,
          yellowFrom:60, yellowTo: 80,
          greenFrom: 40, greenTo: 60,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'+String(gaugeidx)));

        chart.draw(data, options);

          // Adding sensor gauges.
        setInterval(function() {
          data.setValue(0, 1, Math.round(100*state.sensorval[gaugeidx]/1023));
          chart.draw(data, options);
        }, 500);
      }
}

