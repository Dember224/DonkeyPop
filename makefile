initialize:
	docker build -t donkeypop .
	docker stop donkeypop
	docker rm donkeypop
	docker run -d --name donkeypop -p 8000:8000 donkeypop

start:
	docker run donkeypop

stop:
	docker stop donkeypop

format:
	pipenv run black . --exclude '/.gitignore|Pipfile|Pipfile.lock|.mypy_cache/'