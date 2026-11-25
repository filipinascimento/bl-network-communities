[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.1-blue.svg)](https://doi.org/10.25663/brainlife.app.290)

# Network Communities

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Detects the community structure of networks with Louvain (several quality functions, negative weights supported), Infomap or stochastic block models, using igraph, louvain and graph-tool.**

Reads a network in JSON graph format and assigns each node a community label using the chosen method; Louvain variants (modularity, RB configuration, RBER, CPM, significance, surprise) handle negative weights, optionally weighting positive and negative parts asymmetrically (Rubinov and Sporns). Use it before Network Measurements to get modularity, participation coefficient and module degree z-score. Only Louvain supports negative weights; preprocess signed networks for other methods.

| | |
|---|---|
| 📥 **Inputs** | `generic/network` |
| 📤 **Outputs** | `generic/network` |
| 🐳 **Container** | `filsilva/cxnetwork:0.2.0` |
| ⚙️ **Resources** | 1 CPUs · 6 GB memory · 1 h walltime |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.290](https://doi.org/10.25663/brainlife.app.290) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `network` | `generic/network` | yes | Input network. Note that not all the methods support negative weights, please use the Network Preprocessor app before running this App if the network has negative weights. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `generic/network` | A network containing the detected community structure. |

<details>
<summary><b>⚙️ Parameters</b> (5)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `method` | enum | `louvain` | Community detection method - Louvain community detection algorithm, you can choose a variation by setting louvain-quality-function. Louvain quality functions works for negative weights. - Infomap community detection algorithm. - Stochastic block Model can handle layered networks, weighted, directed as well as negative weights. Options: `louvain`, `infomap`, `sbm`. |
| `infomap-trials` | number | `10` | Number of trials for the Infomap community detection algorithm. (ignored if used for other methods) |
| `louvain-quality-function` | enum | `modularity` | Partition quality function to be optimized for the Louvain method: - Modularity: Uses modularity optimization. Accepts weighted networks. - RBConfiguration: Reichardt and Bornholdt’s Potts model with a configuration null model. Accepts weighted networks. - RBER - Implements Reichardt and Bornholdt’s Potts model with an Erdős-Rényi null model. Accepts weighted networks. - Clique Percolation Method (CPM) method. Accepts weighted networks. - Significance: based on KL divergence comparing ER. Not suitable for weighted networks. - Surprise: based on KL divergence. Works with weighted networks. Options: `modularity`, `rbconfiguration`, `rber`, `cpm`, `significance`, `surprise`. |
| `louvain-resolution` | number | `1` | Defines the resolution parameter gamma for the quality functions. |
| `assymetric-negative` | boolean | `true` | If the network contains negative weights, the positive and negative partitions are weighted differently, according to Rubinov, Mikail, and Olaf Sporns. "Weight-conserving characterization of complex functional brain networks." Neuroimage 56, no. 4 (2011): 2068-2079. This seems to be appropriate when analyzing brain networks. |

</details>

📚 **References used by this App:**
- Blondel VD, Guillaume JL, Lambiotte R, Lefebvre E. Fast unfolding of communities in large networks. J Stat Mech P10008 (2008). [doi:10.1088/1742-5468/2008/10/P10008](https://doi.org/10.1088/1742-5468/2008/10/P10008)
- Rosvall M, Bergstrom CT. Maps of random walks on complex networks reveal community structure. PNAS 105(4):1118-1123 (2008). [doi:10.1073/pnas.0706851105](https://doi.org/10.1073/pnas.0706851105)
- Rubinov M, Sporns O. Weight-conserving characterization of complex functional brain networks. NeuroImage 56(4):2068-2079 (2011). [doi:10.1016/j.neuroimage.2011.03.069](https://doi.org/10.1016/j.neuroimage.2011.03.069)
- Peixoto TP. Efficient Monte Carlo and greedy heuristic for the inference of stochastic block models. Phys Rev E 89, 012804 (2014). [doi:10.1103/PhysRevE.89.012804](https://doi.org/10.1103/PhysRevE.89.012804)
- Peixoto TP. Inferring the mesoscale structure of layered, edge-valued and time-varying networks. Phys Rev E 92, 042807 (2015). [doi:10.1103/PhysRevE.92.042807](https://doi.org/10.1103/PhysRevE.92.042807)

<!-- brainlife-app:end -->

Obtain the community structure for networks using the Louvain or Infomap methods. Negative weights are supported only for Louvain.

### Authors
- [Filipi N. Silva](https://filipinascimento.github.io)

### Contributors
- [Franco Pestilli](https://liberalarts.utexas.edu/psychology/faculty/fp4834)


### Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)


### Citations
1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

2. Blondel, Vincent D., Jean-Loup Guillaume, Renaud Lambiotte, and Etienne Lefebvre. "Fast unfolding of communities in large networks." Journal of statistical mechanics: theory and experiment 2008, no. 10 (2008): P10008. [https://doi.org/10.1088/1742-5468/2008/10/P10008](https://doi.org/10.1088/1742-5468/2008/10/P10008)

3. Rosvall, Martin, and Carl T. Bergstrom. "Maps of random walks on complex networks reveal community structure." Proceedings of the National Academy of Sciences 105, no. 4 (2008): 1118-1123.[https://dx.doi.org/10.1073/pnas.0706851105](https://dx.doi.org/10.1073/pnas.0706851105)

4. Rubinov, Mikail, and Olaf Sporns. "Weight-conserving characterization of complex functional brain networks." Neuroimage 56, no. 4 (2011): 2068-2079. [https://doi.org/10.1016/j.neuroimage.2011.03.069](https://doi.org/10.1016/j.neuroimage.2011.03.069)

5. Tiago P. Peixoto. “Efficient Monte Carlo and greedy heuristic for the inference of stochastic block models”, Phys. Rev. E 89, 012804 (2014). [https://doi.org/10.1103/PhysRevE.89.012804](https://doi.org/10.1103/PhysRevE.89.012804)

6. Tiago P. Peixoto. “Inferring the mesoscale structure of layered, edge-valued and time-varying networks”, Phys. Rev. E 92, 042807 (2015). [https://doi.org/10.1103/PhysRevE.92.042807](https://doi.org/10.1103/PhysRevE.92.042807)

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

A sample dataset is provided in folder `data` and `config-sample.json`. Extra examples are provided for other scenarios: `config-sample_negative.json`, `config-sample_layered.json` and `config-sample_nullmodel.json`.

## Output

The output is a `network` data with integrated community labels.



### Dependencies

This App only requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install the python packages defined in `environment.yml`, then you can run the code directly from python using:  

```bash
./main.py config.json
```

