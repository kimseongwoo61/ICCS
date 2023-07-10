//글을 작성하고 DB에 저장하는 기능을 구현함.
<?php
	$con = mysqli_connet("localhost", "pl2105", "kids1017", "Training");
		if ( mysqli_connect_errno() ){
			echo '<script>alert("관리자에게 문의 바랍니다.")</script>';
			echo '<script>
				location.href="https://project-inspector-cdhmk.run.goorm.io"
				location.reload();
				</script>'
		}
		
		else{
			
		}
	


?>


<!DOCTYPE html>

<html lang="en">

	<head>
		<title>Window Rev</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
		<link href="../../../../../setting/layout/styles/layout.css" rel="stylesheet" type="text/css" media="all">
	</head>
	<body id="top">
	<!--<?php
		$con = mysqli_connet("localhost", "pl2105", "kids1017", "Training");
		if ( mysqli_connect_errno() ){
		echo '<script>alert("관리자에게 문의 바랍니다.")</script>';
		echo '<script>
			  location.href="https://project-inspector-cdhmk.run.goorm.io"
			  location.reload();
			  </script>'
	}
	
	else{
		$query = "select id, pw from user where id="+ $input_id +"and pw="+ $input_pw;
		$result = mysqli_query($con, $query);
		
		if($result){
			echo '<script>alert("인가 정보가 확인되었습니다!")</script>';
			echo '<script>
			  location.href="../start/start.html"
			  location.reload();
			  </script>'
		}
		
		else{
			echo '<script>alert("다시 입력해 주세요.")</script>';
			echo '<script>location.reload()</script>';
		}
	?>-->
	
	
	
		<div class="bgded overlay padtop" style="background-image:url('../../../../../images/demo/backgrounds/01.png');"> 
			<header id="header" class="hoc clear">
				<div id="logo" class="fl_left"> 
				  <h1><a href="../index.html">COUPS Training</a></h1>
				</div>
				
				<nav id="mainav" class="fl_right"> 
					<ul class="clear">
						<li class="active"><a href="../../../../start.html">Home</a></li>
						
						<li><a class="drop">Challenges</a>
							<ul>
								<li><a href="Reversing.html">Reversing</a></li>
								<li><a href="Pwnable.html">Pwnable</a></li>
								<li><a href="Webhacking.html">Web hacking</a></li>
								<li><a href="Forensics.html">Forensics</a></li>
								<li><a href="Cryptography.html">Cryptography</a></li>
							</ul>
						</li>
							
						<li><a class="drop" href="#">lectures</a>
							<ul>
								<li><a href="#">입문</a></li>
								<li><a href="#">중급</a></li>
								<li><a href="#">고급</a></li>
								<li><a href="#">기술 문서</a></li>
							</ul>
						</li>
							
						<li><a href="#">Auth</a></li>
						<li><a href="#">Forum</a></li>
						<li><a href="#">Tools</a></li>
					</ul>
				</nav>
			</header>
			
			<div id="breadcrumb" class="hoc clear"> 
				<ul>
				  <li><a href="#">- Windows OS -</a></li>
				</ul>
		    </div>
		</div>
		
		<div class="wrapper row1">
			<section id="ctdetails" class="hoc clear"> 
				<ul class="nospace clear">
					<li class="one_quarter first">
						<div class="block clear"><a><i class="fab fa-napster"></i></a> 
						<span><strong> Analyze the file structure!</strong> PE? ELF? Jar? hmm...</span></div>
					</li>
					
					<li class="one_quarter">
						<div class="block clear"><a><i class="fab fa-expeditedssl"></i></a> 
						<span><strong> Take a detour from protection!</strong> Packing? Obfuscation? ... No problem! </span></div>
					</li>
					
					<li class="one_quarter">
						<div class="block clear"><a><i class="far fa-grin-wink"></i></a> 
						<span><strong> Patience is a skill!</strong> You can do it!</span></div>
					</li>
					
					<li class="one_quarter">
						<div class="block clear"><a><i class="fas fa-map-marker-alt"></i></a> 
						<span><strong> Share your results!</strong> Learn various methods of analysis!</a></span></div>
					</li>
				</ul>
			</section>
		</div>

	<div class="wrapper row3">
		<main class="hoc container clear"> 
			<div class="content three_quarter first"> 
				<h1>- Window File Format Reversing -</h1>
				<img class="imgr borderedbox inspace-5" src="../../../../../images/demo/imgr.gif" alt="">
				<p>Window Rev 카테고리에서는 윈도우 실행파일 PE에 관한 분석기술을 다룹니다.
				</br>실핸파일들을 직접 분석해 봄으로서 컴파일된 결과물들의 내부 구조를 보다더 명확히 이해할 수 있습니다.</p></br>
				
				<h1>- Basic Knowledge -</h1>
				<p>* 기초적인 어셈블리어 문법지식
				</br>* 다양한 시스템 아키텍처에 대한 기본적인 밑바탕(ARM, I386, ...)
				</br>* 분석과정에서 사용되는 디버거 사용법</p><br><br>
				
				
				<h1>Contents</h1>
				<div class="scrollable">
					<table>
						<thead>
							<tr>
								<th>문제</th>
								<th>설명</th>
								<th>Point</th>
								<th>결과</th>
							</tr>
						</thead>
						<?php <!--리버싱 문제 화면 출력-->
							$query = "select * from challenge where category='reversing'";
							$result = mysqli_query($con, $query);
						<tbody><!--DB 쿼리 결과를 화면에 표시해야 함.-->
							<tr>
								<td><a href="#">Value 1</a></td>
								<td>Value 2</td>
								<td>Value 3</td>
								<td>Value 4</td>
							</tr>
							<tr>
								<td>Value 5</td>
								<td>Value 6</td>
								<td>Value 7</td>
								<td><a href="#">Value 8</a></td>
							</tr>
							<tr>
								<td>Value 9</td>
								<td>Value 10</td>
								<td>Value 11</td>
								<td>Value 12</td>
							</tr>
							<tr>
								<td>Value 13</td>
								<td><a href="#">Value 14</a></td>
								<td>Value 15</td>
								<td>Value 16</td>
							</tr>
						</tbody>
						?>
					</table>
				</div>
			</div>
			<div class="sidebar one_quarter"> 
				<h6>Remote Terminal Access</h6><!--원격 웹 ssh 통신 관련 URL을 사용할 수 있도록 링크 사용.-->
				<nav class="sdb_holder">	   <!--ID : guest, PW : guest-->
					<ul>
						<a href="https://webanalyzer.run.goorm.io/ssh/host/127.0.0.1" target=”_blank”><li class="fas fa-terminal"></li>  SSH Connnection</a>
						<li>
							<ul>
								
								<li>- ID : guest</li>
								<li>- PW : guest</li>
							</ul>
						</li></br>
						
						<li><a href="#">이용 가능한 도구들</a>
							<ul>
								<li>- Gdb-Peda</li>
								<li>- radare2</li>
								<li>- Python - Pwntools</li>
								<li>- python - angr</li>
							</ul>
						</li>
					</ul>
				</nav>
			</div>
			<div class="clear"></div>
		</main>
	</div>
	
	<div class="wrapper row5">
		<div id="copyright" class="hoc clear"> 
			<p class="fl_left">Copyright &copy; 2018 - All Rights Reserved - <a href="#">---</a></p>
			<p class="fl_right">Made by HackingTeam.Tango</a></p>
		</div>
	</div>
	<a id="backtotop" href="#top"><i class="fas fa-chevron-up"></i></a>
	</body>
</html>