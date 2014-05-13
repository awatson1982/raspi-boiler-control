<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Schedule</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
	    <h1>New User</h1>
	    <form class="form-inline" role="form" action="/newuser" method="POST">
	      <div class="form-group">
	        User Name: <input type="text" name="userid" class="form-control" placeholder ="User Name" required autocomplete="off"> 
	      </div>
	      <div class="form-group">
	        Password:<input type="password" name="password" class="form-control" placeholder ="Password" required autocomplete="off">
	      </div>
	      <div class="form-group">
	        Confirm Password:<input type="password" name="confpassword" class="form-control" placeholder ="Confirm Password" required autocomplete="off">
	      </div>
	    <br/>
  	    <button type="submit" name="save" value="save" class="btn btn-default">Save</button>
	    </form>
    </div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>