.PHONY: release
VERSION := $(shell python3 setup.py --version)

release:
	@ git commit --allow-empty -m "Release $(VERSION)"
	@ git tag -a $(VERSION) -m "Version $(VERSION)"
	@ git push origin --tags


clean: ## Remove files not in source control
	@ find . -type f -name "*.pyc" -delete
	@ rm -rf dist/*

publish: clean
	@ python3 setup.py sdist bdist_wheel
	@ twine upload dist/*