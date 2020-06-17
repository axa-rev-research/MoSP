# Covid19 Contact Tracing App Simulation
> Studies the impact of the app adoption rate on the infection prevalence based on geo-spatial data.


To fight Covid-19, contact tracing architectures based on the Bluetooth Low Energy (BLE) protocol have been much discussed lately. Leveraging the [Mobile Security & Privacy Simulator](http://bhenne.github.io/MoSP/) distributed by the Computing & Security Group at the Leibniz Universität Hannover in Germany, this project attempts to model digital contact tracing in crowded places like Paris. Among other questions, we studied the impact of installation rates on the success of contact tracing apps.

![](doc/viewer.png?raw=true)

## Installation

Disclaimer: Requires Python 2.7, not compatible with Python 3.x.

```
pip install -r requirements.txt
```

## Usage examples

Launch the simulation:

```
cd mosp_examples
python contact_tracing_wiggler.py & cd ../viewer
python sim_viewer.py
```

Plot the chart:

```
cd mosp_examples
python contact_tracing_plot.py
```

Now, run your own simulations by modifying the parameters and the map in [contact_tracing_wiggler.py](mosp_examples/contact_tracing_wiggler.py)

## Preliminary findings
![](doc/chart.png?raw=true)

A low adoption rate of 20% has no effect at all. An adoption rate of 50% helps to slow the spread of the virus. Even higher adoption rates can achieve to contain the disease.

## Contact
For questions, please feel free to reach out to boris.ruf@axa.com.

## License

This program is a fork of the [MoSP Simulator](http://bhenne.github.io/MoSP/) and it is released under the same license. It is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
