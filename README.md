# Official Repository for the Interactive Track of autoPET IV
The interactive segmentation track for autoPET IV aims to explore click-based interactive models for PET/CT lesion interactive segmentation. Interective models will be evaluated over 11 interactive segmentation steps. In each step, an additional pre-simulated tumor (foreground) and background click, represented as a set of 3D coordinates, will be provided alongside the input image. This process will progress incrementally from 0 clicks to the full allocation of 10 tumor and 10 background clicks per image, resulting in 11 predictions from each model.

<video controls>
  <source src="assets/example_clicks_heatmaps.webm" type="video/webm">
  Your browser does not support the video tag.
</video>



## 1. SW-FastEdit Baseline
Baseline model for lesion segmentation: The SW-FastEdit model (https://github.com/Zrrr1997/SW-FastEdit) 
was used for training the baseline. FDG-PET (SUV) volumes from the autoPET II challenge, concatenated with 3D Gaussian Heatmaps of 10 foreground and 10 background clicks (total: 3 channels), were used as the model inputs.  



## 2. Inference
The current code infers the predictions for 1 example image in the `test/input/demo_data` path. The images in that path need to be in the following simple format:
```
demo_data/
├── imagesTs
    ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0000.nii.gz # ct
    ├──fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0001.nii.gz # pet
    ├──psma_0179419e313f7d8c_2019-06-10_0000.nii.gz # ct 
    ├──psma_0179419e313f7d8c_2019-06-10_0001.nii.gz # pet
    ├──...
├── labelsTs
    ├──fdg_ff39795341_09-22-2005-NA-PET-CT Ganzkoerper  primaer mit KM-98939.nii.gz 
    ├──psma_0179419e313f7d8c_2019-06-10.nii.gz 
    ├──...
```
Clicks are needed for inference in the form of `.json` files. They are located in the `test/input/demo_data/demo_json/Ts_clicks/` path as:
```
demo_json/
├──fdg_ff39795341_09-22-2005-NA-PET-CT Ganzkoerper  primaer mit KM-98939_clicks.json 
├──psma_0179419e313f7d8c_2019-06-10_clicks.json 
├──...
```
where each `.json` file has the following format with 10 tumor and 10 background clicks with `(x, y, z)` coordinates (example below):
```
{"tumor": [[205, 186, 231], [157, 164, 147], [108, 193, 207], [204, 135, 190], [149, 204, 155], [264, 195, 236], [209, 220, 180], [208, 150, 145], [277, 166, 108], [136, 214, 155]], "background": [[196, 176, 19], [157, 209, 95], [179, 220, 102], [217, 188, 144], [175, 232, 297], [196, 199, 13], [182, 176, 56], [189, 223, 132], [194, 225, 242], [204, 234, 246]]}
```

### 2.1 Inference with Docker 
Once you have saved all images + labels in the format described above, simply run:
```
bash test_offline.sh
```
The final predictions will be saved in `test/output/images/automated-petct-lesion-segmentation` 

### 2.2 Inference with Python Script
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

Run script for iterative inference. The outputs will be saved in the same paths as the Docker run.
```
python src/simplified_inference.py -a -i test/input/demo_data/ -o test/output/images/automated-petct-lesion-segmentation/-ta -e 800 --dont_check_output_dir --resume_from model/151_best_0.8534.pt --eval_only --json_dir test/input/demo_data/demo_json/Ts_clicks/ --no_log --no_data --save_pred --loop -c cache/
```
Remove the `--loop` flag if you simply want the final prediction with all 10 tumor and 10 background clicks instead of iterating over all 10 steps. The evaluation metrics will be saved in `test/input/demo_data/demo_json/val_metrics/interactive_metrics.csv` together with an `.npz` file for each `.nii.gz` containing the `DSC`, `FPV`, and `FPN` for each click iteration.

## 3. Click Simulation
To simulate clicks on new data and replicate the exact same conditions as our provided clicks for autoPET IV, you could use the `src/sw_fastedit/utils/simulate_clicks.py` script by first installing all dependencies as in `2.2 Inference with Python Script`. 

The script requires the following arguments:
- `--input_label`: Path to the nifti label
- `--input_pet`: Path to the nifti PET (SUV) image
- `--debug_output`: (Optional) Output path for click visualization for debugging. The output will be two nifti files for foreground and background of Gaussian Heatmaps of the clicks. Used to load in a viewer, e.g. 3D Slicer, to inspect the click simulation.
- `--json_output`: Output path for JSON files containing all clicks

An example script run for the demo data would be:
```
python src/sw_fastedit/utils/simulate_clicks.py \
    --input_label test/input/demo_data/labelsTs/"fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538.nii.gz" \
    --input_pet test/input/demo_data/imagesTs/"fdg_04606080a0_02-20-2003-NA-PET-CT Ganzkoerper  primaer mit KM-22538_0001.nii.gz" \
    --debug_output test/input/demo_data/demo_json/debug_vis_AutoPET_IV/ \
    --json_output test/input/demo_data/demo_json/Ts_clicks/
```
**IMPORTANT: Simulated clicks for the entire autoPET_III dataset can be found in** `assets/`. The dataset can be downloaded using the original link: https://autopet-iii.grand-challenge.org/dataset/ 

If you use the SW-FastEdit model to develop your own algorithms, please cite:
```
Hadlich, Matthias*, and Marinov, Zdravko* et al. "Sliding window fastedit: A framework for lesion annotation in whole-body pet images." 2024 IEEE International Symposium on Biomedical Imaging (ISBI). IEEE, 2024.
DOI: 10.1109/ISBI56570.2024.10635459
```
