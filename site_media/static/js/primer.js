//http://github.com/brentp/primer/

var Primer = (function($){

Primer = function(container, width, height, useGlobalMouseMove) {
    this.container = $(container)
    // get the width from the container
    if(!width){
        width  = this.container.width();
        height = this.container.height();
    }
    this.width = width;
    this.height = height;
    this.primer = this
    this.useGlobalMouseMove = useGlobalMouseMove

    this.actions = []
    this.acted = false;

    this.init()

    this.autoDraw = true
}

Primer.prototype = {
    init: function() {
        $("html head").append("<style>.primer_text { position: absolute; margin: 0; padding: 0; line-height: normal; z-index: 0;}</style>")
        var el = this.container.eq(0)

        el.append('<div id="primer_text"></div>')
        var tel = $("#primer_text", el).eq(0)
        tel.css("position", "relative")
        this.element = tel
        // check if there's already a canvas and use it.
        var canvas = $('canvas', this.container)[0] 
        if (canvas){
            this.width |= canvas.width;
            this.height |= canvas.height;
        }
        else {
            // or create a new one.
            canvas = document.createElement('canvas')
        }
        canvas.width = this.width
        canvas.height = this.height
        canvas.style.zIndex |= '0'
        if (canvas.getContext) {
            el.append(canvas);
        } else {
            // if ExplorerCanvas (adds canvas support to IE) is available,
            // use its G_vmlCanvasManager to initialize the canvas element.
            if (window.G_vmlCanvasManager) {
                window.G_vmlCanvasManager.initElement( $(canvas).appendTo(el).get(0) )
            }
        }
        var jelc = $('canvas', el)
        var elc = jelc[0]
        this.context = elc.getContext('2d')

        this.root = new Primer.Layer()
        this.root.bind(this)

        this.setupExt()

        var self = this

        if (this.useGlobalMouseMove) {
            $('body').bind("mousemove", function(e) {
                if ($(e.target).parents().find(this.container)) {
                    var $target = $(elc)
                    var bounds = $target.offset()
                    e.localX = e.pageX - bounds.left
                    e.localY = e.pageY - bounds.top
                    self.ghost(e)
                } else {
                    self.outOfBounds();
                }
            });
        } else {
            var mousefn = function(e){
                var bounds = $(e.currentTarget).offset()
                e.localX = e.pageX - bounds.left
                e.localY = e.pageY - bounds.top
                self.ghost(e)
            };
            jelc.eq(0).bind("mousemove", mousefn).bind("click", mousefn);
        }

      },
  
      getGlobalX: function() {
          return 0
      },
  
      getGlobalY: function() {
          return 0
      },
  
      addChild: function(child) {
          child.bind(this)
          this.root.addChild(child)
          this.draw()
      },

      removeChild: function(child) {
          this.root.removeChild(child)
          this.draw()
      },

      draw: function(forceDraw) {
          if(this.primer.acted){ return;}
          if (forceDraw || this.autoDraw) {
              this.context.clearRect(0, 0, this.width, this.height)
              $(".primer_text", this.element).remove()
              this.setupExt()
              this.primer.acted = true;
              this.root.draw()
          }
      },

      ghost: function(e) {
          this.root.ghost(e)
          for(var i=0, action; action=this.actions[i++];) {
              action[0].apply(action[2], [action[1]])
          }
          this.actions = [];
          this.primer.acted = false;
    },

     outOfBounds: function() {
         // Do nothing by default
     },

    setupExt: function() {
        this.context.ext = {
            textAlign: "left",
            font: "10px sans-serif"
        }
    }
};

Primer.Layer = function() {
    this.primer = null
    this.context = null
    this.element = null
  
    this.children = []
    this.calls = []
  
    this.x = 0
    this.y = 0
  
    this.visible = true
  
    this.mouseWithin = false
}

Primer.Layer.prototype = {
    bind: function(parent) {
        this.parent = parent;
        this.primer = parent.primer;
        this.context = this.primer.context;
        this.element = this.primer.element;

        var child;
        for(var i=0; child=this.children[i++]; child.bind(this));

    },

    /* x and y setters */
    setX: function(x) {
        this.x = x
        if(this.primer) this.primer.draw()
    },

    setY: function(y) {
        this.y = y
        if(this.primer) this.primer.draw()
    },

    /* global x and y getters */
    getGlobalX: function() {
        return this.x + this.parent.getGlobalX()
    },

    getGlobalY: function() {
        return this.y + this.parent.getGlobalY()
    },

    /* visibility getter/setter */
    setVisible: function(visible) {
        this.visible = visible
        if(this.primer) this.primer.draw()
    },

    /* children */
    addChild: function(child) {
        child.bind(this)
        this.children.push(child)
        if(this.primer) this.primer.draw()
    },

    removeChild: function(child) {
        for (var i=0, c; c=this.children[i]; i++) {
            if (c == child) {
                this.children.splice(i, 1); 
                if(this.primer){ this.primer.draw(); }
                break;
            }
        }
    },

    /* events */
    mouseover: function(fn) {
       this.mouseoverVal = fn
    },
    mouseout: function(fn) {
        this.mouseoutVal = fn
    },
    mousemove: function(fn) {
        this.mousemoveVal = fn
    },
    click: function(fn) {
        this.clickVal = fn
    },

    /* find the (first occurence) of style in the current call stack and
     * replace it. if not found, push it onto the current call stack */
    setStyle: function(style, a, overwrite){
        if(!overwrite){
            this.calls.push([style, a]);
            return
        }
        for(var i=0, call; call=this.calls[i]; i++){
              if(call[0] != style) continue;
             
              this.calls[i] = [style, a];
              if(this.primer){ this.primer.draw(); }
              return;
        }
        this.calls.push([style, a]);
    },

    /* canvas api */
    setFillStyle: function(a, overwrite) {
        this.setStyle("fillStyle", a, overwrite);
    },

    setStrokeStyle: function(a, overwrite) {
        this.setStyle("strokeStyle", a, overwrite)
    },

    setLineWidth: function(a, overwrite) {
        this.setStyle("lineWidth", a, overwrite)
    },

    beginPath: function() {
        this.calls.push(["beginPath"])
    },

    moveTo: function(a, b) {
        this.calls.push(["moveTo", a, b])
    },

    lineTo: function(a, b) {
        this.calls.push(["lineTo", a, b])
    },

    quadraticCurveTo: function(a, b, c, d) {
        this.calls.push(["quadraticCurveTo", a, b, c, d])
    },

    arc: function(a, b, c, d, e, f) {
        this.calls.push(["arc", a, b, c, d, e, f])
    },

    fill: function() {
        this.setStyle("fill")
    },
  
    stroke: function() {
        this.calls.push(["stroke"])
    },
  
    fillRect: function(a, b, c, d) {
        this.calls.push(["fillRect", a, b, c, d])
    },
  
    fillText: function(a, b, c, d, e) {
        this.calls.push(["fillText", a, b, c, d, e])
    },
  
    setTextAlign: function(a, overwrite) {
        this.setStyle("textAlign", a, overwrite)
    },
  
    setFont: function(a, overwrite) {
        this.setStyle("font", a, overwrite)
    },
  
    /* meta canvas api */
  
    rect: function(x, y, w, h) {
        this.beginPath()
        this.moveTo(x, y)
        this.lineTo(x + w, y)
        this.lineTo(x + w, y + h)
        this.lineTo(x, y + h)
        this.lineTo(x, y)
    },
  
    roundedRect: function(x, y, w, h, rad) {
        this.beginPath()
        this.moveTo(x, y + rad);
        this.lineTo(x, y + h - rad);
        this.quadraticCurveTo(x, y + h, x + rad, y + h);
        this.lineTo(x + w - rad, y + h);
        this.quadraticCurveTo(x + w, y + h, x + w, y + h - rad);
        this.lineTo(x + w, y + rad);
        this.quadraticCurveTo(x + w, y, x + w - rad, y);
        this.lineTo(x + rad, y);
        this.quadraticCurveTo(x, y, x, y + rad);
    },

    fillRoundedRect: function(x, y, w, h, rad) {
        this.roundedRect(x, y, w, h, rad)
        this.fill()
    },

    /* draw */
    draw: function() {
        if(!this.visible) { return }

        var ctx = this.context;
        ctx.save()
        ctx.translate(this.x, this.y)

        for(var i=0, call, calls=this.calls; call=calls[i]; i++) {
            var method = call[0];

            switch(method) {
                case "moveTo":           ctx.moveTo(call[1], call[2]); break
                case "lineTo":           ctx.lineTo(call[1], call[2]); break
                case "strokeStyle":       ctx.strokeStyle = call[1]; break
                case "lineWidth":           ctx.lineWidth = call[1]; break
                case "fill":               ctx.fill(); break
                case "stroke":           ctx.stroke(); break
                case "fillStyle":           ctx.fillStyle = call[1]; break
                case "fillRect":           ctx.fillRect(call[1], call[2], call[3], call[4]); break
                case "beginPath":           ctx.beginPath(); break
                case "quadraticCurveTo": ctx.quadraticCurveTo(call[1], call[2], call[3], call[4]); break
                case "arc":               ctx.arc(call[1], call[2], call[3], call[4], call[5], call[6]); break
                case "fillText":           this.extFillText(call[1], call[2], call[3], call[4], call[5]); break
                case "textAlign":           ctx.ext.textAlign = call[1]; break
                case "font":               ctx.ext.font = call[1]; break
            }
        }

        for(var i=0, child; child=this.children[i++]; child.draw());
        ctx.restore()
    },

    /* canvas extensions */
    extFillText: function(text, x, y, width, className) {
        var styles = ''
        styles += 'left: ' + (this.getGlobalX() + x) + 'px;'
        styles += 'top: ' + (this.getGlobalY() + y) + 'px;'
        styles += 'width: ' + width + 'px;'
        styles += 'text-align: ' + this.context.ext.textAlign + ';'
        styles += 'color: ' + this.context.fillStyle + ';'
        styles += 'font: ' + this.context.ext.font + ';'
        this.element.append('<p class="primer_text ' + className + '" style="' + styles + '">' + text + '</p>')
    },

    /* ghost */
    ghost: function(e) {
        if(!this.visible) { return }
        var ctx = this.context;

        ctx.save()
        ctx.translate(this.x, this.y)

        for(var i=0, call; call=this.calls[i++]; ) {
            var method = call[0];

            switch(method) {
                  case "beginPath":           ctx.beginPath(); break
                  case "lineTo":           ctx.lineTo(call[1], call[2]); break
                  case "moveTo":           ctx.moveTo(call[1], call[2]); break
                  case "fill":               this.ghostDetect(e); break
                  case "fillRect":           this.ghostFillRect(e, call[1], call[2], call[3], call[4]); break
                  case "quadraticCurveTo": ctx.quadraticCurveTo(call[1], call[2], call[3], call[4]); break
                  case "arc":               ctx.arc(call[1], call[2], call[3], call[4], call[5], call[6]); break
            }
        }

        if (!jQuery.browser.safari) {
            e.localX -= this.x
            e.localY -= this.y
        }

        /* empty loop */
        for(var i=0, child; child=this.children[i++]; child.ghost(e));

        if (!jQuery.browser.safari) {
            e.localX += this.x
            e.localY += this.y
        }

        ctx.restore()
    },

    ghostDetect: function(e) {
        if(this.primer.acted){ return }
        var testX, testY;
        if (!jQuery.browser.safari) {
            testX = e.localX - this.x
            testY = e.localY - this.y
        } else {
            testX = e.localX
            testY = e.localY
        }
        if(this.context.isPointInPath(testX, testY)) {
            if(this.clickVal && e.type == "click"){
                this.primer.actions.push([this.clickVal, e, this])
            }
            else if(!this.mouseWithin && this.mouseoverVal) {
                this.primer.actions.push([this.mouseoverVal, e, this])
                this.mouseWithin = true
                this.primer.acted = true;
             }
             else if(this.mousemoveVal) {
                 this.primer.actions.push([this.mousemoveVal, e, this])
                 this.primer.acted = true;
             } 
        } else {
             if(this.mouseWithin && this.mouseoutVal) {
                 this.primer.actions.push([this.mouseoutVal, e, this])
                 this.mouseWithin = false
                 this.primer.acted = true;
             }
        }
    },

    ghostFillRect: function(e, x, y, w, h) {
        this.context.beginPath()
        this.context.moveTo(x, y)
        this.context.lineTo(x + w, y)
        this.context.lineTo(x + w, y + h)
        this.context.lineTo(x, y + h)
        this.context.lineTo(x, y)
        this.ghostDetect(e)
    }
};
return Primer;
})(jQuery);