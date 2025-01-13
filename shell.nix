{ pkgs ? import <nixpkgs> {} }:
with pkgs;let
  my-python-packages = ps: with ps; [
    pytorch
    matplotlib
    numpy
    (buildPythonPackage rec {
      pname = "endplay";
      version = "0.5.11";
      src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-2aCQD1Kz7olpbUODZNBvZxtBg8YIK3VjNXisuY9za+Y=";
      };
      # doCheck = false;
      nativeBuildInputs = [
        pkgs.cmake
        pkgs.python3Packages.setuptools
        pkgs.python3Packages.wheel
        pkgs.python3Packages.pip
      ];
      buildInputs = [];
      propagatedBuildInputs = [];
      dontUseCmakeConfigure = true;
      cmakeFlags = [
        (lib.cmakeBool "MI_USE_SUBMODULES" false)
        # (lib.cmakeBool "MI_ENABLE_EMBREE" enableEmbree)
        # (lib.cmakeFeature "MI_DEFAULT_VARIANTS" (builtins.concatStringsSep ";" enableVariants))
      ];
    })
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = [
    my-python
    pkgs.black
    pkgs.ruff
    pkgs.cmake
  ];
}
