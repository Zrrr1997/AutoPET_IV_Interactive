#!/usr/bin/bash

set -euf -o pipefail

SCRIPTPATH="$(dirname "$( cd "$(dirname "$0")" ; pwd -P)")"
SCRIPTPATHCURR="$( cd "$(dirname "$0")" ; pwd -P )"
SCRIPTPATH=$SCRIPTPATHCURR
echo $SCRIPTPATH

./build.sh

VOLUME_SUFFIX=$(dd if=/dev/urandom bs=32 count=1 | md5sum | cut --delimiter=' ' --fields=1)
MEM_LIMIT="15g"  # Maximum is currently 30g, configurable in your algorithm image settings on grand challenge

VOLUME=$SCRIPTPATH/output/ # For saving on the host filesystem (offline inference)

# For grand-challenge - volumes with unique identifiers
#VOLUME=sw_infer_output-$VOLUME_SUFFIX
#docker volume create $VOLUME 
#echo "Volume created, running evaluation"
#make sure to omit --loop when submitting to grand-challenge

echo $VOLUME 

# Do not change any of the parameters to docker run, these are fixed
docker run --rm \
        --memory="${MEM_LIMIT}" \
        --memory-swap="${MEM_LIMIT}" \
        --network="none" \
        --cap-drop="ALL" \
        --security-opt="no-new-privileges" \
        --gpus="all"  \
        --shm-size="128m" \
        --pids-limit="256" \
        -v $SCRIPTPATH/test/input/:/input/ \
        -v $VOLUME:/output/ \
        sw_infer python src/simplified_inference.py -a -i /input/demo_json/demo_data/ -o /output/ -ta -e 800 --dont_check_output_dir --resume_from model/151_best_0.8534.pt --eval_only --json_dir /input/demo_json/Ts_clicks/ --no_log --no_data --save_pred --loop

echo "Evaluation done, checking results"
