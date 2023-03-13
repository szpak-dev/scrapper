reset:
	python cli.py reset --module=${m}

reset_all:
	@make reset m=target
	@make reset m=crawler
	@make reset m=scrapper

clear:
	python cli.py clear --module=${m} --target=${t}

install:
	python cli.py install --module=${m}

install_all:
	@make install m=target
	@make install m=crawler
	@make install m=scrapper

crawl:
	python cli.py crawl --target=${t} --config=default

scrap:
	python cli.py scrap --target=${t}

download:
	python cli.py download --target=${t} --media=image
