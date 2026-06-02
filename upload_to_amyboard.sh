if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename_of_sketch_to_be_uploaded>"
    exit 1
fi

echo "uploading $1 to current/sketch.py on amyboard"
mpremote resume fs cp $1 :current/sketch.py
mpremote soft-reset
