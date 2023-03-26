# LUC
LUC is a congestion control algorithm based on swap-regret-minimizing techniques. In our experiments, we implement LUC through Linux kernel 5.4.0 based on the congestion control plane ([CCP](https://ccp-project.github.io/)). With CCP, developers can write congestion control algorithms with Rust or Python in a safe user-space environment as opposed to writing C and a risk of crashing your kernel, and CCP allows the same algorithm implementation to be run through the Linux kernel.

## Experiment: Emulation on Mininet
The experiments are based on two tools, i.e., [CCP](https://ccp-project.github.io/) and [Mininet](http://mininet.org/). CCP is used to implement LUC and Mininet is the emulation tool to run experiments.
Furthermore, we recommend running the experiments on Linux kernel 5.4.0, as the recommended Linux kernel version of [CCP Kernel Datapath](https://github.com/ccp-project/ccp-kernel) is 5.4.0. 

In the paper, we run mininet experiments to compare LUC with CUBIC and [BBR2](https://github.com/google/bbr/blob/v2alpha/README.md). CUBIC is the default congestion control algorithm in Linux Kernel 5.4.0, but BBR2 needs to be compiled and installed.

In the follows, we give the step-by-step guidance on how to run the experiments.

### Step 1:  Install BBR2
There are two ways to install BBR2:
1. Manullay build and install by following the instructions on https://github.com/google/bbr/blob/v2alpha/README.md.

First, we need to install the tools for compilation:

```
apt install -y build-essential libncurses5-dev git
apt -y build-dep linux
```

Then, download bbr2 and compile it by
```
git clone -o google-bbr -b v2alpha  https://github.com/google/bbr.git
cd bbr
make menuconfig
```
Networking support ---> Networking options ---> TCP: advanced congestion control ---> BBR2 TCP (M)

```
make deb-pkg
```


2. Install the compiled kernel that already installed BBRv2 (we provide a binary package for Debian/Ubuntu under the build directory of this repo). 



If you choose the second way, you can run the following commands to replace the kernel (we tested the kernels work for ubuntu 18.04 LTS):

```
sudo dpkg -i linux-headers-5.4.0-rc6_5.4.0-rc6-2_amd64.deb
sudo dpkg -i linux-image-5.4.0-rc6_5.4.0-rc6-2_amd64.deb
```

Next, we enable the grub menu for selecting kernels. Edit the file /etc/default/grub, and find the following two lines:
```
GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=0
```
Change the two lines to
```
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=30
```
Save the changes and update grub by
```
sudo update-grub
```

Then restart the system. When comes to the grub menu, select the Advanced options for Ubuntu and then select the corresponding kernel to boot the system.

Then, enable BBR by the following commands:
```
echo "net.core.default_qdisc = fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control = bbr2" >> /etc/sysctl.conf
sysctl -p
```


### Step 2: Install CCP
The instructions for installing CCP can be found on their website (https://ccp-project.github.io/ccp-guide/setup/index.html). However, when implementing LUC, we found that some APIs are updated but the instructions on website are not updated at the same time. Therefore, we provide an instudction to install CCP as follows:

1. Install Rust
`curl https://sh.rustup.rs -sSf | sh -s -- -y -v --default-toolchain nightly`
2. Compile and run linux kernel module for CCP
```
git clone https://github.com/ccp-project/ccp-kernel.git
cd ccp-kernel
git submodule update --init --recursive
make
sudo ./ccp_kernel_load ipc=0
```
where ipc=0 is to use netlink sockets. To check whether ccp has been enabled, we can check by the following command:

```
sysctl net.ipv4.tcp_available_congestion_control
```
If you see net.ipv4.tcp_available_congestion_control = reno cubic bbr2 ccp, we have finished the envinronment setup. 

The ccp-kernel module will report statistics to the user-space ccp algorithms. The user-space ccp algorithm determines a congestion window/rate and pass it to the ccp kernel.

3. To run python-based CCP algorithms and plot results, we need to install pyportus, cython, numpy, matplotlib, and pandas
```
sudo apt install python3-pip
sudo pip3 install pyportus numpy cython matplotlib pandas
```

if it shows an error message "python setup.py egg_info failed", run the following commands first:
```
sudo pip3 install setuptools-rust
sudo pip3 install --upgrade pip
```

4. Then, we can run the LUC algoirhtm by first compiling MAB

```
python3 setup.py build_ext --inplace
```
```
python3 luc.py

```
Now, ccp-kernel will report statistics to LUC. LUC will make decisions on the congestion window/rate and pass it back to ccp-kernel.


### Step 3: Install Mininet
We need to install from source. First, get the source code by
```
git clone https://github.com/mininet/mininet
```
Then, install by using the script
```
cd mininet
sudo python3 PYTHON=python3 util/install.sh -a
```




### Step 4: Run the experiments
1. The dumbell topology
Run the script dumbell.py by
```
sudo python3 dumbell.py
```
The results will be saved in the directory of logs. To plot the logs, run the script plot_dumbell.py by
```
python3 plot_dumbell.py
```


2. The parkinglot topology
Run the script parkinglot.py by
```
sudo python3 parkinglot.py
```
The results will be saved in the directory of logs. To plot the logs, run the script plot_dumbell.py by
```
python3 plot_parkinglot.py
```

The figures will be saved as eps in results.



## Experiments with Pantheon
We also use [Patheon](https://pantheon.stanford.edu/) to verify the performance of LUC with real-world traces. The real-world traces used in our paper can be found in https://github.com/ravinet/mahimahi/tree/master/traces. 

The setup and usage of Patheon can be found in https://github.com/StanfordSNR/pantheon.