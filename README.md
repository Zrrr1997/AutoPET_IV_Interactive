# Official Repository for the Interactive Track of autoPET IV
The interactive segmentation track for autoPET IV aims to explore click-based interactive models for PET/CT lesion interactive segmentation. Interective models will be evaluated over 11 interactive segmentation steps. In each step, an additional pre-simulated tumor (foreground) and background click, represented as a set of 3D coordinates, will be provided alongside the input image. This process will progress incrementally from 0 clicks to the full allocation of 10 tumor and 10 background clicks per image, resulting in 11 predictions from each model.

[example_clicks_heatmaps.webm](https://github.com/user-attachments/assets/241dde22-0c03-4a4a-bbfa-5446959e7be2)


## 1. SW-FastEdit Baseline
Baseline model for lesion segmentation: The SW-FastEdit model (https://github.com/Zrrr1997/SW-FastEdit) 
was used for training the baseline. FDG-PET (SUV) volumes from the autoPET II challenge, concatenated with 3D Gaussian Heatmaps of 10 foreground and 10 background clicks (total: 3 channels), were used as the model inputs.  



## 2. Inference with Python Script
If you wish to infer with a script, instead of with the provided Docker, you first need to install all dependencies:

Create conda environment. **Prerequisite: Please make sure you have an installed GPU driver supporting CUDA 12.x!**

```
conda create -n swfastedit python=3.10 -y
conda activate swfastedit
```
Install all dependencies:
```
pip install -U monailabel
pip install -r requirements.txt
```

Run script for iterative inference. The outputs will be saved in the same paths as the `docker run`.
```
python src/simplified_inference.py -a -i test/input/demo_data/ -o test/output/images/automated-petct-lesion-segmentation/-ta -e 800 --dont_check_output_dir --resume_from model/151_best_0.8534.pt --eval_only --json_dir test/input/demo_data/demo_json/Ts_clicks/ --no_log --no_data --save_pred --loop -c cache/
```
Remove the `--loop` flag if you simply want the final prediction with all 10 tumor and 10 background clicks instead of iterating over all 10 steps. The evaluation metrics will be saved in `test/input/demo_data/demo_json/val_metrics/interactive_metrics.csv` together with an `.npz` file for each `.nii.gz` containing the `DSC`, `FPV`, and `FPN` for each click iteration.

The current code infers the predictions for images in the `test/input/demo_data` path. The images in that path need to be in the following simple format:
```
demo_data/
├── imagesTs
    ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0000.nii.gz # ct
    ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0001.nii.gz # pet
    ├──psma_0179419e313f7d8c_2019-06-10_0000.nii.gz # ct 
    ├──psma_0179419e313f7d8c_2019-06-10_0001.nii.gz # pet
    ├──...
├── labelsTs
    ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538.nii.gz 
    ├──psma_0179419e313f7d8c_2019-06-10.nii.gz 
    ├──...
├── demo_json
    ├──Ts_clicks
        ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_clicks.json 
        ├──psma_0179419e313f7d8c_2019-06-10_clicks.json 
        ├──...
```
Clicks are needed for inference in the form of `.json` files. They are located in the `test/input/demo_data/demo_json/Ts_clicks/` path as:
```
demo_json/
├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_clicks.json 
├──psma_0179419e313f7d8c_2019-06-10_clicks.json 
├──...
```
where each `.json` file has the following format with 10 tumor and 10 background clicks with `(x, y, z)` coordinates (example below):
```
{"tumor": [[205, 186, 231], [157, 164, 147], [108, 193, 207], [204, 135, 190], [149, 204, 155], [264, 195, 236], [209, 220, 180], [208, 150, 145], [277, 166, 108], [136, 214, 155]], "background": [[196, 176, 19], [157, 209, 95], [179, 220, 102], [217, 188, 144], [175, 232, 297], [196, 199, 13], [182, 176, 56], [189, 223, 132], [194, 225, 242], [204, 234, 246]]}
```

## 3. Inference with Docker 
The Docker inference requires a slight change of the `.json` format in which the clicks are saved to account for the `Grand Challenge Input Interface`. We have provided the converted clicks in `assets/` but you can also convert them using the `src/sw_fastedit/utils/convert_json.py` script. 

`Grand Challenge` always infers a single input at a time. In our case this would be a PET/CT + Clicks. These should be stored in this format:
```
test/
├── input/
|    ├── images/
|    |   ├── ct/
|    |   |    ├── af3b6605-c2b9-4067-8af5-8b85aafb2ae3.mha
|    |   ├── pet/
|    |   |    ├── af3b6605-c2b9-4067-8af5-8b85aafb2ae3.mha
|    ├── lesion-clicks.json
├── output/
     ├── images/
         ├── tumor-lesion-segmentation/
              ├── DOCKER-OUTPUT-WILL-BE-HERE
```


We have prepared a single example case which you can test by simply running:
```
bash test_offline.sh
```
The final predictions will be saved in `test/output/images/tumor-lesion-segmentation`. To infer further cases, simply swap the PET/CT and clicks for another case and repeat.

The `Grand Challenge` format for the `lesion-clicks.json` file for the clicks should look like this:
```
{
    "version": {"major": 1, "minor": 0}, 
    "type": "Multiple points", 
    "points": [
        {"point": [190, 201, 198], "name": "tumor"}, 
        {"point": [178, 166, 181], "name": "tumor"}, 
        {"point": [193, 204, 196], "name": "tumor"}, 
        {"point": [184, 167, 177], "name": "tumor"}, 
        {"point": [187, 199, 201], "name": "tumor"}, 
        {"point": [182, 163, 177], "name": "tumor"}, 
        {"point": [189, 196, 199], "name": "tumor"}, 
        {"point": [187, 185, 188], "name": "tumor"}, 
        {"point": [187, 204, 196], "name": "tumor"}, 
        {"point": [175, 171, 188], "name": "tumor"}, 
        {"point": [178, 214, 0], "name": "background"}, 
        {"point": [204, 205, 246], "name": "background"}, 
        {"point": [177, 190, 184], "name": "background"}, 
        {"point": [169, 213, 147], "name": "background"}, 
        {"point": [216, 211, 55], "name": "background"}, 
        {"point": [179, 171, 217], "name": "background"}, 
        {"point": [172, 234, 123], "name": "background"}, 
        {"point": [143, 186, 121], "name": "background"}, 
        {"point": [207, 197, 61], "name": "background"}, 
        {"point": [174, 232, 130], "name": "background"}
        ]
}
```


## 4. Click Simulation
To simulate clicks on new data and replicate the exact same conditions as our provided clicks for autoPET IV, you could use the `src/sw_fastedit/utils/simulate_clicks.py` script by first installing all dependencies as in `2.2 Inference with Python Script`. 

The script requires the following arguments:
- `--input_label`: Path to the nifti label
- `--input_pet`: Path to the nifti PET (SUV) image
- `--debug_output`: (Optional) Output path for click visualization for debugging. The output will be two nifti files for foreground and background of Gaussian Heatmaps of the clicks. Used to load in a viewer, e.g. 3D Slicer, to inspect the click simulation.
- `--json_output`: Output path for JSON files containing all clicks
- `--center_offset`: Maximum offset for each dimension (XYZ) to perturb each center click during simulation
- `--edge_offset`: Maximum offset for each dimension (XYZ) to perturb each boundary click during simulation


An example script run for the demo data would be:
```
python src/sw_fastedit/utils/simulate_clicks.py \
    --input_label test/input/demo_data/labelsTs/"fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538.nii.gz" \
    --input_pet test/input/demo_data/imagesTs/"fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0001.nii.gz" \
    --debug_output test/input/demo_data/demo_json/debug_vis_AutoPET_IV/ \
    --json_output test/input/demo_data/demo_json/Ts_clicks/ \
    --center_offset 2 \
    --edge_offset 2
```
**IMPORTANT: Simulated clicks for the entire autoPET_III dataset can be found in** `assets/`. The dataset can be downloaded using the original link: https://autopet-iii.grand-challenge.org/dataset/ 

If you use the SW-FastEdit model to develop your own algorithms, please cite:
```
Hadlich, Matthias*, and Marinov, Zdravko* et al. "Sliding window fastedit: A framework for lesion annotation in whole-body pet images." 2024 IEEE International Symposium on Biomedical Imaging (ISBI). IEEE, 2024.
DOI: 10.1109/ISBI56570.2024.10635459
```
