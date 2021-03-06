<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Boiler Control</title>

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
		<h1>Boiler Control</h1>
		<div class="btn-group">
			<form method="post" action="/newuser">
				<button type="submit" class="btn btn-default">New User</button>
	 		</form>
	 	</div>
		<div class="btn-group">
			<form method="post" action="/getschedule">
				<button type="submit" class="btn btn-default">Set Schedule</button>
			</form>
		</div>
		<div class="btn-group">
			<form method="post" action="/main">
	 			<input type="submit" class="btn btn-default" name="override" value="override">
	 		</form>
	 	</div>
	 	<div class="btn-group">
			<form method="post" action="/settemp">
	 			<button type="submit" class="btn btn-default" name="settemp">Set Temp</button>
	 		</form>
	 	</div>
		<h3>Current Temp:</h3> 
	 	Room {{roomTemp}}<br>
	 	Radiator {{radTemp}}<br>
	 	Outside {{outsideTemp}}
	 </div>
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
