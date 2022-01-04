
import os, stat
from setuptools import setup
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from distutils.extension import Extension

try:
    from tblink_bfms.setup import BfmExtension
    from tblink_bfms.setup import BfmBuildExtCmd
except Exception as e:
    print("Fallback: %s" % str(e))
    from distutils.extension import Extension as BfmExtension
    from setuptools.command.build_ext import build_ext as BfmBuildExtCmd

rootdir = os.path.dirname(os.path.realpath(__file__))

print("rootdir=%s" % rootdir)

class BfmExtension(Extension):
    pass

class BdistWheelCmd(bdist_wheel):
    
    def run(self):
        print("--> BdistWheelCmd")
        bdist_wheel.run(self)
        print("<-- BdistWheelCmd")

class BuildExtCmd(build_ext):
    
    def run(self):
        bfm_extensions = []
        print("BuildExtCmd: %s" % self.build_lib)
        for e in self.extensions:
            print("ext_path=%s" % self.get_ext_fullname(e.name))
        
        i=0
        while i < len(self.extensions):
            if isinstance(self.extensions[i], BfmExtension):
                bfm_extensions.append(self.extensions[i])
                self.extensions.pop(i)
            else:
                i += 1
                
        print("BfmExtensions: %s" % str(bfm_extensions))

        # Build any non-BFM extensions
        build_ext.run(self)
                
class InstallCmd(install):

    def run(self):
        print("InstallCmd")
        install.run(self)

class InstallLibCmd(install_lib):

    def run(self):
        print("InstallLibCmd")
        print("install_dir=%s" % self.install_dir)
        print("build_dir=%s" % self.build_dir)
        install_lib.run(self)


version="0.0.1"

setup(
  name = "tblink-bfms-rv",
  version = version,
  packages=['rv_bfms'],
  package_dir = {'' : 'frontends/python'},
  package_data = {'ivpm': ['scripts/*', 'templates/*']},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("IVPM (IP and Verification Package Manager) is a project-internal package manager."),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "Coverage"],
  url = "https://github.com/fvutils/ivpm",
  ext_modules=[
      BfmExtension(
            os.path.join(rootdir, "rv_bfms.yaml"),
                sources=[
                    os.path.join(rootdir, "backends"),
                    os.path.join(rootdir, "frontends"),
#                    os.path.join(rootdir, "tblink-bfms-rv.core"),
                    ])
      ],
#  entry_points={
#    'console_scripts': [
#      'ivpm = ivpm.__main__:main'
#    ]
#  },
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
      'pyyaml',
      'pyyaml-srcinfo-loader',
      'jsonschema',
      'requirements-parser'
  ],
  cmdclass={
    'install': InstallCmd,
    'install_lib': InstallLibCmd,
    'build_ext' : BfmBuildExtCmd,
    'bdist_wheel': BdistWheelCmd
  },
)

