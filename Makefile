# LINT
remark: package.json
	npx remark *.md docs/*.md --rc-path .remarkrc

package.json:
    npm install -g jsonlint
	npm install `cat npm-requirements.txt`
