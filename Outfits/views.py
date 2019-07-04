{% load staticfiles %}
<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Dashboard</title>

    <!-- Bootstrap core CSS -->
    <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

    <!-- Custom fonts for this template -->
    <link href="{% static 'vendor/fontawesome-free/css/all.min.css' %}" rel="stylesheet" type="text/css">
    <link href='https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>

    <!-- Custom styles for this template -->
    <link href="{% static 'css/clean-blog.min.css' %}" rel="stylesheet">

  </head>

  <body>

    <!-- Navigation -->

    <!-- Page Header -->
    <header class="masthead" style="background-image: url('/static/img/possible-head2.jpg')">
      <div class="overlay"></div>
      <div class="container">
        <div class="row">
          <div class="col-lg-8 col-md-10 mx-auto">
            <div class="page-heading">
              <h1 style = "color: white !important">Hello {{user.username}}</h1>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Post Content -->
    <!-- Main Content -->
    <div class="clearfix">
      <a class="btn btn-primary float-right" href="{% url 'newitem' %}">Add Clothes</a>
    </div>

    <div class="clearfix">
        <a class="btn btn-primary float-left " href="{% url 'myclothes' %}">View my Clothes/Outfits</a>
    </div>

    {% if not styleChosen %}
      <h4> You have not chosen a style preference</h4>
      <h4> Outfits are generated at random if you do not choose one </h4>
      <div class="clearfix">
          <center><a class="btn btn-primary" id = "choiceBtn" href="#">Choose Style Preference</a></center>
      </div>
    {% else %}
    <div class="clearfix">
        <center><a class="btn btn-primary" id = "choiceBtn" href="#">Change Style Preference</a></center>
    </div>
    {% endif %}


    <div class="clearfix">
        <center><a class="btn btn-primary" id = "myBtn" href="#">Generate an Outfit</a></center>
    </div>

    <div id = "myModal" class = "modal">
      <div class = "modal-content">
        <span class = "close">&times;</span>
        
        {% if insufficient %}
          <center><h4>Could not generate outfit due to lack of clothes!</h4></center>
          <div class="clearfix">
            <center><a class="btn btn-primary" href="{% url 'newitem' %}">Click here to add Clothes</a></center>
          </div>
        {% else %}
        <center><h2>Your Outfit!</h2></center>
        {% for cloth in myclothes %}
<!--Name--><h3 id="name">{{cloth.name}}</h3><!--EndName-->
<!--Image--><img src = "{{MEDIA_URL}}{{cloth.image}}"><!--EndImage-->
      {% endfor %}
      <div class="clearfix">
        <center><a class="btn btn-primary" id = "newBtn" href="#">Generate another</a></center>
      </div>

      <div class="clearfix">
          <form action="" method="POST">
              {% csrf_token %}
              <center><input class = "btn btn-primary" type="submit" name="Dislike" value="Dislike" /></center>
          </form>
      </div>
        {% endif %}


      </div>
    </div>

    <div id = "myModal1" class = "modal">
      <div class = "modal-content">
        <span class = "close">&times;</span>
        <div class="clearfix">
          <form action = "" method = "POST">
            {% csrf_token %}
            <img src = "{% static 'img/alexcosta.jpg' %}" height = "300" width = "300">
            <input class  = "btn btn-primary" type = "submit" id = "Style1" name = "Alex Costa Outfits" value = "StyleOne">
            <img src = "{% static 'img/alpham.jpg' %}" height = "300" width = "300">
            <input class  = "btn btn-primary" type = "submit" id = "Style2" name = "Alpha M Outfits" value = "StyleTwo">
            <img src = "{% static 'img/TMF.jpg' %}" height = "300" width = "300" >
            <input class  = "btn btn-primary" type = "submit" id = "Style3" name = "TMF Outfits" value = "StyleThree">
          </form>
        </div>
      </div>
    </div>
    
    <div id = "loadingModal" class = "modal">
      <div class = "modal-content">
        <center><p>Please wait while we come up with outfits! May take 5 seconds to refresh page</p></center>
      </div>
    </div>




    <!-- Footer -->
    <footer>
      <div class="container">
        <div class="row">
          <div class="col-lg-8 col-md-10 mx-auto">

            <p class="copyright text-muted">Copyright &copy; Sober Society</p>
          </div>
        </div>
      </div>
    </footer>

    <!-- Bootstrap core JavaScript -->
    <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
    <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <!-- Custom scripts for this template -->
    <script>
      // Get the modal
        var modal = document.getElementById("myModal");
        var choiceModal = document.getElementById("myModal1")
        var loadingModal = document.getElementById("loadingModal")

        // Get the button that opens the modal
        var styleOne = document.getElementById("Style1")
        var styleTwo = document.getElementById("Style2")
        var styleThree = document.getElementById("Style3")
        var btn = document.getElementById("myBtn");
        var newBtn = document.getElementById("newBtn");
        var choiceBtn = document.getElementById("choiceBtn")

        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks the button, open the modal 
        var clicked = false
        styleOne.onclick = function(){
          choiceModal.style.display = "none";
          loadingModal.style.display = "block";
        }
        btn.onclick = function() {
          alert("hey you clicked me")
          modal.style.display = "block";
        }

        choiceBtn.onclick = function(){
          alert("hey you clicked me")
          choiceModal.style.display = "block";
        }

        newBtn.onclick = function(){
          $.ajax({
            method:"GET",
            url: 'http://127.0.0.1:8000/dashboard',
            success:function(data){
              //First Name indices
              modal.style.display = "none";
              modal.style.display = "block";
              // Stored all names in array
              itemNames = []
              //Store all images in Array
              itemImages = []
              //console.log(firstNewImage)
              //console.log(secondNewImage)
                //Change name and images of all items
              lines = data.split('\n')
              for (i=0;i<lines.length;i++){
                if (lines[i].startsWith('<!--Name')){
                  startingIndex = lines[i].indexOf('<h3')+14
                  endingIndex = lines[i].indexOf('</h3>')
                  itemNames.push(lines[i].slice(startingIndex,endingIndex))
                } else if(lines[i].startsWith('<!--Image')){
                  startingImageIndex = lines[i].indexOf('<img')
                  endingImageIndex = lines[i].indexOf('<!--End')
                  itemImages.push(lines[i].slice(startingImageIndex,endingImageIndex))
                }
              
              }
              for (i=0;i<itemNames.length;i++){
                  document.getElementsByTagName('h3')[i].innerHTML = itemNames[i]
                  document.getElementsByTagName('img')[i].outerHTML = itemImages[i]
              }
              console.log(itemImages)
            },
            failure: function(data){
              console.log('fail bro')
            }
          })
          //modal.style.display = "block";
        }

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
          choiceModal.style.display = "none";
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.display = "none";
          }
          if (event.target == choiceModal){
            choiceModal.style.display = "none";
          }
        }
    </script>
  </body>

</html>
