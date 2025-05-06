#!/bin/bash

clear
echo "-----------------------------------------------------------------------------------------------"
echo ""
echo "          @alexandrglm/easyenv - 1.0 - PYTHON SELF-COMPILER & VENV SETUP"
echo ""
echo "   This script will automatically download, compile, and set up your desired Python version"
echo "   as a virtual environment (venv)."
echo "   Perfect for those Debian users who need to set an specific & NON system-wide Python ver."
echo "   for their projects, isolated from the system, with ease."
echo ""
echo "-----------------------------------------------------------------------------------------------"


while true; do

    echo ""
    echo 'Set Python Version to install (e.g. 3.11.11, 3.2, ...): '
    read -p "(PYTHON VER?) ->   " PYTHON_VER
    
    if [[ "$PYTHON_VER" =~ ^[0-9]+(\.[0-9]+)+$ ]]; then

        break

    else

        echo ""
        echo "ERROR -> Invalid version. Use X.X or X.X.X (E.g. 3.1 / 3.2.4 / 3.11.11 )"
    fi

done
echo ""
while true; do
    
    echo "Set FOLDER NAME (not path) for Python & venv (e.g .venv ): "
    read -p "(PATH?) ->  " VENV_DIR

    if [[ "$VENV_DIR" =~ ^[a-zA-Z0-9._-]+$ ]]; then

        break

    else 

        echo ""
        echo "ERROR -> Venv folder name MUST NOT include PATH symbols ( / \ | $ ), excepting those allowed (. - _ )"
    fi   
done

echo "-----------------------------------------------------------------------------------------------"
echo ""
echo "Source directory  -> $PWD"

echo ""
echo "Python Version    ->  $PYTHON_VER"
echo "PATH for venv     ->  $VENV_DIR"
echo ""
read -p "Type YES to confirm the actions:  " YES

if [ $YES = "YES" ]; then

    echo "Proceeding ...."
    echo "-----------------------------------------------------------------------------------------------"
    PYTHON_VER=${PYTHON_VER}
    VENV_DIR=${VENV_DIR}


    mkdir -p "./$VENV_DIR"

    wget "https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz"
    tar -xvzf "./Python-$PYTHON_VER.tgz"
    rm -rf "./Python-$PYTHON_VER.tgz"
    mv "./Python-$PYTHON_VER" "./$VENV_DIR/$PYTHON_VER"

    cd "./$VENV_DIR/$PYTHON_VER"
    ./configure --prefix="$PWD/../../$VENV_DIR/$PYTHON_VER/install" --enable-optimizations
    make -j"$(nproc)"
    make install

    cd ../../
    find "./$VENV_DIR/$PYTHON_VER/" -mindepth 1 ! -path "./$VENV_DIR/$PYTHON_VER/install*" -exec rm -rf {} +

    "./$VENV_DIR/$PYTHON_VER/install/bin/python3" -m venv "./$VENV_DIR"

    echo ""
    echo "-----------------------------------------------------------------------------------------------"
    echo "Python $PYTHON_VER (non system-wide) as venv has been succesfully installed for this project!"
    echo "-> Now, you can 'source ./$VENV_DIR/bin/activate' this project's venv!"
    exit 0


else
    echo ""
    echo "-----------------------------------------------------------------------------------------------"
    echo "cancelled by the user, bye!"
    exit 1
fi
