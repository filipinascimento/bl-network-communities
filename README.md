[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.1-blue.svg)](https://doi.org/10.25663/brainlife.app.290)

# Network Communities
Obtain the community structure for networks using the Louvain or Infomap methods. Negative weights are supported only for Louvain.

### Authors
- [Filipi N. Silva](filsilva@iu.edu)

<!-- ### Contributors
- Franco Pestilli (franpest@indiana.edu) -->

### Funding
[![NIH-1R01EB029272-01](https://img.shields.io/badge/NIH-1R01EB029272_01-blue.svg)](https://www.nibib.nih.gov/node/113361)


### Citations

1. Blondel, Vincent D., Jean-Loup Guillaume, Renaud Lambiotte, and Etienne Lefebvre. "Fast unfolding of communities in large networks." Journal of statistical mechanics: theory and experiment 2008, no. 10 (2008): P10008. [https://doi.org/10.1088/1742-5468/2008/10/P10008](https://doi.org/10.1088/1742-5468/2008/10/P10008)

2. Rosvall, Martin, and Carl T. Bergstrom. "Maps of random walks on complex networks reveal community structure." Proceedings of the National Academy of Sciences 105, no. 4 (2008): 1118-1123.[https://dx.doi.org/10.1073/pnas.0706851105](https://dx.doi.org/10.1073/pnas.0706851105)

3. Rubinov, Mikail, and Olaf Sporns. "Weight-conserving characterization of complex functional brain networks." Neuroimage 56, no. 4 (2011): 2068-2079. [https://doi.org/10.1016/j.neuroimage.2011.03.069](https://doi.org/10.1016/j.neuroimage.2011.03.069)


## Running the App 

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/brainlife.app.290](https://doi.org/10.25663/brainlife.app.290) via the "Execute" tab.

### Running Locally (on your machine)
Singularity is required to run the package locally.

1. git clone this repo.

```bash
git clone <repository URL>
cd <repository PATH>
```

2. Inside the cloned directory, edit `config-sample.json` with your data or use the provided data.

3. Rename `config-sample.json` to `config.json` .

```bash
mv config-sample.json config.json
```

4. Launch the App by executing `main`

```bash
./main
```

### Sample Datasets

A sample dataset is provided in folder `data` and `config-sample.json`

## Output

The output is a conmat with an extra property contained the communities for each network. The new files end with `_communities.txt` and are placed in the `csv` directory.


<!-- #### Product.json

The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing.  -->

### Dependencies

This App only requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install the python packages defined in `environment.yml`, then you can run the code directly from python using:  

```bash
./main.py config.json
```

