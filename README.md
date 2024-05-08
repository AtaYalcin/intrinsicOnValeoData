If you want to replicate the results (rr)

add the following three lines to the .bashrc file in the Karolina Cluster

ml Anaconda3/2024.02-1
ml CUDA/12.4.0
ml GCC/9.4.0

NOTE : these resources are updated frequently so check for the latest version from the it4i documentation.


clone https://github.com/boschresearch/DroidCalib.git
create a conda environment droidenv using standard terminal commands stated in https://github.com/boschresearch/DroidCalib github page.
	Warning: conda keeps getting stuck at "Solving Environment". Use detailed environment under misc/environment_detailed_vis.yaml (with visualization) or misc/environment_detailed.yaml (without visualization).
	run setup.py (this will take some while)
	activate this environment with "source activate droidenv" rather than "conda activate droidenv" when needed.

we used "Veh01_20230208_105703_076"
Using the S3 procedure defined by the shared documents at adasoffice by valeo, download and unzip data.(since explanation of this procedure might reveal sensitive info, no further details will be provided.)
	Karolina cluster puts storage limitations, thus deleting the extracted .zip files at each extraction is important.
	"for i in *.zip; do unzip "$i" -d "${i%%.zip}"; done" is a benefitial command at extraction of each zip file in a folder into a seperate folder.
	we are not interested in the gps data, it can be deleted right away.

After you completed downloading and preparing the valeo data, you can use "ssh -i aa it4i-XXXXXXXX@karolina.it4i.cz" command(on your own machiene) to download the files to your own local and use GUI tools.

Some of the cameras were nearly distortion free i.e. pinhole and some were with significant distortion, presumably fisheye. To make no assumptions and make this a general workflow with ease of use, Droidcalibs unified camera model mei is used. 

connect to the GPU capable node by "salloc -A DD-23-122 -p qgpu --time=00:45:00" you shall provide your own PROJECT_ID with -A argument, requested gpu queue with -p argument and requested allocation time with --time argument.
	more info about salloc at "https://docs.it4i.cz/dgx2/job_execution/?h=salloc"
	more info about other queues at "https://docs.it4i.cz/general/karolina-partitions/?h=qgpu" 

in order to not waste gpu nodes resources run the following command at the folder containing all the folders containing camera sequences and no other folders.

find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd && source activate droidenv  && cd XXXXX  && python demo.py --imagedir=YYYYY/valeo/'{}' --opt_intr --camera_model=mei --num_images ZZZZZ" \;
replace XXXXX with the path of the folder containing Droidcalib demo.py with respect to current folder(u can use absolute adressing).
Replace YYYYY with the path of the current folder with respect to the folder containing Droidcalib Demo.py (u can use absolute adressing)
Replace ZZZZZ with the number of images that should attend the computation. If image size is < 300 you dont need to şmpose such a limitation. 

the valeo data that was used by us contained around 1800 images. Droidcalib works best when numImages~300.
in our implementation the script was
find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd && source activate droidenv  && cd ./../../../  && python demo.py --imagedir=./datasets/valeo/'{}'  --opt_intr --camera_model=mei --num_images 300" \;

the output can be seen at DroidCalibResults.txt.
the non-eronous result of this test are as follows:
Veh01_20230208_105703_076_CAM_NFV_FW_CE_NO_ENC.npz : fx = 3139.66, fy = 3082.48, ppx = 1361.14, ppy = 1118.40, xi = -0.512
Veh01_20230208_105703_076_CAM_WFV_FW_CE_NO_ENC.npz : fx = 2589.18, fy = 2282.24, ppx = 1532.35, ppy = 1097.41, xi = 0.851

then we run the test again with pinhole assumption i.e.
find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd && source activate droidenv  && cd ./../../../  && python demo.py --imagedir=./datasets/valeo/'{}'  --opt_intr --num_images 300" \;

the output can be seen at DroidCalibResults2.txt.
the non-eronous result of this test are as follows:
Veh01_20230208_105703_076_CAM_NFV_FW_CE_NO_ENC.npz : fx = 4340.35, fy = 3441.87, ppx = 1388.51, ppy = 714.99
Veh01_20230208_105703_076_CAM_SUR_FR_CE_NO_ENC.npz : fx = 1658.95, fy = 1562.62, ppx = 974.20, ppy = 624.25
Veh01_20230208_105703_076_CAM_SUR_RE_CE_SO_ENC.npz : fx = 1583.47, fy = 1579.48, ppx = 973.90, ppy = 649.06
Veh01_20230208_105703_076_CAM_SUR_WM_LE_WE_ENC.npz : fx = 1593.66, fy = 1558.85, ppx = 1036.86, ppy = 808.10
Veh01_20230208_105703_076_CAM_SUR_WM_RI_EA_ENC.npz : fx = 1632.69, fy = 1561.78, ppx = 965.68, ppy = 686.04
Veh01_20230208_105703_076_CAM_WFV_FW_CE_NO_ENC.npz : fx = 2533.10, fy = 2304.01, ppx = 1491.16, ppy = 1027.23
Veh01_20230208_105703_076_CAM_WFV_RW_CE_SO_ENC.npz : fx = 4629.37, fy = 900.80, ppx = 902.36, ppy = 1860.87

testing stage:
we eleminate some of the tests by inspecting image data.

we will test:
Veh01_20230208_105703_076_CAM_NFV_FW_CE_NO_ENC.npz : fx = 4340.35, fy = 3441.87, ppx = 1388.51, ppy = 714.99
as pinhole camera model

further evaluate on:
Veh01_20230208_105703_076_CAM_SUR_FR_CE_NO_ENC.npz : fx = 1658.95, fy = 1562.62, ppx = 974.20, ppy = 624.25
Veh01_20230208_105703_076_CAM_SUR_RE_CE_SO_ENC.npz : fx = 1583.47, fy = 1579.48, ppx = 973.90, ppy = 649.06
Veh01_20230208_105703_076_CAM_WFV_FW_CE_NO_ENC.npz : fx = 2533.10, fy = 2304.01, ppx = 1491.16, ppy = 1027.23
Veh01_20230208_105703_076_CAM_WFV_RW_CE_SO_ENC.npz : fx = 4629.37, fy = 900.80, ppx = 902.36, ppy = 1860.87
whether as pinhole 


definately not pinhole
Veh01_20230208_105703_076_CAM_SUR_WM_LE_WE_ENC.npz : fx = 1593.66, fy = 1558.85, ppx = 1036.86, ppy = 808.10
Veh01_20230208_105703_076_CAM_SUR_WM_RI_EA_ENC.npz : fx = 1632.69, fy = 1561.78, ppx = 965.68, ppy = 686.04
.

we will test 
Veh01_20230208_105703_076_CAM_WFV_FW_CE_NO_ENC.npz : fx = 2589.18, fy = 2282.24, ppx = 1532.35, ppy = 1097.41, xi = 0.851
as unified camera model

ERROR HANDLING:
If you face issues with the environment, specifically torch try deleting and reconfiguring the environement.
