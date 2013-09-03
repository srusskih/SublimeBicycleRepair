dummy:
	exit 0

clean:
	rm -rf SublimeBicycleRepair.sublime-package
	find -name "*.pyc" -exec rm {} \;

# will build a sublime package
build: clean
	zip -r SublimeBicycleRepair.sublime-package `ls` -x .git SublimeBicycleRepair.sublime-package *.pyc
