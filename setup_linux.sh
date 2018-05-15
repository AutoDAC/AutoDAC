function check_virtualenv {
	python -c "import virtualenv"
	if [ $? -ne 0 ]; then
		sudo pip install virtualenv
	fi
	return $status
}

function install_non_python_dep {
	if [[ "$1" != "Darwin" && "$NO_DISPLAY" != "True" ]]; then
		sudo apt-get install -y -qq scrot python3-tk python3-dev
	fi
}

function generate_req {
	echo "$1" >> requirements.txt
}

function generate_requirements {
	if [[ "$NO_DISPLAY" != "True" ]]; then
		generate_req "pyautogui"
		generate_req "pywinauto"
		generate_req "wxPython"

		if [[ "$1" == "Darwin" ]]; then
			generate_req "pyobjc-core"
			generate_req "pyobjc"
		else
			generate_req "python3-xlib"
		fi
	fi

	generate_req "pytest"
	generate_req "pytest-mock"
	generate_req "pytest-cov"
	generate_req "numpy"
	generate_req "psutil"
	generate_req "opencv-python"
	generate_req "pyinstaller"
}


os_name=$(uname)
echo "" > requirements.txt

check_virtualenv
virtualenv -p python3 .
source bin/activate
install_non_python_dep $os_name
pip install --upgrade pip
generate_requirements $os_name
pip install -r requirements.txt

# python-bioformats must be installed after numpy
pip install python-bioformats
