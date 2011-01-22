<script type="text/javascript">
var WIDTH = 958;
var HEIGHT = 838;
var gridWIDTH = 600;
var gridHEIGHT = 600;
var gridOriginX = 150;
var gridOriginY = 30;
var strandList = [ {% for strand in strands %}"{{ strand }}"{% if not forloop.last %},{% endif %}{% endfor %} ].sort();
var knotList = [{% for knot in knots %}['{{ knot.title }}','{{ knot.strand_a }}','{{ knot.strand_b }}','{{ knot.slug }}','{{ knot.tagline }}','{{ knot.blurb }}']{% if not forloop.last %},{% endif %}{% endfor %}]
var knotSet = {};
function buildKnotSet() {
    for (var i = 0; i < knotList.length; i++) {
        var knot = knotList[i];
        if(!knotSet[knot[1]]){
            knotSet[knot[1]] = {};
        }
        //knotSet[knot[1]][knot[2]] = [];
        var knotObject = {};
        knotObject["title"] = knot[0];
        knotObject["slug"] = knot[3];
        knotObject["tagline"] = knot[4];
        knotObject["blurb"] = knot[5];
        if(!(knotSet[knot[1]][knot[2]])){
            knotSet[knot[1]][knot[2]] = [];
        }
        knotSet[knot[1]][knot[2]].push(knotObject);
    }
}
buildKnotSet();
//build a list of knot objects from server, then arrange into set clientside
// var knotSet = {
//     "strand_a": {
//         "strand_b":[{ 
//             "title":"knot.title",
//             "slug":"knot.slug",
//             "tagline":"knot.tagline",
//             "blurb":"knot.blurb" 
//         }, {}],
//     }
// }
var highlightedA = -1;
var highlightedB = -1;
var fillColor = "rgba(0,0,0,1)";
var gridFillColor = "rgba(0,0,0,0.5)";
var textColor = "rgba(0,0,0,0.9)";
var strokeColor = "#660000";
var strokeColorAA = "#EEEEEE";
var highlightColor = "rgba(255,0,0,0.2)";
var textHighlightColor = "rgba(255,0,0,1)";
var backgroundColor = "#ffffff";
var tapCanvas = new Primer('#tapestry', WIDTH, HEIGHT);
// dont draw until all the boxes are added to the screen.
tapCanvas.autoDraw = false;

var hash = '';
if(location.hash){
    hash=location.hash.substr(1).split('&');
}
var strandA = hash[0];
var strandB = '';
highlightedA = strandList.indexOf(strandA)+1;
if(hash.length > 1) {
    strandB = hash[1];
}
highlightedB = strandList.indexOf(strandB)+1;

function drawGrid() {
    var grid = new Primer.Layer();
    var spacingX = gridWIDTH/strandList.length;
    var spacingY = gridHEIGHT/strandList.length;
    for (var i = 1; i <= strandList.length; i++) {
        var drawX = gridOriginX + (i * spacingX);
        var drawY = gridOriginY + (i * spacingY);

        if (i == highlightedA) {
            grid.setFillStyle(highlightColor);
        } else {
            grid.setFillStyle(gridFillColor);
        }
        grid.fillRect( drawX-3, gridOriginY, 6, gridHEIGHT + spacingY);
        if (i == highlightedB) {
            grid.setFillStyle(highlightColor);
        } else {
            grid.setFillStyle(gridFillColor);
        }
        grid.fillRect( gridOriginX, drawY-3, gridWIDTH + spacingX, 6);
        
        grid.setFont("18px 'Droid Sans',Corbel,'Trebuchet MS',sans-serif");
        grid.setFillStyle(fillColor);
        grid.setTextAlign("center");
        grid.fillText(strandList[i-1], drawX - spacingX/2, gridOriginY - 26, spacingX)
        grid.setTextAlign("left");
        grid.fillText(strandList[i-1], 10, drawY - 12, gridOriginX )
    }
    grid.rect(gridOriginX, gridOriginY, gridWIDTH + (spacingX), gridHEIGHT + (spacingY));
    grid.stroke();
    tapCanvas.addChild(grid);
}

function drawDots() {
    var spacingX = gridWIDTH/strandList.length;
    var spacingY = gridHEIGHT/strandList.length;
    for (var a in strandList) {
        for (var b in strandList) {
            if(knotSet[strandList[a]] && knotSet[strandList[a]][strandList[b]]) {
                var kset = knotSet[strandList[a]][strandList[b]];
                var drawX = gridOriginX + ((parseInt(a)+1) * spacingX);
                var drawY = gridOriginY + ((parseInt(b)+1) * spacingY);
                drawDot(strandList[a], strandList[b], kset, drawX, drawY);
            }
        }
    }
}
function drawDot(a, b, kset, x, y) {
    var k = new Primer.Layer();
    var size = kset.length * 15;
    k.size = size;
    
    k.setFillStyle(fillColor);
    k.setStrokeStyle(strokeColor);

    k.setLineWidth(1);

    k.fillRoundedRect(0,0,size,size,size/2);
    k.stroke();
    //k.setStrokeStyle(strokeColorAA);
    //k.roundedRect(-1,-1,size+2,size+2,(size/2)+1);
    //k.stroke();
    k.mouseover(function(){
        document.body.style.cursor = 'pointer';
        this.setFillStyle("#ff0000",true);
        this.draw();
        renderKnotInfo(a, b, kset);
        $("#knots-info").css("top",this.y-$("#knots-info").height()/2);
        $("#knots-info").css("left",this.x-(310+this.size/3));
        $("#knots-info").show();
    });
    k.mouseout(function(){
        document.body.style.cursor = 'default';
        this.setFillStyle(fillColor,true);
        this.draw();
        $("#knots-info").hide();
    });
    // s.click(function(){
    //     this.parent.removeChild(this);
    // });

    k.x = x - size/2;
    k.y = y - size/2;
    tapCanvas.addChild(k);
  }
    //tapCanvas.root.children[5].draw();
        // s.beginPath();
        // s.moveTo(0, 0);
        // s.lineTo(30, 0);
        // s.lineTo(30, 30);
        // s.lineTo(0, 30);
        // s.lineTo(0, 0);
        // s.fill();
// note can attach an event to each
// object and use 'this' to refer to
// that object.
    // s.mousemove(function(e){
    //     this.setX(e.localX); 
    //     this.setY(e.localY); 
    // });
    // tapCanvas.addChild(s);

  drawGrid();
  drawDots();
  $("#spinner").hide();
  tapCanvas.autoDraw = true;
  tapCanvas.root.setVisible(true);


  function renderKnotInfo(a, b, kset) {
    var html = '<h3>'+ a +' & ' + b + '</h3>';
    for (var i in kset){
        knot = kset[i];
        html += '<div class="knot-list" title="'+ knot.blurb + '"><a id="" style="font-size:24px;" href="/knot/'+ knot.slug +'">'+knot.title+'</a>' + '<div>' + knot.tagline + '</div>{#<div>' + knot.blurb + '</div>#}</div>';
    }
    $("#knots-info").html(html);
  }
</script>