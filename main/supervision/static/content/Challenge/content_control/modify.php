<!--전달 정보 : title, score, category , contents-->


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
		$title = $_POST[title];
		$category = $_POST[category];
		$score = $_POST[score];
		$id = $_POST[id];
		$contents = $_POST[contents];
		
		$query = "update 게시판 set title="+ $title +", category="+ $category +", score="+ $score +", contents="+ $contents +"where id ="+ $id
		$result = mysqli_query($con, $query);
		
		if($result){
			echo '<script>alert("정상적으로 글이 수정되었습니다.")</script>';
			echo '<script>
			  location.href="../start/start.html"
			  location.reload();
			  </script>'
		}
		
		else{
			echo '<script>alert("다시 입력해 주세요.")</script>';
			echo '<script>location.reload()</script>';
		}
?>
