<h1 align="center">Network Communities</h1>

<p align="center">
  Detects the community structure of networks with Louvain (several quality functions, negative weights supported), Infomap or stochastic block models, using igraph, louvain and graph-tool.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.290"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.290-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Detects the community structure of networks with Louvain (several quality functions, negative weights supported), Infomap or stochastic block models, using igraph, louvain and graph-tool.**

Reads a network in JSON graph format and assigns each node a community label using the chosen method; Louvain variants (modularity, RB configuration, RBER, CPM, significance, surprise) handle negative weights, optionally weighting positive and negative parts asymmetrically (Rubinov and Sporns). Use it before Network Measurements to get modularity, participation coefficient and module degree z-score. Only Louvain supports negative weights; preprocess signed networks for other methods.

| | |
|---|---|
| **Inputs** | `generic/network` |
| **Outputs** | `generic/network` |
| **Container** | `filsilva/cxnetwork:0.2.0` |
| **Resources** | 1 CPUs · 6 GB memory · 1 h walltime |
| **Run it** | [doi.org/10.25663/brainlife.app.290](https://doi.org/10.25663/brainlife.app.290) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `network` | `generic/network` | yes | Input network. Note that not all the methods support negative weights, please use the Network Preprocessor app before running this App if the network has negative weights. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `generic/network` | A network containing the detected community structure. |

<details>
<summary><b>Parameters</b> (5)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `method` | enum | `louvain` | Community detection method - Louvain community detection algorithm, you can choose a variation by setting louvain-quality-function. Louvain quality functions works for negative weights. - Infomap community detection algorithm. - Stochastic block Model can handle layered networks, weighted, directed as well as negative weights. Options: `louvain`, `infomap`, `sbm`. |
| `infomap-trials` | number | `10` | Number of trials for the Infomap community detection algorithm. (ignored if used for other methods) |
| `louvain-quality-function` | enum | `modularity` | Partition quality function to be optimized for the Louvain method: - Modularity: Uses modularity optimization. Accepts weighted networks. - RBConfiguration: Reichardt and Bornholdt’s Potts model with a configuration null model. Accepts weighted networks. - RBER - Implements Reichardt and Bornholdt’s Potts model with an Erdős-Rényi null model. Accepts weighted networks. - Clique Percolation Method (CPM) method. Accepts weighted networks. - Significance: based on KL divergence comparing ER. Not suitable for weighted networks. - Surprise: based on KL divergence. Works with weighted networks. Options: `modularity`, `rbconfiguration`, `rber`, `cpm`, `significance`, `surprise`. |
| `louvain-resolution` | number | `1` | Defines the resolution parameter gamma for the quality functions. |
| `assymetric-negative` | boolean | `true` | If the network contains negative weights, the positive and negative partitions are weighted differently, according to Rubinov, Mikail, and Olaf Sporns. "Weight-conserving characterization of complex functional brain networks." Neuroimage 56, no. 4 (2011): 2068-2079. This seems to be appropriate when analyzing brain networks. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.290](https://doi.org/10.25663/brainlife.app.290), choose `generic/network` from your project, set the parameters and press **Execute**. The results are saved to your project as `generic/network`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `filsilva/cxnetwork:0.2.0`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "network": "/path/to/network/network",
       "method": "louvain",
       "infomap-trials": 10,
       "louvain-quality-function": "modularity",
       "louvain-resolution": 1,
       "assymetric-negative": true
   }
   ```

3. Run `./main`.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Network Communities. brainlife.io App. [doi:10.25663/brainlife.app.290](https://doi.org/10.25663/brainlife.app.290)
- Blondel VD, Guillaume JL, Lambiotte R, Lefebvre E. Fast unfolding of communities in large networks. J Stat Mech P10008 (2008). [doi:10.1088/1742-5468/2008/10/P10008](https://doi.org/10.1088/1742-5468/2008/10/P10008)
- Rosvall M, Bergstrom CT. Maps of random walks on complex networks reveal community structure. PNAS 105(4):1118-1123 (2008). [doi:10.1073/pnas.0706851105](https://doi.org/10.1073/pnas.0706851105)
- Rubinov M, Sporns O. Weight-conserving characterization of complex functional brain networks. NeuroImage 56(4):2068-2079 (2011). [doi:10.1016/j.neuroimage.2011.03.069](https://doi.org/10.1016/j.neuroimage.2011.03.069)
- Peixoto TP. Efficient Monte Carlo and greedy heuristic for the inference of stochastic block models. Phys Rev E 89, 012804 (2014). [doi:10.1103/PhysRevE.89.012804](https://doi.org/10.1103/PhysRevE.89.012804)
- Peixoto TP. Inferring the mesoscale structure of layered, edge-valued and time-varying networks. Phys Rev E 92, 042807 (2015). [doi:10.1103/PhysRevE.92.042807](https://doi.org/10.1103/PhysRevE.92.042807)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- [Filipi N. Silva](https://filipinascimento.github.io)

**Contributors**

- [Franco Pestilli](https://liberalarts.utexas.edu/psychology/faculty/fp4834)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
