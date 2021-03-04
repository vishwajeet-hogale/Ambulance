
        var hidden = false;

        setInterval(function() {
          document.getElementById("flash").style.visibility = hidden ? "visible" : "hidden";
          
          hidden = !hidden;
        }, 6000);

  