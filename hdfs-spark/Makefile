up:
	ssh deploy@bddst-g05-Node1 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node1.docker-compose.yaml up -d --build' 
	ssh deploy@bddst-g05-Node2 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node2.docker-compose.yaml up -d --build' 
	ssh deploy@bddst-g05-Node3 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node3.docker-compose.yaml up -d --build' 

down:
	ssh deploy@bddst-g05-Node1 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node1.docker-compose.yaml down' 
	ssh deploy@bddst-g05-Node2 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node2.docker-compose.yaml down' 
	ssh deploy@bddst-g05-Node3 'cd ~/deploy/2022-Big-Data-Semester-Project/hdfs-spark; docker compose -f node3.docker-compose.yaml down' 