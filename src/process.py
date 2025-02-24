import SimpleITK
import time
import os

import torch
from simplified_inference import simplified_predict


class Autopet_baseline():  # SegmentationAlgorithm is not inherited in this class anymore

    def __init__(self):
        """
        Write your own input validators here
        Initialize your model etc.
        """
        # set some paths and parameters
        self.input_path = './assets/input/'  # according to the specified grand-challenge interfaces
        self.output_path = './assets/output/'  # according to the specified grand-challenge interfaces
        self.nii_path = './assets/nii_path/'
        self.result_path = './assets/nii_out_path/'
        self.nii_seg_file = 'TCIA_001_0000.nii.gz'
        self.json_path = './assets/json_path/'

        pass

    def convert_mha_to_nii(self, mha_input_path, nii_out_path):  #nnUNet specific
        img = SimpleITK.ReadImage(mha_input_path)
        SimpleITK.WriteImage(img, nii_out_path, True)

    def convert_nii_to_mha(self, nii_input_path, mha_out_path):  #nnUNet specific
        img = SimpleITK.ReadImage(nii_input_path)
        SimpleITK.WriteImage(img, mha_out_path, True)

    def check_gpu(self):
        """
        Check if GPU is available
        """
        print('Checking GPU availability')
        is_available = torch.cuda.is_available()
        print('Available: ' + str(is_available))
        print(f'Device count: {torch.cuda.device_count()}')
        if is_available:
            print(f'Current device: {torch.cuda.current_device()}')
            print('Device name: ' + torch.cuda.get_device_name(0))
            print('Device memory: ' + str(torch.cuda.get_device_properties(0).total_memory))

    def load_inputs(self):
        """
        Read from /input/
        Check https://grand-challenge.org/algorithms/interfaces/
        """
        ct_mha = os.listdir(os.path.join(self.input_path, 'images/ct/'))[0]
        pet_mha = os.listdir(os.path.join(self.input_path, 'images/pet/'))[0]
        uuid = os.path.splitext(ct_mha)[0]

        self.convert_mha_to_nii(os.path.join(self.input_path, 'images/pet/', pet_mha),
                                os.path.join(self.nii_path, 'TCIA_001_0000.nii.gz'))
        self.convert_mha_to_nii(os.path.join(self.input_path, 'images/ct/', ct_mha),
                                os.path.join(self.nii_path, 'TCIA_001_0001.nii.gz'))
        return uuid

    def write_outputs(self, uuid):
        """
        Write to /output/
        Check https://grand-challenge.org/algorithms/interfaces/
        """
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.convert_nii_to_mha(os.path.join(self.result_path, 'predictions', self.nii_seg_file), os.path.join(self.output_path, uuid + ".mha"))
        print('Output written to: ' + os.path.join(self.output_path, uuid + ".mha"))

    def predict(self):
        """
        Your algorithm goes here
        """
        print("segmentation starting!")
        input_folder = self.nii_path
        output_folder = self.result_path
        json_folder = self.json_path
        docker = True
        simplified_predict(input_folder, output_folder, json_folder, docker)
        

        print("segmentation done!")
        if not os.path.exists(os.path.join(self.result_path, 'predictions', self.nii_seg_file)):
            print('waiting for nnUNet segmentation to be created')
        while not os.path.exists(os.path.join(self.result_path, 'predictions', self.nii_seg_file)):
            print('.', end='')
            time.sleep(5)
        #print(cproc)  # since nnUNet_predict call is split into prediction and postprocess, a pre-mature exit code is received but segmentation file not yet written. This hack ensures that all spawned subprocesses are finished before being printed.
        print('Prediction finished')

    def process(self):
        """
        Read inputs from /input, process with your algorithm and write to /output
        """
        # process function will be called once for each test sample
        self.check_gpu()
        print('Start processing')
        uuid = self.load_inputs()
        print('Start prediction')
        self.predict()
        print('Start output writing')
        self.write_outputs(uuid)


if __name__ == "__main__":
    print("START")
    Autopet_baseline().process()
