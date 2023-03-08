mre:
	python cli.py reset --module=manufacturer

min:
	python cli.py install --module=manufacturer

cre:
	python cli.py reset --module=crawler

ccr:
	python cli.py crawl --manufacturer=marttiini --config=default
