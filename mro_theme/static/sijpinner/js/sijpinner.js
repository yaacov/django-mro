(function ($){

  var _validChars = [ 8,      //backspace
                     37,      //left arrow
                     38,      //up arrow
                     39,      //right arrow
                     40,      //down arrow
                     33,      //pageup
                     34 ];    //pagedown
  
  $.fn.sijpinner = function( options ){
  
    var settings = $.extend({
      minimum: 0,
      maximum: 100
    }, options );
  
    return this.each(function(){
    
      /*** START OF LOCAL VARIABLES DEFINITIONS ***/
      
      //this is the inner value of this spinner object
      var value = 0;
      
      /*
       * definitions of various containers.
       * specifically adding support for up and down controllers and
       * overall container
       */
      var container = $("<div/>").addClass("sijpinner-container");
      var upButton = $("<span/>").addClass("add-on")
                                 .append( $("<i/>").addClass("icon-chevron-up")
                                                   .addClass("sijpinner-arrow"));
      var downButton = $("<span/>").addClass("add-on")
                                 .append( $("<i/>").addClass("icon-chevron-down")
                                                   .addClass("sijpinner-arrow"));
      var $this = $(this);
      
      /*** END OF LOCAL VARIABLES DEFINITIONS ***/
      
      /*** START OF LOCAL FUNCTIONS DEFINITIONS ***/
      
      /*
       * changes the inner value by diff. Usually diff
       * should be either 1 or -1.
       * updates the input field accordingly 
       */
      function _changeValue(diff){
        value = _preprocess (value + diff);
        $this.val(value);
      }
      
      /*
       * filter the value through various tests:
       *    in range and is a number
       * if it passed, it will be returned
       * otherwise a better value will be returned
       */
      function _preprocess(val){
        if (val > settings.maximum){
          return settings.maximum;
        }
        if (val < settings.minimum){
          return settings.minimum;
        }
        return isNaN(val)? 0 : val;
      }
      
      /*
       * sets the value of this sijpinner
       * and updates the input field
       */
      function _setValue(val){
        value = _preprocess(val);
        $this.val(value);
        console.log("val=",$this.val(),value);
      }
      
      /*
       * returns the value of the input field
       * as an integer.
       */
      function _getInputValue(){
        try{
          return parseInt($this.val());
        }
        catch(e){
          return 0;
        }
      }
      
      /*** END OF LOCAL FUNCTIONS DEFINITIONS ***/
      
       // layouts the elements in the DOM
      $(this).replaceWith( container );
      container.append( $(this) );
      _setValue(value);
      // adds the up and down buttons
      if (container.css("direction") === "rtl"){
        container.prepend(upButton).prepend(downButton);
        container.addClass("input-append");
      }
      else{
        container.append(upButton).append(downButton);
        container.addClass("input-append");
      }

      //assigns the callbacks for the up/down buttons
      upButton.click(function(ev){
        _changeValue(1);
      });
      
      downButton.click(function(ev){
        _changeValue(-1);
      });
      
      $(this).keypress(function(ev){
        ev = ev || window.event;
        var keyCode = ev.keyCode || ev.which;
        
        if ( _validChars.indexOf(keyCode) > -1 ){
          console.log("very good my minion");
          return true;
        }
        console.log(keyCode);
        var num = parseInt(String.fromCharCode(keyCode), 10);
        return !isNaN(num);
      });
      
      $(this).keyup(function(ev){
        ev = ev || window.event;
        var keyCode = ev.keyCode || ev.which;
        
        switch(keyCode){
          case 38:            //up arrow
            _changeValue(1);
            break;
          case 40:            //down arrow
            _changeValue(-1);
            break;
          case 33:            //page up
            _changeValue(10);
            break;
          case 34:            //page down
            _changeValue(-10);
            break;
          default:            //else
            _setValue(_getInputValue());
            break;
        }
      });
      
      return container;
    });
  };

}(jQuery));
