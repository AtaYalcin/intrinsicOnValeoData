If you want to replicate the results (rr)

add the following three lines to the .bashrc file in the Karolina Cluster

ml Anaconda3/2023.09-0
ml CUDA/11.3.1
ml GCC/9.4.0

clone https://github.com/boschresearch/DroidCalib.git
create a conda environment droidenv using standart terminal commands stated in https://github.com/boschresearch/DroidCalib github page.
	Warning: conda keeps getting stuck at "Solving Environment". Use detailed environment under misc/environment_detailed_vis.yaml (with visualization) or misc/environment_detailed.yaml (without visualization).
	run setup.py (this will take some while)
	activate this environment with "source activate droidenv" rather than "conda activate droidenv" when needed.


Using the S3 procedure defined by the shared documents at adasoffice by valeo, download and unzip data.(since explanation of this procedure might reveal sensitive info, no further details will be provided.)
	Karolina cluster puts storage limitations, thus deleting the extracted .zip files at each extraction is important.
	"for i in *.zip; do unzip "$i" -d "${i%%.zip}"; done" is a benefitial command at extraction of each zip file in a folder into a seperate folder.
	we are not interested in the gps data, it can be deleted right away.

After you completed downloading and preparing the valeo data, you can use "ssh -i aa it4i-XXXXXXXX@karolina.it4i.cz" command(on your own machiene) to download the files to your own local and use GUI tools.

Some of the cameras were nearly distortion free i.e. pinhole and some were with significant distortion, presumably fisheye. To make no assumptions and make this a general workflow with ease of use, Droidcalibs unified camera model mei is used. 

connect to the GPU capable node by "salloc -A DD-23-122 -p qgpu --time=00:45:00" you shall provide your own PROJECT_ID with -A argument, requested gpu queue with -p argument and requested allocation time with --time argument.
	more info about salloc at "https://docs.it4i.cz/dgx2/job_execution/?h=salloc"
	more info about other queues at "https://docs.it4i.cz/general/karolina-partitions/?h=qgpu" 

in order to not waste gpu nodes resources run the following command at the folder containing all the folders containing camera sequences and nothing else.

find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd && source activate droidenv  && cd XXXXX  && python demo.py --imagedir=YYYYY/valeo/'{}' --opt_intr --camera_model=mei" \;
replace XXXXX with the path of the folder containing Droidcalib demo.py with respect to current folder(u can use absolute adressing).
Replace YYYYY with the path of the current folder with respect to the folder containing Droidcalib Demo.py (u can use absolute adressing)
  
the valeo data that was used by us contained around 1800 images. Droidcalib works best when numImages~300 thus we used a stride of 6
in our implementation the script was
find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c "cd '{}' && pwd && source activate droidenv  && cd ./../../../  && python demo.py --imagedir=./datasets/valeo/'{}'  --opt_intr --num_images=300 --camera_model=mei" \;



ERROR HANDLING:
If you face issues with the environment, specifically torch try deleting and reconfiguring the environement(fixed for me)
