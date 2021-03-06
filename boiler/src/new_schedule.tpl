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
		<h1>Boiler Schedule</h1>
		<form class="form-inline" role="form" action="/newschedule" method="POST">
			<div class="form-group">
				<select class="form-control" name="day">
					<option value="MONDAY">Monday
					<option value="TUESDAY">Tuesday
					<option value="WEDNESDAY">Wednesday
					<option value="THURSDAY">Thursday
					<option value="FRIDAY">Friday
					<option value="SATURDAY">Saturday
					<option value="SUNDAY">Sunday	
				</select>
			</div>
			<div class="form-group">	
				<input type="text" name="time" class="form-control" placeholder ="HH:MM:SS">
			</div>
			<div class="form-group">
				<select class="form-control" name="state" >
					<option value="ON">On
					<option value="OFF">Off
				</select>
			</div>
			<div class="form-group">
			    <select class="form-control" name="tmpl">
			        %for item in tmpl: 
			        <option value="{{item}}">{{item}}
			        %end
			    </select>
			</div>
			<button type="submit" name="save" value="save" class="btn btn-default">Save</button>
		</form>
	</div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>