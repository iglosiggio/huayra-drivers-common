huayra-drivers-common
=====================

This package aggregates and abstracts Huayra specific logic and knowledge
about third-party driver packages, and provides APIs for installers and driver
configuration GUIs.

This package is a customized version of [ubuntu-drivers-common][upstream]
tailored for the needs of the _Conectar Igualdad_ project.

[upstream]: https://github.com/tselliot/ubuntu-drivers-common

Command line interface
----------------------
The simplest frontend is the "huayra-drivers" command line tool. You can use
it to show the available driver packages which apply to the current system
(huayra-drivers list), or to install all drivers which are appropriate for
automatic installation (sudo huayra-drivers autoinstall), which is mostly
useful for integration into installers.

Please see "huayra-drivers --help" for details.


Python API
----------
The UbuntuDrivers.detect Python module provides some functions to detect the
system's hardware, matching driver packages, and packages which are eligible
for automatic installation.

The three main functions are:

```python
# Which driver packages apply to this system?
packages = HuayraDrivers.detect.system_driver_packages()

# Which devices need drivers, and which packages do they need?
driver_info = HuayraDrivers.detect.system_device_drivers()

# Which driver package(s) applies to this piece of hardware?
import apt
apt_cache = apt.Cache()
apt_packages = HuayraDrivers.detect.packages_for_modalias(apt_cache, modalias)
```

These functions only use python-apt. They do not need any other dependencies,
root privileges, D-BUS calls, etc.


Detection logic
---------------
The principal method of mapping hardware to driver packages is to use modalias
patterns. Hardware devices export a "modalias" sysfs attribute, for example

```console
$ cat /sys/devices/pci0000:00/0000:00:1b.0/modalias
pci:v00008086d00003B56sv000017AAsd0000215Ebc04sc03i00
```

Kernel modules declare which hardware they can handle with modalias patterns
(globs), e. g.:

```console
$ modinfo snd_hda_intel
[...]
alias:          pci:v00008086d*sv*sd*bc04sc03i00*
```

Driver packages which are not installed by default (e. g. backports of drivers
from newer Linux packages, or the proprietary NVidia driver package
"nvidia-current") have a "Modaliases:" package header which includes all
modalias patterns from all kernel modules that they ship. It is recommended to
add these headers to the package with `dh_modaliases(1)`.

ubuntu-drivers-common uses these package headers to map a particular piece of
hardware (identified by a modalias) to the driver packages which cover that
hardware.


Custom detection plugins
------------------------
For some kinds of drivers the modalias detection approach does not work. For
example, the "sl-modem-daemon" driver requires some checks in
/proc/asound/cards and "aplay -l" to decide whether or not it applies to the
system. These special cases can be put into a "detection plugin", by adding a
small piece of Python code to /usr/share/ubuntu-drivers-common/detect/NAME.py
(shipped in ./detect-plugins/ in the ubuntu-drivers-common source). They need
to export a method

```python
   def detect(apt_cache):
      # do detection logic here
      return ['driver_package', ...]
```

which can do any kind of detection and then return the resulting set of
packages that apply to the current system. Please note that this cannot rely on
having root privileges.
