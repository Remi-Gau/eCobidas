# LINT
remark: package.json
	npx remark *.md docs/*.md docs/**/*.md --rc-path .remarkrc

package.json:
	npm install `cat npm-requirements.txt`

serve_app:
	cd reproschema-ui/src && npm install && npm run serve
